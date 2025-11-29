import smtplib
from email.mime.text import MIMEText
from fastapi import Body
import traceback

def send(request: dict = Body(...)):
    """期待する JSON 形式:
      config= {
        "mail_from":"from@example.com",
        "password":"...",
        "smtp_host":"...",
        "smtp_port":465, #デフォルト値465
        "use_ssl":True  #デフォルト値True
      } 
      
      mail_to= {
        "mail_to":"to@example.com",
        "subject":"...",
        "body":"..."}
      }
    """
    config = request.get("config")
    mail_to = request.get("mail_to")

    if not config or not mail_to:
        return {"status": False, "message": "Required JSON fields: config, mail_to"}

    try:
        msg = MIMEText(mail_to["body"], "plain", "utf-8")
        msg["Subject"] = mail_to["subject"]
        msg["From"] = config["mail_from"]
        msg["To"] = mail_to["mail_to"]

        use_ssl = config.get("use_ssl", True)
        port = int(config.get("smtp_port", 465))
        
        #ssl 有無で接続方法を切り替え
        if use_ssl:
            server = smtplib.SMTP_SSL(config["smtp_host"], port)
        else:
            server = smtplib.SMTP(config["smtp_host"], port)
            server.starttls()

        server.login(config["mail_from"], config["password"])
        server.sendmail(config["mail_from"], [mail_to["mail_to"]], msg.as_string())
        server.quit()
        return {"status": True, "message": "success"}
    except Exception as e:
        return {"status": False, "message": str(e)+"\n"+traceback.format_exc()}
    