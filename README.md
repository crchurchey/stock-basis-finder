Stock Basis Finder
==================

You may own or have inherited an investment that for some reason you don't have the original investment certificate for and hence don't know the cost-basis with dividends and stock splits factored in. This is a problem if you want to sell the investment since the IRS (US) will levy taxes on any gains the investment made. This tool can help you find the cost-basis of your investment.

## Assumptions
I know it seems like a lot of assumptions but hopefully with time I can remove a lot of these by adding new features.
* All investment purchases had no fees*
* The investment is set up in a [DRiP](http://en.wikipedia.org/wiki/Dividend_reinvestment_plan) (All dividends automatically reinvested)
* Cash type dividends were the only dividends paid out during your ownership of the investment
* All purchases were done at the closing price*
* No other lots (aside from the initial investment and reinvested dividends) were bought*
* The investment did not contain any capital gains distributions*
 * This is mainly important for mutual/index funds

\* Future features may be added to remove this assumption...stay tuned

## What is needed?
We can "reverse engineer" the cost-basis given the following information about the investment:
* Current number of shares owned
* Investment price history
* Dividend history
* Split history

You will need to provide this info in order to find your investment's cost-basis. You should already know the number of shares you own and you can find everything else on the intertubes!

##### Historical Prices
I recommend [Google Finance](http://finance.google.com/) for the historical prices:
* Goto http://finance.google.com
* Enter your investment ticker symbol in the search box and hit enter
* In the left-side-bar click 'Historical prices'
* Enter an appropriate start date (i.e one that you are confident is prior to the original purchase date of the investment)
* Leave the end date as the current date
* Click 'Update'
* On the right-side of the page click 'Download to Spreadsheet' and save the CSV file to your hard drive (ex. history.csv)

If you want to get the historical info from somewhere else, that is OK but make sure the CSV file includes a header line and is in this format:
```
Date,Close
dD-MMM-YY,##.##
```
Example file:
```
Date,Close
1-Oct-14,12.34
08-Feb-01,12.30
10-Jan-98,12.00
```
Note that any number or arrangement of the columns in the CSV are acceptable but the CSV must have at least a 'Date' and 'Close' column.

##### Dividend History
Dividend histories are going to be a little more difficult. [Yahoo Finance](http://finance.yahoo.com) has a way to get the the dividend history but unfortunately it does not give you the payable date; it only gives the ex-date (See [this](http://www.investopedia.com/articles/02/110802.asp) article for more info on how dividends work). We need the payable date since that is the date that most DRiP's purchase the new lots with the dividend cash. You may have to go to the companies investment web page to find the detailed dividend info. Once you find this information you need to create a CSV file in the following format:
```
PayDate,Amt
MM-DD-YYYY,#.##
```
Example file:
```
PayDate,Amt
03-01-1985,0.50
```

##### Split History
A good site I've found that can get you the split history is [Get Split History](http://getsplithistory.com):
* Goto http://getsplithistory.com
* Enter your investment ticker symbol in the search box and hit enter
* Select your investment ticker if necessary
* Using the split info on the page, create a CSV file of the form with a new row for each split:
```
split-date,new-shares,original-shares
MM-DD-YYYY,#,#
```
* For example, a 2:1 split on Oct. 1st, 1999 would look like this:
```
split-date,new-shares,original-shares
10-01-1999,2,1
```

## How does it work?
With the data that you provide above, we can work backwards from today and figure out lot purchase prices and number of shares bought. In order to find the basis, we need to figure out the cost of each lot bought (all shares of an investment bought in a single transaction at the same share price are considered a lot). Here is the formula:

<!--
Built this formula here: http://latex.codecogs.com/eqneditor/editor.php

OrigShares \times Dividend = Cash = NewShares \times PayDatePrice
-->

![equation](http://latex.codecogs.com/gif.latex?OrigShares%20%5Ctimes%20Dividend%20%3D%20Cash%20%3D%20NewShares%20%5Ctimes%20PayDatePrice)

So...

<!--
OrigShares \times Dividend = NewShares \times PayDatePrice
-->

![equation](http://latex.codecogs.com/gif.latex?OrigShares%20%5Ctimes%20Dividend%20%3D%20NewShares%20%5Ctimes%20PayDatePrice)

We know the `Dividend` and we know the `PayDatePrice` but we don't know the `NewShares` and we are after the `OrigShares`. We do know this though:

<!--
NewShares = CurrentShares - OrigShares
-->

![equation](http://latex.codecogs.com/gif.latex?NewShares%20%3D%20CurrentShares%20-%20OrigShares)

Now we can replace `NewShares` in the previous equation:

<!--
OrigShares \times Dividend = (CurrentShares - OrigShares) \times PayDatePrice
-->

![equation](http://latex.codecogs.com/gif.latex?OrigShares%20%5Ctimes%20Dividend%20%3D%20%28CurrentShares%20-%20OrigShares%29%20%5Ctimes%20PayDatePrice)

Now the only variable we don't know is `OrigShares` so solve for it. If we trust [WolframAlpha](http://www.wolframalpha.com/input/?i=solve+X*Y+%3D+%28Z-X%29*A+for+X) we get:

<!--
OrigShares = \frac{PayDatePrice \times CurShares}{PayDatePrice + Dividend}
-->

![equation](http://latex.codecogs.com/gif.latex?OrigShares%20%3D%20%5Cfrac%7BPayDatePrice%20%5Ctimes%20CurShares%7D%7BPayDatePrice%20+%20Dividend%7D)

Now that we have an equation to work with we just need to work backwards through each dividend until `OrigShares` converges to 0 or we reach a date that we know is too far back.
