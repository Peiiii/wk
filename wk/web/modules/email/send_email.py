import smtplib
from email.mime.text import MIMEText
from wk import gen_validation_code

class EmailSender:
    def __init__(self,sender,auth_code,debug=False):
        self.sender=sender
        self.auth_code=auth_code
        self.debug=debug
    def send_email_code(self,target,length=6):
        if self.debug:
            return '123456'
        code=gen_validation_code(length=length)
        res=self.send_email(msg_to=target,subject='知识树验证码',content='你的验证码是%s，1小时内有效。'%(code))
        if res is None:
            return None
        return code
    def send_email(self ,msg_to, subject='测试邮件', content='测试邮件的内容',raise_error=False):
        msg_from =self.sender
        passwd=self.auth_code
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
        except:
            if raise_error:
                raise
            return False
        return True


