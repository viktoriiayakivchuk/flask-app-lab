from flask import (render_template, request, redirect, url_for, 
                   Blueprint, session, flash, make_response) 

users_bp = Blueprint('users_bp', 
                     __name__, 
                     template_folder='templates', 
                     url_prefix='/users')

# --- Маршрути з Лаб 3 ---
@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age, title="Greating Page")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users_bp.greetings", name="administrator", age=45, _external=True, title="Greating Page")
    print(to_url)
    return redirect(to_url)

# --- Маршрути з Завдання 1 (Login/Profile/Logout) ---
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'password123':
            session['username'] = username
            flash('Ви успішно увійшли!', 'success') 
            return redirect(url_for('users_bp.profile'))
        else:
            flash('Неправильні дані! Спробуйте ще раз.', 'error') 
            return redirect(url_for('users_bp.login'))

    return render_template('users/login.html')

@users_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть, щоб побачити цю сторінку.', 'error') 
        return redirect(url_for('users_bp.login'))
    
    username = session['username']
    cookies = request.cookies
    
    # === ОНОВЛЕНО ДЛЯ ЗАВДАННЯ 3 ===
    # Читаємо 'profile_theme' кукі, за замовчуванням 'dark'
    profile_theme = request.cookies.get('profile_theme', 'dark')
    
    return render_template('users/profile.html', 
                           username=username, 
                           cookies=cookies,
                           profile_theme=profile_theme) # Передаємо тему в шаблон

@users_bp.route('/logout')
def logout():
    session.pop('username', None) 
    flash('Ви вийшли з системи.', 'success')
    return redirect(url_for('users_bp.login'))

# === МАРШРУТИ ДЛЯ ЗАВДАННЯ 2 (Cookies) ===

@users_bp.route('/add-cookie', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        return redirect(url_for('users_bp.login'))

    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    max_age_str = request.form.get('cookie_max_age')

    if not key or not value:
        flash('Ключ та значення кукі не можуть бути порожніми.', 'error')
        return redirect(url_for('users_bp.profile'))

    max_age_sec = 86400 # 1 день
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
    if 'username' not in session:
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
    if 'username' not in session:
        return redirect(url_for('users_bp.login'))

    response = make_response(redirect(url_for('users_bp.profile')))
    
    deleted_count = 0
    for key in request.cookies:
        if key != 'session':
            response.delete_cookie(key)
            deleted_count += 1
            
    flash(f'Успішно видалено {deleted_count} кукі (окрім сесії).', 'success')
    return response

# === НОВИЙ МАРШРУТ ДЛЯ ЗАВДАННЯ 3 (Тема для Profile) ===
@users_bp.route('/set-profile-theme/<theme>')
def set_profile_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'dark'
    
    response = make_response(redirect(url_for('users_bp.profile')))
    
    response.set_cookie('profile_theme', theme, max_age=30*24*60*60)
    return response