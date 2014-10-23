#!/usr/bin/env python
'''TODO add file comment
'''

import argparse
import datetime
import logging
import sys
import traceback

import csv2dict

DEFAULT_LOG_LEVEL = logging.INFO
LOG_FMT = '%(levelname)s: %(message)s'

# Constants for Price History CSV
PHIST_DEFAULT = 'prices.csv'
PHIST_DATE_KEY = 'Date'
PHIST_PRICE_VAL = 'Close'
PHIST_DATE_FMT = '%Y-%m-%d'

# Constants for Dividend History CSV
DHIST_DEFAULT = 'dividends.csv'
DHIST_DATE_KEY = 'PayDate'
DHIST_AMT_VAL = 'Amt'
DHIST_DATE_FMT = '%m-%d-%Y'

# Constants for Split history CSV
SHIST_DEFAULT = 'splits.csv'
SHIST_DATE_KEY = 'split-date'
SHIST_NEW_SHARES = 'new-shares'
SHIST_OLD_SHARES = 'original-shares'
SHIST_DATE_FMT = '%m-%d-%Y'

DIV_KEY = 'dividend-data'
SPLIT_KEY = 'split-data'

if __name__ == "__main__":

    # Create the parser and then parse the args
    parser = argparse.ArgumentParser(description='Find cost-basis for an investment')
    parser.add_argument('-pf', '--price-file', metavar='<FILE>', type=str, default=PHIST_DEFAULT, help='CSV file that contains the daily price history for the investment (default=%s)' % PHIST_DEFAULT)
    parser.add_argument('-df', '--dividend-file', metavar='<FILE>', type=str, default=DHIST_DEFAULT, help='CSV file that contains the dividend history for the investment (default=%s)' % DHIST_DEFAULT)
    parser.add_argument('-sf', '--split-file', metavar='<FILE>', type=str, default=SHIST_DEFAULT, help='CSV file that contains the split history for the investment (default=%s)' % SHIST_DEFAULT)
    parser.add_argument('--debug', action='store_true', default=False, help='Turn debug statements on or off')
    parser.add_argument('-cs', '--cur-shares', metavar='<#######.##>', type=float, required=True, help='Number of shares of the investment currently owned')

    args = parser.parse_args()

    # Extract args
    hist_csv = args.price_file
    div_csv = args.dividend_file
    split_csv = args.split_file
    cur_shares = args.cur_shares

    # Set the logging level
    if args.debug:
        logging.basicConfig(format=LOG_FMT, level=logging.DEBUG)
    else:
        logging.basicConfig(format=LOG_FMT, level=DEFAULT_LOG_LEVEL)

    logging.debug('History File: %s', hist_csv)
    logging.debug('Dividend File: %s', div_csv)
    logging.debug('Split File: %s', split_csv)
    logging.debug('Current Shares: %d', cur_shares)

    try:
        logging.info('Building price history dictionary from %s...', hist_csv)
        price_dict = csv2dict.build_key_val_dict(hist_csv, PHIST_DATE_KEY, PHIST_PRICE_VAL, PHIST_DATE_FMT)
        logging.info('Building dividend history dictionary from %s...', div_csv)
        div_dict = csv2dict.build_key_val_dict(div_csv, DHIST_DATE_KEY, DHIST_AMT_VAL, DHIST_DATE_FMT)
        logging.info('Building split history dictionary from %s...', split_csv)
        split_dict = csv2dict.build_key_multi_val_dict(split_csv, SHIST_DATE_KEY, [SHIST_NEW_SHARES, SHIST_OLD_SHARES], SHIST_DATE_FMT)

    except Exception as e:
        logging.debug(traceback.format_exc())
        logging.error(e)
        sys.exit(1)

    logging.debug('len(price_dict) = %d', len(price_dict))
    logging.debug('len(div_dict) = %d', len(div_dict))
    logging.debug('len(split_dict) = %d', len(split_dict))

    # Create new dictionary that contains both dividends and splits
    div_splits_dict = dict()
    for date_key in div_dict.keys():
        tmp_dict = {DIV_KEY: div_dict[date_key]}
        div_splits_dict[date_key] = tmp_dict
    for date_key in split_dict.keys():
        if div_splits_dict.has_key(date_key):
            div_splits_dict[date_key][SPLIT_KEY] = split_dict[date_key]
        else:
            tmp_dict = {SPLIT_KEY: split_dict[date_key]}
            div_splits_dict[date_key] = tmp_dict

    # loop over the dividends and splits
    sorted_date_keys = div_splits_dict.keys()
    sorted_date_keys.sort(reverse=True)
    calc_shares = cur_shares
    for date_key in sorted_date_keys:
        # Sometimes dividend pay dates may fall on weekends or holidays so search
        # for the next price history if possible (within reason)
        done = False
        day_displacement = 0
        while not done and day_displacement < 10:
            tmp_key = date_key + datetime.timedelta(days=day_displacement)
            try:
                price = price_dict[tmp_key]
                done = True
            except KeyError:
                # Add one to the day displacement and try again
                day_displacement+=1
        if day_displacement == 10:
            raise Exception('Couldn\'t find the next valid price history date after %s', date_key)

        # First check for dividends and process them first
        if div_splits_dict[date_key].has_key(DIV_KEY):
            div_amt = div_splits_dict[date_key][DIV_KEY]
            cur_shares = (price * cur_shares) / (price + div_amt)

        # Now see if there are splits to process
        if div_splits_dict[date_key].has_key(SPLIT_KEY):
            orig_shares = float(div_splits_dict[date_key][SPLIT_KEY][SHIST_OLD_SHARES])
            new_shares = float(div_splits_dict[date_key][SPLIT_KEY][SHIST_NEW_SHARES])
            cur_shares *= orig_shares / new_shares

        print cur_shares
