from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not email or not password:
            return render_template('login.html', error='Please enter your email and password')
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if not user or not check_password_hash(user['password_hash'], password):
            return render_template('login.html', error='Incorrect email or password')
        session['user_id']   = user['id']
        session['user_name'] = user['name']
        session['role']      = user['role']
        session['dept']      = user['department']
        flash(f"Welcome back, {user['name']}!", 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('login.html', error=None)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
