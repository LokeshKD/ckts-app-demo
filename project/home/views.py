###
# Imports
###
from project import app, db
from project.models import (BuySheet, SellSheet, DaySheet, BalSheet, LifeSheet,
                            ROSheet, User)
from project.home.forms import (BuyForm, SellForm, DayForm, LifeForm, ROForm,
                                SummaryForm)
from project.home.helpers import (updateRecord, computeSummary, addDayRecord,
                                    preComputeSummary, writeSummary)
from project.home.dayHelpers import writeLedgerLife, roRecord

from flask import Blueprint, flash, render_template, url_for, redirect, request
from flask_login import login_required, current_user
from datetime import datetime

###
# Config & Routes
###
home_blueprint = Blueprint('home', __name__, template_folder = 'templates')

####
# Roll Over a Buy Record
@home_blueprint.route('/buy/ro/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def buyRO(record_id):
    error = None
    buy_record = BuySheet.query.filter_by(id = record_id).first()
    form = ROForm(request.form)
    # Pre fill the data from the record
    form.entry_date.data = buy_record.entry_date
    form.agreement.data = buy_record.agreement
    form.lot_size.data = buy_record.lot_size
    form.lot_qty.data = buy_record.lot_qty
    form.holding_type.data = buy_record.entry_trade
    form.trade.data = 'RO_sell'
    form.ro_lot_size.data = buy_record.lot_size
    form.ro_lot_qty.data = buy_record.lot_qty
    form.ro_trade.data = 'RO_buy'

    if request.method == 'POST' and form.validate_on_submit():
        roRecord(form, buy_record, True)
        return redirect(url_for('home.buyOpen'))
    else:
        return render_template('buyRO.html', form=form, error=error)

####
# Editing a Buy Record
@home_blueprint.route('/buy/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def buyEdit(record_id):
    error = None
    buy_record = BuySheet.query.filter_by(id = record_id).first()
    form = BuyForm(request.form, obj=buy_record)
    form.exit_trade.data = 'sell'
    if request.method == 'POST' and form.validate_on_submit():
        buy_record.exit_date  = form.exit_date.data
        buy_record.exit_rate  = form.exit_rate.data
        buy_record.exit_trade = form.exit_trade.data
        updateRecord(buy_record, True)
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
    form.entry_trade.data = 'buy'
    if request.method == 'POST' and form.validate_on_submit():
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
        # Add it to both Buy and Day Records.
        addDayRecord(buy_entry)
        return redirect(url_for('home.buyOpen'))
    else:
        return render_template('buyAdd.html', form=form, error=error)

####
# Gather all buy Positions
@home_blueprint.route('/buy/all')
@login_required # pragma: no cover
def buyAll():
    buy_records = BuySheet.query.filter_by(client_id = current_user.id
                                    ).order_by(BuySheet.id).all()
    return render_template('buyAll.html', buy_records=buy_records)

####
# Gather buy open Positions
@home_blueprint.route('/buy/open')
@login_required # pragma: no cover
def buyOpen():
    buy_records = BuySheet.query.filter_by(client_id = current_user.id
                        ).filter_by(exit_date=None).order_by(BuySheet.id).all()
    return render_template('buyOpen.html', buy_records=buy_records)

####
# Roll Over a Sell Record
@home_blueprint.route('/sell/ro/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def sellRO(record_id):
    error = None
    sell_record = SellSheet.query.filter_by(id = record_id).first()
    form = ROForm(request.form)
    # Pre fill the data from the record
    form.entry_date.data = sell_record.entry_date
    form.agreement.data = sell_record.agreement
    form.lot_size.data = sell_record.lot_size
    form.lot_qty.data = sell_record.lot_qty
    form.holding_type.data = sell_record.entry_trade
    form.trade.data = 'RO_buy'
    form.ro_lot_size.data = sell_record.lot_size
    form.ro_lot_qty.data = sell_record.lot_qty
    form.ro_trade.data = 'RO_sell'

    if request.method == 'POST' and form.validate_on_submit():
        roRecord(form, sell_record, False)
        return redirect(url_for('home.sellOpen'))
    else:
        return render_template('sellRO.html', form=form, error=error)

####
# Editing a Sell Record
@home_blueprint.route('/sell/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required # pragma: no cover
def sellEdit(record_id):
    error = None
    sell_record = SellSheet.query.filter_by(id = record_id).first()
    form = SellForm(request.form, obj=sell_record)
    form.exit_trade.data = 'cover buy'
    if request.method == 'POST' and form.validate_on_submit():
        sell_record.exit_date  = form.exit_date.data
        sell_record.exit_rate  = form.exit_rate.data
        sell_record.exit_trade = form.exit_trade.data
        # False here tells updateRecord to deal with Sell side flow
        updateRecord(sell_record, False)
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
    form.entry_trade.data = 'short sell'
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
        addDayRecord(sell_entry)

        return redirect(url_for('home.sellOpen'))
    else:
        return render_template('sellAdd.html', form=form, error=error)

####
# Gather all sell Positions
@home_blueprint.route('/sell/all')
@login_required # pragma: no cover
def sellAll():
    sell_records = SellSheet.query.filter_by(client_id = current_user.id
                                ).order_by(SellSheet.id).all()
    return render_template('sellAll.html', sell_records=sell_records)

####
# Gather sell open Positions
@home_blueprint.route('/sell/open')
@login_required # pragma: no cover
def sellOpen():
    sell_records = SellSheet.query.filter_by(client_id = current_user.id
                        ).filter_by(exit_date=None).order_by(SellSheet.id).all()
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
                        ).filter_by(exit_date=None).order_by(BuySheet.id).all()
    b_content = computeSummary(buy_records, stored_summary)

    # Deal with Sells
    sell_records = SellSheet.query.filter_by(client_id = current_user.id
                        ).filter_by(exit_date=None).order_by(SellSheet.id).all()
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
    day_records = DaySheet.query.filter_by(client_id = current_user.id
                                            ).order_by(DaySheet.id).all()
    return render_template('dayRecords.html', day_records=day_records)

####
# Ledger/ Balance Records Page
@home_blueprint.route('/ledger', methods=['GET'])   # pragma: no cover
@login_required   # pragma: no cover
def ledger():
    bal_records = BalSheet.query.filter_by(client_id = current_user.id
                                            ).order_by(BalSheet.id).all()
    return render_template('balRecords.html', bal_records=bal_records)

####
# Life Records Page
@home_blueprint.route('/life', methods=['GET'])   # pragma: no cover
@login_required   # pragma: no cover
def life():
    life_records = LifeSheet.query.filter_by(client_id = current_user.id
                                            ).order_by(LifeSheet.id).all()
    return render_template('lifeRecords.html', life_records=life_records)

####
# Roll OVer Records Page
@home_blueprint.route('/rollOvers', methods=['GET'])   # pragma: no cover
@login_required   # pragma: no cover
def rollOvers():
    ro_records = ROSheet.query.filter_by(client_id = current_user.id
                                            ).order_by(ROSheet.id).all()
    return render_template('roRecords.html', ro_records=ro_records)

###
# Hang on routes
###
@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')

@home_blueprint.route('/')
def index():
    return redirect(url_for('home.welcome'))
