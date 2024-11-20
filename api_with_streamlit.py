from openai import OpenAI
from pydantic import BaseModel
import json
import streamlit as st
import os
import requests

def kunwu_api(api, content):
    # api = "openapi-JbYj1Z2V0JqI2WZl7Nqgdtm6YTKsxRN5mvlih40gqyw7btkEIDO1"
    # content = "杯子是一种专门盛水的器皿。其主要功能都是用来饮酒或饮茶，一般容积不大。或在古代喝"



    # 定义 API URL
    url = "https://ai.adlawai.cn/api/v1/chat/completions"

    # 定义请求头（例如包含API密钥）
    headers = {
        "Authorization": f"Bearer {api}",  # 替换为你的实际 API 密钥
        "Content-Type": "application/json"       # 指定数据格式
    }

    # 示例GET请求
    # def make_get_request():
    #     try:
    #         response = requests.get(url, headers=headers, params={"param1": "value1", "param2": "value2"})
    #         # 检查响应状态
    #         if response.status_code == 200:
    #             print("GET请求成功！")
    #             print("响应数据:", response.json())  # 返回JSON格式的响应内容
    #         else:
    #             print(f"请求失败，状态码: {response.status_code}")
    #     except Exception as e:
    #         print(f"GET请求出错: {e}")

    # 示例POST请求
    
    data = {
        "chatId": "111",
        "stream": False,
        "detail": False,
        # "variables": {
                # "target": "保健食品",
            # },
        "messages": [
        {
        "role": "user",
        "content": f'{content} '
        }
        ]
    }
    # 发送JSON格式的数据
    # 打印出响应状态和内容，便于调试
    response = requests.post(url, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Content:",response.json())
    # print("Response Text:", response.text)  # 打印原始文本内容
    if response.status_code == 200 or response.status_code == 201:
        # print("POST请求成功！")
        return( response.json().get("choices", [])[0].get("message", {}).get("content", "" ))
    else:
        return(f"请求失败，状态码: {response.status_code}")

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
# 标题和描述
st.title("Hello, this is 断句 test")
st.write("Try 断句 with openai api")

# 输入框
user_input = st.text_input("Enter Your AD:")
api = st.text_input("Enter Your KunWu API:")

client = OpenAI()


# 下拉菜单
choice = st.selectbox("选择您产品的领域:", ["普通食品", "酒类", "保健食品", "一般产品"])
st.write(f"You chose: {choice}")
if choice == "普通食品":
    st.write("会执行A、B、C模块")

elif choice == "酒类":
    st.write("会执行B、C模块")

elif choice == "保健食品":
    st.write("会执行C模块")

else :
    st.write("会执行D模块")

class Sentence(BaseModel):    
    number: int
    sentence: str
    


class Sentences(BaseModel):
    output: list[Sentence]


completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "将以下文本进行分句，每个句子自然流畅，按句意完整地切分. reponse in JSON format"},
        {"role": "user", "content": f"{user_input}"}
    ],
    response_format=Sentences,
)

math_reasoning = completion.choices[0].message.parsed
output=math_reasoning.model_dump_json()
output_json= json.loads(output)

print(len(output_json.get("output")))


data=[ ]

print(len(output_json.get("output")))
# for i in range(len(output_json.get("output"))):
#     data.append(output_json.get("output")[i])


if st.button("Submit"):
    st.write("——【这是断句结果】——")
    for i in range(len(output_json.get("output"))):
        data.append(output_json.get("output")[i])
    # for i in range(len(output_json.get("output"))):

# print(data)      


        st.write(f"{output_json.get("output")[i]}")

#  ------------------上面是断句,下面是单个句子进行审核----------------------

# 存储 API 返回结果
results = []

# 逐条发送 sentence 内容到 API
for item in data:
    sentence = item['sentence']
    try:
        # 调用 OpenAI API
    #     response = client.chat.completions.create(
    # model="gpt-4o",
    # messages=[
    #     {"role": "system", "content": "翻译成英文"},
    #     {"role": "user", "content": sentence}
    # ])
        result = kunwu_api(api, sentence)
        # 获取 API 的返回内容
       
        # result = response.choices[0].message.content
        
        # 将结果保存到列表
        results.append({'number': item['number'], 'input': sentence, 'output': result})
    except Exception as e:
        print(f"Error processing sentence {item['number']}: {e}")

# 打印所有结果
st.write("——【这是单个句子逐个结果】——")
for res in results:
    st.write(f"Number: {res['number']}")
    st.write(f"Input: {res['input']}")
    st.write(f"Output: {res['output']}")
    st.write("-" * 20)



