import unittest
from src.models.entries.entry import Entry
from src.models.reports.report import Report


class TestReports(unittest.TestCase):
    def test_get_biggest_expense_no_entries_exception(self):
        report = Report(2016, 1, [])
        with self.assertRaises(Exception):
            report.get_biggest_expense()

    def test_entry_selection(self):
        entry1_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }
        entry2_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2014',
        }
        entry3_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/02/2015',
        }

        entry1 = Entry(**entry1_json)
        entry2 = Entry(**entry2_json)
        entry3 = Entry(**entry3_json)

        entries = [entry1, entry2, entry3]
        report = Report(year=2015, month=1, entries=entries)

        self.assertTrue(len(report.entries), 1)
        self.assertEquals(entry1.json(), report.entries[0].json())

    def test_get_income(self):
        entry1_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }
        entry2_json = {
            'amount': -10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }
        entry3_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }

        entry1 = Entry(**entry1_json)
        entry2 = Entry(**entry2_json)
        entry3 = Entry(**entry3_json)

        entries = [entry1, entry2, entry3]
        report = Report(year=2015, month=1, entries=entries)

        self.assertEquals(20.0, report.get_income())

    def test_get_outcome(self):
        entry1_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }
        entry2_json = {
            'amount': -10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }
        entry3_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }

        entry1 = Entry(**entry1_json)
        entry2 = Entry(**entry2_json)
        entry3 = Entry(**entry3_json)

        entries = [entry1, entry2, entry3]
        report = Report(year=2015, month=1, entries=entries)

        self.assertEquals(-10.0, report.get_outcome())


if __name__ == '__main__':
    unittest.main()
