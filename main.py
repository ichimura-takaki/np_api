import fastapi
import smtplib
from email.mime.text import MIMEText
from fastapi import Header, HTTPException
import traceback
import os
import hashlib

# 環境変数から API キーを読み込む
API_KEY = os.getenv("API_KEY", "default_api_key_change_in_production")

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
        mail_from: str = None,
        password: str = None,
        smtp_host: str = None,
        smtp_port: int = 465,
        use_ssl: bool = True
    ):
        """
        メール送信の設定を保存（API キー認証必須）
        ユーザごとに独立した設定を管理
        """
        # API キー検証
        if api_key != API_KEY:
            return {"status": False, "message": "Unauthorized: Invalid API key"}
        
        # API キーをキーとして設定を保存（ユーザ分離）
        config_key = Mail.get_config_key(api_key)
        Mail.configs[config_key] = {
            "mail_from": mail_from,
            "smtp_host": smtp_host,
            "password": password,
            "smtp_port": smtp_port,
            "use_ssl": use_ssl
        }
        
        return {"status": True, "message": "Config saved successfully"}

    @staticmethod
    @app.post("/mail/send")
    def send(
        api_key: str = Header(...),
        mail_to: str = None,
        mail_subject: str = None,
        mail_body: str = None
    ):
        """
        メール送信（API キー認証必須）
        mail_to, mail_subject, mail_body のみ指定
        """
        # API キー検証
        if api_key != API_KEY:
            return {"status": False, "message": "Unauthorized: Invalid API key"}
        
        # API キーに紐付いた設定を取得
        config_key = Mail.get_config_key(api_key)
        mail_config = Mail.configs.get(config_key)
        
        # 設定が保存されているか確認
        if not mail_config or not mail_config.get("mail_from"):
            return {"status": False, "message": "Config not set. Call /mail/config first"}
        
        """ メッセージのオブジェクト """
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

        except Exception as e:
            return {"status": False, "message": str(traceback.format_exc())}

        return {"status": True, "message": "success"}