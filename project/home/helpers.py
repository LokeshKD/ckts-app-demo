###
# Imports
###
from project import db

from flask import render_template, redirect, request
from datetime import datetime

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
# Common Helper function to compute summary for both Buy and Sell
###
def computeSummary(records, is_buy=True):
    # Local Variables
    content = []
    info = {}
    volume = 0
    prev_value = 0
    cur_rate = 0
    run_loss = 0
    unq_agreement = []

    ### TODO
    ## Get unique agreemnt and current rate, rudimentary method
    for record in records:
        if cur_rate == 0:
            cur_rate = record.entry_rate

        if is_buy:
            if cur_rate > record.entry_rate:
                cur_rate = record.entry_rate
        else:
            if cur_rate < record.entry_rate:
                cur_rate = record.entry_rate

        if record.agreement.upper() not in unq_agreement:
            unq_agreement.append(record.agreement)

    ## Get the summary of open Buys
    for record in records:
        if not prev_value:
            prev_value = record.entry_rate - prev_value

        if is_buy:
            depth = cur_rate - record.entry_rate
        else:
            depth = record.entry_rate - cur_rate

        b_info = {
            "gap" : round(prev_value, 2),
            "agreement": record.agreement,
            "lot_qty": record.lot_qty,
            "entry_rate": record.entry_rate,
            "cur_rate": cur_rate,
            "depth": round(depth, 2)
        }
        prev_value = record.entry_rate
        content.append(b_info)
        # TODO re-compute margin after getting prorper cur_rate
        volume += record.entry_rate * record.lot_qty * record.lot_size
        run_loss += depth * record.lot_qty * record.lot_size

    return content, volume, run_loss, unq_agreement


###
# Common Helper function for both Buy and Sell for updation
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
        else:
            record.days_waiting = 0

        # Include deduction of brokerages at the time of exit
        # Brokerage should be calculated at both entry and exit times, though
        # TODO: Revisit this when we get complete info about brokerae & charges
        if is_buy:
            record.rate_diff = record.exit_rate - record.entry_rate - (10 * record.lot_qty)
        else:
            record.rate_diff = record.entry_rate - record.exit_rate - (10 * record.lot_qty)

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
