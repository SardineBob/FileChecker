# coding=UTF-8
from utilset.TableUtil import TableUtil
from component.FileCheckerList import getFileCheckerList

# get file checker list
fileCheckerList = getFileCheckerList()  # list(tuple)
# insert file code
tableUtil = TableUtil()
tableUtil.deleteCode()  # clear data for renew file code
for filename, code, fullpath in fileCheckerList:
    tableUtil.insertCode({
        "FileName": filename,
        "Code": code,
        "FullPath": fullpath
    })
