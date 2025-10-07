from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timedelta
import os
import json
import shutil
from io import BytesIO
import secrets
from markupsafe import escape

app = Flask(__name__)
# セキュリティ強化: ランダムなシークレットキーを生成
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productivity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CSRF保護を有効化
csrf = CSRFProtect(app)

# セキュリティヘッダーの設定
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' https://cdn.jsdelivr.net; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"
    return response

db = SQLAlchemy(app)

# セキュリティ: 入力値のサニタイズ関数
def sanitize_input(text, max_length=None):
    """XSS対策: HTMLタグをエスケープ"""
    if text is None:
        return None
    sanitized = escape(str(text))
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized

def validate_integer(value, min_val=None, max_val=None, default=None):
    """整数値のバリデーション"""
    try:
        val = int(value)
        if min_val is not None and val < min_val:
            return default if default is not None else min_val
        if max_val is not None and val > max_val:
            return default if default is not None else max_val
        return val
    except (ValueError, TypeError):
        return default

def validate_date(date_string):
    """日付のバリデーション"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except (ValueError, TypeError):
        return None

# Settings Model
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pomodoro_work_duration = db.Column(db.Integer, default=25)
    pomodoro_break_duration = db.Column(db.Integer, default=5)
    pomodoro_long_break_duration = db.Column(db.Integer, default=15)
    terms_accepted = db.Column(db.Boolean, default=False)
    terms_accepted_at = db.Column(db.DateTime)

def get_settings():
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()
    return settings

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='todo')
    estimated_pomodoros = db.Column(db.Integer, default=1)
    completed_pomodoros = db.Column(db.Integer, default=0)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class PomodoroSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    session_type = db.Column(db.String(20), default='work')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(20), default='daily')
    color = db.Column(db.String(20), default='primary')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs = db.relationship('HabitLog', backref='habit', lazy=True, cascade='all, delete-orphan')

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    completed = db.Column(db.Boolean, default=True)
    note = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HealthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    weight = db.Column(db.Float)
    exercise_minutes = db.Column(db.Integer)
    water_intake = db.Column(db.Integer)
    sleep_hours = db.Column(db.Float)
    mood = db.Column(db.String(20))
    note = db.Column(db.Text)

class LearningItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='learning')
    progress = db.Column(db.Integer, default=0)
    total_hours = db.Column(db.Float, default=0)
    target_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    sessions = db.relationship('LearningSession', backref='learning_item', lazy=True, cascade='all, delete-orphan')

class LearningSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learning_item_id = db.Column(db.Integer, db.ForeignKey('learning_item.id'), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(20))
    tags = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    goal_type = db.Column(db.String(20), default='short')  # short, medium, long
    target_date = db.Column(db.DateTime)
    progress = db.Column(db.Integer, default=0)  # 0-100
    status = db.Column(db.String(20), default='active')  # active, completed, abandoned
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    reminder_type = db.Column(db.String(20))  # task, habit, custom
    reminder_time = db.Column(db.Time)
    days_of_week = db.Column(db.String(50))  # comma-separated: 0,1,2,3,4,5,6
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    badge_type = db.Column(db.String(50))  # streak, pomodoro, task, etc
    requirement = db.Column(db.Integer)  # number needed to unlock
    icon = db.Column(db.String(50))
    unlocked_at = db.Column(db.DateTime)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    is_running = db.Column(db.Boolean, default=False)

class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='other')  # work, personal, health, study, meeting, other
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    reminder_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Middleware to check terms acceptance
@app.before_request
def check_terms_acceptance():
    # 利用規約関連のページと静的ファイルは除外
    excluded_paths = ['/terms', '/privacy', '/accept_terms', '/decline_terms', '/static/', '/terms-agreement']
    if any(request.path.startswith(path) for path in excluded_paths):
        return None
    
    settings = get_settings()
    if not settings.terms_accepted:
        return redirect(url_for('terms_agreement'))

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/terms-agreement')
def terms_agreement():
    """初回起動時の利用規約同意ページ"""
    return render_template('terms_agreement.html')

@app.route('/accept_terms', methods=['POST'])
def accept_terms():
    """利用規約に同意"""
    settings = get_settings()
    settings.terms_accepted = True
    settings.terms_accepted_at = datetime.utcnow()
    db.session.commit()
    flash('利用規約に同意いただきありがとうございます。アプリをお楽しみください！', 'success')
    return redirect(url_for('dashboard'))

@app.route('/decline_terms', methods=['POST'])
def decline_terms():
    """利用規約に同意しない"""
    return render_template('terms_declined.html')

@app.route('/dashboard')
def dashboard():
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    today_sessions = PomodoroSession.query.filter(
        PomodoroSession.started_at >= today_start,
        PomodoroSession.started_at <= today_end,
        PomodoroSession.completed == True,
        PomodoroSession.session_type == 'work'
    ).count()
    
    today_minutes = PomodoroSession.query.filter(
        PomodoroSession.started_at >= today_start,
        PomodoroSession.started_at <= today_end,
        PomodoroSession.completed == True,
        PomodoroSession.session_type == 'work'
    ).with_entities(db.func.sum(PomodoroSession.duration)).scalar() or 0
    
    active_tasks = Task.query.filter_by(status='in_progress').order_by(Task.priority.desc()).all()
    pending_tasks = Task.query.filter_by(status='todo').order_by(Task.priority.desc(), Task.due_date).limit(5).all()
    
    completed_today = Task.query.filter(
        Task.status == 'completed',
        Task.completed_at >= today_start,
        Task.completed_at <= today_end
    ).count()
    
    return render_template('dashboard.html',
                         today_sessions=today_sessions,
                         today_minutes=today_minutes,
                         active_tasks=active_tasks,
                         pending_tasks=pending_tasks,
                         completed_today=completed_today)

@app.route('/pomodoro')
def pomodoro():
    tasks = Task.query.filter(Task.status.in_(['todo', 'in_progress'])).order_by(Task.priority.desc()).all()
    settings = get_settings()
    return render_template('pomodoro.html', tasks=tasks, settings=settings)

@app.route('/api/pomodoro/start', methods=['POST'])
def start_pomodoro():
    data = request.get_json()
    session_type = data.get('session_type', 'work')
    task_id = data.get('task_id')
    settings = get_settings()
    
    if session_type == 'work':
        duration = settings.pomodoro_work_duration
    elif session_type == 'long_break':
        duration = settings.pomodoro_long_break_duration
    else:
        duration = settings.pomodoro_break_duration
    
    session = PomodoroSession(
        duration=duration,
        session_type=session_type,
        task_id=task_id if task_id else None
    )
    db.session.add(session)
    db.session.commit()
    
    return jsonify({'success': True, 'session_id': session.id, 'duration': duration})

@app.route('/api/pomodoro/complete/<int:session_id>', methods=['POST'])
def complete_pomodoro(session_id):
    session = PomodoroSession.query.get_or_404(session_id)
    session.completed = True
    
    if session.task_id and session.session_type == 'work':
        task = Task.query.get(session.task_id)
        if task:
            task.completed_pomodoros += 1
            if task.status == 'todo':
                task.status = 'in_progress'
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/tasks')
def tasks():
    filter_status = request.args.get('status', 'all')
    query = Task.query
    
    if filter_status != 'all':
        query = query.filter_by(status=filter_status)
    
    tasks = query.order_by(Task.priority.desc(), Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks, filter_status=filter_status)

@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        # 入力値のサニタイズとバリデーション
        title = sanitize_input(request.form.get('title'), max_length=200)
        description = sanitize_input(request.form.get('description'), max_length=1000)
        priority = request.form.get('priority', 'medium')
        
        # 優先度の検証
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'
        
        # ポモドーロ数のバリデーション（1-20の範囲）
        estimated_pomodoros = validate_integer(request.form.get('estimated_pomodoros', 1), min_val=1, max_val=20, default=1)
        
        # 日付のバリデーション
        due_date = validate_date(request.form.get('due_date'))
        
        if not title or len(title.strip()) == 0:
            flash('タスク名を入力してください', 'error')
            return redirect(url_for('add_task'))
        
        task = Task(
            title=title,
            description=description,
            priority=priority,
            estimated_pomodoros=estimated_pomodoros,
            due_date=due_date
        )
        db.session.add(task)
        db.session.commit()
        
        flash('タスクが追加されました！', 'success')
        return redirect(url_for('tasks'))
    
    return render_template('add_task.html')

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.priority = request.form.get('priority')
        task.estimated_pomodoros = int(request.form.get('estimated_pomodoros', 1))
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                task.due_date = None
        else:
            task.due_date = None
        
        db.session.commit()
        flash('タスクが更新されました！', 'success')
        return redirect(url_for('tasks'))
    
    return render_template('edit_task.html', task=task)

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'completed'
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('タスクが削除されました', 'info')
    return redirect(url_for('tasks'))

@app.route('/statistics')
def statistics():
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=6)
    
    daily_stats = []
    for i in range(7):
        day = week_ago + timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        
        sessions = PomodoroSession.query.filter(
            PomodoroSession.started_at >= day_start,
            PomodoroSession.started_at <= day_end,
            PomodoroSession.completed == True,
            PomodoroSession.session_type == 'work'
        ).count()
        
        minutes = PomodoroSession.query.filter(
            PomodoroSession.started_at >= day_start,
            PomodoroSession.started_at <= day_end,
            PomodoroSession.completed == True,
            PomodoroSession.session_type == 'work'
        ).with_entities(db.func.sum(PomodoroSession.duration)).scalar() or 0
        
        tasks_completed = Task.query.filter(
            Task.status == 'completed',
            Task.completed_at >= day_start,
            Task.completed_at <= day_end
        ).count()
        
        daily_stats.append({
            'date': day,
            'sessions': sessions,
            'minutes': minutes,
            'tasks': tasks_completed
        })
    
    total_sessions = PomodoroSession.query.filter_by(completed=True, session_type='work').count()
    total_minutes = PomodoroSession.query.filter_by(completed=True, session_type='work').with_entities(db.func.sum(PomodoroSession.duration)).scalar() or 0
    total_tasks = Task.query.filter_by(status='completed').count()
    
    return render_template('statistics.html',
                         daily_stats=daily_stats,
                         total_sessions=total_sessions,
                         total_minutes=total_minutes,
                         total_tasks=total_tasks)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    settings = get_settings()
    
    if request.method == 'POST':
        # 入力値のバリデーション（5-60分の範囲）
        settings.pomodoro_work_duration = validate_integer(
            request.form.get('work_duration', 25), min_val=5, max_val=60, default=25)
        settings.pomodoro_break_duration = validate_integer(
            request.form.get('break_duration', 5), min_val=1, max_val=30, default=5)
        settings.pomodoro_long_break_duration = validate_integer(
            request.form.get('long_break_duration', 15), min_val=5, max_val=60, default=15)
        
        db.session.commit()
        flash('設定が保存されました！', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html', settings=settings)

# Habits
@app.route('/habits')
def habits():
    today = datetime.utcnow().date()
    all_habits = Habit.query.all()
    
    habits_data = []
    for habit in all_habits:
        today_log = HabitLog.query.filter_by(habit_id=habit.id, date=today).first()
        
        streak = 0
        check_date = today
        while True:
            log = HabitLog.query.filter_by(habit_id=habit.id, date=check_date, completed=True).first()
            if log:
                streak += 1
                check_date = check_date - timedelta(days=1)
            else:
                break
        
        habits_data.append({
            'habit': habit,
            'completed_today': today_log is not None,
            'streak': streak
        })
    
    return render_template('habits.html', habits_data=habits_data, today=today)

@app.route('/habits/add', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'POST':
        # 入力値のサニタイズ
        name = sanitize_input(request.form.get('name'), max_length=100)
        description = sanitize_input(request.form.get('description'), max_length=500)
        frequency = request.form.get('frequency', 'daily')
        color = request.form.get('color', 'primary')
        
        # 頻度の検証
        if frequency not in ['daily', 'weekly', 'custom']:
            frequency = 'daily'
        
        # 色の検証
        if color not in ['primary', 'success', 'danger', 'warning', 'info']:
            color = 'primary'
        
        if not name or len(name.strip()) == 0:
            flash('習慣名を入力してください', 'error')
            return redirect(url_for('add_habit'))
        
        habit = Habit(name=name, description=description, frequency=frequency, color=color)
        db.session.add(habit)
        db.session.commit()
        
        flash('習慣が追加されました！', 'success')
        return redirect(url_for('habits'))
    
    return render_template('add_habit.html')

@app.route('/habits/<int:habit_id>/toggle', methods=['POST'])
def toggle_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    today = datetime.utcnow().date()
    log = HabitLog.query.filter_by(habit_id=habit_id, date=today).first()
    
    if log:
        db.session.delete(log)
    else:
        log = HabitLog(habit_id=habit_id, date=today)
        db.session.add(log)
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/habits/<int:habit_id>/delete', methods=['POST'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    flash('習慣が削除されました', 'info')
    return redirect(url_for('habits'))

# Health
@app.route('/health')
def health():
    logs = HealthLog.query.order_by(HealthLog.date.desc()).limit(30).all()
    return render_template('health.html', logs=logs)

@app.route('/health/add', methods=['GET', 'POST'])
def add_health_log():
    if request.method == 'POST':
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
        
        existing_log = HealthLog.query.filter_by(date=date).first()
        
        if existing_log:
            log = existing_log
        else:
            log = HealthLog(date=date)
        
        weight = request.form.get('weight')
        if weight:
            log.weight = float(weight)
        
        exercise_minutes = request.form.get('exercise_minutes')
        if exercise_minutes:
            log.exercise_minutes = int(exercise_minutes)
        
        water_intake = request.form.get('water_intake')
        if water_intake:
            log.water_intake = int(water_intake)
        
        sleep_hours = request.form.get('sleep_hours')
        if sleep_hours:
            log.sleep_hours = float(sleep_hours)
        
        log.mood = request.form.get('mood')
        log.note = request.form.get('note')
        
        if not existing_log:
            db.session.add(log)
        db.session.commit()
        
        flash('健康記録が保存されました！', 'success')
        return redirect(url_for('health'))
    
    return render_template('add_health_log.html')

# Learning
@app.route('/learning')
def learning():
    items = LearningItem.query.order_by(LearningItem.created_at.desc()).all()
    return render_template('learning.html', items=items)

@app.route('/learning/add', methods=['GET', 'POST'])
def add_learning():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        target_date_str = request.form.get('target_date')
        
        target_date = None
        if target_date_str:
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            except ValueError:
                pass
        
        item = LearningItem(title=title, category=category, description=description, target_date=target_date)
        db.session.add(item)
        db.session.commit()
        
        flash('学習項目が追加されました！', 'success')
        return redirect(url_for('learning'))
    
    return render_template('add_learning.html')

@app.route('/learning/<int:item_id>/session', methods=['POST'])
def add_learning_session(item_id):
    item = LearningItem.query.get_or_404(item_id)
    data = request.get_json()
    duration = float(data.get('duration', 0))
    note = data.get('note', '')
    
    session = LearningSession(learning_item_id=item_id, duration=duration, note=note)
    db.session.add(session)
    
    item.total_hours += duration
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/learning/<int:item_id>/update', methods=['POST'])
def update_learning_progress(item_id):
    item = LearningItem.query.get_or_404(item_id)
    data = request.get_json()
    item.progress = int(data.get('progress', 0))
    item.status = data.get('status', item.status)
    
    if item.status == 'completed' and not item.completed_at:
        item.completed_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'success': True})

# Journal
@app.route('/journal')
def journal():
    entries = JournalEntry.query.order_by(JournalEntry.date.desc()).all()
    return render_template('journal.html', entries=entries)

@app.route('/journal/add', methods=['GET', 'POST'])
def add_journal():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        mood = request.form.get('mood')
        tags = request.form.get('tags')
        date_str = request.form.get('date')
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
        
        entry = JournalEntry(title=title, content=content, mood=mood, tags=tags, date=date)
        db.session.add(entry)
        db.session.commit()
        
        flash('日記が保存されました！', 'success')
        return redirect(url_for('journal'))
    
    return render_template('add_journal.html')

@app.route('/journal/<int:entry_id>')
def view_journal(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    return render_template('view_journal.html', entry=entry)

@app.route('/journal/<int:entry_id>/delete', methods=['POST'])
def delete_journal(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('日記が削除されました', 'info')
    return redirect(url_for('journal'))

# Calendar
@app.route('/calendar')
def calendar_view():
    year = request.args.get('year', datetime.utcnow().year, type=int)
    month = request.args.get('month', datetime.utcnow().month, type=int)
    
    # Get all events for the month
    month_start = datetime(year, month, 1)
    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)
    
    tasks = Task.query.filter(Task.due_date >= month_start, Task.due_date < month_end).all()
    habits = Habit.query.all()
    health_logs = HealthLog.query.filter(HealthLog.date >= month_start.date(), HealthLog.date < month_end.date()).all()
    journal_entries = JournalEntry.query.filter(JournalEntry.date >= month_start.date(), JournalEntry.date < month_end.date()).all()
    events = CalendarEvent.query.filter(CalendarEvent.start_time >= month_start, CalendarEvent.start_time < month_end).all()
    
    return render_template('calendar.html', year=year, month=month, tasks=tasks, habits=habits, 
                         health_logs=health_logs, journal_entries=journal_entries, events=events)

@app.route('/calendar/event/add', methods=['GET', 'POST'])
def add_calendar_event():
    if request.method == 'POST':
        # 入力値のサニタイズ
        title = sanitize_input(request.form.get('title'), max_length=200)
        description = sanitize_input(request.form.get('description'), max_length=1000)
        category = request.form.get('category', 'other')
        location = sanitize_input(request.form.get('location'), max_length=200)
        
        # カテゴリの検証
        valid_categories = ['work', 'meeting', 'personal', 'health', 'study', 'other']
        if category not in valid_categories:
            category = 'other'
        
        if not title or len(title.strip()) == 0:
            flash('予定名を入力してください', 'error')
            return redirect(url_for('add_calendar_event'))
        
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('end_date')
        end_time = request.form.get('end_time')
        
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
        except ValueError:
            flash('開始日時が正しくありません', 'error')
            return redirect(url_for('add_calendar_event'))
        
        end_datetime = None
        if end_date and end_time:
            try:
                end_datetime = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
                # 終了時刻が開始時刻より前でないかチェック
                if end_datetime < start_datetime:
                    flash('終了時刻は開始時刻より後にしてください', 'error')
                    return redirect(url_for('add_calendar_event'))
            except ValueError:
                pass
        
        event = CalendarEvent(
            title=title,
            description=description,
            category=category,
            start_time=start_datetime,
            end_time=end_datetime,
            location=location
        )
        db.session.add(event)
        db.session.commit()
        
        flash('予定が追加されました！', 'success')
        return redirect(url_for('calendar_view'))
    
    return render_template('add_calendar_event.html')

@app.route('/calendar/event/<int:event_id>/delete', methods=['POST'])
def delete_calendar_event(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('予定が削除されました', 'info')
    return redirect(url_for('calendar_view'))

@app.route('/api/check_reminders')
def check_reminders():
    """30分前のリマインダーをチェック"""
    now = datetime.utcnow()
    reminder_time = now + timedelta(minutes=30)
    
    # 30分後に開始するイベントを取得（±5分の範囲）
    events = CalendarEvent.query.filter(
        CalendarEvent.start_time >= reminder_time - timedelta(minutes=5),
        CalendarEvent.start_time <= reminder_time + timedelta(minutes=5),
        CalendarEvent.reminder_sent == False
    ).all()
    
    reminders = []
    for event in events:
        event.reminder_sent = True
        reminders.append({
            'id': event.id,
            'title': event.title,
            'start_time': event.start_time.strftime('%H:%M'),
            'category': event.category
        })
    
    db.session.commit()
    return jsonify({'reminders': reminders})

# Goals
@app.route('/goals')
def goals():
    active_goals = Goal.query.filter_by(status='active').order_by(Goal.target_date).all()
    completed_goals = Goal.query.filter_by(status='completed').order_by(Goal.completed_at.desc()).limit(5).all()
    return render_template('goals.html', active_goals=active_goals, completed_goals=completed_goals)

@app.route('/goals/add', methods=['GET', 'POST'])
def add_goal():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        goal_type = request.form.get('goal_type', 'short')
        target_date_str = request.form.get('target_date')
        
        target_date = None
        if target_date_str:
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            except ValueError:
                pass
        
        goal = Goal(title=title, description=description, goal_type=goal_type, target_date=target_date)
        db.session.add(goal)
        db.session.commit()
        
        flash('目標が追加されました！', 'success')
        return redirect(url_for('goals'))
    
    return render_template('add_goal.html')

@app.route('/goals/<int:goal_id>/update', methods=['POST'])
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    data = request.get_json()
    goal.progress = int(data.get('progress', 0))
    
    if goal.progress >= 100 and goal.status != 'completed':
        goal.status = 'completed'
        goal.completed_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'success': True})

# Notes
@app.route('/notes')
def notes():
    all_notes = Note.query.order_by(Note.is_pinned.desc(), Note.updated_at.desc()).all()
    return render_template('notes.html', notes=all_notes)

@app.route('/notes/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        
        note = Note(title=title, content=content, tags=tags)
        db.session.add(note)
        db.session.commit()
        
        flash('メモが保存されました！', 'success')
        return redirect(url_for('notes'))
    
    return render_template('add_note.html')

@app.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('メモが削除されました', 'info')
    return redirect(url_for('notes'))

# Time Tracking
@app.route('/timetracking')
def timetracking():
    entries = TimeEntry.query.order_by(TimeEntry.start_time.desc()).limit(50).all()
    running_entry = TimeEntry.query.filter_by(is_running=True).first()
    return render_template('timetracking.html', entries=entries, running_entry=running_entry)

@app.route('/timetracking/start', methods=['POST'])
def start_tracking():
    data = request.get_json()
    project_name = data.get('project_name')
    description = data.get('description', '')
    
    # Stop any running entries
    running = TimeEntry.query.filter_by(is_running=True).all()
    for entry in running:
        entry.is_running = False
        entry.end_time = datetime.utcnow()
        entry.duration_minutes = int((entry.end_time - entry.start_time).total_seconds() / 60)
    
    entry = TimeEntry(project_name=project_name, description=description, start_time=datetime.utcnow(), is_running=True)
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({'success': True, 'entry_id': entry.id})

@app.route('/timetracking/stop/<int:entry_id>', methods=['POST'])
def stop_tracking(entry_id):
    entry = TimeEntry.query.get_or_404(entry_id)
    entry.is_running = False
    entry.end_time = datetime.utcnow()
    entry.duration_minutes = int((entry.end_time - entry.start_time).total_seconds() / 60)
    db.session.commit()
    
    return jsonify({'success': True, 'duration': entry.duration_minutes})

# Reports
@app.route('/reports')
def reports():
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Weekly stats
    week_pomodoros = PomodoroSession.query.filter(
        PomodoroSession.started_at >= datetime.combine(week_ago, datetime.min.time()),
        PomodoroSession.completed == True,
        PomodoroSession.session_type == 'work'
    ).count()
    
    week_tasks = Task.query.filter(
        Task.status == 'completed',
        Task.completed_at >= datetime.combine(week_ago, datetime.min.time())
    ).count()
    
    # Monthly stats
    month_pomodoros = PomodoroSession.query.filter(
        PomodoroSession.started_at >= datetime.combine(month_ago, datetime.min.time()),
        PomodoroSession.completed == True,
        PomodoroSession.session_type == 'work'
    ).count()
    
    month_tasks = Task.query.filter(
        Task.status == 'completed',
        Task.completed_at >= datetime.combine(month_ago, datetime.min.time())
    ).count()
    
    return render_template('reports.html',
                         week_pomodoros=week_pomodoros,
                         week_tasks=week_tasks,
                         month_pomodoros=month_pomodoros,
                         month_tasks=month_tasks)

# Achievements
@app.route('/achievements')
def achievements():
    # Initialize achievements if not exists
    if Achievement.query.count() == 0:
        init_achievements()
    
    all_achievements = Achievement.query.all()
    
    # Check and unlock achievements
    check_achievements()
    
    return render_template('achievements.html', achievements=all_achievements)

def init_achievements():
    achievements_data = [
        {'name': '初めの一歩', 'description': '最初のポモドーロを完了', 'badge_type': 'pomodoro', 'requirement': 1, 'icon': 'alarm'},
        {'name': 'ポモドーロ初心者', 'description': '10回のポモドーロを完了', 'badge_type': 'pomodoro', 'requirement': 10, 'icon': 'alarm-fill'},
        {'name': 'ポモドーロマスター', 'description': '100回のポモドーロを完了', 'badge_type': 'pomodoro', 'requirement': 100, 'icon': 'trophy'},
        {'name': '習慣の力', 'description': '7日連続で習慣を達成', 'badge_type': 'streak', 'requirement': 7, 'icon': 'fire'},
        {'name': '継続は力なり', 'description': '30日連続で習慣を達成', 'badge_type': 'streak', 'requirement': 30, 'icon': 'star-fill'},
        {'name': 'タスクハンター', 'description': '50個のタスクを完了', 'badge_type': 'task', 'requirement': 50, 'icon': 'check-circle-fill'},
    ]
    
    for data in achievements_data:
        achievement = Achievement(**data)
        db.session.add(achievement)
    
    db.session.commit()

def check_achievements():
    # Check pomodoro achievements
    total_pomodoros = PomodoroSession.query.filter_by(completed=True, session_type='work').count()
    for achievement in Achievement.query.filter_by(badge_type='pomodoro', unlocked_at=None).all():
        if total_pomodoros >= achievement.requirement:
            achievement.unlocked_at = datetime.utcnow()
    
    # Check task achievements
    total_tasks = Task.query.filter_by(status='completed').count()
    for achievement in Achievement.query.filter_by(badge_type='task', unlocked_at=None).all():
        if total_tasks >= achievement.requirement:
            achievement.unlocked_at = datetime.utcnow()
    
    db.session.commit()

# Backup and Export
@app.route('/backup')
def backup_database():
    """データベースのバックアップをダウンロード"""
    try:
        db_path = 'productivity.db'
        if os.path.exists(db_path):
            # バックアップファイル名に日時を付ける
            backup_name = f'productivity_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            return send_file(db_path, as_attachment=True, download_name=backup_name)
        else:
            flash('データベースファイルが見つかりません', 'error')
            return redirect(url_for('settings'))
    except Exception as e:
        flash(f'バックアップエラー: {str(e)}', 'error')
        return redirect(url_for('settings'))

@app.route('/terms')
def terms():
    """利用規約ページ"""
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    """プライバシーポリシーページ"""
    return render_template('privacy.html')

@app.route('/contact')
def contact():
    """お問い合わせページ"""
    return render_template('contact.html')

@app.route('/faq')
def faq():
    """よくある質問ページ"""
    return render_template('faq.html')

@app.route('/export/json')
def export_json():
    """すべてのデータをJSONでエクスポート"""
    try:
        data = {
            'export_date': datetime.now().isoformat(),
            'tasks': [{'id': t.id, 'title': t.title, 'status': t.status, 
                      'priority': t.priority, 'created_at': t.created_at.isoformat() if t.created_at else None}
                     for t in Task.query.all()],
            'habits': [{'id': h.id, 'name': h.name, 'frequency': h.frequency}
                      for h in Habit.query.all()],
            'health_logs': [{'id': h.id, 'date': h.date.isoformat() if h.date else None,
                           'weight': h.weight, 'exercise_minutes': h.exercise_minutes}
                          for h in HealthLog.query.all()],
            'learning_items': [{'id': l.id, 'title': l.title, 'progress': l.progress,
                              'total_hours': l.total_hours}
                             for l in LearningItem.query.all()],
            'journal_entries': [{'id': j.id, 'title': j.title, 'date': j.date.isoformat() if j.date else None}
                              for j in JournalEntry.query.all()],
            'events': [{'id': e.id, 'title': e.title, 'category': e.category,
                       'start_time': e.start_time.isoformat() if e.start_time else None}
                      for e in CalendarEvent.query.all()],
            'goals': [{'id': g.id, 'title': g.title, 'progress': g.progress, 'status': g.status}
                     for g in Goal.query.all()],
            'notes': [{'id': n.id, 'title': n.title, 'content': n.content}
                     for n in Note.query.all()]
        }
        
        # JSONファイルとして返す
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        buffer = BytesIO(json_data.encode('utf-8'))
        buffer.seek(0)
        
        filename = f'productivity_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/json')
    except Exception as e:
        flash(f'エクスポートエラー: {str(e)}', 'error')
        return redirect(url_for('settings'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
