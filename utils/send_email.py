# coding=utf-8

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from utils.config import get_path
"""
第一步获取最新测试报告
第二步发送邮箱 （这一步不想执行的话，可以注释掉最后面那个函数就行）
"""
# 当前脚本的真实路径
cur_path = get_path()


def get_report_file(report_path):
    """第三步：获取最新的测试报告
    :param report_path:
    """
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    #logger.info("获取最新测试生成的报告："+lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def send_mail(sender, psw, receiver, smtpserver, report_file):
    """第四步：发送最新的测试报告内容
    :param psw:
    :param sender:
    :param smtpserver:
    :param report_file:
    :param receiver:
    """
    with open(report_file, "rb") as f:
        mail_body = f.read()  # 读取报告模板内容
    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['Subject'] = u"自动化测试报告"
    msg["from"] = sender
    msg["to"] = ",".join(receiver)  # 只能字符串
    msg.attach(body)
    msg.attach(MIMEText('自动化测试报告，有疑问及时沟通，因邮箱兼容问题，详细打开附件查看更直观', 'plain', 'utf-8'))

    # 添加附件
    att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename= "report.html"'
    msg.attach(att)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)  # 连服务器
        smtp.login(sender, psw)
    except:
        smtp = smtplib.SMTP_SSL(smtpserver)
        smtp.login(sender, psw)  # 登录
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    #logger.info("测试报告发送成功")
