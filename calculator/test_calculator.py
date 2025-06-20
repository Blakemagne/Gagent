import unittest
from pkg.calculator import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_parentheses(self):
        self.assertEqual(self.calculator.evaluate("(2 + 3) * 4"), 20.0)
        self.assertEqual(self.calculator.evaluate("2 * (3 + 4)"), 14.0)
        self.assertEqual(self.calculator.evaluate("10 - (4 / 2)"), 8.0)
        self.assertEqual(self.calculator.evaluate("((10 - 4) / 2)"), 3.0)

    def test_power(self):
        self.assertEqual(self.calculator.evaluate("2 ** 3"), 8.0)
        self.assertEqual(self.calculator.evaluate("3 ** 2"), 9.0)
        self.assertEqual(self.calculator.evaluate("2 ** (1 + 2)"), 8.0)

    def test_precedence(self):
        self.assertEqual(self.calculator.evaluate("2 + 3 * 4"), 14.0)
        self.assertEqual(self.calculator.evaluate("2 * 3 + 4"), 10.0)
        self.assertEqual(self.calculator.evaluate("2 + 3 ** 2"), 11.0)

if __name__ == '__main__':
    unittest.main()