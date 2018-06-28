import re

def as_valid_filename(filename):
    return re.sub('[^\w_.)( -]', '', filename)
