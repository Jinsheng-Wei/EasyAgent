import os
import sys
sys.path.append("..") 

#init_prompt is used to get action(which tool to use) according to the thought and question
init_prompt='''
请根据以下工具和工具描述:{tools_description},选择工具完成我的任务。
question:{question_orgin}
回复格式如下:
Thought:
Action:工具名称
'''

observation_prompt='''
执行链如下：
{memory_history}
执行完最后的action得到的结果是：{action_answer}，帮我续写Observation和Status，格式如下：
Observation:action执行的结果
Status:完成/未完成
'''


task_decomposition_prompt='''
请帮我把任务进行分解，我的任务是{question_orgin}
任务分解为:
1.
2.
'''



    