#!/usr/bin/env python
'''
Usage:
    ./accountant.py  [--report] [--diff] [DATE1] [DATE2] [--date-format=DATE_FMT] [--debug]
'''
import sys
import pprint
from time import strftime
from time import strptime
from docopt import docopt

# Get Configuratino values
args = docopt (__doc__, version="Accountant v1.0")

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
        self.amount  = self._parse_amount (entry [AMOUNT_POS])
        self.category = entry [CAT_POS].rstrip ()
        self.comment  = entry [COMMENT_POS].rstrip ()


    def _parse_amount (self, float_str):
        float_sanitized = float_str.replace ('"', '').replace ("'",'')
        return float (float_sanitized)

    def get_date (self, entry):
        if len (entry) >= 3:
            return strptime (entry [DATE_POS], date_format)
        else:
            return None

    def __repr__ (self):
        if self.outcome:
            amount = -self.amount
        else:
            amount = self.amount
        return '%s, %0.2f, %s - %s' % \
                (strftime('%Y-%m-%d', self.date), amount, self.category, self.comment)



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


def report_month (year, month, entries = []):
    if 0 == len (entries):
        return
    report = {'_incomes':0.0, '_outcomes':0.0}

    for entry in entries:
        if str is type (entry):
            entry = entry.split (',')
        entryd = EntryDrive (entry)

        if year == entryd.date.tm_year and month == entryd.date.tm_mon:
            if entryd.category not in report.keys():
                report [entryd.category] = 0

            report [entryd.category] += entryd.amount

            if not entryd.outcome:
                report ['_incomes'] += entryd.amount
            else:
                report ['_outcomes'] += entryd.amount

    return report


def main (entries):
    pp = pprint.PrettyPrinter (indent = 4)
    if args ['--report']:
        print ('Report %s' % args ['DATE1'])
        year, month = args ['DATE1'].split ('-')
        report = report_month ( int (year), int (month), entries)
        pp.pprint (report)

    if args ['--diff']:
        print ('Diff %s vs %s' % (args ['DATE1'], args ['DATE2']))
        year1, month1 = args ['DATE1'].split('-')
        year2, month2 = args ['DATE2'].split('-')

        report1 = report_month (int (year1), int (month1), entries)
        report2 = report_month (int (year2), int (month2), entries)
        diff = {}

        for key in report1.keys ():
            if key in report2.keys ():
                try:
                    diff [key] = '%0.2fp' % (100.0 * ((report1 [key] - report2 [key]) / report1 [key]))
                except ZeroDivisionError:
                    diff [key] = '0.0'
            else:
                diff [key] = '100p'

        pp.pprint (diff)


if __name__ == '__main__':
    entries = open("Spese - Inbox.csv").readlines()
    main (entries)
