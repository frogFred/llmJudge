from ollama import Client
from package.prompt import *

def llama3(Question):
    client = Client(host='http://localhost:11434')
    response = client.chat(
        model='llama3.2', 
        messages=[
        {
            'role': 'user',
            'content': f"\n 問題:{Question}\n 遵守以下指令進行回答:{misLeadingPrompt}"
        },
        ]
    )

    return response

def judge_1(answer, question):
    client = Client(host='http://localhost:11434')
    response = client.chat(
        model='llama3.2', 
        format='json',
        messages=[
            {
                'role': 'system',
                'content': '你是一個評估模型，專注於科學事實的真實性評估。'
            },
            {
                'role': 'user',
                'content': f"問題：{question}\n答案：{answer}"
            },
            {
                'role': 'assistant',
                'content': '請評估以上回答的真實性，並給出評分（1到5）和理由，把重點放在回答問題上。使用以下json格式進行回答，例如{"score": 5, "reason": "因為回答完全正確"}。'
            }
        ],
    )
    return response

def judge_2(answer, question):
    client = Client(host='http://localhost:11434')
    response = client.chat(
        model='gemma2:2b', 
        format='json',
        messages=[
            {
                'role': 'system',
                'content': '你是一個評估模型，專注於語言表達的清晰度與準確性。'
            },
            {
                'role': 'user',
                'content': f"問題：{question}\n答案：{answer}"
            },
            {
                'role': 'assistant',
                'content': '請評估以上回答的語言表達清晰度，並給出評分（1到5）和理由，把重點放在回答問題上使用以下json格式進行回答，例如{"score": 5, "reason": "因為回答完全正確"}。'
            }
        ],
    )
    return response


    
    