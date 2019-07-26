###
# Imports
###
from project import app, db
from project.models import BuySheet, SellSheet, DaySheet, BalSheet, LifeSheet, User
from project.home.forms import BuyForm, SellForm, DayForm, BalForm, LifeForm
from flask import render_template, Blueprint, flash, url_for, redirect, request
from flask_login import login_required, current_user
from datetime import date, datetime

###
# Config
###

home_blueprint = Blueprint('home', __name__,
                        template_folder = 'templates')

###
# Helper Functions
###
'''
from functools import wraps
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap
'''

###
# Common Helper function for both Buy and See for updation
###
def updateRecord(request, form, record, error, is_buy=True):
    # According to Buy or Sell Sheet deal accordingly.
    if request.method == 'POST' and form.validate_on_submit():

        record.entry_date = form.entry_date.data
        record.ro_num = form.ro_num.data
        record.order_start_date = form.order_start_date.data
        record.agreement = form.agreement.data
        record.lot_size = form.lot_size.data
        record.lot_qty = form.lot_qty.data
        record.entry_rate = form.entry_rate.data
        record.entry_trade = form.entry_trade.data
        record.exit_date = form.exit_date.data
        record.exit_rate = form.exit_rate.data
        record.exit_trade = form.exit_trade.data

        # Compute the values
        exit_date = datetime.strptime(form.exit_date._value(),"%d/%m/%Y")
        start_date = datetime.strptime(form.order_start_date._value(),"%d/%m/%Y")
        days = (exit_date - start_date).days
        # This is to counter a problem with SQLAlchelmy not updating
        # an Integer flied with 0
        if days > 0:
            record.days_waiting = days

        if is_buy:
            record.rate_diff = record.exit_rate - record.entry_rate
        else:
            record.rate_diff = record.entry_rate - record.exit_rate

        record.profit = record.lot_qty * record.lot_size * record.rate_diff
        record.depth = record.depth # Computed during "summary" evaluation

        db.session.commit()

        # TODO
        # Now write to DaySheet
        #
        if is_buy:
            return redirect(url_for('home.buyOpen'))
        else:
            return redirect(url_for('home.sellOpen'))
    else:
        if is_buy:
            return render_template('buyEdit.html', form=form, error=error)
        else:
            return render_template('sellEdit.html', form=form, error=error)


###
# Routes
###

###
# Editing a Buy Record
###
@home_blueprint.route('/buy/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def buyEdit(record_id):

    error = None
    buy_record = BuySheet.query.filter_by(id = record_id).first()
    form = BuyForm(request.form, obj=buy_record)
    # True here tells updateRecord to deal with Buy side flow
    return updateRecord(request,form, buy_record, error, True)

###
# Adding a Buy Record
###
@home_blueprint.route('/buy/add', methods=['GET', 'POST'])
@login_required # pragma: no cover
def buyAdd():

    error = None
    form = BuyForm(request.form)

    if form.validate_on_submit():
        buy_entry = BuySheet(
            form.entry_date.data,
            form.ro_num.data,
            form.order_start_date.data,
            form.agreement.data,
            form.lot_size.data,
            form.lot_qty.data,
            form.entry_rate.data,
            form.entry_trade.data,
            client_id=current_user.id
        )
        db.session.add(buy_entry)
        db.session.commit()
        # TODO
        # Now write to DaySheet
        #
        return redirect(url_for('home.buyOpen'))
    else:
        return render_template('buyAdd.html', form=form, error=error)


###
# Gather all buy Positions
###
@home_blueprint.route('/buy/all')
@login_required # pragma: no cover
def buyAll():
    buy_records = BuySheet.query.filter_by(client_id = current_user.id).all()
    return render_template('buyAll.html', buy_records=buy_records)

###
# Gather buy open Positions
###
@home_blueprint.route('/buy/open')
@login_required # pragma: no cover
def buyOpen():
    buy_records = BuySheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    return render_template('buyOpen.html', buy_records=buy_records)


###
# Editing a Sell Record
###
@home_blueprint.route('/sell/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def sellEdit(record_id):

    error = None
    sell_record = SellSheet.query.filter_by(id = record_id).first()
    form = BuyForm(request.form, obj=sell_record)
    # False here tells updateRecord to deal with Sell side flow
    return updateRecord(request, form, sell_record, error, False)

###
# Adding a Sell Record
###
@home_blueprint.route('/sell/add', methods=['GET', 'POST'])
@login_required # pragma: no cover
def sellAdd():

    error = None
    form = SellForm(request.form)

    if form.validate_on_submit():
        sell_entry = SellSheet(
            form.entry_date.data,
            form.ro_num.data,
            form.order_start_date.data,
            form.agreement.data,
            form.lot_size.data,
            form.lot_qty.data,
            form.entry_rate.data,
            form.entry_trade.data,
            client_id=current_user.id
        )
        db.session.add(sell_entry)
        db.session.commit()
        # TODO
        # Now write to DaySheet
        #
        return redirect(url_for('home.sellOpen'))
    else:
        return render_template('sellAdd.html', form=form, error=error)


###
# Gather all sell Positions
###
@home_blueprint.route('/sell/all')
@login_required # pragma: no cover
def sellAll():
    sell_records = SellSheet.query.filter_by(client_id = current_user.id).all()
    return render_template('sellAll.html', sell_records=sell_records)

###
# Gather sell open Positions
###
@home_blueprint.route('/sell/open')
@login_required # pragma: no cover
def sellOpen():
    sell_records = SellSheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    return render_template('sellOpen.html', sell_records=sell_records)


# use decorators to link the function to a url
@home_blueprint.route('/summary', methods=['GET', 'POST'])   # pragma: no cover
@login_required   # pragma: no cover
def summary():
    '''
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            form.title.data,
            form.description.data,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted.')
        return redirect(url_for('home.home'))
    else:
        #posts = db.session.query(BlogPost).all()

    error = None
    form = None
    posts = None
    '''
    return render_template('summary.html')
    # render_template('home.html', posts=posts, form=form, error=error)

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')

@home_blueprint.route('/')
def index():
    return redirect(url_for('home.welcome'))
