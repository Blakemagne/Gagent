
from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, x, y):
        pass

class Addition(Operation):
    def execute(self, x, y):
        return x + y

class Subtraction(Operation):
    def execute(self, x, y):
        return x - y

class Multiplication(Operation):
    def execute(self, x, y):
        return x * y

class Division(Operation):
    def execute(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y

class Calculator:
    def __init__(self):
        self.operations = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division()
        }

    def calculate(self, x, y, operator):
        operation = self.operations.get(operator)
        if not operation:
            raise ValueError("Invalid operator")
        return operation.execute(x, y)

if __name__ == '__main__':
    calculator = Calculator()
    x = 10
    y = 5
    operator = '+'
    result = calculator.calculate(x, y, operator)
    print(f"{x} {operator} {y} = {result}")

    x = 10
    y = 5
    operator = '/'
    result = calculator.calculate(x, y, operator)
    print(f"{x} {operator} {y} = {result}")
