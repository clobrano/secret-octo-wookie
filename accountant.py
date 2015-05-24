#!/usr/bin/env python
'''
Usage:
    ./accountant.py  [--report=DATE] [--diff] [DATE1] [DATE2] [--date-format=DATE_FMT] [--debug]
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
        self.date_str = strftime ('%d/%m/%Y', self.date)
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
                (strftime('%Y-%m-%d', self.date), amount, self.category, self.comment)


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


def report_month (year, month, entries = []):
    if 0 == len (entries):
        return {}
    biggest_expense_amount = 0.0
    report = {
            '_outcomes': [],
            '_incomes': [],
            '_tot_incomes':0.0,
            '_tot_outcomes':0.0,
            '_biggest_expense': None}

    for entry in entries:
        if type (entry) is str:
            entry = entry.split (',')
        entryd = EntryDrive (entry)

        if year == entryd.date.tm_year and month == entryd.date.tm_mon:
            if entryd.outcome and entryd.category != 'Rent' and abs (entryd.amount) > biggest_expense_amount:
                report ['_biggest_expense'] = entryd
                biggest_expense_amount = abs (entryd.amount)
            report = add_entry_to_report (report = report, entry = entryd)
    return report


def report_year (year, entries = []):
    if 0 == len (entries):
        return {}
    report = {'_incomes':0.0, '_outcomes':0.0}
    for row in entries:
        logd (row)
        logd ('type (row) is {0}'.format (type (row)))
        if type (row) is str:
            row = row.split (',')
        entry = EntryDrive (row)

        if year == entry.date.tm_year:
            if entry.category not in report.keys():
                report [entry.category] = 0

            report [entry.category] += entry.amount

            if not entry.outcome:
                report ['_incomes'] += entry.amount
            else:
                report ['_outcomes'] += entry.amount

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


def report_render (report = {}, title = 'Report'):
    templateLoader = jinja2.FileSystemLoader (searchpath = '/')
    templateEnv = jinja2.Environment (loader=templateLoader)
    cwd = os.getcwd()
    template = templateEnv.get_template (os.path.join (cwd, 'report_template.html'))
    templateVars = { 'title' : title, 'report' : report }
    templateEnv.filters ['datetime'] = format_datetime
    outputText = template.render (templateVars)

    return outputText


def main (entries):
    if args ['--report'] is not None:
        date = args ['--report']
        print ('Report %s' % date)
        if '-' in date:
            year, month = date.split ('-')
            report = report_month (int (year), int (month), entries)
        else:
            year = int (date)
            report = report_year (year, entries)

        report_print (report)
        html = report_render (report, 'Report %s' % date)
        file = open ('%s.html' % date, 'w')
        file.write (html)
        file.close ()

    if args ['--diff']:
        date1 = args ['DATE1']
        date2 = args ['DATE2']
        print ('Diff %s vs %s' % (date1, date2))
        if '-' in date1:
            year1, month1 = date1.split('-')
            report1 = report_month (int (year1), int (month1), entries)
        else:
            year1 = date1
            report1 = report_year (int (year1), entries)

        if '-' in date2:
            year2, month2 = date2.split('-')
            report2 = report_month (int (year2), int (month2), entries)
        else:
            year2 = date2
            report2 = report_year (int (year2), entries)

        diff_report = diff (report1, report2)

        report_print (diff_report)


if __name__ == '__main__':
    entries = open("Spese - Inbox.csv").readlines()
    main (entries)
