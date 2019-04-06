# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 07:18:51 2019

@author: dep17364
"""

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale
from werkzeug.urls import url_parse
from guess_language import guess_language
from app import app, db
from app.forms import (
    LoginForm, RegistrationForm, EditProfileForm, PurchaseForm, ResetPasswordRequestForm, ResetPasswordForm
)
from app.models import User, Purchase, Shop
from app.email import send_password_reset_email
from app.translate import translate


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PurchaseForm()
    if form.validate_on_submit():
        language = guess_language(form.subject.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        shopname = form.shopname.data
        shop = Shop.query.filter_by(shopname=shopname).first()
        if shop is None:
            shop = Shop(shopname=shopname)
        purchaser = User.query.filter_by(username=form.purchaser.data).first()
        if purchaser is None:
            purchaser = current_user
        purchase = Purchase(
            purchase_date=form.purchase_date.data,
            purchaser=purchaser,
            value=form.value.data,
            seller=shop,
            subject=form.subject.data,
            author=current_user,
            language=language
        )
        db.session.add(purchase)
        db.session.commit()
        flash(_("Your purchase is traced now!"))
        return redirect(url_for('index'))
    else:
        page = request.args.get('page', 1, type=int)
        purchases = current_user.followed_purchases().paginate(
            page,
            app.config['PURCHASES_PER_PAGE'],
            False
        )
        next_url = url_for('index', page=purchases.next_num) if purchases.has_next else None
        prev_url = url_for('index', page=purchases.prev_num) if purchases.has_prev else None
        return render_template(
            'index.html',
            title=_("Home Page"),
            form=form,
            purchases=purchases.items,
            next_url=next_url,
            prev_url=prev_url
        )


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    purchases = Purchase.query.order_by(Purchase.timestamp.desc()).paginate(
        page,
        app.config['PURCHASES_PER_PAGE'],
        False
    )
    next_url = url_for('explore', page=purchases.next_num) if purchases.has_next else None
    prev_url = url_for('explore', page=purchases.prev_num) if purchases.has_prev else None
    return render_template(
        'index.html',
        title=_('Explore'),
        purchases=purchases.items,
        next_url=next_url,
        prev_url=prev_url
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    else:
        return render_template('login.html', title=_("Sign In"), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# noinspection PyArgumentList
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_("Congratulations, you are now a registered user!"))
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title=_('Register'), form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    purchases = user.purchases.order_by(Purchase.timestamp.desc()).paginate(
        page,
        app.config['PURCHASES_PER_PAGE'],
        False
    )
    next_url = url_for('user', username=user.username, page=purchases.next_num) if purchases.has_next else None
    prev_url = url_for('user', username=user.username, page=purchases.prev_num) if purchases.has_prev else None
    return render_template(
        'user.html',
        user=user,
        purchases=purchases.items,
        next_url=next_url,
        prev_url=prev_url
    )


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.remindings = form.remindings.data
        db.session.commit()
        flash(_("Your changes have been saved."))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.remindings.data = current_user.remindings
        return render_template('edit_profile.html', title=_("Edit Profile"), form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_("User %(username)s not found.", username=username))
        return redirect(url_for('index'))
    elif user == current_user:
        flash(_("You cannot follow yourself!"))
        return redirect(url_for('user', username=username))
    else:
        current_user.follow(user)
        db.session.commit()
        flash(_("You are following %(username)s!", username=username))
        return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_("User %(username)s not found.", username=username))
        return redirect(url_for('index'))
    elif user == current_user:
        flash(_("You cannot unfollow yourself!"))
        return redirect(url_for('user', username=username))
    else:
        current_user.unfollow(user)
        db.session.commit()
        flash(_("You are not following %(username)s!", username=username))
        return redirect(url_for('user', username=username))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_("Check your email for instructions to reset your password"))
        return redirect(url_for('login'))
    else:
        return render_template('reset_password_request.html', title=_("Reset Password"), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif not user:
        return redirect(url_for('index'))
    elif form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Your password has been reset."))
        return redirect(url_for('login'))
    else:
        return render_template('reset_password.html', form=form)


@app.route('/translate', methods=['Post'])
@login_required
def translate():
    return jsonify(
        {
            'text': translate(
                request.form['text'],
                src=request.form['source_language'],
                dest=request.form['dest_language']
            )
        }
    )
