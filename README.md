Stock Basis Finder
==================

You may own or have inherited an investment that for some reason you don't have the original investment certificate for and hence don't know the cost-basis with dividends and stock splits factored in. This is a problem if you want to sell the investment since the IRS (US) will levy taxes on any gains the investment made. This tool can help you find the cost-basis of your investment.

See the [Stock Basis Finder Wiki](https://github.com/crchurchey/stock-basis-finder/wiki) for more in-depth info on this application.

## What is needed?
We can "reverse engineer" the cost-basis given the following information about the investment:
* Current number of shares owned
* Investment price history (Need daily **High** & **Low** prices)
* Dividend history (Need Dividend **Payment Date**)
* Reinvestment offset (DRiP's vary in how close to the payment date they invest the dividend)
* Split history

You will need to provide this info in order to find your investment's cost-basis. You should already know the number of shares you own and you can find everything else on the intertubes!

##### Historical Prices
I recommend [Yahoo Finance](http://finance.yahoo.com/) for the historical prices (Google will only export 4000 records at a time which makes things more complicated if you need more records than that):
* Goto http://finance.yahoo.com
* Enter your investment ticker symbol in the search box and hit enter
* In the left-side-bar click **'Historical prices'**
* Enter an appropriate start date (i.e one that you are confident is prior to the original purchase date of the investment)
* Leave the end date as the current date
* Make sure the **'Daily'** radio button is selected
* Click **'Get Prices'**
* At the bottom of the page click **'Download to Spreadsheet'** and save the CSV file to your hard drive (ex. prices.csv)

If you want to get the historical info from somewhere else, that is OK but make sure the CSV file includes a header line and is in this format:
```
Date,High,Low
YYYY-MM-DD,##.##,##.##
```
Example file:
```
Date,High,Low
2014-10-01,12.34,12.12
2001-02-08,12.30,12.28
1998-01-10,12.00,11.99
```
Note that any number or arrangement of the columns in the CSV are acceptable but the CSV must have at least a **'Date'**, **'High'**, and **'Low'** column.

##### Dividend History
Dividend histories are going to be a little more difficult. [Yahoo Finance](http://finance.yahoo.com) has a way to get the the dividend history but unfortunately it does not give you the payable date; it only gives the ex-date (See [this](http://www.investopedia.com/articles/02/110802.asp) article for more info on how dividends work). We need the payable date since that date plus the DRiP offset tells when the new lots are purchased with the dividend cash. You may have to go to the company's investment web page to find the detailed dividend info. Once you find this information you need, create a CSV file in the following format:
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
* For example, a **2:1** split on **Oct. 1st, 1999** would look like this:
```
split-date,new-shares,original-shares
10-01-1999,2,1
```

## Disclaimer
The author of this application is not and does not claim to be any of the following:
* Tax Advisor/Expert
* Fiduciary
* Financial Advisor of any sort (Fiduciary, CFP, etc.)
* Investment Advisor/Expert
* Attorney/Lawyer of any sort

This software can aid in finding the approximate purchase date as well as the cost-basis of investments. You may use the info this application outputs in any way you see fit but the author is not liable for any legal issues that may arise from using the data the application outputs.
