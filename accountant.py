#!/usr/bin/env python
'''
Usage:
    ./accountant.py [--report=DATE] [--diff] [DATE1] [DATE2] [--date-format=DATE_FMT] [--debug] [--dest=DIR]
'''

import sys
import os
import jinja2
import pprint
from time import strftime
from time import strptime
from docopt import docopt

# Get Configuratino values
args = docopt (__doc__, version="Accountant v1.0")

debug = args ['--debug']

if args ['--debug']:
    print args

date_format = '%d/%m/%Y'

OUTCOME_POS = 1
DATE_POS = 2
AMOUNT_POS = 3
CAT_POS = 4
COMMENT_POS = 5


class EntryDrive (object):

    def __init__ (self, entry = []):
        self.outcome = (entry [OUTCOME_POS] == 'Outcome')
        self.date    = self.get_date (entry)
        self.date_str = strftime (date_format, self.date)
        self.amount  = self._parse_amount (entry [AMOUNT_POS])
        self.category = entry [CAT_POS].rstrip ()
        self.comment  = entry [COMMENT_POS].rstrip ()


    def _parse_amount (self, float_str):
        float_sanitized = float_str.replace ('"', '').replace ("'",'')
        return float (float_sanitized)

    def get_date (self, entry):
        try:
            if len (entry) >= 3:
                return strptime (entry [DATE_POS], date_format)
            else:
                return None
        except ValueError as err:
            print ('ValueError for entry {0} and date {1}'.format (entry, entry [DATE_POS]))
            print (err)
            return None

    def __repr__ (self):
        if self.outcome:
            amount = -self.amount
        else:
            amount = self.amount
        return '%s, %0.2f, %s - %s' % \
                (self.date_str, amount, self.category, self.comment)


def logd (msg):
    if debug:
        print (msg)


def get_date (entry):
        if len (entry) >= 3:
            return time.strptime (entry [DATE_POS], '%d/%m/%Y')
        else:
            return None

def select_entries (entry, month, year):
    date = get_date (entry)
    if date.tm_year == year and date.tm_mon == month:
        return entry

    return None

def add_entry_to_report (entry, report = {}):
    if '_categories' not in report.keys():
        report ['_categories'] = {}

    if entry.category not in report ['_categories'].keys():
        report ['_categories'] [entry.category] = 0

    if entry.outcome:
        report ['_outcomes'].append (entry)
    else:
        report ['_incomes'].append (entry)

    report ['_categories'] [entry.category] += entry.amount

    if entry.outcome:
        report ['_tot_outcomes'] += entry.amount
    else:
        report ['_tot_incomes'] += entry.amount

    return report


def diff (report1 = {}, report2 = {}):
    report_diff = {}
    categories = report1 ['_categories'].keys ()
    categories.extend (report2 ['_categories'].keys ())
    categories = set (categories)

    for cat in categories:
        if cat in report1 ['_categories'].keys () and cat in report2 ['_categories'].keys ():
           expense1 = abs (report1 ['_categories'] [cat])
           expense2 = abs (report2 ['_categories'] [cat])
           if expense1 > expense2:
               report_diff [cat] = '+%0.2f%s' % ((100.0 * (expense1 - expense2) / expense1), '%')
           elif expense1 < expense2:
               report_diff [cat] = '%0.2f%s' % ((100.0 * (expense1 - expense2) / expense2), '%')
           else:
               report_diff [cat] = '0.0%s' % ('%')

        elif cat in report1 ['_categories'].keys ():
            if report1 ['_categories'] [cat] > 0:
                report_diff [cat] = '+100.0%'
        else:
            if report2 ['_categories'] [cat] > 0:
                report_diff [cat] = '-100.0%'

    return report_diff


def report_print (report = {}, category = None):
    printer = pprint.PrettyPrinter (indent = 4)
    printer.pprint (report)


def report_render (report = {}, diff_mon = {}, diff_year = {}, categories = [], title = 'Report'):
    cwd = os.getcwd()
    templateLoader = jinja2.FileSystemLoader (searchpath = '/')
    templateEnv = jinja2.Environment (loader=templateLoader)
    template = templateEnv.get_template (os.path.join (cwd, 'report_template.html'))
    template = templateEnv.get_template (os.path.join (cwd, 'report_template.html'))
    templateVars = { 'title' : title, 'report' : report, 'diff_mon' : diff_mon, 'diff_year' : diff_year, 'categories' : categories}
    outputText = template.render (templateVars)
    return outputText

def make_report (year, month=None, entries = []):
    if 0 == len (entries):
        return {}

    biggest_expense_amount = 0.0
    report = {
            '_categories' : {},
            '_outcomes': [],
            '_incomes': [],
            '_tot_incomes':0.0,
            '_tot_outcomes':0.0,
            '_biggest_expense': None}

    for entry in entries:
        try:
            if year == entry.date.tm_year and (None == month or month == entry.date.tm_mon):
                if entry.outcome and entry.category != 'Rent' and abs (entry.amount) > biggest_expense_amount:
                    report ['_biggest_expense'] = entry
                    biggest_expense_amount = abs (entry.amount)

                report = add_entry_to_report (report = report, entry = entry)
        except AttributeError as er:
            print (entry)
            raise AttributeError

    return report;


def make_report_diff (entries, year1, year2, month1=None, month2=None):
    report1 = make_report (year1, month1, entries)
    report2 = make_report (year2, month2, entries)

    diff_report = diff (report1, report2)

    return diff_report


def parse_date (date):
    year  = None
    month = None

    if '-' in date:
        year, month = date.split ('-')
        month = int (month)
    else:
        year = date

    year = int (year)

    return year, month


def main (entries):
    entryObjs = []
    categories = set ()
    for entry in entries:
        if type (entry) is str:
            entry = entry.split (',')
        entryObj = EntryDrive (entry)
        categories.add (entryObj.category)
        entryObjs.append (entryObj)

    categories = list (categories)
    categories.sort ()

    if args ['--report'] is not None:
        print ('Report %s' % (args ['--report']))

        date = args ['--report']
        year, month = parse_date (date)

        report = make_report (year=year, month=month, entries=entryObjs)
        diff_mon = make_report_diff (entries=entryObjs, year1=year, year2=year, month1=month, month2=month-1)
        diff_year = make_report_diff (entries=entryObjs, year1=year, year2=year-1, month1=month, month2=month)

        html = report_render (report, diff_mon, diff_year, categories, 'Report %s' % date)

        if args ['--dest']:
            output_filepath = os.path.join (args ['--dest'], '%s.html' % date)
        else:
            cwd = os.getcwd()
            output_filepath = os.path.join (cwd, '%s.html' % date)

        file = open (output_filepath, 'w')
        file.write (html)
        file.close ()

    if args ['--diff']:
        print ('Report %s v.s. %s' % (args ['DATE1'], args ['DATE2']))
        year1, month1 = parse_date (args ['DATE1'])
        year2, month2 = parse_date (args ['DATE2'])

        diff_report = make_report_diff (entries, year1, year2, month1, month2)

        report_print (diff_report)


if __name__ == '__main__':
    entries = open("Spese - Inbox.csv").readlines()
    main (entries)
