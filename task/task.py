import os
import sys
import datetime
import re
sys.path.append("..") 
class TaskManager:
    def __init__(self) -> None:
        self.task_list = []
        self.now_task_id = 0

    def read_all_task_status(self):
        for task in self.task_list:
            print(task.id," ", task.content," ",task.status)

    def whether_all_task_done(self):
        for task in self.task_list:
            if task.status == 0:
                return False
        return True

class Task:
    def __init__(self) -> None:
        self.status = 0 #0表示未完成，1表示完成
        self.content = ''
        self.id = None
        self.memory = ""  #存储每个task中的记忆信息
        self.result = ""  #存储每个task的结果


def form_task(subtask_list,task_manager):
    subtask_list = re.split(r'\d+\.\s*', subtask_list)[1:]  # [1:] 是为了去掉第一个空字符串
    subtask_list = [step.strip('。.\n') for step in subtask_list]
    for i in range(len(subtask_list)):
        task = Task()
        task.content = subtask_list[i]
        task.id = i
        task.status = 0
        task_manager.task_list.append(task)