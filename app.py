import os
from flask import Flask, render_template
from database import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.tasks import tasks_bp

app = Flask(__name__)
app.secret_key = 'mj-limited-secret-key-2025'

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(tasks_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
