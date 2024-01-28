import re

def perform_opertion(sentence):
    #regex to extract number and operation keywords....
    pattern = r'(\d+(\.[0-9]+)?)\s*(add|sum|plus|subtract|minus|times|multipy|divided by|over|[+]|[-]|[*]|[/])\s*(\d+(\.[0-9]+)?)'
    pattern2 = r'\s*(\d+(\.\d+)?)\s*(and|of|from|by)\s*(\d+(\.\d+)?)'
    pattern3 = r'\s*(add|sum|plus|subtract|minus|times|product|multipy|divided by|over)\s*'
    
    sum = ['sum', 'add', 'plus','+']
    minus = ['subtract','minus','-']
    times = ['multipy','times','product','*']
    divide = ['divided by', 'over','/']
    
    #search for pattern in sentence...
    match = re.search(pattern,sentence)  #to identify parttens like  1 plus 1  or  1  +  1....... 
    
    #match2 and match3 is combined to identify the partten 'sum of 1 and 1' or 'multiple of 3 and 4'.....
    match2 = re.findall(pattern2,sentence)   
    match3 = re.findall(pattern3,sentence)
    
    if match:     
        num1 = float(match.group(1))
        ops = str(match.group(3))
        num2 = float(match.group(4))      
        # print(num1, ops, num2)
    elif match2 and match3:
        print('second match')
        # match3 = match3[0]
        num1 = int(match2[0][0])
        num2 = int(match2[0][3])
        ops = str(match3[0]) 
        # print(num1, ops, num2)
    else:
        
        return f'Please rephrase the question'
        
    r = 0.0
    # determining the type of operation to perform........
    if ops in sum:
        # print('summation operator')
        r = num1 + num2
        return f'the anwser is: {r}'
    elif ops in minus:
        # print('subtraction operator')
        r = num1 - num2
        return f'the anwser is: {r}'
    elif ops in times:
        # print('multiplication operator')
        r = num1 * num2
        return f'the anwser is: {r}'
    elif ops in divide:
        # print('division operator')
        r = num1 / num2
        return f'the anwser is: {r}'

# words = input('Enter a statemant:')

# perform_opertion(words)