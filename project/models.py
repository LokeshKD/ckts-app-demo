from project import db
from project import bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import date, datetime

# Buy and Sell Records
class BuySheet(db.Model):

    __tablename__ = "buySheet"

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    ro_num = db.Column(db.Integer, nullable=False, default=0)
    order_start_date = db.Column(db.Date, nullable=False)
    agreement = db.Column(db.String, nullable=False)
    lot_size = db.Column(db.Integer, nullable=False)
    lot_qty = db.Column(db.Integer, nullable=False)
    entry_rate = db.Column(db.Float, nullable=False)
    entry_trade = db.Column(db.String, nullable=False)
    days_waiting = db.Column(db.Integer)
    exit_date = db.Column(db.Date)
    exit_rate = db.Column(db.Float)
    exit_trade = db.Column(db.String)
    rate_diff = db.Column(db.Float)
    profit = db.Column(db.Float)
    depth = db.Column(db.Float)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

# Sell and Buy Records
class SellSheet(db.Model):

    __tablename__ = "sellSheet"

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    ro_num = db.Column(db.Integer, nullable=False, default=0)
    order_start_date = db.Column(db.Date, nullable=False)
    agreement = db.Column(db.String, nullable=False)
    lot_size = db.Column(db.Integer, nullable=False)
    lot_qty = db.Column(db.Integer, nullable=False)
    entry_rate = db.Column(db.Float, nullable=False)
    entry_trade = db.Column(db.String, nullable=False)
    days_waiting = db.Column(db.Integer)
    exit_date = db.Column(db.Date)
    exit_rate = db.Column(db.Float)
    exit_trade = db.Column(db.String)
    rate_diff = db.Column(db.Float)
    profit = db.Column(db.Float)
    depth = db.Column(db.Float)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

# Day Book
class DaySheet(db.Model):

    __tablename__ = "daySheet"

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    agreement = db.Column(db.String, nullable=False)
    lot_size = db.Column(db.Integer, nullable=False)
    lot_qty = db.Column(db.Integer, nullable=False)
    trade_rate = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float)
    total_profit = db.Column(db.Float)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

# Balance Records
class BalSheet(db.Model):

    __tablename__ = "balSheet"

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    bank_name = db.Column(db.String, nullable=False)
    credit = db.Column(db.Float, nullable=False)
    tot_credit = db.Column(db.Float, nullable=False)
    debit = db.Column(db.Float, nullable=False)
    tot_debit = db.Column(db.Float, nullable=False)
    net_credit = db.Column(db.Float, nullable=False)
    book_profit = db.Column(db.Float, nullable=False)
    open_buys = db.Column(db.Integer, nullable=False)
    open_sells = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    run_loss = db.Column(db.Float, nullable=False)
    net_profit = db.Column(db.Float, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

# Life Records
class LifeSheet(db.Model):

    __tablename__ = "lifeSheet"

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    max_open_pos = db.Column(db.Integer, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)
    margin_used = db.Column(db.Float, nullable=False)
    life = db.Column(db.Float, nullable=False)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

# User Records
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    mobile = db.Column(db.String, nullable=False)
    regDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role = db.Column(db.String, nullable=False, default="Client")
    broker = db.Column(db.String, nullable=False, default="ABML")
    station = db.Column(db.String, nullable=False, default="HYD-10")
    dormant = db.Column(db.Boolean, nullable=False, default=False)

    buy_sheet = relationship("BuySheet", backref="buy")
    sell_sheet = relationship("SellSheet", backref="sell")
    day_sheet = relationship("DaySheet", backref="day")
    bal_sheet = relationship("BalSheet", backref="bal")
    life_sheet = relationship("LifeSheet", backref="life")
    #ro_sheet = relationship("ROSheet", backref="ro")

    def __init__(self, name, email, password, birth_date, regDate=datetime.utcnow,
            mobile="000", role="Client", broker="ABML", station="HYD-10", dormant=False):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.birth_date = birth_date
        self.regDate = regDate
        self.mobile = mobile
        self.role = role
        self.broker = broker
        self.station = station
        self.dormant = dormant

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_dormant(self):
        return self.dormant

    def __repr__(self):
        return '<name {}>'.format(self.name)
