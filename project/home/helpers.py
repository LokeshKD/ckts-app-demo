###
# Imports
###
from project import db
from project.models import DaySheet, SummarySheet, BuySheet, SellSheet

#from flask import render_template, redirect, request
from flask_login import current_user
from datetime import datetime, date

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
####
# Retun a list of 3 nifty agreements. Current, Next and Later
# Each are in the format "Nifty Aug 19" ; an example
def getNiftyAgreements():
    # Simple solution for overflow.
    months = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                "Sep", "Oct", "Nov", "Dec", "Jan", "Feb" ]

    cur_month = datetime.today().month
    yr = datetime.today().year - 2000 # two digit year
    years = [str(yr) for i in range(3)]

    # Case for [19, 19, 20]
    if cur_month == 11:
        years[2] = str(yr+1)
    # Case for [19, 20, 20]
    if cur_month == 12:
        years[1:3] = [str(yr+1) for i in range(1,3)]

    agms = ["Nifty "+i for i in months[cur_month-1:cur_month+2]]
    return [agms[i] + " " + years[i] for i in range(3)]


####
# Add a default Summary Sheet
def addDefaultSummary(agms):
    ## Initialize
    entry = SummarySheet(
                0, 0, agms[0], 0, agms[1], 0, agms[2], 0, current_user.id
            )
    db.session.add(entry)
    db.session.commit()
    return entry

####
# pre-compute summary with proper data.
def preComputeSummary():
    agms = getNiftyAgreements()
    summary = SummarySheet.query.filter_by(client_id = current_user.id).first()
    if not summary:
        summary = addDefaultSummary(agms)
    return agms, summary

####
# Get rate based on value stored for THE Agreement
def getRate(agrmnt, summary):
    # get the month in smallcase
    mnth = agrmnt.split()[1].lower()

    if mnth in summary.first_label.lower():
        return summary.first_rate
    if mnth in summary.second_label.lower():
        return summary.second_rate
    if mnth in summary.third_label.lower():
        return summary.third_rate
    # Something is wrong
    return 0.0

####
# Update depth of each record and return
# volume and running loss of positions combined
def updateDepth(records, summary, is_buy=True):
    # Locals
    volume = 0.0
    run_loss = 0.0
    num = 0

    for record in records:
        num += 1
        depth = 0.0
        cur_rate = float(getRate(record.agreement, summary))

        if is_buy:
            depth = cur_rate - record.entry_rate
        else:
            depth = record.entry_rate - cur_rate

        if not record.depth or record.depth > depth:
            record.depth = round(depth, 2)

        volume += record.entry_rate * record.lot_qty * record.lot_size
        run_loss += record.depth * record.lot_qty * record.lot_size

    return num, volume, run_loss

####
# Write Summary; alongside update buy and sell records depth
def writeSummary(form, scrips, summary):

    summary.first_label = scrips[0]
    summary.first_rate = form.cur_month.data
    summary.second_label = scrips[1]
    summary.second_rate = form.next_month.data
    summary.third_label = scrips[2]
    summary.third_rate = form.later_month.data

    # Deal with Buys
    buy_records = BuySheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    b_num, b_vol, b_loss = updateDepth(buy_records, summary, True)

    # Deal with Sells
    sell_records = SellSheet.query.filter_by(client_id = current_user.id
                                ).filter_by(exit_date=None).all()
    s_num, s_vol, s_loss = updateDepth(sell_records, summary, False)

    summary.volume = (lambda: b_vol, lambda: s_vol)[s_vol > b_vol]()
    summary.run_loss = b_loss + s_loss

    db.session.commit()
    return b_num, s_num

####
# Common Helper function to compute summary for both Buy and Sell
def computeSummary(records, str_sum):
    # Local Variables
    content = []
    prev_value = 0.0

    ## Get the summary of open Buys
    for record in records:
        if not prev_value == 0.0:
            prev_value = record.entry_rate - prev_value

        cur_rate = getRate(record.agreement, str_sum)

        if not record.depth:
            record.depth = 0.0

        b_info = {
            "gap" : round(prev_value, 2),
            "agreement": record.agreement,
            "lot_qty": record.lot_qty,
            "entry_rate": round(record.entry_rate, 2),
            "cur_rate": round(cur_rate, 2),
            "depth": round(record.depth, 2)
        }
        prev_value = record.entry_rate
        content.append(b_info)

    return content


####
# Common Helper function for both Buy and Sell for updating
#  closing of a Position and making an entry into DaySheet
####
def updateRecord(record, is_buy=True, exit_rate=0):
    # Compute the values
    #exit_date = datetime.strptime(form.exit_date._value(),"%d/%m/%Y")
    #start_date = datetime.strptime(form.order_start_date._value(),"%d/%m/%Y")
    exit_date = datetime.strptime(str(record.exit_date),"%Y-%m-%d")
    start_date = datetime.strptime(str(record.order_start_date),"%Y-%m-%d")
    days = (exit_date - start_date).days

    # This is to counter a problem with SQLAlchelmy not updating
    # an Integer flied with 0
    if days > 0:
        record.days_waiting = days
    else:
        record.days_waiting = 0

    #Include deduction of brokerages at the time of exit
    #Brokerage should be calculated at both entry and exit times, though
    #TODO: Revisit this when we get complete info about brokerae & charges
    if is_buy:
        record.rate_diff = float(record.exit_rate) - record.entry_rate - (10 * record.lot_qty)
    else:
        record.rate_diff = record.entry_rate - float(record.exit_rate) - (10 * record.lot_qty)

    #If this is a Roll Over Update, maintain the following.
    #exit_rate will be filled by the caller for Roll Overs
    if 'RO' in record.exit_trade:
        record.rate_diff =  0.0
    else:
        exit_rate = record.exit_rate

    record.profit = float(record.lot_qty * record.lot_size * record.rate_diff)

    #Write to DaySheet
    #Get the last record for this user.
    day_record = DaySheet.query.filter_by(client_id = current_user.id
                    ).order_by(DaySheet.id.desc()).first()

    day_entry = DaySheet(
        record.exit_date,
        record.agreement,
        record.lot_size,
        record.lot_qty,
        exit_rate,
        record.exit_trade,
        round(record.profit, 2),
        round(day_record.total_profit + record.profit, 2),
        client_id=current_user.id
    )

    db.session.add(day_entry)
    db.session.commit()

####
# Add a Day record for each buy/sell NEW entry
####
def addDayRecord(entry):
    # Write to DaySheet
    # Get the last record for this user
    day_record = DaySheet.query.filter_by(client_id = current_user.id
                        ).order_by(DaySheet.id.desc()).first()
    total_profit = 0.0
    if day_record:
        total_profit = day_record.total_profit

    day_entry = DaySheet(
        entry.entry_date,
        entry.agreement,
        entry.lot_size,
        entry.lot_qty,
        entry.entry_rate,
        entry.entry_trade,
        0.0, # Profit for addition is always 0
        total_profit,
        client_id=current_user.id
    )

    db.session.add(entry)
    db.session.add(day_entry)
    db.session.commit()
