from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CalculationHistory  # Import the CalculationHistory model
history = []
#define operators
OPERATORS = {
    'plus': '+',
    'minus': '-',
    'into': '*',
    'upon': '/',
    'power': '^'
}
#Function to get operator precedence
def precedence(op):
    precedence_map = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    return precedence_map.get(op, 0)
#Function to apply operations
def applyOp(a, b, op):
    operators = {'+': lambda x, y: x + y, '-': lambda x, y: x - y,
                 '*': lambda x, y: x * y, '/': lambda x, y: x / y,
                 '^': lambda x, y: x ** y}
    return operators[op](a, b)
#Function to evaluate an expression
def evaluate(expression):
    values = []
    ops = []
    i = 0
    while i < len(expression):
        token = expression[i]
        if token.isdigit():
            val = 0
            while i < len(expression) and expression[i].isdigit():
                val = val * 10 + int(expression[i])
                i += 1
            values.append(val)
            i -= 1
        elif token in ('+', '-', '*', '/', '^'):
            while ops and precedence(ops[-1]) >= precedence(token):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                if op == '/' and val2 == 0:
                    return "Zero Divide Error"
                values.append(applyOp(val1, val2, op))
            ops.append(token)
        i += 1
    while ops:
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        if op == '/' and val2 == 0:
            return "Zero Divide Error"
        values.append(applyOp(val1, val2, op))
    return values[0]
#Calculation requests
@csrf_exempt
def calculate(request, expression):
    global OPERATORS
    try:
        parts = expression.split('/')
        for i in range(len(parts)):
            if parts[i] in OPERATORS.keys():
                parts[i] = OPERATORS[parts[i]]
        question = ''.join(parts)
        result = evaluate(parts)
        # Save calculation history into the database
        history.insert(0, {"question": question, "answer": result})
        history_entry = CalculationHistory(question=question, answer=result)
        history_entry.save()
        if len(history) > 20:
            history.pop()
        return JsonResponse({"question": question, "answer": result})
    except ValueError:
        return JsonResponse({"error": "Invalid expression"}, status=400)
#Retrieve history data
def history_view(request):
    history_entries = CalculationHistory.objects.all().order_by('-id')[:20]
    history_data = [{"question": entry.question, "answer": entry.answer} for entry in history_entries]
    return JsonResponse(history_data, safe=False)
#Display available endpoints
def index(request):
    endpoints = [
        {"endpoint": "/history", "description": "Lists the last 20 operations performed on the server and the answers."},
        {"endpoint": "/<operand1>/<operator>/<operand2>", 
         "description": "Perform a mathematical operation.",
         "eg": {
            "/5/plus/3": "{question:”5+3”,answer:8}",
            "/3/minus/5": "{question:”3-5”, answer: -2}",
            "/3/minus/5/plus/8": "{question:”3-5+8”, answer: 6}",
            "/3/into/5/plus/8/into/6": "{question:”3*5+8*6”, answer: 63}"  
         }
        }
    ]
    return JsonResponse(endpoints, safe=False)