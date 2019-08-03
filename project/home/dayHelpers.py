###
# Imports
###
from project import db
from project.models import DaySheet, SummarySheet, BalSheet, LifeSheet

#from flask import render_template, redirect, request
from flask_login import current_user
from datetime import datetime, date

####
# Helper Functions that are suppose-dly used once in a day
####

####
# Add default Balance
def addDefaultBalance(entry_date = date.today(), bank_name = "Bank", credit = 0,
                debit = 0, book_profit = 0, volume = 0, run_loss = 0):

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
# Write to Ledger and Life
# We will be working with summary and Day Sheets.
####
def writeLedgerLife(open_b, open_s):

    day_record = DaySheet.query.filter_by(client_id = current_user.id
                    ).order_by(DaySheet.id.desc()).first()
    summary = SummarySheet.query.filter_by(client_id = current_user.id).first()

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
        day_record.total_profit,
        open_b,
        open_s,
        summary.volume,
        summary.run_loss,
        net_profit,
        net_amt,
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
