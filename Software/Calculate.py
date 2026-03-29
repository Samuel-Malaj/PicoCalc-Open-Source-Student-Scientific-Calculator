import math
import time

def is_float(char): # checks if the value is a number
    try:
        float(char)
        return True
    except (ValueError, TypeError):
        return False

def join_nums(text): # joins all the side by side digits into one number for calculations
    end = False
    counter = 0
    if len(text) > 1:
        while not end:
            counter += 1
            for pos, char in enumerate(text[:-1]):
                if is_float(char) and is_float(text[pos + 1]): # checks if the value and the next value are both numbers
                    text[pos: pos + 2] = [text[pos] + text[pos + 1]]
                    break
                if char == '.':
                    text[pos-1: pos + 2] = [text[pos-1] + '.' + text[pos + 1]]
                    break

                if counter >= (len(text)-1):
                    end = True
    return text

def compress_MultiplyDivide(expression): # does multipliplication + division
    print(expression)
    expression = join_nums(expression)
    print('Joined: ',expression)
    for char in expression:
        if char == 'x':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 * num2
                expression[expression.index(char)-1: expression.index(char)+2] = str(compressed_value)

                return expression

            except:
                return ['Syntax Error']

        if char == '/':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 / num2
                expression[expression.index(char)-1: expression.index(char)+2] = str(compressed_value)

                return expression

            except:
                return ['Syntax Error']


def compress_AddSub(expression): # function does addition and subtraction
    expression = join_nums(expression)
    print(expression)
    for char in expression:
        if char == '+':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 + num2
                expression[expression.index(char)-1: expression.index(char)+2] = [str(compressed_value)]
                
                return expression

            except:
                return ['syntax error']

        if char == '-':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 - num2
                expression[expression.index(char)-1: expression.index(char)+2] = [str(compressed_value)]

                return expression

            except:
                return ['syntax error']

def get_compressed_MultiplyDivide(expression): # keeps multiplying and dividing untill all multiplication + division is done
    while 'x' in expression or '/' in expression:
        expression = compress_MultiplyDivide(expression)
    return expression 

def get_compressed_AddSub(expression): # function keeps going through expression untill all addition and subtraction is done
    while '+' in expression or ('-' in expression and '-' not in expression[0]):
        expression = compress_AddSub(expression)
    return expression

def calculate(expression):
    expression = get_compressed_MultiplyDivide(expression)
    print(expression)
    expression = get_compressed_AddSub(expression)

    return expression
