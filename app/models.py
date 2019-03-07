# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 08:22:04 2019

@author: dep17364
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
from datetime import datetime
from time import time
from app import db, login, app


# connect db user table with flask login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# followers association table
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class Shop(db.Model):
    ___tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    shopname = db.Column(db.String(64), index=True, unique=True)
    purchases = db.relationship('Purchase', backref='seller', lazy='dynamic')

    def __repr__(self):
        return "<Shop {}>".format(self.shopname)


# db user table 
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    purchases = db.relationship('Purchase', backref='author', lazy='dynamic')
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
            app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms='HS256'
            )['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    subject = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    purchaser = db.Column(db.String(64))
    purchase_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return "<Value {}€>".format(str(self.value))
