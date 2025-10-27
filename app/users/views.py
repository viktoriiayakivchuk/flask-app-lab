from flask import request, redirect, url_for, render_template, flash, session, Blueprint

# Defining a blueprint
users_bp = Blueprint(
    'users_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@users_bp.route("/hi/<string:name>") #/hi/ivan?age=45
def greetings (name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html",name=name, age=age, title="Greating Page")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users_bp.greetings", name="administrator", age=45, _external=True,title="Greating Page")
    print(to_url)
    return redirect(to_url)


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
    if 'username' in session:
        username = session['username'] 
        return render_template('users/profile.html', username=username)
    else:
        flash('Будь ласка, увійдіть, щоб побачити цю сторінку.', 'error') 
        return redirect(url_for('users_bp.login'))

@users_bp.route('/logout')
def logout():
    session.pop('username', None) 
    flash('Ви вийшли з системи.', 'success')
    return redirect(url_for('users_bp.login'))

from . import views