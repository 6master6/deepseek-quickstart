import os
from openai import OpenAI


# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="ollama",
    base_url="http://49.51.197.197:11434/v1",  
)


response = client.chat.completions.create(
        model="deepseek-r1:1.5b",
        messages=[{'role': 'user', 'content':  '9.9 和 9.11 谁大'}]
        
    )

print(" 最终答案：")
print(response.choices[0].message.content)
