#!/usr/bin/env python
"""TODO add file comment!
"""

from datetime import datetime
import logging
import StringIO

def strip_bom(fname):
    """Return file object with Byte Order Mark (BOM) stripped off.

    Note: if the file does not exist the exception will need to be handled by
        the calling code.
    """
    logging.debug("Stripping the BOM (if present) off %s...", fname)
    with open(fname, 'r') as raw:
        pre_strip = raw.read()

    # decode; if utf-8 this will strip off BOM, else nothing changes
    post_strip = pre_strip.decode('utf-8-sig')
    return StringIO.StringIO(post_strip)

def find_missing_csv_fields(dict_reader, field_list):
    """Return list of all fields in field_list that dict_reader is missing"""
    missing_fields = list()
    for field in field_list:
        if field not in dict_reader.fieldnames:
            missing_fields.append(field)

    return missing_fields

def build_dict(reader, dict_key, dict_val, date_fmt, fname):
    """Creates the dictionary from the data; {date: value}

    Note: Raise an informative exception if there is an incorrectly formatted
        date. It is up to the calling code to handle it.
    """
    my_dict = dict()
    for item in reader:
        try:
            date_key = datetime.strptime(item[dict_key], date_fmt).date()
        except ValueError:
            # Add better message
            raise ValueError('Incorrect date format in %s. \'%s\' doesn\'t match %s' % (fname, item[dict_key], date_fmt))

        # Make sure this date key hasn't been added before. If it has log the
        # warning but still update the existing key with the new value
        if date_key in my_dict.keys():
            logging.warning("This date has appeared more than once: %s. Please ensure that %s has unique dates and try again", date_key.strftime(date_fmt), fname)

        my_dict[date_key] =  float(item[dict_val])

    return my_dict
