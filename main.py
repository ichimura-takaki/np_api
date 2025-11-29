from fastapi import FastAPI, Header, HTTPException
import os
import mail

app = FastAPI()

API_KEY = os.getenv("API_KEY", "dev-key")  # 環境変数から読み込み

@app.post("/mail/send")
def send_mail(request: dict, x_api_key: str = Header(...)):
    """キー検証後、mail モジュールに委譲"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    # mail.py のビジネスロジックを呼び出し
    return mail.send(request)
