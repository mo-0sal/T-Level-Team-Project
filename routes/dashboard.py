from flask import Blueprint, render_template, redirect, url_for, session
from database import get_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    conn = get_db()
    uid  = session['user_id']
    role = session['role']

    if role == 'staff':
        my_tasks = conn.execute(
            "SELECT * FROM tasks WHERE assigned_to = ? ORDER BY due_date ASC", (uid,)
        ).fetchall()
        pending   = [t for t in my_tasks if t['status'] == 'pending']
        in_prog   = [t for t in my_tasks if t['status'] == 'in_progress']
        completed = [t for t in my_tasks if t['status'] == 'completed']
        conn.close()
        return render_template('dashboard.html',
            my_tasks=my_tasks, pending=pending,
            in_prog=in_prog, completed=completed)

    # manager / admin sees all tasks
    all_tasks = conn.execute(
        """SELECT tasks.*, users.name AS assigned_name
           FROM tasks
           LEFT JOIN users ON tasks.assigned_to = users.id
           ORDER BY tasks.due_date ASC"""
    ).fetchall()
    pending   = [t for t in all_tasks if t['status'] == 'pending']
    in_prog   = [t for t in all_tasks if t['status'] == 'in_progress']
    completed = [t for t in all_tasks if t['status'] == 'completed']
    on_hold   = [t for t in all_tasks if t['status'] == 'on_hold']
    conn.close()
    return render_template('dashboard.html',
        all_tasks=all_tasks, pending=pending,
        in_prog=in_prog, completed=completed, on_hold=on_hold)
