###
# Imports
###
from project import db
from project.models import (BuySheet, SellSheet, DaySheet, SummarySheet,
                        BalSheet, LifeSheet, ROSheet)
from project.home.helpers import preComputeSummary, updateRecord, addDayRecord

#from flask import render_template, redirect, request
from flask_login import current_user
from datetime import datetime, date

####
# Helper Functions that are suppose-dly used once in a day or late
####

####
# Add default Balance
def addDefaultBalance(entry_date = date.today(), bank_name = "Bank", credit = 0.0,
                debit = 0.0, book_profit = 0.0, volume = 0.0, run_loss = 0.0):

    entry = BalSheet(
        entry_date = entry_date,
        bank_name = bank_name,
        credit = credit,
        tot_credit = credit,
        debit = debit,
        tot_debit = debit,
        net_credit = credit,
        book_profit = book_profit,
        open_buys = 0,
        open_sells = 0,
        volume = volume,
        run_loss = run_loss,
        net_profit = book_profit + run_loss,
        net_amount = credit + book_profit + run_loss,
        client_id = current_user.id
    )
    db.session.add(entry)
    db.session.commit()
    return entry

####
# Add Default dayRecord
def addDefaultDayRecord():
    entry = DaySheet(
        entry_date = date.today(),
        agreement = "None",
        lot_size = 75,
        lot_qty = 1,
        trade_rate = 0.0,
        trade_type = "None",
        profit = 0.0,
        total_profit = 0.0,
        client_id = current_user.id
    )
    db.session.add(entry)
    db.session.commit()
    return entry

####
# Write to Ledger and Life
# We will be working with summary and Day Sheets
def writeLedgerLife(open_b, open_s):

    day_record = DaySheet.query.filter_by(client_id = current_user.id
                            ).order_by(DaySheet.id.desc()).first()
    if not day_record:
        day_record = addDefaultDayRecord()

    summary = SummarySheet.query.filter_by(client_id = current_user.id).first()
    if not summary:
        ignore, summary = preComputeSummary()

    balance = BalSheet.query.filter_by(client_id = current_user.id
                    ).order_by(BalSheet.id.desc()).first()
    if not balance:
        balance = addDefaultBalance(entry_date = day_record.entry_date)

    net_credit = balance.tot_credit - balance.tot_debit
    net_profit = day_record.total_profit + summary.run_loss
    net_amt = net_credit + net_profit

    bal_entry = BalSheet(
        day_record.entry_date,
        balance.bank_name,
        balance.credit,
        balance.tot_credit,
        balance.debit,
        balance.tot_debit,
        net_credit,
        round(day_record.total_profit,2),
        open_b,
        open_s,
        round(summary.volume, 2),
        round(summary.run_loss,2),
        round(net_profit, 2),
        round(net_amt, 2),
        current_user.id
    )

    margin_percent = 0.08 # TODO : revisit once after gathering proper data.
    max_open_pos = (lambda: open_b, lambda: open_s)[open_s > open_b]()
    margin = summary.volume * margin_percent
    life = (net_amt - margin) / (max_open_pos * day_record.lot_size)

    life_entry = LifeSheet(
        day_record.entry_date,
        max_open_pos,
        round(net_amt, 2),
        round(margin, 2),
        round(life, 2),
        current_user.id
    )

    db.session.add(bal_entry)
    db.session.add(life_entry)
    db.session.commit()

####
# Roll Over a Record.
def roRecord(form, record, is_buy=True):
    # compute and commit Roll Over Record
    premium = float(form.ro_rate.data - form.expiry_rate.data + 10) # TODO Revisit

    ro_record = ROSheet(
        form.entry_date.data, form.agreement.data, form.lot_size.data,
        form.lot_qty.data, form.holding_type.data, form.expiry_rate.data,
        form.trade.data, form.ro_date.data, form.ro_agreement.data,
        form.ro_lot_size.data, form.ro_lot_qty.data, form.ro_rate.data,
        form.ro_trade.data, premium, current_user.id
    )
    db.session.add(ro_record)
    db.session.commit()

    #Update the Rolled over record
    record.exit_date = form.ro_date.data
    record.exit_rate = premium
    record.exit_trade = form.trade.data
    updateRecord(record, is_buy, float(form.expiry_rate.data))

    if is_buy:
        #Add a new Rolled over buy entry and push it to Day Record
        buy_entry = BuySheet(
          form.ro_date.data, record.ro_num + 1, record.order_start_date,
          form.ro_agreement.data, form.ro_lot_size.data, form.ro_lot_qty.data,
          form.ro_rate.data, form.ro_trade.data, client_id=current_user.id
        )
        addDayRecord(buy_entry)
    else:
        #Add a new Rolled over sell entry and push it to Day Record
        sell_entry = SellSheet(
          form.ro_date.data, record.ro_num + 1, record.order_start_date,
          form.ro_agreement.data, form.ro_lot_size.data, form.ro_lot_qty.data,
          form.ro_rate.data, form.ro_trade.data, client_id=current_user.id
        )
        addDayRecord(sell_entry)
