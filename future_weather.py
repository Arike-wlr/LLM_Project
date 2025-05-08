import requests
import os
from datetime import datetime
import json
from dotenv import load_dotenv

"""免费版可以调取未来三天的天气情况，有时间尝试一下，就直接给出精简版的了"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "当你想查询指定城市指定未来时间的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    },
                    "date":{
                        "type": "string",
                        "description": '格式包括“今天”、“明天”、“昨天”、"1⽉2号"、"1⽉2⽇"、"2023年1⽉2号","2023年1⽉2⽇" 等'
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    }
]

def get_weather_info(location):
    try:
        load_dotenv()
        params = {
            "key":os.getenv("WEATHER_API_KEY"),
            "location": location,
            "language": "zh-Hans",
            "unit": "c",
            "start":"0",
            "day":"5"
        }
        url = "https://api.seniverse.com/v3/weather/daily.json"
        r = requests.get(url, params=params)
        r.raise_for_status()
        now_data = r.json()["results"][0]['now']
        weather_text = now_data["text"]
        temperature = now_data["temperature"]
        message = (

        )
        return message
    except requests.exceptions.RequestException as e:
        return f"天气查询失败：{str(e)}"
    except (KeyError, IndexError) as e:
        return "天气数据解析错误，请检查API响应格式。"

def get_current_time():
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return f"当前时间：{formatted_time}。"

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
            "content": input('请输入：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
            "role": "user"
        }
    ]
    first_response = get_response(messages)
    print(f"\n第一轮调用结果：{first_response}")
    assistant_output = first_response['output']['choices'][0]['message']
    messages.append(assistant_output)
    if 'tool_calls' not in assistant_output:
        print(f"最终答案：{assistant_output['content']}")
        return
    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
        tool_info = {"name": "get_current_weather", "role": "tool"}
        location = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
        tool_info['content'] = get_weather_info(location)
    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
        tool_info = {"name": "get_current_time", "role": "tool"}
        tool_info['content'] = get_current_time()
    print(f"工具输出信息：{tool_info['content']}")
    messages.append(tool_info)
    second_response = get_response(messages)
    print(f"第二轮调用结果：{second_response}")
    print(f"结合专业天气数据的答案：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()