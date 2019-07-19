# -*- coding = utf-8 -*-

import requests


def getVideoList(url):
    """
    参数：仓库链接
    功能：获取视频名称。
    返回值：视频列表，id列表
    """
    websiteCode = requests.get(url)
    code = websiteCode.text
    times = code.count('<td class="content">')
    codeList = code.split('<a class="js-navigation-open" title="')[1:]
    videos = []
    ids = []
    print(times)
    for i in range(times):
        videoName = codeList[i].split('"')[0]
        videoId = codeList[i].split('" id="')[1].split('"')[0]
        print(str(i)+" "+videoName)
        if ".mp4" in videoName.lower() or ".flv" in videoName.lower():
            videos.append(videoName)
            ids.append(videoId)
        del videoId
        del videoName
    return videos, ids

def getUrl(fileNames, url):
    """
    参数：文件名称
    功能：获取视频链接
    完成方法：发现Github上原始文件Url的规律为https://github.com/仓库名/raw/master/文件路径
    返回值：视频链接列表
    """
    fileUrlList = []
    libraryName = url.split("https://github.com/")[1].split("/")[0:2]
    for fileName in fileNames:
        if ".mp4" in fileName.lower() or ".flv" in fileName.lower():
            fileUrlList.append("https://github.com/{0}/raw/master/{1}".format(libraryName[0]+"/"+libraryName[1], fileName))
    return fileUrlList

def getFileName(fileList):
    videoNameList = []
    for item in fileList:
        item = item.strip(".mp4").strip(".flv")
        videoNameList.append(item)
    return videoNameList

def createCode(videoNameList, fileUrlList, videoIdList, codeFile):
    """
    参数：文件名称列表，文件链接列表，文件id列表，代码文件
    功能：将已有数据批量写入代码并形成列表
    返回值：代码列表
    """
    codeList = []
    for i in range(len(videoNameList)):
        codeF = open(codeFile, "r", encoding = "utf-8")
        code = codeF.read()
        codeF.close()
        codeList.append(code.format(fileUrlList[i], videoNameList[i], "github id: "+videoIdList[i]))
    return codeList


url = input("请输入仓库链接：")
fileNameList, videoIdList = getVideoList(url)
fileUrlList = getUrl(fileNameList, url)
videoNameList = getFileName(fileNameList)
codeList = createCode(videoNameList, fileUrlList, videoIdList, "sourcecode.txt")
codeIntoFile = open("code.txt", "w+", encoding="utf-8")
for i in codeList:
    codeIntoFile.write("{}\n".format(i))
print("程序完成")
a = input()
