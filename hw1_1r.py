#1
name = input('name? ')
def privet(imya):
    print('hi,', imya)
privet(name)
print()

#2
a = float(input('first number? '))
b = float(input('second number? '))
def sum(number):
    print(number)
c = a + b
sum(c)
print()

#3
a = float(input('write your number '))
def isEven(number):
    if a % 2 == 0:
        print('true')
    else:
        print('false')
isEven(a)
print()

#4
n = int(input('number of apples? '))
def apples(number):
    print('i have ' + str(number) +' apples')
apples(n)
print()

#5
x = float(input('write your number '))
x2 = x**2
def getPower(number):
    print(number)
getPower(x2)
print()