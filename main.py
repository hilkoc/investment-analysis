""" Command line interface for investment_analysis.py"""
import investment_analysis as ia
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd



def analyze_investemnt_returns(current_value, csv_file):
    df_date = pd.read_csv(csv_file, index_col="Date", parse_dates=True)
    df = ia.transform_df_to_relative_days(df_date)
    irr, cash_pnl, initial_guess, total_invested = ia.analyze_pnl(current_value, df)
    ia.report_pnl(irr, cash_pnl, initial_guess, current_value, total_invested)


def irr(args):
    csv_file = args.csv_file
    if csv_file is None:
        print("No csv file given. Using sample.csv. Specify a csv file to use with --csv_file filename.csv")
        csv_file = "sample.csv"
    analyze_investemnt_returns(args.current_value, csv_file)


def compound(args):
    """ For an investment or a savings account, use a positive initial balance and positive deposit 
        For a pension fund, use a positive initial balance and negative deposit. The deposit is the monthly pension income.
        For a debt, such as a mortgage, use a negative inital balance and positive deposit. The deposit is the montly mortgage payment
    """
    months, rate, deposit, initial = args.months, args.rate, args.deposit, args.initial
    print(f"An investment starting at {initial:,.2f}, with {months} monthly deposits of {deposit:,.2f} having an annual return of {rate*100:,.2f}%, grows to:")
    result = ia.monthly_growth(months, rate, deposit, initial)
    print(f"{result:,.2f}")


def print_months_remaining(rate, deposit, initial):
    months = ia.months_remaining(rate, deposit, initial)
    if months is None:
        print("Never.")
    else:
        years = months // 12
        print(f"{years:,d} years and {months - 12*years:d} months")


def pension(args):
    rate, deposit, initial = args.rate, args.deposit, args.initial
    print(f"A pension fund of {initial:,.0f}, invested at an annual return of {rate*100:,.2f}%, drawing a monthly income of {deposit:,.2f}, runs out after:")
    print_months_remaining(rate, deposit, initial)
    
    
def mortgage(args):
    rate, deposit, initial = args.rate, args.deposit, args.initial
    print(f"A mortgage of {initial:,.0f}, with an annual interest rate of {rate*100:,.2f}%, and monthly repayments of {deposit:,.2f} is repayed after:")
    print_months_remaining(rate, deposit, initial)


def main():
    extra_help = """ run: '%(prog)s subcommand --help'   for more help on each subcommand.\n
    Examples:
    %(prog)s      irr 5000
    %(prog)s compound  120 1000   0.05 --initial 2000
    %(prog)s pension  1000 0.02 250000
    %(prog)s mortgage 1000 0.02 150000
    """
    parser = argparse.ArgumentParser(prog=None, usage="%(prog)s subcommand [parameters]", epilog=extra_help, formatter_class=argparse.RawTextHelpFormatter)
    show_help  = lambda args: parser.print_help()
    parser.set_defaults(func=show_help)
    subparsers = parser.add_subparsers(help="available subcommands:\n")
    irr_parser = subparsers.add_parser("irr", help="Find the internal rate of return of a list of cashflows")
    irr_parser.add_argument("current_value", type=float, help="Total value of the invested amounts today")
    irr_parser.add_argument("--csv_file", help="Csv file containing columns 'Date' and 'Amount'. Defaults to sample.csv")
    irr_parser.set_defaults(func=irr)

    compound_parser = subparsers.add_parser('compound', help='Compute the compounded return of a regular investment')
    compound_parser.add_argument("months", type=int, help="The number of months the investment repeats")
    compound_parser.add_argument("deposit", type=float, help="The amount deposited at the end of each month")
    compound_parser.add_argument("rate", type=float, help="The annual rate of return on the investment")
    compound_parser.add_argument("--initial", type=float, default=0, help="The starting balance, defaults to 0")
    compound_parser.set_defaults(func=compound)

    pension_parser = subparsers.add_parser('pension', help='Compute the nr of months income can be drawn from an investment')
    pension_parser.add_argument("deposit", type=float, help="The amount of income drawn at the end of each month")
    pension_parser.add_argument("rate", type=float, help="The annual rate of return on the investment")
    pension_parser.add_argument("initial", type=float, help="The starting balance, defaults to 0")
    pension_parser.set_defaults(func=pension)

    mortgage_parser = subparsers.add_parser('mortgage', help='Compute the nr of months it takes to repay a debt')
    mortgage_parser.add_argument("deposit", type=float, help="The amount repayed at the end of each month")
    mortgage_parser.add_argument("rate", type=float, help="The annual rate of return on the investment")
    mortgage_parser.add_argument("initial", type=float, help="The starting balance, defaults to 0")
    mortgage_parser.set_defaults(func=mortgage)

    args = parser.parse_args()
    args.func(args)


def example():
    today = pd.Timestamp.today() 
    current_value = 10800
    days_ago = [7, 365, 730]
    amounts = [4000, 3000, 2000]
    df = pd.DataFrame({"Amount": amounts}, index=days_ago)
    df.index.name = "Days ago"
    irr, cash_pnl, initial_guess, total_invested = ia.analyze_pnl(current_value, df)
    ia.report_pnl(irr, cash_pnl, initial_guess, current_value, total_invested)


if __name__ == "__main__":
    main()