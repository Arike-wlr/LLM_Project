import os
import json
import requests
from dotenv import load_dotenv

tools=[
{
        "type":"function",
        "function":{
            "name":"analyse_movies",
            "description":"当你想要分析某一部电影或综合比较分析几部电影的基本信息的时候非常有用。",
            "parameters":{
                "type":"object",
                "properties": {
                    "movies_name":{
                        "type":"list",
                        "description":"列表元素为一个或多个电影的名称，如肖申克的救赎、霸王别姬等，每个名称为一个电影。若用户的输入中没有提到电影名称，就填入None"
                    }
                }
            },
            "required":["movies_name"]
        }
    },
    {
        "type":"function",
        "function":{
            "name":"analyse_movies'short_comments",
            "description":"当你想要了解一部电影的影评或综合分析比较几部电影的影评的时候非常有用",
            "parameters":{
                "type":"object",
                "properties": {
                    "movies_name":{
                        "type":"list",
                        "description":"列表元素为一个或多个电影的名称，如肖申克的救赎、霸王别姬等，每个名称为一个电影。"
                    }
                }
            },
            "required":["movies_name"]
        }
    }
]

def get_movies(movies_name):
    with open("movies.json","r",encoding="utf-8") as f:
        info = json.load(f)
    if movies_name is None:
        return info

    else:
        movieinfo=[]
        for key, information in info.items():
            for name in movies_name:
                if name in information["name"]:
                    movieinfo.append(information)
        return movieinfo

def get_short_comments(movies_name):
    comments = []
    for i in range(0,30,3):
        with open(f"short_comments/comments{i + 1}.json", "r", encoding="utf-8") as f:
            info0 = json.load(f)
        for movie_name in movies_name:
            if movie_name in info0["comment1"]["movie_name"]:
                with open(f"short_comments/comments{i+2}.json", "r", encoding="utf-8") as f:
                    info1 = json.load(f)
                with open(f"short_comments/comments{i+3}.json", "r", encoding="utf-8") as f:
                    info2 = json.load(f)
                comments.append( str(info0) + str(info1) + str(info2))
    return comments


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
        """不需要其它工具的情况，直接回复"""
        print(f"最终回复：{assistant_output['content']}")
        return

    elif assistant_output['tool_calls'][0]['function']['name'] == 'analyse_movies':
        tool_info = {"name": "analyse_movies", "role": "tool"}
        movie_name=json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['movie_name']
        tool_info['content'] = str(get_movies(movie_name))
        messages.append(tool_info)
        user_prompt={'content':"你对电影有着深入的了解和深刻的见解，现在请结合电影信息，回答user之前的提问,无需再次调用工具。",'role':'system'}
        messages.append(user_prompt)

        second_response = get_response(messages)
        #print(second_response)
        print(f"最终回复：{second_response['output']['choices'][0]['message']['content']}")

    elif assistant_output['tool_calls'][0]['function']['name'] == "analyse_movies'short_comments":
        tool_info = {"name": "analyse_short_comments", "role": "tool"}
        movies_name=json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['movies_name']
        tool_info['content'] = str(get_short_comments(movies_name))
        messages.append(tool_info)
        user_prompt={'content':"你对电影的影评有着深刻的见解，现在请结合电影短评，回答user之前的提问,无需再次调用工具。",'role':'system'}
        messages.append(user_prompt)
        second_response = get_response(messages)
        print(f"最终回复：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()