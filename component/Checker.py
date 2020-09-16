# coding=UTF-8
import os
from datetime import datetime
from utilset.TableUtil import TableUtil
from component.FileCheckerList import getFileCheckerList
from component.SMTP import sendMail


# 執行檔案雜湊比對
def doFileChecker():
    # get file checker list
    fileCheckerList = getFileCheckerList()  # list(tuple)
    # check file code
    tableUtil = TableUtil()
    tableList = tableUtil.selectCode()["data"]  # list(tuple)
    result = []
    # 檢查檔案雜湊值是否相符
    for filename, code, fullpath in fileCheckerList:
        status, message = __isFileCodeMatch(fullpath, code, tableList)
        if status is False:
            result.append(message)
            continue
    # 反向檢查，是不是有檔案被刪除
    for filename, code, fullpath, codetime in tableList:
        if __isFileExist(fullpath, fileCheckerList) is False:
            result.append("檔案路徑:" + fullpath + "，已被刪除，無法比對雜湊值。")
    # 判斷，若有錯誤訊息，則寫入log並寄送mail
    if len(result) > 0:
        __outputLog(result)
        status, message = sendMail(result)
        print("寄送Mail成功。" if status else message)

    print("檢查無誤。" if len(result) <= 0 else result)


# 查詢檔案，與現有的雜湊值比對是否相符
def __isFileCodeMatch(filePath, fileCode, table):
    for filename, code, fullpath, codetime in table:
        if filePath == fullpath:
            return (True, "") if fileCode == code else (False, "檔案路徑:" + fullpath + "，雜湊值不相符。")
    return (False, "檔案路徑:" + filePath + "，是新增的檔案，無法比對雜湊值。")


# 反向檢查，是否有檔案被刪除
def __isFileExist(tablefilePath, checkerList):
    for filename, code, fullpath in checkerList:
        if tablefilePath == fullpath:
            return True
    return False


# 寫入Log檔
def __outputLog(result):
    logFilename = datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ".log"
    # 檢查log資料夾不存在則建立
    if os.path.exists("log") is False:
        os.mkdir("log")
    with open(os.path.join("log", logFilename), "w", encoding='UTF8') as f:
        f.write("\n".join(result))
