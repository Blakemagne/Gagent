
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y

def exponentiate(x, y):
    return x ** y

import math

def square_root(x):
    if x < 0:
        return "Cannot calculate square root of a negative number"
    return math.sqrt(x)

def factorial(x):
    if x < 0:
        return "Cannot calculate factorial of a negative number"
    if not isinstance(x, int):
        return "Cannot calculate factorial of a non-integer number"
    if x == 0:
        return 1
    else:
        result = 1
        for i in range(1, x + 1):
            result *= i
        return result
