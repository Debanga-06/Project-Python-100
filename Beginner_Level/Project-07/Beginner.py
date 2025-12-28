input_value = input("Enter a word or number: ")
reversed_value = input_value[::-1]

if input_value == reversed_value:
    print(f"{input_value} is a palindrome.")
else:
    print(f"{input_value} is not a palindrome.")
