import re
from function_call.functions import get_tools_description
from function_call.tool_define import tools,tool_call,task_decomposition
from prompt_template.prompt_termplate import init_prompt
from LLM import request_llm
from utils.utils import parse_action,parse_thought,parse_observation,parse_status
from react.react import react
from task.task import TaskManager,Task,form_task
def one_turn_function_call(question,tools_description,history):
    #调用LLM 进行初始回答以及工具选择
    user_input = question
    question = init_prompt.format(tools_description=tools_description, question_orgin=question)
    answer =request_llm(question)
    #解析回答的内容 thought和action
    thought = parse_thought(answer)
    action = parse_action(answer)
    print("调用的工具为:",action)
    history =history + "\nThought:"+thought + "\nAction:"+action
    
    action_answer = tool_call(user_input,thought,action,history)
    # print("action_answer",action_answer)
    #更具调用结果续写observation
    observation, status = react(action_answer,history)
    history = history + "\nObservation:"+observation+"\nSTATUS:"+status
    return observation,history,status

def update_task_status(task_manager,status,final_answer,memory):
    task_id =task_manager.now_task_id
    if status =="完成":
        #如果任务完成了，我需要把任务完成的结果作为下一个任务的输入（对记忆进行修改）
        task_manager.task_list[task_id].status ==1
        task_manager.task_list[task_id].result = final_answer
        if task_manager.now_task_id +1 >= len(task_manager.task_list):
            print("All task done")
            return "DONE"
        else:
            task_manager.now_task_id +=1
        task_content = task_manager.task_list[task_manager.now_task_id].content
        task_status_memory = "\n当前任务仍然已经完成，得到的结果是："+final_answer+",要执行的下一个任务是："+task_content
        task_manager.task_list[task_manager.now_task_id].memory = task_status_memory
    else:
        task_content = task_manager.task_list[task_manager.now_task_id].content
        task_status_memory = "\n当前任务仍然未完成，因此现在的任务任然是："+task_content
        memory = memory + task_status_memory
    return "NOT DONE"

if __name__=='__main__':
    tools_description=get_tools_description(tools)
    input = "先获得当前时间，再将其中所有数字加起来，结果是什么？(要求任务分解步骤尽可能少)"

    #任务分解 task decomposition
    subtask_list = task_decomposition(input)
    task_manager = TaskManager()
    form_task(subtask_list,task_manager)
    task_manager.read_all_task_status()
    
    step = 0
    while task_manager.whether_all_task_done()==False:
        print(f"第{step}轮开始------------------------------------")
        now_task = task_manager.task_list[task_manager.now_task_id].content
        print(f"当前任务为{now_task}")
        final_answer, task_manager.task_list[task_manager.now_task_id].memory, status= one_turn_function_call(\
                                                                    now_task,tools_description,
                                                                     task_manager.task_list[task_manager.now_task_id].memory)
        all_task_status = update_task_status(task_manager,status,final_answer,task_manager.task_list[task_manager.now_task_id].memory)
    
        print(f"得到的结果为{final_answer}")
        print(f"第{step}轮结束------------------------------------")        
        if all_task_status == "DONE":
            break

        step +=1

    print("All task done")
    