from flask import (render_template, request, make_response, 
                   redirect, url_for, flash, Blueprint)
# Видаляємо 'from app import app'
from app.forms import ContactForm
import logging

# Створюємо Blueprint 'main_bp' (як у прикладі викладача)
main_bp = Blueprint('main', __name__)

logging.basicConfig(filename='contact.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Змінюємо @app.route на @main_bp.route
@main_bp.route('/')
def resume(): 
    agent = request.user_agent 
    return render_template('resume.html', agent=agent)

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts(): 
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        
        logging.info(f"New Contact: Name={name}, Email={email}, Subject={form.subject.data}")
        flash(f'Дякуємо, {name} ({email})! Ваше повідомлення надіслано.', 'success')
        
        return redirect(url_for('main.contacts')) # Змінюємо url_for

    return render_template('contacts.html', form=form)

# Маршрут set_profile_theme ВИДАЛЕНО звідси