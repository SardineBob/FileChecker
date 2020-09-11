# coding=UTF-8
import time
from utilset.ConfigUtil import ConfigUtil
from component.Checker import doFileChecker

print("開始執行檔案雜湊比對檢查。")
interval = ConfigUtil().ScanInterval
active = True
try:
    while active:
        doFileChecker()
        time.sleep(interval)
except KeyboardInterrupt:
    active = False
print("停止執行檔案雜湊檢查")
input("按一下enter離開")