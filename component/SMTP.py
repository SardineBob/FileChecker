# coding=UTF-8
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utilset.ConfigUtil import ConfigUtil


# 寄送Mail
def sendMail(mailContent):
    configUtil = ConfigUtil()
    SMTP = configUtil.SMTP
    # 收集資料
    ttls = SMTP["ttls"]
    host = SMTP["host"]
    port = SMTP["port"]
    account = SMTP["account"]
    password = SMTP["password"]
    subject = "[帝緯]檔案雜湊檢查報告"
    content = "<br />".join(mailContent)
    fromAddr = SMTP["from"]
    ToAddr = ";".join(SMTP["to"])
    # 產生Mail內容
    message = MIMEMultipart()
    message["From"] = fromAddr
    message["To"] = ToAddr
    message["Subject"] = subject
    message.attach(MIMEText(content, "html", "UTF8"))
    # 執行寄送Mail
    try:
        with smtplib.SMTP(host, port) as smtp:
            smtp.ehlo()
            if ttls is True:
                smtp.starttls()
            smtp.login(account, password)
            smtp.send_message(message)
    except Exception as err:
        __outputLog(err)
        return (False, "寄送Mail發生問題，請查看maillog。")
    # 寄送成功寫入log
    __outputLog(str(message) + "\n主旨:" + subject +
                "\n內容:\n" + "\n".join(mailContent))
    return (True, "")


# 寫入Log檔
def __outputLog(result):
    logFilename = datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ".maillog"
    # 檢查log資料夾不存在則建立
    if os.path.exists("maillog") is False:
        os.mkdir("maillog")
    with open(os.path.join("maillog", logFilename), "w", encoding='UTF8') as f:
        f.write(str(result) + "\n")
