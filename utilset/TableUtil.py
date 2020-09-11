# coding=UTF-8
import os
from datetime import datetime
from utilset.SqlLiteUtil import SqlLiteUtil


# 將每個檔案算好雜湊，存於sqlite
class TableUtil():

    __dbFile = "filecode.db"
    __sqlLiteUtil = None

    def __init__(self):
        self.__sqlLiteUtil = SqlLiteUtil()
        # 先檢查dbfile是否存在
        self.__checkDB()

    # 檢查DB是否已產生
    def __checkDB(self):
        # 檢查DB檔案是否存在，不存在則開啟
        if os.path.isfile(self.__dbFile) is False:
            self.__createDB()

    # 產生DB檔案
    def __createDB(self):
        command = "CREATE TABLE FileCode(\
            FileName Text NOT NULL,\
            Code Text NOT NULL,\
            FullPath Text NOT NULL,\
            CodeTime Text NOT NULL,\
            PRIMARY KEY (FileName, CodeTime)\
        )"
        # do create db
        self.__sqlLiteUtil.Execute(self.__dbFile, command, [])

    # insert雜湊資料
    def insertCode(self, para):
        # 取出相關Insert資料
        fileName = para['FileName']
        code = para['Code']
        fullPath = para['FullPath']
        codeTime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # insert 指令
        command = " INSERT INTO FileCode VALUES (:fileName, :code, :fullPath, :codeTime) "
        parameter = {
            'fileName': fileName,
            'code': code,
            'fullPath': fullPath,
            'codeTime': codeTime
        }
        # do insert to db
        self.__sqlLiteUtil.Execute(self.__dbFile, command, parameter)

    # select所有雜湊資料
    def selectCode(self):
        # 回傳物件
        result = {
            'status': False,
            'message': '',
            'data': []
        }
        # select 指令
        command = " SELECT * FROM FileCode "
        # get data from db
        data = self.__sqlLiteUtil.Execute(self.__dbFile, command, [])
        result['status'] = True
        result['data'] = data
        return result

    # delete雜湊資料，用於renew
    def deleteCode(self):
        # 回傳物件
        result = {
            'status': False,
            'message': '',
            'data': []
        }
        # delete 指令
        command = " DELETE FROM FileCode "
        # get data from db
        self.__sqlLiteUtil.Execute(self.__dbFile, command, [])
        result['status'] = True
        result['message'] = "delete ok"
        return result