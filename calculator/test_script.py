
from calculator_refactored import Calculator

calculator = Calculator()

# Test cases
test_cases = [
    (1, 2, "add", 3),
    (5, 3, "subtract", 2),
    (4, 6, "multiply", 24),
    (10, 2, "divide", 5),
    (5, 0, "divide", ValueError),  # Division by zero
    ("a", 2, "add", ValueError),  # Invalid input
    (1, 2, "invalid", ValueError)   # Invalid operation
]

for x, y, operation, expected in test_cases:
    try:
        result = calculator.calculate(x, y, operation)
        if expected == ValueError:
            print(f"Test failed: {x} {operation} {y} should have raised ValueError")
        elif result != expected:
            print(f"Test failed: {x} {operation} {y} expected {expected}, got {result}")
        else:
            print(f"Test passed: {x} {operation} {y} = {result}")
    except ValueError:
        if expected == ValueError:
            print(f"Test passed: {x} {operation} {y} raised ValueError as expected")
        else:
            print(f"Test failed: {x} {operation} {y} raised unexpected ValueError")
    except Exception as e:
        print(f"Test failed: {x} {operation} {y} raised unexpected exception: {e}")
