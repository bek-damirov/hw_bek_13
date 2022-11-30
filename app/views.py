from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app import db, app
from .models import Transactions, User
from .forms import TransactionsForm, UserForm


def transaction_list():
    transaction = Transactions.query.all()
    return render_template('transactions_list.html', transaction=transaction)


@login_required
def transaction_create():
    form = TransactionsForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            transaction = Transactions()
            form.populate_obj(transaction)
            db.session.add(transaction)
            db.session.commit()
            flash('Транзакция успешно сохранена', 'success')
            return redirect(url_for('transactions_list'))
    return render_template('transaction_form.html', form=form)


@login_required
def transaction_update(id):
    transaction = Transactions.query.get(id)
    form = TransactionsForm(request.form, obj=transaction)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(transaction)
            db.session.add(transaction)
            db.session.commit()
            return redirect(url_for('transactions_list'))
    return render_template('transaction_form.html', form=form)


@login_required
def transaction_delete(id):
    transaction = Transactions.query.get(id)
    if request.method == 'POST':
        db.session.delete(transaction)
        db.session.commit()
        return redirect(url_for('transactions_list'))
    return render_template('transaction_delete.html', transaction=transaction)


def transaction_detail(id):
    transaction = Transactions.query.get(id)
    return render_template('transaction_detail.html', transaction=transaction)


def register_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            flash(f'Пользователь {user.username} успешно зарегистрирован', 'success')
            return redirect(url_for('login'))
    return render_template('user_form.html', form=form)


def login_view():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # user = User()
            # form.populate_obj(user)
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('успешно авторизован', 'primary')
                return redirect(url_for('transactions_list'))
            else:
                flash('неправильно введен логин или пароль', 'danger')
    return render_template('user_form.html', form=form)


def logout_view():
    logout_user()
    return redirect(url_for('transactions_list'))