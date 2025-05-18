from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'julis_sec_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Username already existing')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('board'))
        flash('login failed')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/board')
def board():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('board.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task = Task(
        title=request.form['title'],
        description=request.form['description'],
        label=request.form['label'],
        priority=request.form['priority'],
        comments=request.form['comments'],
        status='To Do',
        user_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('board'))

@app.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task and task.owner == current_user:
        task.status = request.form['status']
        db.session.commit()
    return ('', 204)

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        db.create_all()
    app.run(debug=True)