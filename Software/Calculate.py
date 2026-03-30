import math

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
                return ['syntax error']
                
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
                return ['syntax error']
                
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
                return ['syntax error']

def compress_indeces(expression):
    expression = join_nums(expression)
    for char in expression:
        if char == '^':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char) + 1])
                compressed_value = num1 ** num2
                expression[expression.index(char)-1: expression.index(char)+2] = str(compressed_value)

                return expression

            except:
                print('Syntax Error')

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

            except:
                return ['Syntax Error']

        if char == '/':
            try:
                num1 = float(expression[expression.index(char)-1])
                num2 = float(expression[expression.index(char)+1])
                compressed_value = num1 / num2
                expression[expression.index(char)-1: expression.index(char)+2] = [str(compressed_value)]

                return expression

            except:
                return ['Syntax Error']

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

        
###############################################################################################################

''' funcctions do all calculations in expression until none remain '''
def get_compressed_sci(expression):
    for i in sci_operators:
        while i in expression: 
            expression = compress_sci_operators(expression)
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
    expression = get_compressed_indeces(expression)
    expression = get_compressed_MultiplyDivide(expression)
    expression = get_compressed_AddSub(expression)
    expression = ''.join(expression)
    return expression

''' calculation example '''
expression = ['8', '-', '2', 'x', 'sin(', '4', '3', '.', '5', '/', '2', ')']
expression = calculate(expression)
print(expression)
