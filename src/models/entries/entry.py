import datetime
import uuid
from time import strptime, strftime
from src.models.entries.constants import DATE_FORMAT


class Entry(object):
    def __init__(self, amount, category, description, date=None, sign=1, _id=None):
        self.amount = amount if isinstance(amount, float) else sign*float(amount.replace('"',''))
        self.category = category
        self.description = description
        self.date = date if not isinstance(date, str) else strptime(date, DATE_FORMAT)
        self._id = _id if _id is not None else uuid.uuid4().hex

    def get_date(self):
        return strftime(DATE_FORMAT, self.date) 

    def json(self):
        return {
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'date': self.get_date(),
            '_id': self._id
        }

    def __eq__(self, other):
        return self._id == other._id
