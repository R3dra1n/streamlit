from openai import OpenAI
from pydantic import BaseModel
import json
import streamlit as st
import os
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
# 标题和描述
st.title("Hello, this is 断句 test")
st.write("Try 断句 with openai api")

# 输入框
user_input = st.text_input("Enter Your AD:")

client = OpenAI()

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

if st.button("Submit"):
    for i in range(len(output_json.get("output"))):

        


        st.write(f"{output_json.get("output")[i]}")
