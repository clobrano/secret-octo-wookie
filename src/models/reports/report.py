import src.models.reports.errors as ReportErrors
from src.models.categories.category import Category
from src.models.categories.constants import CATEGORIES



class Report(object):
    def __init__(self, year, month=None, entries=[]):
        self.year = year
        self.month = month
        self.entries = []
        categories = [Category(name, keywords) for name, keywords in CATEGORIES.items()]
        for e in entries:
            if e.date.tm_year == year and \
                    (month is None or e.date.tm_mon == month):
                self.entries.append(e)
                for c in categories:
                    if c.name == e.category:
                        c.update_amount(e.amount)
        self.entries.sort(key=lambda x: x.date.tm_mday)
        self.categories = categories

    def get_incomes(self):
        return [e for e in self.entries if e.amount > 0]

    def get_income(self):
        return sum([e.amount for e in self.entries if e.amount > 0])

    def get_outcomes(self):
        return [e for e in self.entries if e.amount < 0]

    def get_outcome(self):
        return sum([e.amount for e in self.entries if e.amount < 0])

    def get_biggest_expense(self):
        if len(self.entries) == 0:
            raise ReportErrors.EmptyReportException("No entries in this report")
        else:
            entries = sorted(self.entries, key=lambda x: x.amount)

            return entries[0]

    def compare_categories(self, report):
        self.categories.sort(key=lambda x:x.name)
        ref = sorted(report.categories, key=lambda x:x.name)

        for x, y in zip(self.categories, ref):
            if x.amount == y.amount:
                variation = 0.0
            elif x.amount == 0.0 and y.amount != 0.0:
                variation = -1.0
            elif x.amount != 0.0 and y.amount == 0.0:
                variation = 1.0
            else:
                variation = (abs(x.amount) - abs(y.amount))/abs(x.amount)
            x.variation = round(variation * 100.0, 1)

    def json(self):
        biggest_expense = self.get_biggest_expense()
        categories = sorted(self.categories, key=lambda x:x.amount)
        return {
            'year': self.year,
            'month': self.month,
            'income': self.get_income(),
            'incomes': [i.json() for i in self.get_incomes()],
            'outcome': self.get_outcome() * -1,
            'outcomes': [o.json() for o in self.get_outcomes()],
            'biggest_expense_amount': biggest_expense.amount,
            'biggest_expense_category': biggest_expense.category,
            'biggest_expense_date': biggest_expense.get_date(),
            'entries': [e.json() for e in self.entries],
            'categories': [c.json() for c in categories],
        }

    def compare(report):
        pass
