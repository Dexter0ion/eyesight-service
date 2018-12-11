from email import *
class ServEmail():
    sender = None
    password = None
    recevier = None
    smtp_server = None

    def __init__(self, sender, password, recevier, smtp_server):
        self.sender = sender
        self.password = password
        self.recevier = recevier
        self.smtp_server = smtp_server

    def __str__(self):
        return 'ServEmail:Class to send email'

    def trysendone(self):
        #from_addr = input('From: ')
        #password = input('Password: ')
        #to_addr = input('To: ')
        #smtp_server = input('SMTP server: ')

        msg = MIMEText('爱你爱你爱你爱你爱你', 'plain', 'utf-8')
        msg['From'] = Header("超超的Sever-ServEC", 'utf-8')
        msg['To'] = Header("JUJU", 'utf-8')
        msg['Subject'] = Header(u'晚安宝宝', 'utf-8').encode()

        try:
            server = smtplib.SMTP(self.smtp_server)
            server.set_debuglevel(1)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, [self.recevier], msg.as_string())
            server.quit()
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
