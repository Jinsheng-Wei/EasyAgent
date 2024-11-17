

'''
react mainly used to get the observation and check the task situation

'''

import os
import sys
sys.path.append("..") 
from prompt_template.prompt_termplate import observation_prompt
from LLM import request_llm
from utils.utils import parse_action,parse_thought,parse_observation,parse_status

def react(action_answer,history):
    obs_prompt = observation_prompt.format(memory_history=history,action_answer=action_answer)
    answer = request_llm(obs_prompt)
    observation = parse_observation(answer)
    status = parse_status(answer)
    return observation,status