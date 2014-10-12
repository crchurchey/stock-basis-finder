#!/usr/bin/env python

import argparse
import csv
from datetime import datetime
import logging
import StringIO
import sys

LOG_LEVEL = logging.DEBUG
LOG_FMT = '%(levelname)s: %(message)s'

PHIST_DATE_KEY = 'Date'
PHIST_PRICE_VAL = 'Close'
PHIST_DATE_FMT = '%d-%b-%y'

DHIST_DATE_KEY = 'PayDate'
DHIST_AMT_VAL = 'Amt'
DHIST_DATE_FMT = '%d-%m-%Y'

def strip_bom(fname):
    """Return file object with Byte Order Mark (BOM) stripped off."""
    try:
        logging.debug("Stripping the BOM (if present) off %s...", fname)
        with open(fname, 'r') as raw:
            pre_strip = raw.read()
    except IOError as e:
        logging.error(e)
        sys.exit(1)

    # decode; if utf-8 this will strip off BOM, else nothing changes
    post_strip = pre_strip.decode('utf-8-sig')
    return StringIO.StringIO(post_strip)

def find_missing_fields(dict_reader, field_list):
    """Return list of all fields in field_list that dict_reader is missing"""
    missing_fields = list()
    for field in field_list:
        if field not in dict_reader.fieldnames:
            missing_fields.append(field)

    return missing_fields

def build_dict(reader, dict_key, dict_val, date_fmt, fname):
    """Creates the dictionary from the data; {date: value}"""
    my_dict = dict()
    for item in reader:
        try:
            date_key = datetime.strptime(item[dict_key], date_fmt).date()
        except ValueError as e:
            logging.error(e)
            logging.error('Please check the date formats in %s and try again', fname)
            sys.exit(1)

        # Make sure this date key hasn't been added before
        if date_key in my_dict.keys():
            logging.error("This date has appeared more than once: %s", date_key.strftime(date_fmt))
            logging.error("Please ensure that %s has unique dates and try again", fname)
            sys.exit(1)
        my_dict[date_key] =  float(item[dict_val])

    return my_dict

def process_price_csv(fname):
    """Process price the history CSV and return the price history data structure.

    Ensure the price history file is a CSV file and has the necessary columns.
    Then build a list of dictionaries of dates to closing prices for each line
    and return it.

    Note: that since we are sensitive to the csv columns, we cannot just read in
    the file straight with the csv.DictReader since it doesn't support stripping
    off the BOM. We have to first read the characters in (which will strip off
    the BOM) and then pass it to the DictReader via a StringIO. I'm open to
    better suggestions.
    """
    csv_reader = csv.DictReader(strip_bom(fname))

    missing_fields = find_missing_fields(csv_reader, [PHIST_DATE_KEY, PHIST_PRICE_VAL])
    if missing_fields:
        logging.error("The historical prices CSV is missing these column(s): %s", (", ".join(missing_fields)))
        logging.error("Please ensure that the CSV contains these fields and try again")
        sys.exit(1)

    # Build the historical price dictionary
    logging.debug('Building the price history dictionary...')
    return build_dict(csv_reader, PHIST_DATE_KEY, PHIST_PRICE_VAL, PHIST_DATE_FMT, fname)

def process_div_csv(fname):
    """Process the dividend history CSV and return the dividend history data structure

    Same as process_price_csv() but looking for dividend specific columns and a
    different date format.
    """
    csv_reader = csv.DictReader(strip_bom(fname))

    missing_fields = find_missing_fields(csv_reader, [DHIST_DATE_KEY, DHIST_AMT_VAL])
    if missing_fields:
        logging.error("The dividend history CSV is missing these column(s): %s", (", ".join(missing_fields)))
        logging.error("Please ensure that the CSV contains these fields and try again")
        sys.exit(1)

    logging.debug('Building the dividend history dictionary...')
    return build_dict(csv_reader, DHIST_DATE_KEY, DHIST_AMT_VAL, DHIST_DATE_FMT, fname)

if __name__ == "__main__":

    # Set the logging level
    logging.basicConfig(format=LOG_FMT, level=LOG_LEVEL)

    # Create the parser and then parse the args
    parser = argparse.ArgumentParser(description='Find cost-basis for an investment')
    parser.add_argument('-ph', '--price-history', metavar='<FILE>', type=str, default='history.csv', help='CSV file that contains the daily price history for the investment')
    parser.add_argument('-d', '--dividends', metavar='<FILE>', type=str, default='dividends.csv', help='CSV file that contains the dividend history for the investment')

    #TODO add argument for split

    args = parser.parse_args()

    # Extract args
    hist_csv = args.price_history
    div_csv = args.dividends
    logging.debug('History File: %s', hist_csv)
    logging.debug('Dividend File: %s', div_csv)

    price_dict = process_price_csv(hist_csv)
    div_dict = process_div_csv(div_csv)

    logging.debug('len(price_dict) = %d', len(price_dict))
    logging.debug('len(div_dict) = %d', len(div_dict))
