import numpy as np
import pandas as pd
from scipy.optimize import fsolve


def irr_equation(x, df, current_value):
    total = -current_value
    for days, row in df.iterrows():
        total += row.Amount * x**(days/365)
    return total


def internal_rate_of_return(df, current_value, initial_guess):
    xzero = fsolve(irr_equation, initial_guess, args=(df, current_value,))
    annualized_irr = xzero[0] -1 
    # cont_comp_irr = np.log(annualized_irr+1)
    return annualized_irr


def analyze_pnl(current_value, df) :
    """ 
    :param current_value: number.
    :param df: pd.DataFrame indexed by integers and having a column "Amount".
    The Amount represents the amount invested. Negative numbers are withdraws.
    The row index for the Amount is the number of days that has passed since the Amount was invested,
    and the date on which the given current_value was reached.

    :return irr: the continuously compounded internal rate of return
    """
    total_invested = df.Amount.sum()
    cash_pnl = current_value - total_invested
    overall_return = cash_pnl / total_invested
    initial_guess = np.exp(overall_return)
    # print(f"    debug initial_guess {initial_guess}")
    irr = internal_rate_of_return(df, current_value, initial_guess)
    return irr, cash_pnl, overall_return, total_invested


def report_pnl(irr, cash_pnl, initial_guess, current_value, total_invested):
    print(f"Value today            : {current_value:,.2f}")
    print(f"Total invested         : {total_invested:,.2f}")
    print(f"Cash PnL               : {cash_pnl:,.2f}")
    print(f"Overall return         : {initial_guess*100:,.2f}%")
    print(f"Internal rate of return: {irr*100:,.2f}%")


def transform_df_to_relative_days(df_date, today=None):
    today = pd.Timestamp.today() if today is None else today
    days_ago = pd.Series(df_date.index).apply(lambda t : (today - t).days)
    df = df_date.set_index(days_ago)
    return df


def compounded_growth(nr_periods, rate, deposit=1, initial=0):
    """ rate:    growth rate per period
        deposit: amount deposited at the end of each period
        initial: inital deposit
        returns: the value after nr_periods of growth
    """
    if 0 == rate:
        return initial + nr_periods * deposit
    g = 1 + rate
    initial_grown  = initial * g**nr_periods
    deposits_grown = deposit * (g**nr_periods - 1)/(g -1)
    amount = initial_grown + deposits_grown
    return amount


def monthly_growth(months, annual_rate, deposit=1, initial=0):
    monthly_rate = (1 + annual_rate) ** (1/12) - 1
    return compounded_growth(months, monthly_rate, deposit, initial)


def pension_drawdown(months, rate, monthly_drawdown, pension_pot):
    """ Returns the balance left in the pension pot after drawing an income for the given nr of months """
    return monthly_growth(months, rate, -monthly_drawdown, pension_pot)


def mortgage_remaining(months, rate, monthly_repayment, notional):
    """ Returns the balance left to pay after the given nr of months """
    return monthly_growth(months, rate, monthly_repayment, -notional)


def months_remaining(rate, md, pot):
    months = 0
    r = pot
    r1 = pension_drawdown(1, rate, md, pot)
    if (r <= r1):
        return None  # The pot never runs out
    while(0 < pension_drawdown(months, rate, md, pot)):
        months += 1
    return months
