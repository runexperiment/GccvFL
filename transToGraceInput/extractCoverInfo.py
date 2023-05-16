# -*- coding: utf-8 -*-

# 此文件在gcov命令生成覆盖信息后被调用，是用于存储覆盖信息的
import pickle
import re
import subprocess
from tqdm import tqdm
import os, sys
import Setting
import common
from pycparser import c_parser, c_ast

# 当前目录夹应该是在项目文件夹下
dev = Setting.dev["extractCoverInfo"]


def getFunInProblem(fileList,file):
    for f in fileList:
        if f['id'] == file:
            return True
    with open(" ", "rb") as f:
        problem = pickle.load(f)
    return False
def getinProblem(fileList,file):
    for i,f in enumerate(fileList):
        if f == file:
            return i
    fileList.append(file)

    return len(fileList)-1
def getProblemFile(problemName,pwd,fileName,inName,result,gcovFileName,errLines=[]):
    # 检查文件是否存在
    if os.path.exists(common.jointPath(['../','../',Setting.resultDir,  problemName+'.pkl'])):
        # 读取文件内容
        with open(common.jointPath(['../','../',Setting.resultDir,  problemName+'.pkl']), "rb") as f:
            problem = pickle.load(f)
    else:
        # 文件不存在，创建一个空列表
        problem = {
            'pwd':pwd,
            'id': problemName,
            'fileList':[],
            "inList": [],
            'fileId':[],
        }
    inListId = getinProblem(problem['inList'],inName) # 设置输入文件的Id
    lenFile = len(problem['fileId'])                  # 获取目前的代码文件数量
    fileId = getinProblem(problem['fileId'],fileName) # 设置代码文件的Id
    filelistLen = ...
    file = ...
    code = []
    maxi = []
    gcovInfo,functions = get_functions(maxi, code, common.jointPath([Setting.gcovDirName, gcovFileName]))

    if lenFile != len(problem['fileId']):  # 如果当前文件还没有存储在pkl文件里
        # 分解函数
        # functions = get_functions(maxi,code,common.jointPath([Setting.gcovDirName,gcovFileName]))
        functionList = []
        # 预处理function单元，也就是file的funcList
        parser = c_parser.CParser()
        for i,(funName,fun,fun_start,fun_end) in enumerate(functions):  # 对于每个函数
            (temp1,temp2,funname) = funName
            # print(pwd,'pwd',fileName)
            func={
                'pwd': common.jointPath([pwd,fileName]),
                'id': i,
                'startLine': fun_start,
                'endLine': fun_end,
                'name': funname,
            }
            # # 对于每个函数，开始对每个函数内语句类型进行判断
            # for j in range(fun_start,fun_end):
            #     methods = code[j]['code']+'\n'
            functionList.append(func)
        problem['fileList'].append({
            'id': fileId,
            "pwd": common.jointPath([pwd,fileName]),
            'result':[],
            'errLines': errLines,
            'lineId':code,
            'maxi':maxi,
            'funList':functionList,
            'codeList':code
        })
    filelistLen = len(problem['fileList'])
    # 将测试的结果放到res中
    file = problem['fileList'][filelistLen - 1]
    file['result'].append(result)

    for i,line in enumerate(file['maxi']):

        if '#' in gcovInfo[i]:
            line.append(0)
        elif '-' in gcovInfo[i]:
            line.append(0)
        else:
            line.append(1)
    # print(problem)

    # 在列表末尾添加一个字符串
    # print(problem)
    # 将数据写入文件
    with open(common.jointPath(['../','../',Setting.resultDir,problemName+'.pkl']), "wb") as f:
        pickle.dump(problem, f)
# 获取函数名  可用
def getFuncName(File):
    # 读取代码文件
    with open(File, 'r') as f:
        code = f.read()
    # print(code)
    # 正则表达式匹配所有的函数
    pattern = r'\w+\s+\w+\s*\([^)]*\)\s*{'
    functions = re.findall(pattern, code)

    # 输出所有函数名
    # for function in functions:
    #     print(function.split('(')[0])
    #     print("\n")

# 用于获取所有函数体内的函数调用、if等带括号的情况。
def getFun(fileName):
    with open(fileName, 'r') as f:
        content = f.readlines()
    pattern = r'^\s*(?P<symbol>[#:\-\d]*)\s*(?P<function>\w+)\s*\('
    # print("content = ",content,"]]]]]")
    for line in content:
        match = re.match(pattern, line)
        print(match)
        if match:
            print(match.group('symbol'), match.group('function'))
        print('\n')
def getLineType(code_line):
    if re.match(r'.* if\s*\(.+\)\s*$', code_line):
        return 'IfStatement'
    elif re.match(r'^\s*while\s*\(.+\)\s*$', code_line):
        return 'WhileStatement'
    elif re.match(r'^\s*switch\s*\(.+\)\s*$', code_line):
        return 'switchStatement'
    elif re.match(r'^\s*return\s+.+\s*$', code_line):
        return 'ReturnStatement'
    elif re.match(r'^\s*struct\s+\w+\s*{\s*$', code_line):
        return 'ConstructorDeclaration'
    elif re.match(r'^\s*break\s*;\s*$', code_line):
        return 'BreakStatement'
    elif re.match(r'^\s*continue\s*;\s*$', code_line):
        return 'ContinueStatement'
    elif re.match(r'^.*=.*;.*$', code_line):
        return 'StatementExpression'
    elif re.match(r'^.*\(.*\).*$', code_line):
        return 'funCall'
    elif re.match(r'^.* .*\s*;$', code_line):
        return 'LocalVariableDeclaration'
    else:
        return 'others'

# # 定义一个递归遍历AST节点并打印节点类型和位置信息的函数
# def print_node_type_and_location(node):
#     # 如果节点是c_ast.Node对象（所有节点都是）
#     if isinstance(node, c_ast.Node):
#         # 打印节点类型和位置信息
#         print(f"Found a {type(node).__name__} at {node.coord}")
#         # print(node.coord,type(node))
#         # 遍历节点的所有子节点
#         for child in node.children():
#             # 递归调用本函数
#             print_node_type_and_location(child[1])
#
# 获取函数体和函数列表
def get_functions(maxi,code,filename):
    LineInfo = ...
    with open(filename, 'r') as f:
        LineInfo = f.readlines()
    with open(filename, 'r') as f:
        content = f.read()
    pattern = r'/\*.*?\*/'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    LineInfo = content.split('\n')
    # print(LineInfo)
    lines=[]
    gcovInfo=[]
    for i,line in enumerate(LineInfo):
        if not line.strip() or line.strip().startswith('//'):
            continue
        tempLine = line.split(':')
        # print(tempLine,'tempLine')
        tempLine[1] = int(tempLine[1])-1

        if int(tempLine[1]) == -1:
            continue
        maxi.append([])
        gcovInfo.append(tempLine[0])
        code.append({
            'id': tempLine[1],
            'code': tempLine[2].rstrip('\n'),
            'type':  "others",
            'lineNum': tempLine[1]
        })
        lines.append((tempLine[0],tempLine[1],tempLine[2].rstrip('\n')))
    # covTimes
    functions = []
    func_start = None
    funcNamelist =[]
    braces = 0
    for i, (covTimes,lineNum,line) in enumerate(lines):
        # print(i,covTimes,lineNum,line)
        # Skip empty or comment lines
        if not line.strip() or line.strip().startswith('//'):
            continue
        # Check for function start
        if not func_start and re.match(r'\w+\s+\w+\s*\([^)]*\)\s*' , line) and ';' not in line:
            func_start = i
            code[i]['type'] = 'Method'
            # funcNamelist.append(line.split('(')[0]+'(')
            braces += line.count('{') - line.count('}')
            continue
        # print(func_start," i = ",i)
        # Check for function end
        if func_start is not None:
            braces += line.count('{') - line.count('}')
            code[i]['type'] = getLineType(line)
            if braces == 0 :
                functions.append((lines[func_start],lines[func_start:i+1], func_start+1, i+1))
                func_start = None
    # print(funcNamelist,'---------')
    return gcovInfo,functions
def start(problemName,gcovFileName,codeFileName,result, inName,errLines=[]):
    pwd = common.pwd()
    print("extractCoverInfo . pwd",pwd)
    getProblemFile(problemName,pwd,codeFileName,inName,result,gcovFileName,errLines)
    """  
    当前目录位于项目文件夹下，已读取所生成的覆盖信息，接下来开始创建对应代码的.pkl文件，如果已经存在则不创建
    接下来开始对覆盖信息进行处理
    一. 本任务的需求： 
        1. 提取函数和函数内的语句，将函数名与函数体的每行语句作为节点，每个函数名与函数内语句都有一条边，同时每条函数体语句与对应的测试用例也有一条边
            a. 识别函数名
            b. 识别出函数体
            c. 结合上面两条信息
    二. 具体步骤
        1. 构造合适的数据结构
        2. 设计合适的算法提取函数名及其函数体
        3. 设计合适的算法提取对应语句的执行次数
    三. 保存
        1. 读取曾经的pkl文件，若没有，则创建新的
            pkl内应该是一个list，元素为
        2. 
    """




