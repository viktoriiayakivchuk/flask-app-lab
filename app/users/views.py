from flask import (render_template, request, redirect, url_for, 
                   Blueprint, session, flash, make_response)
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import select
from app import db, bcrypt
from app.users.models import User
from app.forms import LoginForm
from .forms import RegistrationForm

users_bp = Blueprint('users_bp', 
                     __name__, 
                     template_folder='templates', 
                     url_prefix='/users')

# --- Маршрути з Лаб 3 (Привітання) ---
@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age, title="Greeting Page")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users_bp.greetings", name="administrator", age=45, _external=True, title="Greeting Page")
    return redirect(to_url)

# === РЕЄСТРАЦІЯ (Лаб 9) ===
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Якщо користувач вже авторизований - перенаправляємо на профіль
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

# === ВХІД (Лаб 9) ===
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Якщо користувач вже авторизований - перенаправляємо на профіль
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        # Вхід за Email (згідно з методичкою)
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Ви успішно увійшли!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users_bp.profile'))
        else:
            flash('Вхід не вдався. Перевірте email та пароль.', 'danger')

    return render_template('users/login.html', form=form)

# === ВИХІД (Лаб 9) ===
@users_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'success')
    return redirect(url_for('users_bp.login'))

# === ПРОФІЛЬ (Лаб 9 - захищений) ===
@users_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', 
                           username=current_user.username, 
                           cookies=request.cookies)

# === СПИСОК КОРИСТУВАЧІВ (Лаб 9, п.6 - захищений) ===
@users_bp.route('/users')
@login_required
def users_list():
    users = db.session.scalars(select(User)).all()
    return render_template('users/users_list.html', users=users, count=len(users))

# === РОБОТА З КУКІ (Лаб 4) ===
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