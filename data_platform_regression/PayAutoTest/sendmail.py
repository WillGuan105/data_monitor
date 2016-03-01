#coding=utf-8

import smtplib,email,sys
from email.Message import Message
from email.mime.multipart import MIMEMultipart
from email.Header import Header
from email.mime.text import MIMEText

class MmsEmail:
    def __init__(self,cc=''):

        self.smtpserver='mail.mail_address'
        self.smtpuser='dip-test@mlsmsg.mail_address'
        self.smtppass='Dip-test123'
        self.smtpport='25'
        self.emailfrom='diptest@mail_address'
        self.server=smtplib.SMTP(self.smtpserver,self.smtpport)
        self.server.ehlo()
        self.server.login(self.smtpuser,self.smtppass)
        #self.to=['zhibinren','haiyuanhuang','chengyunwang','mengliu','xiaofenzhang']
        self.to=['weiguan']
        self.cc=cc
        if self.cc :
            self.to.append(self.cc)
        self.subj='fackcube job failed'

        # 发送文件或html邮件
    def sendTxtMail(self, to, sub, content, subtype='html'):
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = self.emailfrom
        msg['To'] = ";".join(to)
        try:
            failed = self.server.sendmail(self.emailfrom,to,msg.as_string())   # may also raise exc
        except Exception ,ex:
            print Exception,ex
            return 'Error - send failed'

    def addsuff(self,a):
        return a+'@mail_address'

    def sendmessage(self,to='',subj='',content='',attach=None):
        msg = Message()
        COMMASPACE = ', '
        if not to:
            to=self.to
        to=map(self.addsuff,to)
        print to
        if not subj:
            subj=self.subj
        if not content:
            content=self.subj
        msg = MIMEMultipart()

        msg['From']    = self.emailfrom
        if self.cc:
            msg['CC'] = self.cc

        msg['To']      =COMMASPACE.join(to)

        msg['Subject'] = Header(subj,'utf-8')
        msg['Date']    = email.Utils.formatdate()
        # msg.set_payload(content)
        if not attach:
            msg.set_payload(content)
        else:
            msg.attach(content)
            msg.attach(attach)
        try:

            failed = self.server.sendmail(self.emailfrom,to,msg.as_string())   # may also raise exc
        except Exception ,ex:
            print Exception,ex
            return 'Error - send failed'
        else:
            return "send success!"

def sendMail(to='',subj='',content='',attach=None):
    mailIns=MmsEmail()
    mailIns.sendTxtMail(to,subj,content)
    #mailIns.sendmessage(to,subj,content,attach)

# if __name__=="__main__":

#     to='weiguan@mail_address'
#     cc='weiguan'
#     subj='gwtest'
#     print 'Type message text, end with line="."'
#     #text = 'content'
#     a=MmsEmail()

#     a.sendmessage(to=['weiguan','weiguan'])
