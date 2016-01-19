import os
import json
from src.models.entries.entry import Entry
from src.models.categories.category import Category
from src.models.categories.constants import CATEGORIES


def get_entries(json_data_fullpath):
    with open(json_data_fullpath, 'r') as f:
        json_data = json.loads(f.read())

    return [Entry(**jd) for jd in json_data]


def update_json(json_data_fullpath, entries=[]):
    if not isinstance(entries, list):
        raise Exception("Expecting a list as input")

    if len(entries) == 0:
        raise Exception("Entries list is empty")

    if not isinstance(entries[0], Entry):
        raise Exception("Expecting a list of Entry")

    old_entries = get_entries(json_data_fullpath)

    saved_ids = [entry._id for entry in old_entries]

    data = [e.json() for e in entries if e._id not in saved_ids]

    open(json_data_fullpath, 'w').write(json.dumps(data, indent=2))


def parse_cvs(cvs_fullpath,
              amount_col,
              description_col,
              date_col,
              outcome_col,
              category_col):
    categories = [Category(name, keywords) for name, keywords in
                  CATEGORIES.items()]
    lines = open(cvs_fullpath).readlines()
    entries = []
    for line in lines:
        sign = 1
        line = line.replace('\n', '')
        data = line.split(',')

        nominal_category = data[category_col]
        best_ratio = 0.0
        best_category = Category('Unknown')
        for category in categories:
            ratio = category.similarity(nominal_category)

            if ratio > best_ratio:
                best_ratio = ratio
                best_category = category.name

        if outcome_col >= 0:
            if data[outcome_col].lower() == 'outcome':
                sign = -1

            entry = Entry(amount=data[amount_col],
                          category=best_category,
                          description=data[description_col],
                          date=data[date_col],
                          sign=sign)
        entries.append(entry)

    return entries
