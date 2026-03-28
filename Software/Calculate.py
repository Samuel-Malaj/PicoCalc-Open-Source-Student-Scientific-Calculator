import math
import operator
import time
import traceback

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
            for char in text[:-1]:
                pos = text.index(char)

                if is_float(char) and is_float(text[pos + 1]): # checks if the value and the next value are both numbers
                    text[pos: pos + 2] = [text[pos] + text[pos + 1]]
                    break

                if counter >= (len(text)-1):
                    end = True
    return text


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

def get_compressed_AddSub(expression): # function keeps going through expression untill all addition and subtraction is done
    while '+' in expression or ('-' in expression and '-' not in expression[0]):
        expression = compress_AddSub(expression)
        print(expression)

    print('FINAL: ', expression)
    return expression

expression = ['5', '6', '+', '3', '-', '1', '0', '-', '1', '0', '0', '+']
answer = get_compressed_AddSub(expression)
print(answer)
