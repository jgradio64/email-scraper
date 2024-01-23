from email.header import decode_header
import datetime
import email
import imaplib
import json
import os

# move to helper file
def build_date(days_ago):
    """
    Purpose: Builds a date string for the mail search function
    Input: An integer that indicates how far back you want to check
    Output: A string in the format 'day-month-year', uses textual shorthand for month.
    Output example: "01-Jan-1990"
    """
    today = datetime.datetime.now()
    target_date = today - datetime.timedelta(days=days_ago)
    day = target_date.day
    month = target_date.strftime('%b')
    year = target_date.year
    date_string = str(day) + "-" + month + "-" + str(year)
    return date_string


# Decodes a string if it is in utf-8
def helper_decode(encoded_array):
    result = encoded_array
    # Decode any byte strings.
    for x in range(len(result)):
        if isinstance(result[x], bytes):
            result[x] = result[x].decode('utf-8')
        elif isinstance(x, str):
            pass
    return result


# Flattens a list of tuples to just be a list
def flatten(array):
    return [e for l in array for e in l]


# Removes an instance of the string "utf-8" 
# quite weird I know, but this just works
def helper_filter(array):
    result = array
    if "utf-8" in result:
        result.remove("utf-8")
    if None in result:
        result.remove(None)
    return result


# Gets just the email address from the header of an email.
def extract_email_address(sender_array):
    res = [i.find('@') for i in sender_array]
    for x in range(len(res)):
        if res[x] > 0:
            return sender_array[x]