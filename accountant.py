#!/usr/bin/env python
import sys
import pprint
from time import strftime
from time import strptime

class EntryDrive (object):

    def __init__ (self, entry = []):
        self.outcome = (entry [1] == 'Outcome')
        self.date    = self.get_date (entry)
        self.amount  = self._parse_amount (entry [3])
        self.category = entry [4].rstrip ()
        self.comment  = entry [5].rstrip ()


    def _parse_amount (self, float_str):
        float_sanitized = float_str.replace ('"', '').replace ("'",'')
        return float (float_sanitized)

    def get_date (self, entry):
        if len (entry) >= 3:
            return strptime (entry [2], '%d/%m/%Y')
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
            return time.strptime (entry [2], '%d/%m/%Y')
        else:
            return None

def select_entries (entry, month, year):
    date = get_date (entry)
    if date.tm_year == year and date.tm_mon == month:
        return entry

    return None


def report_month (year, month, entries = []):
    print ('Report for %d-%d' % (year, month))
    if 0 == len (entries):
        return
    report = {'_incomes':0.0, '_outcomes':0.0}

    for entry in entries:
        if str is type (entry):
            entry = entry.split (',')
        entryd = EntryDrive (entry)

        if year == entryd.date.tm_year and month == entryd.date.tm_mon:
            print (entryd)
            if entryd.category not in report.keys():
                report [entryd.category] = 0

            report [entryd.category] += entryd.amount

            if not entryd.outcome:
                report ['_incomes'] += entryd.amount
            else:
                report ['_outcomes'] += entryd.amount

    return report


if __name__ == '__main__':
    entries = open("Spese - Inbox.csv").readlines()
    year = int(sys.argv[1])
    month = int (sys.argv [2])

    for entry in entries:
        entry = entry.split(',')
        e = EntryDrive(entry)
        if e.date.tm_year == year and e.date.tm_mon == month:
            print e

    pp = pprint.PrettyPrinter (indent = 4)
    report = report_month (year, month, entries)
    pp.pprint (report)
    report_prev_month = report_month (year, month - 1, entries)
    pp.pprint (report_prev_month)
    diff = {}

    for key in report.keys ():
        if key in report_prev_month.keys ():
            try:
                diff [key] = '%0.2fp' % (100.0 * ((report [key] - report_prev_month [key]) / report [key]))
            except ZeroDivisionError:
                diff [key] = '0.0'
        else:
            diff [key] = '100p'

    pp.pprint (diff)

