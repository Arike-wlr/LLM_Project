import requests
import os
from datetime import datetime
import json
from dotenv import load_dotenv

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # parameter,意为：参数
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {  # 查询天气时需要提供位置，因此参数设置为location
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
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
    """通过天气软件的api获取当前指定城市的天气情况和气温"""
    try:
        load_dotenv()
        params = {
            "key":os.getenv("WEATHER_API_KEY"),
            "location": location,
            "language": "zh-Hans",
            "unit": "c"
        }
        url = "https://api.seniverse.com/v3/weather/now.json"
        r = requests.get(url, params=params)
        now_data = r.json()["results"][0]['now']
        weather_text = now_data["text"]
        temperature = now_data["temperature"]
        message = (
            f"{location}当前天气：{weather_text}，"
            f"温度 {temperature}°C，"
        )
        return message

    except requests.exceptions.RequestException as e:
        return f"天气查询失败：{str(e)}"

    except (KeyError, IndexError) as e:
        return "天气数据解析错误，请检查API响应格式。"

def get_current_time():
    """获取当前的时间"""
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return f"当前时间：{formatted_time}。"

def get_response(messages):
    """调用大模型获得回复"""
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
    """输入prompt，并三轮调取大模型获得最终回复"""
    messages = [
        {
            "content": input('请输入您的问题：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
            "role": "user"
        }
    ]

    #第一轮调用
    first_response = get_response(messages)
    print(f"\n第一轮调用结果：{first_response}")
    assistant_output = first_response['output']['choices'][0]['message']
    messages.append(assistant_output)

    #分析第一轮的调用结果，判断是否需要外部工具
    if 'tool_calls' not in assistant_output:
        """不需要其它工具的情况，直接回复"""
        print(f"回复：{assistant_output['content']}")
        return

    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
        """获取天气需要三轮调取"""
        tool_info = {"name": "get_current_weather", "role": "tool"}
        location = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
        print(
            f"工具输出信息：{location}{str(datetime.now())[0:10]}的天气是什么？"
        )#提取了城市和日期（当前日期）信息

        #搭建第二轮调用的message
        tool_info['content'] = get_weather_info(location)
        messages.append(tool_info)

        #进行第二轮调用
        second_response = get_response(messages)
        print(f"第二轮调用结果：{second_response}")
        print(f"结合专业天气数据的答案：{tool_info['content']}")

        #搭建第三轮调用的message
        third_quary = {
            'content': f'现在请结合当地当前的天气状况，回答user的提问，可根据天气状况适当给出可行的建议：{second_response['output']['choices'][0]['message']['content']}',
            'role': 'system'}
        messages.append(third_quary)

        #进行第三轮调用
        third_response = get_response(messages)
        print(f"第三轮调用结果：{third_response}")
        print(f"最终答案：{third_response['output']['choices'][0]['message']['content']}")

    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
        """获取时间两轮就可以结束了"""
        #搭建第二轮调用的message
        tool_info = {"name": "get_current_time", "role": "tool"}
        tool_info['content'] = get_current_time()
        print(f"工具输出信息：{tool_info['content']}")
        messages.append(tool_info)

        #进行第二轮调用
        second_response = get_response(messages)
        print(f"第二轮调用结果：{second_response}")
        print(f"最终答案：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()