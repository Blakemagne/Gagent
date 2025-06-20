import ast
import operator as op

class Calculator:
    def __init__(self):
        pass

    def calculate(self, expression):
        """Evaluates a mathematical expression string."""
        # Supported operators
        operators = {
            ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
            ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg
        }

        def eval_expr(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
            elif isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](eval_expr(node.operand))
            else:
                raise TypeError(node)

        node_tree = ast.parse(expression, mode='eval').body
        return eval_expr(node_tree)

if __name__ == '__main__':
    calculator = Calculator()
    expression = "(2 + 3) * 4"
    result = calculator.calculate(expression)
    print(f"{expression} = {result}")