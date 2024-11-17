
import os
import sys
import datetime
sys.path.append("..") 
from LLM import request_llm
#tools : list of dict   用来定义工具的名称、描述、参数等信息
from prompt_template.prompt_termplate import task_decomposition_prompt
from function_call.bing_search import query_bing
tools = [
        {
            'name_for_human': '谷歌搜索',
            'name_for_model': 'google_search',
            'description_for_model': '谷歌搜索是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。',
            'parameters': [
                {
                    'name': 'search_query',
                    'description': '搜索关键词或短语',
                    'required': True,
                    'schema': {'type': 'string'},
                }
            ]
        },
        {
            'name_for_human': '计算器',
            'name_for_model': 'calculator',
            'description_for_model': '进行加减乘除运算',
        },
        {
            'name_for_human': '日历',
            'name_for_model': 'calendar',
            'description_for_model': '获得当前年月日以及时间',
        },
        {
            'name_for_human': '距离计算器',
            'name_for_model': 'distance_calculation',
            'description_for_model': '可以根据目标单位和地图api查询的位置信息，计算出地图上所有其他单位与目标单位的距离',
            'parameters': [
                {
                    'target_and_mapdict': ( {'weapon_query':['x1','y1'],'unit2':['x2','y2'],'unit3':['x3','y3'],'unit4':['x4','y4']}),
                    'description': '包括目标单位在内的所有地图上单位的名称和位置参数:{被计算的单位名称:[该单位的x坐标,该单位的y坐标],被计算的另外一个单位名称:[该单位的x坐标,该单位的y坐标],地图上的其他单位名称(可省略):[该单位的x坐标,该单位的y坐标](可省略)}',
                    'required': True,
                    'schema': {'type': 'string'},
                }
            ],
        },
    ]


def tool_call(question,thought,tool_name):
    print("tool_name",tool_name)
    if tool_name == '计算器' or tool_name == 'calculator':
        #用LLM或者其他模型将数学式子转换为计算式
        question = f"原始问题是：{question} 当前的Thought是：{thought}\n请帮我将该问题转换为数学表达式，以方便我调用本地的计算工具进行计算。要求回复只包括数学表达式，不包括其他内容。"
        expression = request_llm(question)
        print("expression",expression)
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return f"计算错误: {e}"
    elif tool_name == '谷歌搜索' or tool_name == 'google_search':
        response = query_bing(question)
        print("in tool loop!!!!!!!!!!!!!!!!!!!\n","question",question)
        print("\nresponse",response)
        return response
    elif tool_name == '日历' or tool_name == 'calendar':
        #用LLM或者其他模型获取当前时间
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       
        return current_time

def task_decomposition(question):
    question = task_decomposition_prompt.format(question_orgin=question)
    return request_llm(question)