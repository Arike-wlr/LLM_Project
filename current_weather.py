import current_weather_3_ans as cw3a

def call_with_messages():
    """输入prompt，并调取大模型获得精简版最终回复
    其中将三轮调取简化为两轮"""
    messages = [
        {
            "content": input('请输入您的问题：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
            "role": "user"
        }
    ]

    #第一轮调用，与之前相同，需让大模型判断是否需要使用工具。
    first_response = cw3a.get_response(messages)
    assistant_output = first_response['output']['choices'][0]['message']
    messages.append(assistant_output)

    if 'tool_calls' not in assistant_output:
        print(f"回复：{assistant_output['content']}")
        return

    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
        tool_info = {"name": "get_current_weather", "role": "tool"}
        location = cw3a.json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
        tool_info['content'] = cw3a.get_weather_info(location)
        messages.append(tool_info)
        user_prompt={'content':"现在请结合当地当前的天气状况，回答user之前的提问,可适当给出可行的建议",'role':'user'}
        messages.append(user_prompt)

    elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
        tool_info = {"name": "get_current_time", "role": "tool"}
        tool_info['content'] = cw3a.get_current_time()
        messages.append(tool_info)

    #第二轮调用时大模型已经可以根据工具的内容有所输出，可将第三轮调用的prompt在第二轮调用时提前传入
    second_response = cw3a.get_response(messages)
    print(f"最终回复：{second_response['output']['choices'][0]['message']['content']}")

if __name__ == '__main__':
    call_with_messages()