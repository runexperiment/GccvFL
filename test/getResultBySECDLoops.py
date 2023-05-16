import csv
import json
import os
import pickle
import subprocess
import sys

import common
import batchRunFileSetting
from pyecharts.charts import Page, Bar

types = {
    # "test": ["1642"],
    "SimpleExpressions": ['2810', '2811', '2812', '2813' ],
    "Conditionals_C": ["2824", "2825", "2827", "2828", "2830", "2831", "2832", "2833"],
    "Conditionals_C++ ": ["1642", "2122", "2208"],
    "Loops_C": ["2864", "2865", "2866", "2867", "2868", "2869", "2870", "2871"],
    "Loops_C++": ["1335", "1500", "1687", "1912", "1927", "1947", "1951", "2111", "2112", "2327"]
}


def getFileInfo(data):
    lineSum = 0  # 语句总数量
    minLineNumber = -1  # 代码中最小的行数
    maxLineNumber = -1  # 代码中最大的行数
    errLineNumber = 0  # 错误行总数
    for index, file in enumerate(data):
        if index == 0:
            minLineNumber = len(file['codeList'])
            maxLineNumber = len(file['codeList'])
        else:
            if minLineNumber > len(file['codeList']):
                minLineNumber = len(file['codeList'])
            if maxLineNumber < len(file['codeList']):
                maxLineNumber = len(file['codeList'])
        lineSum += len(file['codeList'])
        errLineNumber += len(file['errLines'])

    return (lineSum, errLineNumber, minLineNumber, maxLineNumber)


def getQuesInfo(ques):
    # puTong = ["1","3","5","10","EXAM"]

    allKey = ques.keys()
    print(allKey)
    if "sumTop1" in allKey:
        return ques['sumTop1'], ques['sumTop3'], ques['sumTop5'], ques['sumTop10'], ques['sumEXAM'], ques['errLineNum']
    else:
        return ques['top'][0], ques['top'][2], ques['top'][4], ques['top'][9], ques['EXAM']*ques['ansNum'],ques['ansNum']

    # return getFileInfo(ques['fileList'])


def getTypeInfo(data):
    # temp = [
    #     {"type": "top1", "val": 0},
    #     {"type": "top3", "val": 0},
    #     {"type": "top5", "val": 0},
    #     {"type": "top10", "val": 0},
    #     {"type": "EXAM", "val": 0},
    #     {"type": "errLineNum", "val": 0},
    # ]
    preStr = ""
    keys = data.keys()
    if "Grace1335" in keys:
        preStr = "Grace"
    myRes = {}
    for key in types:
        myRes[key] = [
            {"type": "top1",  "val": 0},
            {"type": "top3",  "val": 0},
            {"type": "top5",  "val": 0},
            {"type": "top10", "val": 0},
            {"type": "EXAM",  "val": 0},
            {"type": "errLineNum", "val": 0},
        ]
        for index, ques in enumerate(types[key]):
            item = data[preStr+ques]
            classisInfo = getQuesInfo(item)
            print(len(classisInfo), (myRes[key]),key)
            for j in range(len(  myRes[key])):
                myRes[key][j]["val"] += classisInfo[j]

        myRes[key].append( {"type": "A-EXAM", "val": ((myRes[key][-2]["val"]) /(myRes[key][-1]["val"])) })
            # print(ques,classisInfo[1],errLineNumber)
        # print(key)
        # print(key,  ", " = ", (lineSum,errLineNumber,minLineNumber,maxLineNumber))
    return myRes
    # for index, file in enumerate(item)
from pyecharts import options as opts
def getVal(type2,data):
    for item in data:
        if type2 == item['type']:
            if "EXAM" not in type2:
                return item['val']
            return round(item["val"],3)

def draw(data):
    page = Page()
    xAxis = list(data.keys())
    print(xAxis)
    yaxisList = list(data[xAxis[0]].keys())
    # yaxisList 是分类，如CD、SE、loops
    barNames = ["top1","top3","top5","top10","EXAM" ]
    # with open("Performance_Of_Techniques_on_Different_CateGories.csv", 'w', newline="")as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(["CateGores", "Techniques", "A-EXAM", "TOP-1", "TOP-3", "TOP-5", "TOP-10"])
    #     for k, v in data.items():
    #         writer.writerow([k] + [item['val'] for item in v])
    lineName = "VsusFL_res_sus.xlsxresult.json"
    for yaxisName in yaxisList:
        bar = Bar(init_opts=opts.InitOpts(width="100%"))
        mulBar = {}
        for barName in barNames:
            mulBar[barName] = [] # 给每个柱子创建数组容器

        myx = []
        for x in xAxis:
            isData = data[x][yaxisName]
            myx.append(x.split("_")[0])
            if x == lineName:
                for barName in barNames:
                    bar.set_series_opts(markline_opts=opts.MarkLineOpts(
                        data=[opts.MarkLineItem(y=getVal(barName,isData),name=barName)]
                    ))

            for barName in barNames:
                mulBar[barName].append(getVal(barName,isData))
        # print(barNames)
        for barName in barNames:
            bar.add_yaxis(barName,mulBar[barName])

        bar.add_xaxis(myx)

        bar.set_global_opts(title_opts=opts.TitleOpts(title=yaxisName),xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
        page.add(bar)
    page.render(batchRunFileSetting.drawPerformanceDifferentCateGories+".html")

# def printCSV(data):

if __name__ == "__main__":
    temp = common.dirList(batchRunFileSetting.baseLineDir)
    allData = {}
    for dir in temp:
        if ".json" in dir:
            with open(common.jointPath([batchRunFileSetting.baseLineDir,dir]), 'rb') as f:
                data = json.load(f)
            allData[dir] = getTypeInfo(data)
    draw(allData)
    common.writeJson(allData,batchRunFileSetting.drawPerformanceDifferentCateGories+".json")


    # fileList = []
    # topArr = {}
    # xaxias = -1
    # topArr[1] = []
    # topArr[3] = []
    # topArr[5] = []
    # topArr[10] = []
    #

