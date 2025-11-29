import smtplib
from email.mime.text import MIMEText
from fastapi import Body
import traceback

def send(request: dict = Body(...)):
    """期待する JSON 形式:
      mail_from= {
        "address":"from@example.com",
        "password":"...",
        "smtp_host":"...",
        "smtp_port":465, #デフォルト値465
        "use_ssl":True  #デフォルト値True
      } 
      
      mail_to= {
        "address":"to@example.com",
        "subject":"...",
        "body":"..."}
      }
    """
    mail_from = request.get("mail_from")
    mail_to = request.get("mail_to")

    if not mail_from or not mail_to:
        return {"status": False, "message": "Required JSON fields: mail_from.address, mail_to.address"}

    try:
        msg = MIMEText(mail_to["body"], "plain", "utf-8")
        msg["Subject"] = mail_to["subject"]
        msg["From"] = mail_from["address"]
        msg["To"] = mail_to["address"]

        use_ssl = mail_from.get("use_ssl", True)
        port = int(mail_from.get("smtp_port", 465))
        
        #ssl 有無で接続方法を切り替え
        if use_ssl:
            server = smtplib.SMTP_SSL(mail_from["smtp_host"], port)
        else:
            server = smtplib.SMTP(mail_from["smtp_host"], port)
            server.starttls()

        server.login(mail_from["address"], mail_from["password"])
        server.sendmail(mail_from["address"], [mail_to["address"]], msg.as_string())
        server.quit()
        return {"status": True, "message": "success"}
    except Exception as e:
        return {"status": False, "message": str(e)+"\n"+traceback.format_exc()}
    