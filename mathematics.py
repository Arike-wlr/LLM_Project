import os
import requests
from dotenv import load_dotenv
import json
from sympy import parse_expr, sympify, SympifyError
from sympy.core.symbol import Symbol

tools=[
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "当你想要实现数学计算的时候非常有用。",
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
                "content": json.dumps(cal_result)
            }
            print(tool_info)
            messages.append(tool_info)
            user_prompt = {'content': "你是个数学家，有着分析和计算能力，现在请结合工具给出的信息，回答user之前的提问，无需再次调用工具。",
                       'role': 'system'}
            messages.append(user_prompt)
            second_response = get_response(messages)
            print(f"最终回复：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()