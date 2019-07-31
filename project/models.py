from project import db
from project import bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import date, datetime

# Buy and Sell Records
class BuySheet(db.Model):

    __tablename__ = 'buy_sheet'

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
    ro_num = db.Column(db.Integer, nullable=False, default=0)
    order_start_date = db.Column(db.Date, nullable=False)
    agreement = db.Column(db.String, nullable=False)
    lot_size = db.Column(db.Integer, nullable=False)
    lot_qty = db.Column(db.Integer, nullable=False)
    entry_rate = db.Column(db.Float, nullable=False)
    entry_trade = db.Column(db.String, nullable=False)
    days_waiting = db.Column(db.Integer, default=0)
    exit_date = db.Column(db.Date)
    exit_rate = db.Column(db.Float)
    exit_trade = db.Column(db.String)
    rate_diff = db.Column(db.Float)
    profit = db.Column(db.Float)
    depth = db.Column(db.Float)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, entry_date, ro_num, order_start_date, agreement,
                lot_size, lot_qty, entry_rate, entry_trade, days_waiting=0,
                exit_date=None, exit_rate=None, exit_trade=None, rate_diff=None,
                profit=None, depth=None, client_id=None):
        self.entry_date = entry_date
        self.ro_num = ro_num
        self.order_start_date = order_start_date
        self.agreement = agreement
        self.lot_size = lot_size
        self.lot_qty = lot_qty
        self.entry_rate = entry_rate
        self.entry_trade = entry_trade
        self.days_waiting = days_waiting
        self.exit_date = exit_date
        self.exit_rate = exit_rate
        self.exit_trade = exit_trade
        self.rate_diff = rate_diff
        self.profit = profit
        self.depth = depth
        self.client_id = client_id

# Sell and Buy Records
class SellSheet(db.Model):

    __tablename__ = 'sell_sheet'

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
    ro_num = db.Column(db.Integer, nullable=False, default=0)
    order_start_date = db.Column(db.Date, nullable=False)
    agreement = db.Column(db.String, nullable=False)
    lot_size = db.Column(db.Integer, nullable=False)
    lot_qty = db.Column(db.Integer, nullable=False)
    entry_rate = db.Column(db.Float, nullable=False)
    entry_trade = db.Column(db.String, nullable=False)
    days_waiting = db.Column(db.Integer, default=0)
    exit_date = db.Column(db.Date)
    exit_rate = db.Column(db.Float)
    exit_trade = db.Column(db.String)
    rate_diff = db.Column(db.Float)
    profit = db.Column(db.Float)
    depth = db.Column(db.Float)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, entry_date, ro_num, order_start_date, agreement,
                lot_size, lot_qty, entry_rate, entry_trade, days_waiting=0,
                exit_date=None, exit_rate=None, exit_trade=None, rate_diff=None,
                profit=None, depth=None, client_id=None):
        self.entry_date = entry_date
        self.ro_num = ro_num
        self.order_start_date = order_start_date
        self.agreement = agreement
        self.lot_size = lot_size
        self.lot_qty = lot_qty
        self.entry_rate = entry_rate
        self.entry_trade = entry_trade
        self.days_waiting = days_waiting
        self.exit_date = exit_date
        self.exit_rate = exit_rate
        self.exit_trade = exit_trade
        self.rate_diff = rate_diff
        self.profit = profit
        self.depth = depth
        self.client_id = client_id

# Day Book
class DaySheet(db.Model):

    __tablename__ = 'day_sheet'

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
    agreement = db.Column(db.String, nullable=False)
    lot_size = db.Column(db.Integer, nullable=False)
    lot_qty = db.Column(db.Integer, nullable=False)
    trade_rate = db.Column(db.Float, nullable=False)
    trade_type = db.Column(db.String, nullable=False)
    profit = db.Column(db.Float)
    total_profit = db.Column(db.Float)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, entry_date, agreement, lot_size, lot_qty, trade_rate,
                trade_type, profit=0, total_profit=0, client_id=None):
        self.entry_date = entry_date
        self.agreement = agreement
        self.lot_size = lot_size
        self.lot_qty = lot_qty
        self.trade_rate = trade_rate
        self.trade_type = trade_type
        self.profit = profit
        self.total_profit = total_profit
        self.client_id = client_id


# Balance Records
class BalSheet(db.Model):

    __tablename__ = 'bal_sheet'

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
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

    def __init__(self, entry_date, bank_name, credit, tot_credit, debit,
                tot_debit, net_credit, book_profit, open_buys, open_sells,
                volume, run_loss, net_profit, net_amount, client_id):
        self.entry_date = entry_date
        self.bank_name = bank_name
        self.credit = credit
        self.tot_credit = tot_credit
        self.debit = debit
        self.tot_debit = tot_debit
        self.net_credit = net_credit
        self.book_profit = book_profit
        self.open_buys = open_buys
        self.open_sells = open_sells
        self.volume = volume
        self.run_loss = run_loss
        self.net_profit = net_profit
        self.net_amount = net_amount
        self.client_id = client_id


# Life Records
class LifeSheet(db.Model):

    __tablename__ = 'life_sheet'

    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False)
    max_open_pos = db.Column(db.Integer, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)
    margin_used = db.Column(db.Float, nullable=False)
    life = db.Column(db.Float, nullable=False)

    client_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, entry_date, max_open_pos, net_amount, margin_used,
                    life, client_id):
        self.entry_date = entry_date
        self.max_open_pos = max_open_pos
        self.net_amount = net_amount
        self.margin_used = margin_used
        self.life = life
        self.client_id = client_id

# User Records
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    mobile = db.Column(db.String, nullable=False)
    regDate = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String, nullable=False)
    broker = db.Column(db.String, nullable=False)
    station = db.Column(db.String, nullable=False)
    dormant = db.Column(db.Boolean, nullable=False)

    buy_sheet = relationship("BuySheet", backref="buy_sheet")
    sell_sheet = relationship("SellSheet", backref="sell_sheet")
    day_sheet = relationship("DaySheet", backref="day_sheet")
    bal_sheet = relationship("BalSheet", backref="bal_sheet")
    life_sheet = relationship("LifeSheet", backref="life_sheet")
    #ro_sheet = relationship("ROSheet", backref="ro")

    def __init__(self, name, email, password, birth_date, mobile="000",
            regDate=datetime.now(), role="Client", broker="ABML",
            station="HYD-10", dormant=False):
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
