import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)



# 非流式响应
def gpt(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-3.5-turbo-ca", messages=messages)
    # print(completion.choices[0].message.content)
    response = completion.choices[0].message.content
    return response

def gpt_tream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = client.chat.completions.create(
        # model='o1-preview-ca',
        model='gpt-3.5-turbo-ca',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

def request_llm(question):
    messages = [{'role': 'user','content': question },]
    return gpt(messages)


if __name__ == '__main__':
    # with open('prompt.yaml', 'r', encoding='utf-8') as file:
    #     yaml_text = file.read()
    prompt = "What is the capital of France?"
    messages = [{'role': 'user','content': prompt },]

    # 非流式调用
    gpt(messages)
    # 流式调用
    # gpt_35_api_stream(messages)