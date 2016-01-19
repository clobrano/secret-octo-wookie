import unittest
from src.models.categories.category import Category
from src.models.categories.constants import CATEGORIES


class TestCategory(unittest.TestCase):
    def test_similarity(self):
        category = Category('Fuel', CATEGORIES['Fuel'])
        self.assertEquals(category.similarity('Car Fuel'), 1.0)

if __name__ == '__main__':
    unittest.main()
