from flask import render_template, request, make_response, redirect, url_for, flash
from app import app 
from app.forms import ContactForm
import logging

logging.basicConfig(filename='contact.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

@app.route('/')
def resume(): 
    """Показує сторінку резюме (тепер це головна сторінка)."""
    agent = request.user_agent 
    return render_template('resume.html', agent=agent)

@app.route('/contacts', methods=['GET', 'POST']) 
def contacts(): 
    form = ContactForm()

    if form.validate_on_submit():
        # Дані успішно пройшли валідацію
        name = form.name.data
        email = form.email.data
        
        logging.info(f"New Contact: Name={name}, Email={email}, Subject={form.subject.data}")

        flash(f'Дякуємо, {name} ({email})! Ваше повідомлення надіслано.', 'success')
        
        return redirect(url_for('contacts'))

    # Якщо GET-запит або валідація не пройдена, просто рендеримо сторінку
    return render_template('contacts.html', form=form)
