# -*- coding: utf-8 -*-
# noinspection PyUnresolvedReferences
"""Describe the application database tables to handle the application data
(backend). The models or tables are described with the SQLAlchemy orm layer.
The database tables are of two different types of tables. The first type of
table is a basic data table which includes mixed data and described by a class
(SQLAlchemy Model). The second type of table is a cross reference table which
only includes ids from data tables as foreign keys.

.. module:: models
   :platform: Unix, Windows
   :synopsis: Describe the application database models or tables for Flask.

.. moduleauthor:: Tobias Wulf <tobias.x57756c66@gmail.com>
   :version: 0.9
   :status: development

:Classes:

    :class:`Shop`
    :class:`User`
    :class:`Purchase`

:Attributes:

    :param followers: User follower references.
                      Connected user ids (foreign keys).
    :type followers: db.Table

:Functions:

    :func:`load_user`

.. seealso::

    :mod:`flask_login`
    :mod:`werkzeug.security`
    :mod:`hashlib`
    :mod:`jwt`
    :mod:`datetime`
    :mod:`time`
    :mod:`app`
"""

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
from datetime import datetime
from time import time
from app import db, login
import pandas as pd
import numpy as np
import os.path as op


# noinspection PyShadowingBuiltins
@login.user_loader
def load_user(id):
    """Connect db user table with flask login."""
    return User.query.get(int(id))


# followers association table
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# purchases association table, user made purchases
purchases_table = db.Table(
    'purchases_table',
    db.Column('purchaser_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('purchase_id', db.Integer, db.ForeignKey('purchase.id'))
)


# noinspection PyUnresolvedReferences
class Shop(db.Model):
    """Describe database table of shops where users do purchases.

    :Attributes:

        :param __tablename__: Database table name.
        :type __tablename__: str
        :param id: Primary key. New assigned for every entry. Unique.
        :type id: int
        :param shopname: Name of the shop.
        :type shopname: str
        :param purchases: Reference to each purchase as foreign key. Fetched
                          by shop id in purchase table.
        :type purchases: db.relationship
    """

    ___tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    shopname = db.Column(db.String(64), index=True, unique=True)
    sales = db.relationship('Purchase', backref='seller', lazy='dynamic')

    def __repr__(self):
        """Print for single element of database table."""
        return "<Shop {}>".format(self.shopname)


class UnknownUserError(Exception):
    pass


# noinspection PyBroadException,PyShadowingBuiltins
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Purchase', backref='author', lazy='dynamic')
    purchases = db.relationship(
        'Purchase',
        secondary=purchases_table,
        backref='user_purchase',
        lazy='dynamic'
    )
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    remindings = db.Column(db.String(140))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size
        )

    def add_purchase(self, purchase):
        if not self.bought(purchase):
            self.purchases.append(purchase)

    def rm_purchase(self, purchase):
        if self.bought(purchase):
            self.purchases.remove(purchase)

    def bought(self, purchase):
        return self.purchases.filter(
            purchases_table.c.purchase_id == purchase.id
        ).count() > 0

    def bought_purchases(self):
        purchased = Purchase.query.join(
            purchases_table,
            (purchases_table.c.purchase_id == Purchase.id)).filter(
            purchases_table.c.purchaser_id == self.id
        )
        return purchased.order_by(Purchase.timestamp.desc())

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    def followed_purchases(self):
        followed = Purchase.query.join(
            followers, (followers.c.followed_id == Purchase.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )
        own = Purchase.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Purchase.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms='HS256'
            )['reset_password']
        except:
            return
        return User.query.get(id)

    @classmethod
    def get_user_list(cls):
        return User.query.order_by(User.username)

    def __repr__(self):
        return "<User {}>".format(self.username)


_dtypes = dict(
    user=np.str,
    purchaser=np.str,
    purchase_date=str,
    shop=np.str,
    subject=np.str,
    value=np.float32
)
_csv_path = 'notebooks/purchase_list.csv'


class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    subject = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    purchaser = db.relationship(
        'User',
        secondary=purchases_table,
        backref='purchase_user',
        lazy='dynamic'
    )
    purchase_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return "<Value {}€>".format(str(self.value))

    def get_purchaser(self):
        find_user = User.query.join(
            purchases_table,
            (purchases_table.c.purchaser_id == User.id)).filter(
            purchases_table.c.purchase_id == self.id)
        return find_user.first()

    # noinspection PyDefaultArgument
    @classmethod
    def _load_from_csv(cls, path: str = _csv_path, dtypes: dict = _dtypes):
        """Load purchases from .csv file."""

        if not op.isfile(path):
            raise FileNotFoundError(path)
        return pd.read_csv(
            'notebooks/purchase_list.csv',
            sep=';',
            header=0,
            dtype=dtypes,
            parse_dates=['purchase_date']
        )

    @classmethod
    def _add_purchases_from_csv(cls):
        """Add purchases from .csv file to database table. Works only with
        known users.
        """

        for index, row in Purchase._load_from_csv().iterrows():
            user = User.query.filter_by(username=row['user']).first()
            if user is None:
                db.session.rollback()
                raise UnknownUserError("user {0} unknown".format(row['user']))
            purchaser = User.query.filter_by(username=row['purchaser']).first()
            if purchaser is None:
                db.session.rollback()
                raise UnknownUserError(
                    "purchaser {0} unknown".format(row['purchaser'])
                )
            shop = Shop.query.filter_by(shopname=row['shop']).first()
            if shop is None:
                shop = Shop(shopname=row['shop'])
                db.session.add(shop)

            check_purchase_exists_query = db.session.query(Purchase).filter(
                Purchase.user_id == user.id,
                Purchase.purchase_date == row['purchase_date'],
                Purchase.shop_id == shop.id,
                Purchase.subject == row['subject'],
                Purchase.value == row['value']
            )

            if not db.session.query(
                    check_purchase_exists_query.exists()).scalar():
                purchase = Purchase(
                        author=user,
                        purchase_date=row['purchase_date'],
                        seller=shop,
                        subject=row['subject'],
                        value=row['value'],
                        language=''
                )
                purchaser.add_purchase(purchase)
                db.session.add(purchase)
        db.session.commit()
