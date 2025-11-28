# Simple Calculator application by using python

# Taking user input
a = int(input("Enter the 1st Number : "))
b = int(input("Enter the 2nd Number : "))
print(type(a)) # Variables type
print(type(b)) # Variables type

c = input("Enter the operations (+ , - , * , / , power , Remainder) : ")

if c == '+' :
  sum = a + b
  print("The Sum Result is : ", sum)
elif c == '-' :
  sub = a - b
  print("The Substraction Result is :", sub)
elif c == '*' :
  multi = a * b
  print("The Multiplication Result is :", multi)
elif c == 'power' :
  pow = a ** b
  print("The Power Result is :", pow)
elif c == '/' :
  if b == 0 :
    print("Can't divided by Zero.!!")
  else :
   div = a / b
   print("The Division Result is :", div)
elif c == 'Remainder' :
  if b == 0 :
    print("Can't divided by Zero.!!")
  else :
   Rem = a % b
   print("The Remainder Result is :", Rem)
else :
  print("Enter Operation method to get result.")