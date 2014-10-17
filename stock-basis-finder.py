#!/usr/bin/env python
'''TODO add file comment
'''

import argparse
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

# Constants for Split history CSV
SHIST_DEFAULT = 'splits.csv'
SHIST_DATE_KEY = 'split-date'
SHIST_NEW_SHARES = 'new-shares'
SHIST_OLD_SHARES = 'original-shares'
SHIST_DATE_FMT = '%m-%d-%Y'

if __name__ == "__main__":

    # Set the logging level
    logging.basicConfig(format=LOG_FMT, level=LOG_LEVEL)

    # Create the parser and then parse the args
    parser = argparse.ArgumentParser(description='Find cost-basis for an investment')
    parser.add_argument('-ph', '--price-history', metavar='<FILE>', type=str, default=PHIST_DEFAULT, help='CSV file that contains the daily price history for the investment (default=%s)' % PHIST_DEFAULT)
    parser.add_argument('-d', '--dividends', metavar='<FILE>', type=str, default=DHIST_DEFAULT, help='CSV file that contains the dividend history for the investment (default=%s)' % DHIST_DEFAULT)
    parser.add_argument('-s', '--splits', metavar='<FILE>', type=str, default=SHIST_DEFAULT, help='CSV file that contains the split history for the investment (default=%s)' % SHIST_DEFAULT)

    #TODO add argument for split

    args = parser.parse_args()

    try:
        # Extract args
        hist_csv = args.price_history
        div_csv = args.dividends
        split_csv = args.splits
        logging.debug('History File: %s', hist_csv)
        logging.debug('Dividend File: %s', div_csv)
        logging.debug('Split File: %s', split_csv)

        price_dict = csv2dict.build_key_val_dict(hist_csv, PHIST_DATE_KEY, PHIST_PRICE_VAL, PHIST_DATE_FMT)
        div_dict = csv2dict.build_key_val_dict(div_csv, DHIST_DATE_KEY, DHIST_AMT_VAL, DHIST_DATE_FMT)
        split_dict = csv2dict.build_key_multi_val_dict(split_csv, SHIST_DATE_KEY, [SHIST_NEW_SHARES, SHIST_OLD_SHARES], SHIST_DATE_FMT)


        logging.debug('len(price_dict) = %d', len(price_dict))
        logging.debug('len(div_dict) = %d', len(div_dict))
        logging.debug('len(split_dict) = %d', len(split_dict))
    except Exception as e:
        logging.debug(traceback.format_exc())
        logging.error(e)
        sys.exit(1)
