from . import post_bp
from flask import render_template, redirect, url_for, flash, abort, request
from app import db 
from .models import Post, Tag 
from .forms import PostForm 
from app.users.models import User 

#  ДОПОМІЖНА ФУНКЦІЯ 
def _load_form_choices(form):
    """
    Завантажує списки (choices) для авторів та тегів у форму.
    """
    # Завантажуємо авторів (як у вас було)
    authors = db.session.scalars(db.select(User)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    
    # Завантажуємо теги (нове для пункту 11)
    tags = db.session.scalars(db.select(Tag)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

# 1. READ (Список постів)
@post_bp.route('/') 
def get_posts():
    posts = db.session.scalars(
        db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    ).all()
    return render_template("posts.html", posts=posts)

# 2. READ (Деталі одного поста) 
@post_bp.route('/<int:id>') 
def detail_post(id):
    post = db.get_or_404(Post, id)
    if not post.is_active:
        abort(404)
    return render_template("detail_post.html", post=post)

# 3. CREATE (Створення нового поста)
@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    
    # Викликаємо нашу функцію, щоб заповнити <select> (і авторів, і теги)
    _load_form_choices(form)

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.posted.data,
            is_active=form.is_active.data,
            category=form.category.data,
            user_id=form.author_id.data 
        )
        
        # form.tags.data - це список ID, наприклад [1, 3]
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()
        new_post.tags.extend(selected_tags)
  
        db.session.add(new_post)
        db.session.commit()
        
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.detail_post', id=new_post.id))
    
    return render_template("add_post.html", form=form, form_title="Створення нового поста")

# 4. UPDATE (Редагування поста)
@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post) 

    # Завантажуємо вибори для авторів та тегів
    _load_form_choices(form)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.posted.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.user_id = form.author_id.data
        
        # Очищуємо старі теги
        post.tags.clear()
        # Додаємо нові обрані теги
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()
        post.tags.extend(selected_tags)

        db.session.commit()
        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    # При GET-запиті:
    if not form.is_submitted():
        form.author_id.data = post.user_id
        # Встановлюємо, які теги мають бути обрані за замовчуванням
        form.tags.data = [tag.id for tag in post.tags]


    return render_template("add_post.html", form=form, form_title="Редагування поста")

# 5. DELETE (Видалення поста) 
@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост успішно видалено.', 'success')
        return redirect(url_for('posts.get_posts'))
    
    return render_template("delete_confirm.html", post=post)