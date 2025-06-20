class OperationStrategy:
    def execute(self, x, y):
        raise NotImplementedError


class Add(OperationStrategy):
    def execute(self, x, y):
        return x + y


class Subtract(OperationStrategy):
    def execute(self, x, y):
        return x - y


class Multiply(OperationStrategy):
    def execute(self, x, y):
        return x * y


class Divide(OperationStrategy):
    def execute(self, x, y):
        if y == 0:
            raise ValueError("Division by zero is not allowed.")
        return x / y


class Calculator:
    def __init__(self):
        self.operations = {
            'add': Add(),
            'subtract': Subtract(),
            'multiply': Multiply(),
            'divide': Divide()
        }

    def calculate(self, x, y, operation):
        try:
            x = float(x)
            y = float(y)
        except ValueError:
            raise ValueError("Invalid input: Both x and y must be numeric values.")

        if operation not in self.operations:
            raise ValueError(f"Invalid operation: '{operation}' is not a supported operation. Supported operations are: {', '.join(self.operations.keys())}")

        try:
            return self.operations[operation].execute(x, y)
        except Exception as e:
            raise Exception(f"An error occurred during the {operation} operation: {e}")


if __name__ == '__main__':
    calculator = Calculator()
    try:
        x = input("Enter first number: ")
        y = input("Enter second number: ")
        operation = input("Enter operation (add, subtract, multiply, divide): ")
        result = calculator.calculate(x, y, operation)
        print("Result:", result)
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
