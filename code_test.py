
import re

if __name__=='__main__':
    input = "先获得当前时间，再将其中所有数字加起来，结果是什么？"

    # 任务分解 task decomposition

    # 原始字符串
    steps_str = '11. 获取当前时间.\n2. 将时间中的所有数字相加得出结果。'

    # 使用正则表达式按照 "数字." 分割字符串
    steps = re.split(r'\d+\.\s*', steps_str)[1:]  # [1:] 是为了去掉第一个空字符串
    print("steps", steps)

    steps = [step.strip('。.\n') for step in steps]

    print("steps", steps)

    # i=0
    # memory_history= "Question:"+input
    # while i<=3:
    #     i+=1
    #     final_answer, memory_history, status= one_turn_function_call(input,tools_description,memory_history)
    #     print(f"第{i}轮任务执行完毕")
    #     print(final_answer+"\n")
    #     print(memory_history)