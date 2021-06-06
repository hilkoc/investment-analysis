# Investment Analysis

A python module for computing the internal rate of return of an arbitrary set of cashflows.

In addition some other functions are provided to compute metrics related to the compounded return of a regular investment.


## Requirements

python with `numpy`, `scipy`, `pandas`.

## How to use

The `investment_analysis.py` module can be imported in an existing project.

Alternatively, use the provided command line interface in `main.py`.
Run:

`python main.py --help`

to print the available subcommands. Run:

`python main.py subcommand --help`

to see the required parameters and help for each subcommand.


## Examples

### Internal rate of return

Suppose you make irregular investments that make a varying return, say the stock market. What would be the constant interest rate that would have brought your investments to same value today? That is the internal rate of return. To calculate it, enter all the deposits into a csv file, in the format shown in `sample.csv`. Check the current value of your investments, say it is 5,000,  and then run:

`python main.py irr --csv_file sample.csv 5000`

This prints a summary of your investment performance, including the internal rate of return.


### Performance of a regular investment

Suppose you make regular investments in an account with a fixed rate of return, such as a savings account. Say you have a starting balance of 2,000, for the next 10 years or 120 months, deposit 1,000 each month and the account makes an annual return of 5%. To see what the value is after 10 years, run:

`python main.py compound  120 1000 0.05 --initial 2000`


If instead of in a savings account, you invest in a the stock market with an unknown return, you can first use the `irr` calculation to find the past performance of your investments. If the internal rate of return was 5%, this `compound` command will project the future value of your investments, assuming the internal rate of return stays the same.


### Pension

 Are you saving enough for retirement? Suppose the regular investments are in a pension fund. After first computing the `irr` on past investments, then projecting that forward using the `compound` command, you can find an estimate of what your pension fund will be worth at retirement age. How long can you draw income from that pension fund?

 Let's say the projected value of the pension fund is 250,000 and the fund can continue to make a fixed return of 2% per year. You plan to withdraw an income of 1,000 per month. Run:

 `python main.py pension 1000 0.02 250000`

 to find out for how many months you can continue to draw income.

To compute how much is left in the pension fund after 10 years, use the `compound` command with a negative deposit:

`python main.py compound  120 -1000 0.02 --initial 250000`


### Mortgage

The same calculations can be used to find out how long it takes to repay a debt. Suppose the outstanding balance on a mortgage is 150,000,  the mortgage rate is 2%. The number of months it takes to repay the morgage, while making monthly repayments of 1,000 can be found with:

`python main.py mortgage 1000 0.02 150000`

To compute what the mortgage balance is after 10 years, use the `compound` command with a negative initial amount:

`python main.py compound  120 1000 0.02 --initial -250000`




