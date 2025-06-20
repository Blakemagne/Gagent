import ast
import operator as op
import sys

def calculate(expression):
    """Evaluates a mathematical expression string."""
    # Supported operators
    operators = {
        ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
        ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg
    }

    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](eval_expr(node.operand))
        else:
            raise TypeError(node)

    node_tree = ast.parse(expression, mode='eval').body
    return eval_expr(node_tree)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        expression = sys.argv[1]
        try:
            result = calculate(expression)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
    else:
        print("Please provide a mathematical expression as a command-line argument.")