#!/usr/bin/env python
'''TODO add file comment!
'''

from datetime import datetime
import csv
import logging
import StringIO

def _strip_bom(fname):
    '''Return file object with Byte Order Mark (BOM) stripped off.

    Note: if the file does not exist the exception will need to be handled by
        the calling code.
    '''
    logging.debug('Stripping the BOM (if present) off %s...', fname)
    with open(fname, 'r') as raw:
        pre_strip = raw.read()

    # decode; if utf-8 this will strip off BOM, else nothing changes
    post_strip = pre_strip.decode('utf-8-sig')
    return StringIO.StringIO(post_strip)

def _find_missing_csv_fields(dict_reader, field_list):
    '''Return list of all fields in field_list that dict_reader is missing'''
    missing_fields = list()
    for field in field_list:
        if field not in dict_reader.fieldnames:
            missing_fields.append(field)

    return missing_fields

def _get_csv_reader(fname, check_fields):
    '''Create the CSV reader object and check it for the passed in fields'''
    csv_reader = csv.DictReader(_strip_bom(fname))
    missing_fields = _find_missing_csv_fields(csv_reader, check_fields)
    if missing_fields:
        raise Exception('%s is missing these column(s): %s' % (fname, (', '.join(missing_fields))))
    return csv_reader

def build_key_val_dict(fname, dict_key, dict_val, date_fmt):
    '''Creates a dictionary from a CSV file fname from two columns in the file

    {dict_key: dict_val}

    Exceptions are raised under these circumstances (calling code should handle 
    accordingly):
        * The file doesn't exist (via _get_csv_reader())
        * The CSV does not contain the header fields in 'dict_key' and/or 
          'dict_val' (via _get_csv_reader)
        * A date is not formatted correctly
        * The date appears more than once in the CSV file

    Note: that since we are sensitive to the csv columns, we cannot just read in
    the file straight with the csv.DictReader since it doesn't support stripping
    off the BOM. We have to first read the characters in (which will strip off
    the BOM) and then pass it to the DictReader via a StringIO. I'm open to
    better suggestions.
    '''
    csv_reader = _get_csv_reader(fname, [dict_key, dict_val])

    my_dict = dict()
    for item in csv_reader:
        try:
            date_key = datetime.strptime(item[dict_key], date_fmt).date()
        except ValueError:
            raise ValueError('Incorrect date format in %s. \'%s\' doesn\'t match %s' % (fname, item[date_key], date_fmt))

        # Make sure this date key hasn't been added before. If it has log the
        # warning but still update the existing key with the new value
        if date_key in my_dict.keys():
            raise Exception('This date has appeared more than once: %s. Please ensure that %s has unique dates and try again', date_key.strftime(date_fmt), fname)

        my_dict[date_key] = float(item[dict_val])

    return my_dict

def build_key_multi_val_dict(fname, dict_key, val_list, date_fmt):
    '''Creates a dictionary to a dictionary from a CSV file and it's values.

    {dict_key: {val1: val, val2: val,...}}
    '''
    # create a copy of the val_list so we can add the key to it for the filed checker
    check_vals = list(val_list)
    check_vals.append(dict_key)
    csv_reader = _get_csv_reader(fname, check_vals)

    my_dict = dict()
    for item in csv_reader:
        try:
            date_key = datetime.strptime(item[dict_key], date_fmt).date()
        except ValueError:
            raise ValueError('Incorrect date format in %s. \'%s\' doesn\'t match %s' % (fname, item[date_key], date_fmt))

        # Make sure this date key hasn't been added before. If it has log the
        # warning but still update the existing key with the new value
        if date_key in my_dict.keys():
            raise Exception('This date has appeared more than once: %s. Please ensure that %s has unique dates and try again', date_key.strftime(date_fmt), fname)

        # build inner dict
        inner_dict = dict()
        for inner_key in val_list:
            inner_dict[inner_key] = item[inner_key]

        my_dict[date_key] = inner_dict

    return my_dict
