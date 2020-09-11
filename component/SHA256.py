# coding=UTF-8

import hashlib


# 計算檔案SHA256雜湊值
def getSHA256(filePath):
    sha256 = hashlib.sha256()
    sha256.update(filePath)
    return sha256.hexdigest()
