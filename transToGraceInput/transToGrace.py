# -*- coding: utf-8 -*-
import json
import os
import pickle
import common
import time
import Setting

lineTypeList = {'IfStatement': 0, 'WhileStatement': 1, 'switchStatement': 2, 'ReturnStatement': 3,
                'ConstructorDeclaration': 4, 'BreakStatement': 5, 'ContinueStatement': 6, 'StatementExpression': 7,
                'funCall': 8, 'LocalVariableDeclaration': 9, 'others': 10, 'Method': 11}


def getMethods(item, file):
    funList = file['funList']
    item['methods'] = {}
    for i, fun in enumerate(funList):
        theKey = fun['pwd'][1:-2].replace('/', '.') + ':' + fun['name'].split()[1].split('(')[0] + '(' + \
                 fun['name'].split()[1] + ')'
        item['methods'][theKey] = fun['id']
    return
def getEdge3Andltype(item, file):
    edge3 = set()
    lineId = file['lineId']
    ltype = {}
    lines = {}
    fileName = file['pwd'].split('/')[-1]
    for i, line in enumerate(lineId):
        ltype[i] = line['type']
        edge3.add((i, lineTypeList[line['type']]))
        lines[fileName + str(i)] = i

    item['ltype'] = ltype
    item['edge3'] = edge3
    item['lines'] = lines
    return



def getEdgeAndEdge10(item, file):
    maxi = file['maxi']
    result = file['result']
    edge = set()
    edge10 = set()
    testF={}
    testC={}
    FNum = 0
    CNum = 0
    for i,item2 in enumerate(result):
        if item2 == 0:
            testF[i] = FNum
            FNum +=1

        else:
            testC[i] = CNum
            CNum +=1


    for i, line in enumerate(maxi):
        for j, item2 in enumerate(line):
            if result[j] == 0:
                temp = (i, testF[j])
                edge.add(temp)
            else:
                temp = (i, testC[j])
                edge10.add(temp)
    item['edge'] = edge
    item['edge10'] = edge10
    return


def getEdge2(item, file):
    funList = file['funList']
    edge2 = set()
    for i, fun in enumerate(funList):
        for i in range(fun['startLine'], fun['endLine']):
            edge2.add((fun['id'], i))
    item['edge2'] = edge2


def getRtest(item, file,inList):
    item['rtest'] = {}
    item['ftest'] = {}
    RNum = 0
    FNum = 0
    for index,value in enumerate(file['result']):
        if value == 1:
            item['rtest'][ inList[index] ] = RNum
            RNum+=1
        else:
            item['ftest'][inList[index]] = FNum
            FNum+=1
    # item['rtest'] = [index for index, value in enumerate(file['result']) if value == 1]


# def getFtest(item, file,):
#     item['ftest'] = {}
#     for index, value in enumerate(file['result']):
#         if value == 1:
#             item['rtest'][inList[index]] = index
#     # item['rtest'] = [index for index, value in enumerate(file['result']) if value == 1]

def handleVsus(rowOutput):
    lineRank = {}
    sumLine = 1
    rowLine = 0
    for lit in rowOutput:
        rowLine+=len(lit)
    for lit in rowOutput:
        for rowNumber in lit:
            rowNumber -=1
            lineRank[rowNumber] =   sumLine
        sumLine+=len(lit)
    return  lineRank

if __name__ == "__main__":
    res = []
    startTime = time.perf_counter()
    fileList = common.dirList(Setting.resultDir)
    VsusResult = ...
    #  # 读取所有的配吗，这个文件要通过Grace2.0里面的
    with open("pre_result/VsusFL_res_sus.xlsxresult.json",'rb') as f:

        VsusResult = json.load(f)

    for i, problemName in enumerate(fileList):
        # item = {}
        # item['edge'].add((0,0))
        gracePkl = []
        print(Setting.resultDir,problemName)
        VsusQuesRes = VsusResult[ problemName[:-4] ]
        with open(common.jointPath([Setting.resultDir, problemName]), 'rb') as f:
            problem = pickle.load(f)
        for j, file in enumerate(problem['fileList']):
            fileName = problem['fileId'][ file['id'] ]

            # 找到对应的Vsus的怀疑排名
            item = {}
            item['VsusRank'] = handleVsus(VsusQuesRes[fileName]['RawOutput'])

            item['proj'] = file['id']
            item['ans'] = file['errLines']

            item['linem'] = []
            getMethods(item, file)
            getRtest(item, file,problem['inList'])
            # getFtest(item, file)
            getEdge3Andltype(item, file)
            # getLines(item, file)
            getEdgeAndEdge10(item, file)
            getEdge2(item, file)
            gracePkl.append(item)
        with open(os.path.join(Setting.resultDir, 'Grace' + problem['id']+'.pkl'), 'wb') as f:
            pickle.dump(gracePkl, f)
    print("时间： ", time.perf_counter() - startTime)