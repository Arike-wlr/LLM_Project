import os
import requests
from dotenv import load_dotenv
import json
from sympy import parse_expr, sympify, SympifyError
from sympy.core.symbol import Symbol
from sympy import integrate, limit, diff, oo ,symbols
import numpy as np

tools=[
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "当你想要实现初等数学计算和初等函数计算的时候非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression":{
                        "type": "string",
                        "description": "数学计算的表达式，包括加减乘除、乘方、根号、指数对数和三角函数，如1*2+3-sin(pi)",
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mathmatics_analyser",
            "description": "当你想要实现极限导数积分计算的时候非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression":{
                        "type": "string",
                        "description": "包含自变量的数学表达式，如x**2、exp(x)等等",
                    },
                    "variables":{
                        "type": "string",
                        "description": "表达式里涉及的自变量，如x，a等等",
                    },
                    "operation":{
                        "type": "string",
                        "description": "需要对表达式进行的操作，'integrate' 'limit' or 'diff'",
                    }
                },
                "required": ["expression","varibles","operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "matrix_calculator",
            "description": "当你想要实现矩阵计算的时候非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "first_matrix":{
                        "type": "string",
                        "description": "numpy矩阵,例如 [[1,2],[3,4]]",
                    },
                    "second_matrix":{
                        "type": "string",
                        "description": "numpy矩阵，但如果用户的输入里没有涉及第二个矩阵，就填入‘None’",
                    },
                    "operation":{
                        "type": "string",
                        "description": "需要对矩阵进行的操作，求逆'inv' 求行列式'determinant' or 两个矩阵相乘'dot'",
                    }
                },
                "required": ["first_matrix","operation"]
            }
        }
    }
]

def calculate(expression: str) -> str:
    # 定义允许的函数和符号白名单
    allowed_functions = {
        'sin', 'cos', 'tan', 'sqrt', 'log', 'exp', 'pi', 'E','+', '-', '*', '/', '^', '**', '(', ')'
    }

    try:
        # 使用 parse_expr 解析表达式，并禁用局部变量
        expr = parse_expr(
            expression,
            evaluate=False,  # 禁止直接求值（防止执行代码）
            local_dict={},  # 禁用局部变量
            transformations='all'  # 禁用隐式乘法等高级解析
        )

        # 检查表达式中的符号和函数是否在白名单内
        for atom in expr.atoms():
            if isinstance(atom, Symbol):
                func_name = str(atom)
                if func_name not in allowed_functions:
                    return f"错误：检测到未授权的函数或变量 '{func_name}'"

        # 安全求值（数值计算）
        result = sympify(expr).evalf()
        return f"计算结果：{result}"

    except SympifyError:
        return "表达式解析失败，请检查输入格式。"
    except Exception as e:
        return f"计算错误：{str(e)}"

def calculus(expr_str: str, operation: str, var: str):
    """积分/极限/导数计算"""
    try:
        x = symbols(var)
        expr = parse_expr(expr_str)

        if operation == "integrate":
            res= integrate(expr, (x, 0, oo))  #定积分，默认求0到正无穷

        elif operation == "limit":
            res= limit(expr, x, 0)  #默认求x→0的极限

        elif operation == "diff":
            res= diff(expr, x)  #求导数
        return f"计算结果：{res}"

    except SympifyError:
        return "表达式解析失败，请检查输入格式。"
    except Exception as e:
        return f"计算错误：{str(e)}"

def matrix_operation(matrixf: str, operation: str, matrixs=None ):
    try:
        matrix_1 = np.array(eval(matrixf), dtype=float)
        if operation in ["dot", "inv", "determinant"]:
            if operation == "inv":
                res = np.linalg.inv(matrix_1)
            elif operation == "determinant":
                res = np.linalg.det(matrix_1)
            elif operation == "dot":
                matrix_2 = np.array(eval(matrixs), dtype=float)
                res = matrix_1 @ matrix_2
            return f"计算结果:{res}"
        else:
            return "不支持的操作"
    except Exception as e:
        return f"矩阵运算错误：{str(e)}"

def get_response(messages):
    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_key}'}
    body = {
        'model': 'qwen-turbo',
        "input": {
            "messages": messages
        },
        "parameters": {
            "result_format": "message",
            "tools": tools
        }
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

def call_with_messages():
    messages = [
        {
            "content": input('请输入您的问题：'),
            "role": "user"
        }
    ]
    first_response = get_response(messages)
    print(first_response)
    assistant_output = first_response['output']['choices'][0]['message']
    messages.append(assistant_output)

    if 'tool_calls' not in assistant_output:
        print(f"最终回复：{assistant_output['content']}")
        return

    elif 'tool_calls' in assistant_output:
        tool_call = assistant_output['tool_calls'][0]
        if tool_call['function']['name'] == 'calculator':
            args = json.loads(tool_call['function']['arguments'])
            expression = args.get('expression')
            cal_result = calculate(expression)
            tool_info = {
                "name": "calculator",
                "role": "tool",
                "content": cal_result
            }
            messages.append(tool_info)
            user_prompt = {'content': "你是个数学家，有强大的计算能力，现在请结合工具给出的信息，回答user之前的提问，无需再次调用工具。",
                       'role': 'system'}

        elif tool_call['function']['name'] == 'mathmatics_analyser':
            args = json.loads(tool_call['function']['arguments'])
            expression = args.get('expression')
            variables = args.get('variables')
            operation = args.get('operation')
            cal_result =calculus(expression, operation, variables)
            tool_info = {
                "name": "mathmatics_analyser",
                "role": "tool",
                "content": cal_result
            }
            messages.append(tool_info)
            user_prompt = {'content': "你是数学分析专家，有强大的数学分析专业素养与能力，现在请结合工具给出的信息，回答user之前的提问，无需再次调用工具。",
                       'role': 'system'}

        elif tool_call['function']['name'] == 'matrix_calculator':
            args = json.loads(tool_call['function']['arguments'])
            first_matrix = args.get('first_matrix')
            second_matrix = args.get('second_matrix')
            operation = args.get('operation')
            print(operation)
            cal_result = matrix_operation(first_matrix,operation,second_matrix)
            tool_info = {
                "name": "matrix_calculator",
                "role": "tool",
                "content": cal_result
            }
            print(tool_info)
            messages.append(tool_info)
            user_prompt = {'content': "你是高等代数专家，你有强大的计算能力和专业素养，可以结合工具给出的信息，回答user之前的提问，无需再次调用工具",
                'role': 'system'}
        messages.append(user_prompt)
        second_response = get_response(messages)
        print(f"最终回复：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()