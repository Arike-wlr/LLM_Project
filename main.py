import current_weather_3_ans
import analyse_movie
import finance_analyse
import mathematics
import os
import requests
from dotenv import load_dotenv

tools=[current_weather_3_ans.tools[0],
       current_weather_3_ans.tools[1],
       analyse_movie.tools[0],
       analyse_movie.tools[1],
       finance_analyse.tools[0],
       mathematics.tools[0],
       mathematics.tools[1],
       mathematics.tools[2]
]
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
            "content": input('请输入您的问题：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
            "role": "user"
        }
    ]

    first_response = get_response(messages)
    assistant_output = first_response['output']['choices'][0]['message']
    messages.append(assistant_output)

    if 'tool_calls' not in assistant_output:
        """不需要其它工具的情况，直接回复"""
        print(f"回复：{assistant_output['content']}")
        return

    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
        tool_info = {"name": "get_current_weather", "role": "tool"}
        location = current_weather_3_ans.json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
        tool_info['content'] = current_weather_3_ans.get_weather_info(location)
        messages.append(tool_info)
        user_prompt={'content':"你是一个天气方面的专家，现在请结合当地当前的天气状况，回答user之前的提问,可适当给出可行的建议，无需再次调用工具。",'role':'system'}

    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
        tool_info = {"name": "get_current_time", "role": "tool", 'content': current_weather_3_ans.get_current_time()}
        messages.append(tool_info)
        user_prompt={'content':"请根据工具输出回答user之前的提问",'role':'system'}

    elif assistant_output['tool_calls'][0]['function']['name'] == 'analyse_movies':
        tool_info = {"name": "analyse_movies", "role": "tool"}
        movie_name=analyse_movie.json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['movie_name']
        tool_info['content'] = str(analyse_movie.get_movies(movie_name))
        messages.append(tool_info)
        user_prompt={'content':"你对电影有着深入的了解和深刻的见解，现在请结合电影信息，回答user之前的提问,无需再次调用工具。",'role':'system'}

    elif assistant_output['tool_calls'][0]['function']['name'] == "analyse_movies'short_comments":
        tool_info = {"name": "analyse_short_comments", "role": "tool"}
        movie_name=analyse_movie.json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['movie_name']
        tool_info['content'] = str(analyse_movie.get_short_comments(movie_name))
        messages.append(tool_info)
        user_prompt={'content':"你对电影的影评有着深刻的见解，现在请结合电影短评，回答user之前的提问,无需再次调用工具。",'role':'system'}

    elif 'tool_calls' in assistant_output:
        tool_call = assistant_output['tool_calls'][0]
        if tool_call['function']['name'] == 'analyse_stocks':
            args = finance_analyse.json.loads(tool_call['function']['arguments'])
            symbol = args.get('symbol', 'IBM')
            date = args.get('date')
            stock_data = finance_analyse.get_stock_info(symbol=symbol, date=date)
            tool_info = {
                "name": "analyse_stocks",
                "role": "tool",
                "content": finance_analyse.json.dumps(stock_data)
            }
            messages.append(tool_info)
            user_prompt = {
                'content': "你是个金融和股票方面的专家，有着强大的股票分析能力，现在请结合股票信息，回答user之前的提问，无需再次调用工具。",
                'role': 'system'}

        elif tool_call['function']['name'] =='calculator':
            args = mathematics.json.loads(tool_call['function']['arguments'])
            expression = args.get('expression')
            cal_result = mathematics.calculate(expression)
            tool_info = {
                "name": "calculator",
                "role": "tool",
                "content":cal_result
            }
            messages.append(tool_info)
            user_prompt = {'content': "你是个数学家，有强大的计算能力，现在请结合工具给出的信息，回答user之前的提问，无需再次调用工具。",
                       'role': 'system'}

        elif tool_call['function']['name'] == 'mathmatics_analyser':
            args = mathematics.json.loads(tool_call['function']['arguments'])
            expression = args.get('expression')
            variables = args.get('variables')
            operation = args.get('operation')
            cal_result =mathematics.calculus(expression, operation, variables)
            tool_info = {
                "name": "mathmatics_analyser",
                "role": "tool",
                "content": cal_result
            }
            messages.append(tool_info)
            user_prompt = {'content': "你是数学分析学科的专家，有强大的数学分析专业素养与能力，现在请结合工具给出的信息，回答user之前的提问，无需再次调用工具。",
                       'role': 'system'}

        elif tool_call['function']['name'] == 'matrix_calculator':
            args = mathematics.json.loads(tool_call['function']['arguments'])
            first_matrix = args.get('first_matrix')
            second_matrix = args.get('second_matrix')
            operation = args.get('operation')
            cal_result = mathematics.matrix_operation(first_matrix, operation,second_matrix )
            tool_info = {
                "name": "matrix_calculator",
                "role": "tool",
                "content": cal_result
            }
            messages.append(tool_info)
            user_prompt = {'content': "你是高等代数专家，有强大的矩阵运算能力和专业素养，可以结合工具给出的信息，回答user之前的提问，无需再次调用工具",
                'role': 'system'}
    messages.append(user_prompt)
    second_response = get_response(messages)
    print(f"最终回复：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()