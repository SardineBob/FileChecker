# coding=UTF-8
import os
import configparser
import json


# 設定檔存取元件
class ConfigUtil():

    __filePath = 'config.ini'
    RootPath = None
    ScanInterval = None
    SkipDirs = None
    SkipFiles = None
    SMTP = None

    def __init__(self):
        # 判斷設定檔是否存在，不存在則給予預設參數值
        if os.path.exists(self.__filePath) is False:
            self.__saveConfig(self.__initConfig())
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取溫控設備設定
        self.RootPath = json.loads(config["SystemConfig"]["rootPath"])
        self.ScanInterval = json.loads(config["SystemConfig"]["scanInterval"])
        self.SkipDirs = json.loads(config["SystemConfig"]["skipDirs"])
        self.SkipFiles = json.loads(config["SystemConfig"]["skipFiles"])
        self.SMTP = json.loads(config["SystemConfig"]["smtp"])

    # 提供外部呼叫設定檔存檔
    def save(self):
        self.__saveConfig({
            "rootPath": self.RootPath,
            "scanInterval": self.ScanInterval,
            "skipDirs": self.SkipDirs,
            "skipFiles": self.SkipFiles,
            "smtp": self.SMTP,
        })

    # 設定檔存檔
    def __saveConfig(self, para):
        # 讀取設定參數
        rootPath = para["rootPath"]
        scanInterval = para["scanInterval"]
        skipDirs = para["skipDirs"]
        skipFiles = para["skipFiles"]
        smtp = para["smtp"]
        # 產生設定檔物件
        config = configparser.ConfigParser()
        # 產生系統設定參數
        config['SystemConfig'] = {
            'rootPath': json.dumps(rootPath, ensure_ascii=False),
            'scanInterval': json.dumps(scanInterval, ensure_ascii=False),
            'skipDirs': json.dumps(skipDirs, ensure_ascii=False),
            'skipFiles': json.dumps(skipFiles, ensure_ascii=False),
            'smtp': json.dumps(smtp, ensure_ascii=False),
        }
        # 寫入設定檔
        with open(self.__filePath, 'w', encoding='UTF8') as configFile:
            config.write(configFile)

    # 初始化設定檔
    def __initConfig(self):
        return {
            "rootPath": "/test/",
            "scanInterval": 10,
            "skipDirs": [".git"],
            "skipFiles": [],
            "smtp": {
                "ttls": False,
                "host": "smtp.gmail.com",
                "port": 587,
                "account": "@gmail.com",
                "password": "XX",
                "from": "@gmail.com",
                "to": ["@gmail.com"]
            }
        }
