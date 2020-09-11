# coding=UTF-8
import os
from utilset.ConfigUtil import ConfigUtil
from component.SHA256 import getSHA256


# 取得算好雜湊的檔案清單
def getFileCheckerList():
    # get file list
    checkerList = __getFileList()  # list(tuple)
    # get file sha256 code
    fileList = []
    for path, filename, fullpath in checkerList:
        with open(fullpath, "rb") as f:
            fileBytes = f.read()
            code = getSHA256(fileBytes)
            fileList.append((filename, code, fullpath))
    return fileList


# 取得要掃描的檔案路徑清單
def __getFileList():
    # Read config.ini
    configUtil = ConfigUtil()
    # Read config parameter
    rootPath = configUtil.RootPath
    skipDirs = configUtil.SkipDirs
    skipFiles = configUtil.SkipFiles
    # 取得跟目錄底下所有包含子目錄裡面的資料夾與檔案清單
    allList = os.walk(rootPath)
    # 逐一找出需要計算雜湊的檔案
    fileList = []
    for path, dirs, files in allList:
        # 過濾排除跳過的資料夾
        dirs[:] = [d for d in dirs if d not in skipDirs]
        # 只要這一行資料夾底下無檔案，跳過
        if(len(files) <= 0):
            continue
        # 收集檔案清單
        for filename in files:
            # 過濾排除跳過的副檔名
            if filename.endswith(tuple(skipFiles)) is True:
                continue
            fileList.append((path, filename, os.path.join(path, filename)))
    return fileList
