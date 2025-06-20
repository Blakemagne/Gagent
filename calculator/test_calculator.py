import unittest
import advanced_calculator

class TestAdvancedCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(advanced_calculator.add(1, 2), 3)
        self.assertEqual(advanced_calculator.add(-1, 2), 1)
        self.assertEqual(advanced_calculator.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(advanced_calculator.subtract(1, 2), -1)
        self.assertEqual(advanced_calculator.subtract(-1, 2), -3)
        self.assertEqual(advanced_calculator.subtract(0, 0), 0)

    def test_multiply(self):
        self.assertEqual(advanced_calculator.multiply(1, 2), 2)
        self.assertEqual(advanced_calculator.multiply(-1, 2), -2)
        self.assertEqual(advanced_calculator.multiply(0, 0), 0)

    def test_divide(self):
        self.assertEqual(advanced_calculator.divide(1, 2), 0.5)
        self.assertEqual(advanced_calculator.divide(-1, 2), -0.5)
        self.assertEqual(advanced_calculator.divide(0, 1), 0)
        self.assertEqual(advanced_calculator.divide(1, 0), "Cannot divide by zero")

    def test_exponentiate(self):
        self.assertEqual(advanced_calculator.exponentiate(2, 3), 8)
        self.assertEqual(advanced_calculator.exponentiate(2, -1), 0.5)
        self.assertEqual(advanced_calculator.exponentiate(0, 0), 1)

    def test_square_root(self):
        self.assertEqual(advanced_calculator.square_root(4), 2)
        self.assertEqual(advanced_calculator.square_root(0), 0)
        self.assertEqual(advanced_calculator.square_root(-1), "Cannot calculate square root of a negative number")

    def test_factorial(self):
        self.assertEqual(advanced_calculator.factorial(0), 1)
        self.assertEqual(advanced_calculator.factorial(5), 120)
        self.assertEqual(advanced_calculator.factorial(1), 1)
        self.assertEqual(advanced_calculator.factorial(-1), "Cannot calculate factorial of a negative number")
        self.assertEqual(advanced_calculator.factorial(1.5), "Cannot calculate factorial of a non-integer number")

if __name__ == '__main__':
    unittest.main()
