#!/usr/bin/env python
"""TODO add file comment
"""

import argparse
import csv
import logging
import sys
import traceback

import csv2dict

LOG_LEVEL = logging.DEBUG
LOG_FMT = '%(levelname)s: %(message)s'

# Constants for Price History CSV
PHIST_DEFAULT = 'prices.csv'
PHIST_DATE_KEY = 'Date'
PHIST_PRICE_VAL = 'Close'
PHIST_DATE_FMT = '%d-%b-%y'

# Constants for Dividend History CSV
DHIST_DEFAULT = 'dividends.csv'
DHIST_DATE_KEY = 'PayDate'
DHIST_AMT_VAL = 'Amt'
DHIST_DATE_FMT = '%d-%m-%Y'


def process_price_csv(fname):
    """Process the price history CSV and return the price history data structure.

    Ensure the price history file is a CSV file and has the necessary columns.
    Then build a list of dictionaries of dates to closing prices for each line
    and return it.

    Note: that since we are sensitive to the csv columns, we cannot just read in
    the file straight with the csv.DictReader since it doesn't support stripping
    off the BOM. We have to first read the characters in (which will strip off
    the BOM) and then pass it to the DictReader via a StringIO. I'm open to
    better suggestions.
    """
    #TODO move most of this logic into csv2dict.build_dict()
    csv_reader = csv.DictReader(csv2dict.strip_bom(fname))

    missing_fields = csv2dict.find_missing_csv_fields(csv_reader, [PHIST_DATE_KEY, PHIST_PRICE_VAL])
    if missing_fields:
        logging.error("The historical prices CSV is missing these column(s): %s", (", ".join(missing_fields)))
        logging.error("Please ensure that the CSV contains these fields and try again")
        sys.exit(1)

    # Build the historical price dictionary
    logging.debug('Building the price history dictionary...')
    return csv2dict.build_dict(csv_reader, PHIST_DATE_KEY, PHIST_PRICE_VAL, PHIST_DATE_FMT, fname)

def process_div_csv(fname):
    """Process the dividend history CSV and return the dividend history data structure

    Same as process_price_csv() but looking for dividend specific columns and a
    different date format.
    """
    csv_reader = csv.DictReader(csv2dict.strip_bom(fname))

    missing_fields = csv2dict.find_missing_csv_fields(csv_reader, [DHIST_DATE_KEY, DHIST_AMT_VAL])
    if missing_fields:
        logging.error("The dividend history CSV is missing these column(s): %s", (", ".join(missing_fields)))
        logging.error("Please ensure that the CSV contains these fields and try again")
        sys.exit(1)

    logging.debug('Building the dividend history dictionary...')
    return csv2dict.build_dict(csv_reader, DHIST_DATE_KEY, DHIST_AMT_VAL, DHIST_DATE_FMT, fname)

if __name__ == "__main__":

    # Set the logging level
    logging.basicConfig(format=LOG_FMT, level=LOG_LEVEL)

    # Create the parser and then parse the args
    parser = argparse.ArgumentParser(description='Find cost-basis for an investment')
    parser.add_argument('-ph', '--price-history', metavar='<FILE>', type=str, default=PHIST_DEFAULT, help='CSV file that contains the daily price history for the investment (default=%s)' % PHIST_DEFAULT)
    parser.add_argument('-d', '--dividends', metavar='<FILE>', type=str, default=DHIST_DEFAULT, help='CSV file that contains the dividend history for the investment (default=%s)' % DHIST_DEFAULT)

    #TODO add argument for split

    args = parser.parse_args()

    try:
        # Extract args
        hist_csv = args.price_history
        div_csv = args.dividends
        logging.debug('History File: %s', hist_csv)
        logging.debug('Dividend File: %s', div_csv)

        price_dict = process_price_csv(hist_csv)
        div_dict = process_div_csv(div_csv)

        logging.debug('len(price_dict) = %d', len(price_dict))
        logging.debug('len(div_dict) = %d', len(div_dict))
    except Exception as e:
        logging.debug(traceback.format_exc())
        logging.error(e)
        sys.exit(1)
