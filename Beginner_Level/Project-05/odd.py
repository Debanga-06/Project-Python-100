def check_odd_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

user_input = int(input("Enter a number: "))
result = check_odd_even(user_input)
print(f"The number {user_input} is {result}.")
