import math
import time
import decimal

sci_operators = ['sin(', 'cos(', 'tan(']

def is_float(char):
    try:
        float(char)
        return True
    except (ValueError, TypeError):
        return False

def join_nums(text):
    end = False
    counter = 0

    if len(text) > 1:
        while not end:
            counter += 1
            for pos, char in enumerate(text[:-1]):   
                if is_float(char) and is_float(text[pos + 1]):
                    text[pos: pos + 2] = [text[pos] + text[pos + 1]]
                    break

                if char == '.':
                    text[pos-1: pos + 2] = [text[pos-1] + '.' + text[pos + 1]]
                    break
                
                if counter >= (len(text)-1):
                         end = True

    return text

def get_error(expression, e): # function handles errors
    error = str(e)
    if 'Syntax Error' in expression or 'not in list' in error or 'could not convert' in error:
        return ['Syntax Error']

    elif 'Math Error' in expression:
        return ['Math Error']

    elif 'Result too large' in error:
        return ['Math Error']

    else:
        return ['Error']

############# Calculations ##########
def compress_sci_operators(expression): # goes through expression and carries out all scientific calculations e.g sin() cos() tan()
    expression = join_nums(expression)
    for char in expression:
        ############ SIN ##########
        if char == 'sin(':
            try:
                sin_nums = expression[expression.index('sin(') + 1: expression.index(')')]

                while len(sin_nums) > 1:
                    sin_nums = [calculate(sin_nums)]
                sin_nums = join_nums(sin_nums)[0]

                if is_float(sin_nums):
                    sin_nums = math.radians(float(''.join(sin_nums)))
                    
                compressed_value = math.sin(sin_nums)
                expression[expression.index('sin('): expression.index(')') + 1] = [str(compressed_value)]

                return expression
                
            except Exception as e:
                return get_error(expression, e)
                
        ############ COS ##########
        if char == 'cos(':
            try:
                cos_nums = expression[expression.index('cos(') + 1: expression.index(')')]

                while len(cos_nums) > 1:
                    cos_nums = [calculate(cos_nums)]
                cos_nums = join_nums(cos_nums)[0]
                
                if is_float(cos_nums):
                    cos_nums = math.radians(float(''.join(cos_nums)))
                  
                compressed_value = math.cos(cos_nums)                
                expression[expression.index('cos('): expression.index(')') + 1] = [str(compressed_value)]
                
                return expression
                
            except Exception as e:
                return get_error(expression, e)
                
        ############ TAN ##########
        if char == 'tan(':
            try:
                tan_nums = expression[expression.index('tan(') + 1: expression.index(')')]

                while len(tan_nums) > 1:
                    tan_nums = [calculate(tan_nums)]
                tan_nums = join_nums(tan_nums)[0]
                
                if is_float(tan_nums):
                    tan_nums = math.radians(float(''.join(tan_nums)))
                  
                compressed_value = math.tan(tan_nums)             
                expression[expression.index('tan('): expression.index(')') + 1] = [str(compressed_value)]

                return expression
                
            except Exception as e:
                return get_error(expression, e)

def compress_brackets(expression): # Calcuates the values of all expressions enclosed within brackets
    expression = join_nums(expression)
    for pos, char in enumerate(expression):
        if char == '(':
            try:
                open_bracket = pos
                closed_bracket = (expression[::-1].index(')') * -1) -1

                sub_expression = expression[pos+1: closed_bracket]

                if closed_bracket == -1:
                    closed_bracket = None

                else:
                    closed_bracket += 1

                compressed_value = calculate(sub_expression)
                expression[expression.index('('): closed_bracket] = [compressed_value]
                expression

                return expression

            except Exception as e:
                return get_error(expression, e)
            

def compress_indeces(expression):
    expression = join_nums(expression)
    for char in expression:
        if char == '^':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char) + 1])
                compressed_value = str(float(decimal.Decimal(num1 ** num2)))

                expression[expression.index(char)-1: expression.index(char)+2] = str(compressed_value)


                return expression

            except Exception as e:
                return get_error(expression, e)

def compress_MultiplyDivide(expression): # goes through expression and does all multiplication and division
    expression = join_nums(expression)
    for char in expression:
        if char == 'x':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 * num2
                expression[expression.index(char)-1: expression.index(char)+2] = [str(compressed_value)]

                return expression

            except Exception as e:
                return get_error(expression, e)

        if char == '/':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 / num2
                expression[expression.index(char)-1: expression.index(char)+2] = [str(compressed_value)]

                return expression

            except Exception as e:
                return get_error(expression, e)

def compress_AddSub(expression):
    expression = join_nums(expression) # goes though expression and does all addition and subtraction
    for char in expression:
        if char == '+':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 + num2
                expression[expression.index(char)-1: expression.index(char)+2] = [str(compressed_value)]
                
                return expression

            except Exception as e:
                return get_error(expression, e)
            
        if char == '-':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 - num2
                expression[expression.index(char)-1: expression.index(char)+2] = [str(compressed_value)]

                return expression

            except Exception as e:
                return get_error(expression, e)

        
###############################################################################################################

''' funcctions do all calculations in expression until none remain '''
def get_compressed_sci(expression):
    for i in sci_operators:
        while i in expression: 
            expression = compress_sci_operators(expression)
    return expression

def get_compressed_brackets(expression):
    while '(' in expression:
        expression = compress_brackets(expression)
    return expression

def get_compressed_brackets(expression):
    while '(' in expression:
        expression = compress_brackets(expression)
    return expression

def get_compressed_indeces(expression):
    while '^' in expression:
        expression = compress_indeces(expression)
    return expression

def get_compressed_MultiplyDivide(expression):
    while 'x' in expression or '/' in expression:
        expression = compress_MultiplyDivide(expression)
    return expression

def get_compressed_AddSub(expression):
    while '+' in expression or ('-' in expression and expression.index('-') > 0):
        expression = compress_AddSub(expression)
    return expression

def calculate(expression): #compresses all functions into one in BIDMAS order 
    expression = get_compressed_sci(expression)
    expression = get_compressed_brackets(expression)
    expression = get_compressed_indeces(expression)
    expression = get_compressed_MultiplyDivide(expression)
    expression = get_compressed_AddSub(expression)
    expression = ''.join(expression)
    if not is_float(expression) and expression not in ['Syntax Error', 'Error', 'Math Error']:
        return 'Syntax Error'
    return expression

''' example calculations '''
expression = ['(', '8', '-', '2', 'x', 'sin(', '4', '3', '.', '5', '/', '2', ')', ')', '^', '2'] # output = '52.69141325766067'
print(calculate(expression))

expression = ['9', '^', '9', '9', '9', '9', 'sin('] # output = 'Syntax Error'
print(calculate(expression))

expression = ['tan(', '9', '0', ')'] # output = '1.633123935319537e+16'
print(calculate(expression))

expression = ['21.75']# output = '21.75'
print(calculate(expression))

expression = ['sin(', '3', '0', ')', '^', '2', '+', 'cos(', '3', '0', ')', '^', '2'] # output = '1'
print(calculate(expression))

expression = ['999', '^', '99999999'] # output = 'Math Error'
print(calculate(expression))
