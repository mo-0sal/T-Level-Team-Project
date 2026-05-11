from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks')
def list_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    conn  = get_db()
    uid   = session['user_id']
    role  = session['role']
    status_filter = request.args.get('status', 'all')
    dept_filter   = request.args.get('dept',   'all')

    if role == 'staff':
        query  = "SELECT tasks.*, users.name AS assigned_name FROM tasks LEFT JOIN users ON tasks.assigned_to = users.id WHERE tasks.assigned_to = ?"
        params = [uid]
    else:
        query  = "SELECT tasks.*, users.name AS assigned_name FROM tasks LEFT JOIN users ON tasks.assigned_to = users.id WHERE 1=1"
        params = []

    if status_filter != 'all':
        query += " AND tasks.status = ?"
        params.append(status_filter)
    if dept_filter != 'all':
        query += " AND tasks.department = ?"
        params.append(dept_filter)

    query += " ORDER BY tasks.due_date ASC"
    task_list = conn.execute(query, params).fetchall()
    departments = conn.execute("SELECT DISTINCT department FROM tasks ORDER BY department").fetchall()
    conn.close()
    return render_template('tasks.html', tasks=task_list,
                           departments=departments,
                           status_filter=status_filter,
                           dept_filter=dept_filter)


@tasks_bp.route('/tasks/<int:task_id>')
def view_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    conn = get_db()
    task = conn.execute(
        """SELECT tasks.*, u1.name AS assigned_name, u2.name AS creator_name
           FROM tasks
           LEFT JOIN users u1 ON tasks.assigned_to = u1.id
           LEFT JOIN users u2 ON tasks.created_by  = u2.id
           WHERE tasks.id = ?""", (task_id,)
    ).fetchone()
    if not task:
        flash('Task not found', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    notes = conn.execute(
        """SELECT task_notes.*, users.name AS author_name
           FROM task_notes
           JOIN users ON task_notes.author_id = users.id
           WHERE task_notes.task_id = ?
           ORDER BY task_notes.created_at ASC""", (task_id,)
    ).fetchall()
    conn.close()
    return render_template('task_detail.html', task=task, notes=notes)


@tasks_bp.route('/tasks/<int:task_id>/note', methods=['POST'])
def add_note(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    note = request.form.get('note', '').strip()
    if note:
        conn = get_db()
        conn.execute(
            "INSERT INTO task_notes (task_id, author_id, note) VALUES (?,?,?)",
            (task_id, session['user_id'], note)
        )
        conn.commit()
        conn.close()
        flash('Note added.', 'success')
    return redirect(url_for('tasks.view_task', task_id=task_id))


@tasks_bp.route('/tasks/<int:task_id>/status', methods=['POST'])
def update_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    new_status = request.form.get('status')
    allowed = ['pending', 'in_progress', 'completed', 'on_hold']
    if new_status not in allowed:
        flash('Invalid status.', 'danger')
        return redirect(url_for('tasks.view_task', task_id=task_id))
    conn = get_db()
    # staff can only update tasks assigned to them
    if session['role'] == 'staff':
        conn.execute(
            "UPDATE tasks SET status=? WHERE id=? AND assigned_to=?",
            (new_status, task_id, session['user_id'])
        )
    else:
        conn.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
    conn.commit()
    conn.close()
    flash('Status updated.', 'success')
    return redirect(url_for('tasks.view_task', task_id=task_id))


@tasks_bp.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if 'user_id' not in session or session['role'] not in ('manager', 'admin'):
        return redirect(url_for('auth.login'))
    conn = get_db()
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        assigned_to = request.form.get('assigned_to') or None
        department  = request.form.get('department', 'General')
        priority    = request.form.get('priority', 'medium')
        due_date    = request.form.get('due_date') or None
        if not title:
            staff_list = conn.execute("SELECT id, name, department FROM users WHERE role='staff' ORDER BY name").fetchall()
            conn.close()
            return render_template('task_create.html', error='Please enter a task title', staff=staff_list)
        conn.execute(
            """INSERT INTO tasks (title, description, assigned_to, created_by, department, priority, due_date)
               VALUES (?,?,?,?,?,?,?)""",
            (title, description, assigned_to, session['user_id'], department, priority, due_date)
        )
        conn.commit()
        conn.close()
        flash('Task created.', 'success')
        return redirect(url_for('tasks.list_tasks'))
    staff_list = conn.execute("SELECT id, name, department FROM users WHERE role='staff' ORDER BY name").fetchall()
    conn.close()
    return render_template('task_create.html', error=None, staff=staff_list)
