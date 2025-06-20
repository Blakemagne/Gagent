# calculator.py

def divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": divide,
            "**": lambda a, b: a ** b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "**": 3,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression):
        tokens = []
        current_number = ""
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isdigit() or char == '.':
                current_number += char
            elif char == '*':
                if i + 1 < len(expression) and expression[i + 1] == '*':
                    if current_number:
                        tokens.append(current_number)
                        current_number = ""
                    tokens.append("**")
                    i += 1  # Skip the second *
                else:
                    if current_number:
                        tokens.append(current_number)
                        current_number = ""
                    tokens.append("*")
            elif char in self.operators or char in ["(", ")"]:
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)
            elif char.isspace():
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
            else:
                raise ValueError(f"Invalid character: {char}")
            i += 1
        if current_number:
            tokens.append(current_number)
        return tokens


    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if not operators:
                    raise ValueError("Mismatched parentheses")
                operators.pop()  # Remove the opening parenthesis
            elif token in self.operators:
                while (
                    operators
                    and operators[-1] != "("
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    val = float(token)
                    values.append(val)
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            if operators[-1] == "(":
                raise ValueError("Mismatched parentheses")
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))