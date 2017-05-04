from flask import current_app
from . import db, login_manager, bcrypt
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


relationship_table = db.Table('relationship_table',
                              db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
                              db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
                              db.PrimaryKeyConstraint('order_id', 'product_id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    mob = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    address_1 = db.Column(db.String(256), nullable=False)
    address_2 = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    pincode = db.Column(db.Integer)
    member_since = db.Column(db.DateTime(), default=datetime.now)
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    def password_hash(self, password):      # Stores the value of password by hashing it first
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):    # Checks if password given is correct or not
        return bcrypt.check_password_hash(self.password, password)

    def generate_confirmation_token(self, expiration=86400):    # generating encrypted tokens
        # Using id of the user for expiration of 1 day
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})                    # dict object for storing the id

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)           # Loads the token back to dict form
        except:
            return False                    # for any exceptions
        if data.get('confirm') != self.id:  # if the token did not verify
            return False
        try:
            self.confirmed = True           # if verified, adding in database
            db.session.add(self)
            db.session.commit()
            return True
        except:                             # for any exceptions
            db.session.rollback()
            return False

    def generate_reset_token(self, expiration=86400):   # token with 1 day expiration date
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})              # loading id of the user in token

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)               # loading id from token to verify
        except:
            return 'The link is expired. Please try again.'       # for exceptions
        if data.get('reset') != self.id:        # if not equal False
            return "Token couldn't be verified. Please try again."
        try:
            self.password_hash(new_password)    # creating hash for the new password
            db.session.add(self)                # adding new password
            db.session.commit()
            return 'True'
        except:
            db.session.rollback()               # if any exception rollback to previous stage
            return 'Something Went Wrong. Please try again'


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

    def is_administrator(self):
        return False


class Contact(db.Model):
    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, index=True)
    mob = db.Column(db.String(15), nullable=False)
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    description = db.Column(db.Text())


class Transaction(db.Model):
    __tablename__ = 'tranactions'
    id = db.Column(db.Integer, primary_key=True)
    acc_no = db.Column(db.String(20), nullable=False)
    acc_name = db.Column(db.String(64), nullable=False)
    bank = db.Column(db.String(64), nullable=False)
    ifsc = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Boolean, default=False)     # False: Buy, True: Sell
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    bit_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    products = db.relationship('Product', secondary=relationship_table, backref='orders')
    pick_up = db.Column(db.Date(), nullable=False)
    status = db.Column(db.String(20))
    service = db.Column(db.String(20))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(64), nullable=False)


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)


class Mobile(db.Model):
    __tabename__ = 'mobiles'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16), nullable=False, unique=True)


@login_manager.user_loader                  # callback function for login_manager
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser
