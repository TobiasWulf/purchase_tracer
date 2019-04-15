from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import get_locale
from flask_babel import lazy_gettext as _l
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, PurchaseForm
from app.models import User, Purchase, Shop
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PurchaseForm(purchaser=current_user.username)
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
            purchaser=purchaser.username,
            value=form.value.data,
            seller=shop,
            subject=form.subject.data,
            author=current_user,
            language=language
        )
        db.session.add(purchase)
        db.session.commit()
        flash(_l("Your purchase is traced now!"))
        return redirect(url_for('main.index'))
    else:
        page = request.args.get('page', 1, type=int)
        purchases = current_user.followed_purchases().paginate(
            page,
            current_app.config['PURCHASES_PER_PAGE'],
            False
        )
        next_url = url_for('main.index', page=purchases.next_num) \
            if purchases.has_next else None
        prev_url = url_for('main.index', page=purchases.prev_num) \
            if purchases.has_prev else None
        return render_template(
            'index.html',
            title=_l("Home Page"),
            form=form,
            purchases=purchases.items,
            next_url=next_url,
            prev_url=prev_url
        )


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    purchases = Purchase.query.order_by(Purchase.timestamp.desc()).paginate(
        page,
        current_app.config['PURCHASES_PER_PAGE'],
        False
    )
    next_url = url_for('main.explore', page=purchases.next_num) \
        if purchases.has_next else None
    prev_url = url_for('main.explore', page=purchases.prev_num) \
        if purchases.has_prev else None
    return render_template(
        'index.html',
        title=_l('Explore'),
        purchases=purchases.items,
        next_url=next_url,
        prev_url=prev_url
    )


# noinspection PyShadowingNames
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    purchases = user.purchases.order_by(Purchase.timestamp.desc()).paginate(
        page,
        current_app.config['PURCHASES_PER_PAGE'],
        False
    )
    next_url = url_for(
        'main.user',
        username=user.username,
        page=purchases.next_num
    ) if purchases.has_next else None
    prev_url = url_for(
        'main.user',
        username=user.username,
        page=purchases.prev_num
    ) if purchases.has_prev else None
    return render_template(
        'user.html',
        user=user,
        purchases=purchases.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.remindings = form.remindings.data
        db.session.commit()
        flash(_l("Your changes have been saved."))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.remindings.data = current_user.remindings
        return render_template(
            'edit_profile.html',
            title=_l("Edit Profile"),
            form=form
        )


# noinspection PyShadowingNames
@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_l("User %(username)s not found.", username=username))
        return redirect(url_for('main.index'))
    elif user == current_user:
        flash(_l("You cannot follow yourself!"))
        return redirect(url_for('main.user', username=username))
    else:
        current_user.follow(user)
        db.session.commit()
        flash(_l("You are following %(username)s!", username=username))
        return redirect(url_for('main.user', username=username))


# noinspection PyShadowingNames
@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_l("User %(username)s not found.", username=username))
        return redirect(url_for('main.index'))
    elif user == current_user:
        flash(_l("You cannot unfollow yourself!"))
        return redirect(url_for('main.user', username=username))
    else:
        current_user.unfollow(user)
        db.session.commit()
        flash(_l("You are not following %(username)s!", username=username))
        return redirect(url_for('main.user', username=username))


@bp.route('/translate', methods=['Post'])
@login_required
def translate_text():
    return jsonify(
        dict(
            text=translate(
                request.form['text'],
                src=request.form['source_language'],
                dest=request.form['dest_language']
            )
        )
    )
