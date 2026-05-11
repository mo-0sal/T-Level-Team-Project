from werkzeug.security import generate_password_hash
from database import get_db, init_db

def seed():
    init_db()
    conn = get_db()
    conn.execute("DELETE FROM task_notes")
    conn.execute("DELETE FROM tasks")
    conn.execute("DELETE FROM users")
    conn.commit()

    users = [
        ("Admin User",    "admin@mj.com",      generate_password_hash("password123"), "admin",   "Management"),
        ("Sarah Manager", "sarah@mj.com",       generate_password_hash("password123"), "manager", "Administration"),
        ("Tom Finance",   "tom@mj.com",         generate_password_hash("password123"), "manager", "Finance"),
        ("Alice Smith",   "alice@mj.com",       generate_password_hash("password123"), "staff",   "Administration"),
        ("Ben Jones",     "ben@mj.com",         generate_password_hash("password123"), "staff",   "Finance"),
        ("Claire HR",     "claire@mj.com",      generate_password_hash("password123"), "staff",   "HR"),
        ("David IT",      "david@mj.com",       generate_password_hash("password123"), "staff",   "IT Support"),
    ]
    for u in users:
        conn.execute(
            "INSERT INTO users (name, email, password_hash, role, department) VALUES (?,?,?,?,?)", u
        )
    conn.commit()

    admin = conn.execute("SELECT id FROM users WHERE email='admin@mj.com'").fetchone()
    sarah = conn.execute("SELECT id FROM users WHERE email='sarah@mj.com'").fetchone()
    tom   = conn.execute("SELECT id FROM users WHERE email='tom@mj.com'").fetchone()
    alice = conn.execute("SELECT id FROM users WHERE email='alice@mj.com'").fetchone()
    ben   = conn.execute("SELECT id FROM users WHERE email='ben@mj.com'").fetchone()
    claire = conn.execute("SELECT id FROM users WHERE email='claire@mj.com'").fetchone()

    tasks = [
        ("Update client contact records",  "Review and update all client contact details in the shared folder", alice['id'], sarah['id'],  "Administration", "high",   "in_progress", "2025-06-01"),
        ("Prepare Q2 invoices",            "Generate and send Q2 invoices to all active clients",               ben['id'],   tom['id'],    "Finance",        "high",   "pending",     "2025-05-30"),
        ("Staff onboarding documents",     "Prepare welcome pack and contracts for two new starters",           claire['id'],sarah['id'],  "HR",             "medium", "pending",     "2025-06-10"),
        ("Monthly payroll run",            "Process May payroll for all 40 employees",                         ben['id'],   tom['id'],    "Finance",        "high",   "pending",     "2025-05-28"),
        ("Book meeting room for Q2 review","Reserve the main conference room for the Q2 review meeting",        alice['id'], sarah['id'],  "Administration", "low",    "completed",   "2025-05-20"),
        ("IT equipment audit",             "Log and tag all IT equipment across all departments",               None,        admin['id'],  "IT Support",     "medium", "pending",     "2025-06-15"),
        ("Update employee handbook",       "Revise the handbook with updated remote working policy",            claire['id'],admin['id'],  "HR",             "medium", "on_hold",     "2025-06-20"),
        ("Client report — TechCo Ltd",    "Produce monthly progress report for TechCo Ltd",                    alice['id'], sarah['id'],  "Administration", "high",   "in_progress", "2025-05-29"),
    ]
    for t in tasks:
        conn.execute(
            """INSERT INTO tasks (title, description, assigned_to, created_by, department, priority, status, due_date)
               VALUES (?,?,?,?,?,?,?,?)""", t
        )
    conn.commit()

    task1 = conn.execute("SELECT id FROM tasks WHERE title='Update client contact records'").fetchone()
    task2 = conn.execute("SELECT id FROM tasks WHERE title='Prepare Q2 invoices'").fetchone()

    conn.execute("INSERT INTO task_notes (task_id, author_id, note) VALUES (?,?,?)",
                 (task1['id'], alice['id'], "Started reviewing records — about 30% done so far."))
    conn.execute("INSERT INTO task_notes (task_id, author_id, note) VALUES (?,?,?)",
                 (task1['id'], sarah['id'], "Please prioritise the West Midlands clients first."))
    conn.execute("INSERT INTO task_notes (task_id, author_id, note) VALUES (?,?,?)",
                 (task2['id'], ben['id'], "Waiting on invoice template update from Tom before I can proceed."))
    conn.commit()
    conn.close()

    print("Database seeded!")
    print("Admin:   admin@mj.com   / password123")
    print("Manager: sarah@mj.com   / password123")
    print("Manager: tom@mj.com     / password123")
    print("Staff:   alice@mj.com   / password123")
    print("Staff:   ben@mj.com     / password123")

if __name__ == '__main__':
    seed()
