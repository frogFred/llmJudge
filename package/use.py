from ollama import Client
from package.prompt import *

def llama3(Question):
    client = Client(host='http://localhost:11434')
    response = client.chat(
        model='llama3.2', 
        messages=[
        {
            'role': 'user',
            'content': f"參考資料:{data}\n 問題:{Question}\n 遵守以下指令:{misLeadingPrompt}"
        },
        ],
        temperature = 0,
    )

    return response