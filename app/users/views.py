import os
import secrets
from PIL import Image
from datetime import datetime, timezone
from flask import (render_template, request, redirect, url_for, 
                   Blueprint, session, flash, make_response, current_app)
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import select
from app import db, bcrypt
from app.users.models import User
from app.forms import LoginForm
from .forms import RegistrationForm, UpdateAccountForm, ChangePasswordForm

users_bp = Blueprint('users_bp', 
                     __name__, 
                     template_folder='templates', 
                     url_prefix='/users')

@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

def save_picture(form_picture):
    """
    Зберігає зображення профілю:
    1. Генерує випадкове ім'я (hex).
    2. Зменшує зображення до 125x125 (Pillow).
    3. Зберігає у static/images.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Шлях до папки static/images
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    
    # Зміна розміру
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    return picture_fn


# --- Основні маршрути ---

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age, title="Greeting Page")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users_bp.greetings", name="administrator", age=45, _external=True, title="Greeting Page")
    return redirect(to_url)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Акаунт успішно створено для {form.username.data}!', 'success')
        return redirect(url_for('users_bp.login'))
    
    return render_template('users/register.html', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Ви успішно увійшли!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users_bp.profile'))
        else:
            flash('Вхід не вдався. Перевірте email та пароль.', 'danger')

    return render_template('users/login.html', form=form)

@users_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'success')
    return redirect(url_for('users_bp.login'))

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    password_form = ChangePasswordForm()
    
    if 'submit' in request.form and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        db.session.commit()
        flash('Ваш акаунт оновлено!', 'success')
        return redirect(url_for('users_bp.profile'))
    
    if 'submit_password' in request.form and password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash('Невірний поточний пароль.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Ваш пароль успішно змінено!', 'success')
            return redirect(url_for('users_bp.profile'))

    # --- GET ЗАПИТ ---
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='images/' + current_user.image)
    profile_theme = request.cookies.get('profile_theme', 'light') 

    return render_template('users/profile.html', 
                           title='Profile',
                           image_file=image_file, 
                           form=form,
                           password_form=password_form,
                           profile_theme=profile_theme,
                           username=current_user.username,
                           cookies=request.cookies)

@users_bp.route('/users')
@login_required
def users_list():
    users = db.session.scalars(select(User)).all()
    return render_template('users/users_list.html', users=users, users_count=len(users))

# === РОБОТА З КУКІ 

@users_bp.route('/add-cookie', methods=['POST'])
def add_cookie():
    if not current_user.is_authenticated:
        return redirect(url_for('users_bp.login'))
        
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    max_age_str = request.form.get('cookie_max_age')
    
    if not key or not value:
        flash('Ключ та значення кукі не можуть бути порожніми.', 'error')
        return redirect(url_for('users_bp.profile'))
        
    max_age_sec = 86400 
    if max_age_str:
        try:
            max_age_sec = int(max_age_str)
        except ValueError:
            flash('Неправильний формат терміну дії. Встановлено 1 день.', 'warning')
            
    response = make_response(redirect(url_for('users_bp.profile')))
    response.set_cookie(key, value, max_age=max_age_sec)
    flash(f'Кукі "{key}" успішно додано!', 'success')
    return response

@users_bp.route('/delete-cookie', methods=['POST'])
def delete_cookie():
    if not current_user.is_authenticated:
        return redirect(url_for('users_bp.login'))
        
    key_to_delete = request.form.get('cookie_key_delete')
    if not key_to_delete:
        flash('Введіть ключ кукі для видалення.', 'error')
        return redirect(url_for('users_bp.profile'))
        
    response = make_response(redirect(url_for('users_bp.profile')))
    if key_to_delete in request.cookies:
        response.delete_cookie(key_to_delete)
        flash(f'Кукі "{key_to_delete}" видалено.', 'success')
    else:
        flash(f'Кукі "{key_to_delete}" не знайдено.', 'error')
    return response

@users_bp.route('/delete-all-cookies', methods=['POST'])
def delete_all_cookies():
    if not current_user.is_authenticated:
        return redirect(url_for('users_bp.login'))
        
    response = make_response(redirect(url_for('users_bp.profile')))
    deleted_count = 0
    for key in request.cookies:
        if key != 'session':
            response.delete_cookie(key)
            deleted_count += 1
    flash(f'Успішно видалено {deleted_count} кукі (окрім сесії).', 'success')
    return response

@users_bp.route('/set-profile-theme/<theme>')
def set_profile_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'dark'
    response = make_response(redirect(url_for('users_bp.profile')))
    response.set_cookie('profile_theme', theme, max_age=30*24*60*60)
    return response