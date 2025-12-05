from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import select, or_
from app import db
from . import expenses_bp
from .models import Expense, ExpenseCategory
from .forms import ExpenseForm

@expenses_bp.route('/')
@login_required
def get_expenses():
    # Отримуємо параметри з URL для пошуку та сортування
    search_query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'date') # за замовчуванням сортуємо за датою

    # Базовий запит (тільки свої витрати)
    query = select(Expense).where(Expense.user_id == current_user.id)

    # 1. ПОШУК (Фільтрація)
    if search_query:
        # Шукаємо, якщо текст є в назві (title) 
        query = query.where(Expense.title.ilike(f"%{search_query}%"))

    # 2. СОРТУВАННЯ
    if sort_by == 'amount':
        query = query.order_by(Expense.amount.desc()) # Найдорожчі зверху
    elif sort_by == 'category':
        query = query.join(Expense.category).order_by(ExpenseCategory.name)
    else:
        query = query.order_by(Expense.created_at.desc()) # Нові зверху (default)

    expenses = db.session.scalars(query).all()
    
    # Рахуємо суму (для відфільтрованого списку)
    total_amount = sum(e.amount for e in expenses)
    
    return render_template('expenses/expenses_list.html', 
                           expenses=expenses, 
                           total=total_amount,
                           search_query=search_query)

@expenses_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_expense():
    form = ExpenseForm()
    
    # Завантажуємо категорії для випадаючого списку
    categories = db.session.scalars(select(ExpenseCategory)).all()
    form.category.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        expense = Expense(
            title=form.title.data,
            amount=form.amount.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Витрату успішно додано!', 'success')
        return redirect(url_for('expenses_bp.get_expenses'))

    return render_template('expenses/create_expense.html', form=form, title="Додати витрату")

@expenses_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_expense(id):
    expense = db.get_or_404(Expense, id)
    
    # ПЕРЕВІРКА ВЛАСНИКА
    if expense.user_id != current_user.id:
        abort(403) 

    form = ExpenseForm()
    
    # Завантажуємо категорії
    categories = db.session.scalars(select(ExpenseCategory)).all()
    form.category.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        expense.title = form.title.data
        expense.amount = form.amount.data
        expense.category_id = form.category.data
        db.session.commit()
        flash('Витрату успішно оновлено!', 'success')
        return redirect(url_for('expenses_bp.get_expenses'))

    elif request.method == 'GET':
        form.title.data = expense.title
        form.amount.data = expense.amount
        form.category.data = expense.category_id

    return render_template('expenses/update_expense.html', form=form, expense=expense)

@expenses_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_expense(id):
    expense = db.get_or_404(Expense, id)
    
    # ПЕРЕВІРКА ВЛАСНИКА
    if expense.user_id != current_user.id:
        abort(403)

    db.session.delete(expense)
    db.session.commit()
    flash('Витрату видалено.', 'success')
    return redirect(url_for('expenses_bp.get_expenses'))