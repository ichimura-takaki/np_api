import fastapi
import smtplib
from email.mime.text import MIMEText
from fastapi import Header, Body
import traceback
import os
import hashlib

# 環境変数から API キーを読み込む
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set in environment variables")

app = fastapi.FastAPI()

# ===== Mail クラス =====
class Mail:
    # API キーごとの設定を保持（ユーザ分離）
    configs = {}

    @staticmethod
    def get_config_key(api_key: str) -> str:
        """API キーをハッシュ化してキーとする"""
        return hashlib.sha256(api_key.encode()).hexdigest()

    @staticmethod
    @app.post("/mail/config")
    def config(
        api_key: str = Header(...),
        mail_from: str = Body(None),
        password: str = Body(None),
        smtp_host: str = Body(None),
        smtp_port: int = Body(465),
        use_ssl: bool = Body(True)
    ):
        # API キー検証
        if api_key != API_KEY:
            return {"status": False, "message": "Unauthorized: Invalid API key"}

        # 必須項目チェック
        if not mail_from or not password or not smtp_host:
            return {"status": False, "message": "Missing required fields: mail_from, password, smtp_host"}

        # API キーをキーとして設定を保存
        config_key = Mail.get_config_key(api_key)
        Mail.configs[config_key] = {
            "mail_from": mail_from,
            "password": password,
            "smtp_host": smtp_host,
            "smtp_port": smtp_port,
            "use_ssl": use_ssl
        }

        return {"status": True, "message": "Config saved successfully"}

    @staticmethod
    @app.post("/mail/send")
    def send(
        api_key: str = Header(...),
        mail_to: str = Body(None),
        mail_subject: str = Body(None),
        mail_body: str = Body(None)
    ):
        # API キー検証
        if api_key != API_KEY:
            return {"status": False, "message": "Unauthorized: Invalid API key"}

        # 必須項目チェック
        if not mail_to or not mail_subject or not mail_body:
            return {"status": False, "message": "Missing required fields: mail_to, mail_subject, mail_body"}

        # API キーに紐付いた設定を取得
        config_key = Mail.get_config_key(api_key)
        mail_config = Mail.configs.get(config_key)

        if not mail_config or not mail_config.get("mail_from"):
            return {"status": False, "message": "Config not set. Call /mail/config first"}

        # メッセージのオブジェクト
        msg = MIMEText(mail_body, "plain", "utf-8")
        msg['Subject'] = mail_subject
        msg['From'] = mail_config["mail_from"]
        msg['To'] = mail_to

        try:
            if mail_config["use_ssl"]:
                smtpobj = smtplib.SMTP_SSL(mail_config["smtp_host"], mail_config["smtp_port"])
                smtpobj.ehlo()
            else:
                smtpobj = smtplib.SMTP(mail_config["smtp_host"], mail_config["smtp_port"])
                smtpobj.ehlo()
                smtpobj.starttls()

            smtpobj.login(mail_config["mail_from"], mail_config["password"])
            smtpobj.sendmail(mail_config["mail_from"], mail_to, msg.as_string())
            smtpobj.quit()

        except Exception:
            return {"status": False, "message": traceback.format_exc()}

        return {"status": True, "message": "success"}
