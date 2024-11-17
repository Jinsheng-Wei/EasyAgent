import re
from function_call.functions import get_tools_description
from function_call.tool_define import tools,tool_call,task_decomposition
from prompt_template.prompt_termplate import init_prompt
from LLM import request_llm
from utils.utils import parse_action,parse_thought
from react.react import react
def one_turn_function_call(question,tools_description,history):
    #调用LLM 进行初始回答以及工具选择
    user_input = question
    question = init_prompt.format(tools_description=tools_description, question_orgin=question)
    answer =request_llm(question)
    #解析回答的内容 thought和action
    thought = parse_thought(answer)
    action = parse_action(answer)
    history =history + "\nThought:"+thought + "\nAction:"+action
    
    action_answer = tool_call(user_input,thought,action)
    # print("action_answer",action_answer)
    #更具调用结果续写observation
    observation, status = react(action_answer,history)
    history = history + "\nObservation:"+observation+"\nSTATUS:"+status
    return observation,history,status



if __name__=='__main__':
    tools_description=get_tools_description(tools)
    input = "先获得当前时间，再计算100乘以100？"

    #任务分解 task decomposition
    subtask_list = task_decomposition(input)
    print("subtask_list",subtask_list)

    # i=0
    # memory_history= "Question:"+input
    # while i<=3:
    #     i+=1
    #     final_answer, memory_history, status= one_turn_function_call(input,tools_description,memory_history)
    #     print(f"第{i}轮任务执行完毕")
    #     print(final_answer+"\n")
    #     print(memory_history)
    #     if status =='完成':
    #         break