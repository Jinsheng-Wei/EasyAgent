import os
import sys
sys.path.append("..") 
from function_call.tool_define import tools,tool_call



def get_tools_description(tools):
    tools_description=''
    for i in tools:
        """{'name_for_human': '谷歌搜索',
        'name_for_model': 'google_search',
        'description_for_model': '谷歌搜索是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。'},"""
        tools_description+='\n'+i['name_for_model']+':'+i['description_for_model']
    tools_description+='\n'
    return tools_description


if __name__=='__main__':
    tools_description = get_tools_description(tools)
    print(tools_description)