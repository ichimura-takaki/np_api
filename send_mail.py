import smtplib
from email.mime.text import MIMEText
import traceback

class MailClient():
    def __init__(self,mail_from,password,smtp_host,smtp_port=465,use_ssl=True):
        self.mail_from=mail_from
        self.smtp_host=smtp_host
        self.password=password
        self.smtp_port=smtp_port
        self.use_ssl=use_ssl

    def send(self, mail_to, mail_subject, mail_body):
        """ メッセージのオブジェクト """
        msg = MIMEText(mail_body, "plain", "utf-8")
        msg['Subject'] = mail_subject
        msg['From'] = self.mail_from
        msg['To'] = mail_to

        try:
            if use_ssl:
                smtpobj = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
                smtpobj.ehlo()
            else:
                smtpobj = smtplib.SMTP(self.smtp_host, self.smtp_port)
                smtpobj.ehlo()
                smtpobj.starttls()

            smtpobj.login(self.mail_from, self.password)
            smtpobj.sendmail(self.mail_from, mail_to, msg.as_string())
            smtpobj.quit()

        except Exception as e:
            return False,str(traceback.format_exc())

        return True,"success"

# 直接起動の場合はこちらの関数を実行
if __name__== "__main__":
    mail_from = r"送信するアドレスを入れてください"
    password = r"ログインパスワードを入れてください"
    smtp_host = r"実際の SMTP ホスト名に置き換えてください"
    smtp_port = "465" #省略可( SSL の場合は通常 465、TLS の場合は 587)
    use_ssl = True #省略可( SSL を使う場合は True、TLS の場合は False)

    mail_to = r"宛先のアドレスを入れてください"
    mail_subject = r"件名テスト"
    mail_body = r"本文テスト"

    #以下のイメージでapiを使います
    mail = MailClient(mail_from, password, smtp_host, smtp_port, use_ssl)
    result = mail.send(mail_to, mail_subject, mail_body)
    
    #デバッグ用の出力です
    print(result)