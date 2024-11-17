import re

def parse_action(answer):
    action_match = re.search(r'Action:\s*(.*)', answer)
    action = action_match.group(1).strip() if action_match else None
    return action

def parse_thought(answer):  
    thought_match = re.search(r'Thought:\s*(.*)', answer)
    thought = thought_match.group(1).strip() if thought_match else None
    return thought

def parse_observation(answer):
    observation_match = re.search(r'Observation:\s*(.*)', answer)
    observation = observation_match.group(1).strip() if observation_match else None
    return observation

def parse_status(answer):
    status_match = re.search(r'Status:\s*(.*)', answer)
    status = status_match.group(1).strip() if status_match else None
    return status