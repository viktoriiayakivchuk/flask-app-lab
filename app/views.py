from flask import render_template, request
from app import app 

@app.route('/')
def resume(): 
    """Показує сторінку резюме (тепер це головна сторінка)."""
    agent = request.user_agent 
    return render_template('resume.html', agent=agent)

@app.route('/contacts')
def contacts(): 
    return render_template('contacts.html')
