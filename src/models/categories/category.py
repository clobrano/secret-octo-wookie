from difflib import SequenceMatcher


class Category(object):
    def __init__(self, name, keywords=[], amount=0.0, variation=0.0):
        self.name = name
        self.keywords = keywords
        self.amount = amount
        self.variation = variation

    def update_amount(self, amount):
        self.amount += amount

    def similarity(self, category_name):
        main_ratio = SequenceMatcher(None, self.name, category_name).ratio()
        if main_ratio == 1.0:
            return main_ratio

        for key in self.keywords:
            ratio = SequenceMatcher(None, key, category_name).ratio()
            if ratio == 1.0:
                return ratio

            if ratio > main_ratio:
                main_ratio = ratio

        return main_ratio

    def json(self):
        return {
            'name': self.name,
            'amount': self.amount,
            'variation': self.variation
        }
