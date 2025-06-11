from functions.get_file_content import get_file_content

if __name__ == "__main__":
    print("Test 1: get_file_content('calculator', 'main.py')")
    print(get_file_content("calculator", "main.py"))
    print("\n" + "-"*60 + "\n")

    print("Test 2: get_file_content('calculator', 'pkg/calculator.py')")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("\n" + "-"*60 + "\n")

    print("Test 3: get_file_content('calculator', '/bin/cat')")
    print(get_file_content("calculator", "/bin/cat"))
    print("\n" + "-"*60 + "\n")

