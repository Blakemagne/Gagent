import sys

if __name__ == '__main__':
    if len(sys.argv) > 2:
        num1 = int(sys.argv[1])
        num2 = int(sys.argv[2])
        print(num1 + num2)
    else:
        print("Please provide two numbers as arguments.")