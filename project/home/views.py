###
# Imports
###
from project import app, db
from project.models import (BuySheet, SellSheet, DaySheet, BalSheet, LifeSheet, User)
from project.home.forms import (BuyForm, SellForm, DayForm, LifeForm, SummaryForm)
from project.home.helpers import (updateRecord, computeSummary, addDayRecord,
                                    preComputeSummary, writeSummary)
from project.home.dayHelpers import writeLedgerLife

from flask import Blueprint, flash, render_template, url_for, redirect, request
from flask_login import login_required, current_user
from datetime import datetime

###
# Config
###
home_blueprint = Blueprint('home', __name__,
                        template_folder = 'templates')

###
# Routes
###

####
# Editing a Buy Record
@home_blueprint.route('/buy/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def buyEdit(record_id):

    error = None
    buy_record = BuySheet.query.filter_by(id = record_id).first()
    form = BuyForm(request.form, obj=buy_record)

    if request.method == 'POST' and form.validate_on_submit():
        # False here tells updateRecord to deal with Sell side flow
        updateRecord(form, buy_record, True)
        return redirect(url_for('home.buyOpen'))
    else:
        return render_template('buyEdit.html', form=form, error=error)

####
# Adding a Buy Record
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
        # Add it to both Sell and Day Records.
        addDayRecord(form, buy_entry)

        return redirect(url_for('home.buyOpen'))
    else:
        return render_template('buyAdd.html', form=form, error=error)

####
# Gather all buy Positions
@home_blueprint.route('/buy/all')
@login_required # pragma: no cover
def buyAll():
    buy_records = BuySheet.query.filter_by(client_id = current_user.id).all()
    return render_template('buyAll.html', buy_records=buy_records)

####
# Gather buy open Positions
@home_blueprint.route('/buy/open')
@login_required # pragma: no cover
def buyOpen():
    buy_records = BuySheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    return render_template('buyOpen.html', buy_records=buy_records)

####
# Editing a Sell Record
@home_blueprint.route('/sell/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def sellEdit(record_id):

    error = None
    sell_record = SellSheet.query.filter_by(id = record_id).first()
    form = BuyForm(request.form, obj=sell_record)

    if request.method == 'POST' and form.validate_on_submit():
        # False here tells updateRecord to deal with Sell side flow
        updateRecord(form, sell_record, False)
        return redirect(url_for('home.sellOpen'))
    else:
        return render_template('sellEdit.html', form=form, error=error)

####
# Adding a Sell Record
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
        # Add it to both Sell and Day Records.
        addDayRecord(form, sell_entry)

        return redirect(url_for('home.sellOpen'))
    else:
        return render_template('sellAdd.html', form=form, error=error)

####
# Gather all sell Positions
@home_blueprint.route('/sell/all')
@login_required # pragma: no cover
def sellAll():
    sell_records = SellSheet.query.filter_by(client_id = current_user.id).all()
    return render_template('sellAll.html', sell_records=sell_records)

####
# Gather sell open Positions
@home_blueprint.route('/sell/open')
@login_required # pragma: no cover
def sellOpen():
    sell_records = SellSheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    return render_template('sellOpen.html', sell_records=sell_records)

####
# Summary Page
@home_blueprint.route('/summary', methods=['GET', 'POST'])   # pragma: no cover
@login_required   # pragma: no cover
def summary():

    # TODO: Margin variables to be extracted from a database, later
    margin_percent = 0.08
    form = SummaryForm(request.form)
    agreements, stored_summary = preComputeSummary()

    if request.method == 'POST' and form.validate_on_submit():
        open_buys, open_sells = writeSummary(form, agreements, stored_summary)
        writeLedgerLife(open_buys, open_sells)
        return redirect(url_for('home.summary'))

    # Pre fill the data from previously computed summary
    form.cur_month.data   = stored_summary.first_rate
    form.next_month.data  = stored_summary.second_rate
    form.later_month.data = stored_summary.third_rate

    # Deal with Buys
    buy_records = BuySheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    b_content = computeSummary(buy_records, stored_summary)

    # Deal with Sells
    sell_records = SellSheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    s_content = computeSummary(sell_records, stored_summary)

    ## The Summary
    volume = stored_summary.volume
    margin = volume * margin_percent
    run_loss = stored_summary.run_loss
    investment = margin - run_loss

    summary = {
        "margin": round(margin,5),
        "volume": round(volume,5),
        "run_loss": round(run_loss,5),
        "investment": round(investment,5)
    }

    return render_template('summary.html', form=form, b_content=b_content,
                s_content=s_content, summary=summary, agreements=agreements)

####
# dayRecords Page
@home_blueprint.route('/dayRecords', methods=['GET'])   # pragma: no cover
@login_required   # pragma: no cover
def dayRecords():
    day_records = DaySheet.query.filter_by(client_id = current_user.id).all()
    return render_template('dayRecords.html', day_records=day_records)

####
# Ledger/ Balance Records Page
@home_blueprint.route('/ledger', methods=['GET'])   # pragma: no cover
@login_required   # pragma: no cover
def ledger():
    bal_records = BalSheet.query.filter_by(client_id = current_user.id).all()
    return render_template('balRecords.html', bal_records=bal_records)

####
# Life Records Page
@home_blueprint.route('/life', methods=['GET'])   # pragma: no cover
@login_required   # pragma: no cover
def life():
    life_records = LifeSheet.query.filter_by(client_id = current_user.id).all()
    return render_template('lifeRecords.html', life_records=life_records)

###
# Hang on routes
###
@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')

@home_blueprint.route('/')
def index():
    return redirect(url_for('home.welcome'))
