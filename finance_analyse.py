import os
import json
import requests
from dotenv import load_dotenv

tools=[
    {
        "type":"function",
        "function":{
            "name":"analyse_stocks",
            "description":"获取指定股票的金融信息。当你想要了解股票金融信息的时候非常有用。",
             "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "（必填）股票代码，例如AAPL、IBM、TSLA等。如果用户未提供，请提示用户输入。"
                },
                "date": {
                        "type": "string",
                        "description": "（可选）日期（格式：YYYY-MM-DD）。仅当用户明确指定日期时填写，否则留空。例如 2025-05-11",
                        "format": "date"
            }
        },
        "required": ["symbol"]
            }
        }
    }
]

def get_stock_info(symbol="IBM", date=None):
    load_dotenv()
    api_key = os.getenv("FINANCE_API_KEY")
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    time_series = data.get("Time Series (Daily)", {})

    if date is None:
        return data

    if date in time_series:
        return {
            "symbol": symbol,
            "date": date,
            "open": time_series[date]["1. open"],
            "high": time_series[date]["2. high"],
            "low": time_series[date]["3. low"],
            "close": time_series[date]["4. close"],
            "volume": time_series[date]["5. volume"]
        }
    else:
        return {
            "symbol": symbol,
            "date": date,
            "error": "未找到该日期的股票数据"
        }

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
    #print(first_response)
    assistant_output = first_response['output']['choices'][0]['message']
    messages.append(assistant_output)

    if 'tool_calls' not in assistant_output:
        print(f"最终回复：{assistant_output['content']}")
        return

    elif 'tool_calls' in assistant_output:
        tool_call = assistant_output['tool_calls'][0]
        if tool_call['function']['name'] == 'analyse_stocks':
            args = json.loads(tool_call['function']['arguments'])
            symbol = args.get('symbol', 'IBM')
            date = args.get('date')
            stock_data = get_stock_info(symbol=symbol, date=date)
            tool_info = {
                "name": "analyse_stocks",
                "role": "tool",
                "content": json.dumps(stock_data)
            }
            messages.append(tool_info)
            user_prompt = {'content': "你是个金融和股票方面的专家，有着强大的股票分析能力，现在请结合股票信息，回答user之前的提问，无需再次调用工具。",
                       'role': 'system'}
            messages.append(user_prompt)
            second_response = get_response(messages)
            #print(second_response)
            print(f"最终回复：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()