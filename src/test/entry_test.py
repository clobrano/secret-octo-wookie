import unittest
import datetime
import time
from src.models.entries.entry import Entry


class TestEntry(unittest.TestCase):
    def test_json(self):
        exp_json = {
            'amount': 10.0,
            'description': "some description",
            'category': 'personal',
            'date': '01/01/2015',
        }

        entry = Entry(**exp_json)

        self.assertEquals(exp_json, entry.json())
        self.assertTrue(isinstance(entry.date, time.struct_time))

        entry = Entry(amount='10.0',
                      description = "some description",
                      category = "personal",
                      date='01/01/2015')
        self.assertTrue(isinstance(entry.amount, float))

if __name__ == '__main__':
    unittest.main()
