## Imports ###
from flask_wtf import FlaskForm
from wtforms import TextField, DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired

### Forms ###
class MessageForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])

# Form Representing Buy Sheet
class BuyForm(FlaskForm):
    entry_date = DateField('Entry Date', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    ro_num = IntegerField('Roll Over Number',
        validators=[DataRequired()]
    )
    order_start_date = DateField('Order Start Date', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    agreement = TextField('Agreement',
        validators=[DataRequired()]
    )
    lot_size = IntegerField('Lot Size',
        validators=[DataRequired()]
    )
    lot_qty = IntegerField('Lot Quantity',
        validators=[DataRequired()]
    )
    entry_rate = DecimalField('Entry Rate', places=5,
        validators=[DataRequired()]
    )
    entry_trade = TextField('Entry Trade Type',
        validators=[DataRequired()]
    )
    days_waiting = IntegerField('Days took to Close the Position')
    exit_date = DateField('Order Exit Date', format='%d/%m/%Y')
    exit_rate = DecimalField('Exit Rate', places=5)
    exit_trade = TextField('Exit Trade Type')
    rate_diff = DecimalField('Diffence in Exit and Entry Rates', places=5)
    profit = DecimalField('Profit made', places=5)
    depth = DecimalField('Profit made', places=5)

# For Representing Sell Sheet
class SellForm(FlaskForm):
    entry_date = DateField('Entry Date', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    ro_num = IntegerField('Roll Over Number',
        validators=[DataRequired()]
    )
    order_start_date = DateField('Order Start Date', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    agreement = TextField('Agreement',
        validators=[DataRequired()]
    )
    lot_size = IntegerField('Lot Size',
        validators=[DataRequired()]
    )
    lot_qty = IntegerField('Lot Quantity',
        validators=[DataRequired()]
    )
    entry_rate = DecimalField('Entry Rate', places=5,
        validators=[DataRequired()]
    )
    entry_trade = TextField('Entry Trade Type',
        validators=[DataRequired()]
    )
    days_waiting = IntegerField('Days took to Close the Position')
    exit_date = DateField('Order Exit Date', format='%d/%m/%Y')
    exit_rate = DecimalField('Exit Rate', places=5)
    exit_trade = TextField('Exit Trade Type')
    rate_diff = DecimalField('Diffence in Exit and Entry Rates', places=5)
    profit = DecimalField('Profit made', places=5)
    depth = DecimalField('Profit made', places=5)

# Form Representing Day Records
class DayForm(FlaskForm):
    entry_date = DateField('Entry Date', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    agreement = TextField('Agreement',
        validators=[DataRequired()]
    )
    lot_size = IntegerField('Lot Size',
        validators=[DataRequired()]
    )
    lot_qty = IntegerField('Lot Quantity',
        validators=[DataRequired()]
    )
    trade = TextField('Trade Type Executed',
        validators=[DataRequired()]
    )
    profit = DecimalField('Profit made for this Trade', places=5)
    total_profit = DecimalField('Total Profit', places=5)

# Form Representing Balance Sheet
class BalForm(FlaskForm):
    entry_date = DateField('Entry Date', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    bank_name = TextField('Bank Name',
        validators=[DataRequired()]
    )
    credit = DecimalField('Credit amount that came', places=5,
        validators=[DataRequired()]
    )
    tot_credit = DecimalField('Total Credit amount', places=5,
        validators=[DataRequired()]
    )
    debit = DecimalField('Debit amount taken', places=5,
        validators=[DataRequired()]
    )
    tot_debit = DecimalField('Total Debited amount', places=5,
        validators=[DataRequired()]
    )
    net_credit = DecimalField('Net Credit amount', places=5,
        validators=[DataRequired()]
    )
    book_profit = DecimalField('Booked Profit', places=5,
        validators=[DataRequired()]
    )
    open_buys = IntegerField('Open Buy Positions',
        validators=[DataRequired()]
    )
    open_sells = IntegerField('Open Sell Positions',
        validators=[DataRequired()]
    )
    volume = DecimalField('Volume', places=5,
        validators=[DataRequired()]
    )
    run_loss = DecimalField('Running Loss', places=5,
        validators=[DataRequired()]
    )
    net_profit = DecimalField('Net Profit', places=5,
        validators=[DataRequired()]
    )
    net_amount = DecimalField('Net Amount', places=5,
        validators=[DataRequired()]
    )

# Form Representing Life Sheet
class LifeForm(FlaskForm):
    entry_date = DateField('Entry Date', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    max_open_pos = IntegerField('Max Open Buy/Sell Positions',
        validators=[DataRequired()]
    )
    net_amount = DecimalField('Net Amount', places=5,
        validators=[DataRequired()]
    )
    margin_used = DecimalField('Margin Money Used', places=5,
        validators=[DataRequired()]
    )
    life = DecimalField('Life Remaining in Points', places=5,
        validators=[DataRequired()]
    )
