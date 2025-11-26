# np_api

# アジェンダ
gas用のapiです。railwayをサーバとしています。
pythonのfastAPIを使用して記述されてます。
gas側での使い方を記述します。

# mail機能
MAIL_CONIFIG内のmail_from,password,smtp_hostだけ修正してください(6-8行目くらい)
こちらは最初に1回だけ書けばいい初期設定です。
```初期設定.js
// ===== Mail 初期化 =====
const API_URL = "https://your-railway-url";
const API_KEY = "your_secret_api_key";

const MAIL_CONFIG = {
  mail_from: "送信したいメアド",
  password: "ログイン用パスワード",
  smtp_host: "SMTPのホスト名を入れてください",
  smtp_port: 465,　//デフォルト値です。場合によって変えてください。
  use_ssl: true　//デフォルト値です。場合によって変えてください。
};

//ココから下は触れる必要はありません。コピペして貼り付けてください。
// ===== Mail 初期化 =====
function initializeMail() {
  const options = {
    method: "post",
    contentType: "application/json",
    headers: { "api-key": API_KEY },
    payload: JSON.stringify(MAIL_CONFIG),
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(API_URL + "/mail/config", options);
  Logger.log(JSON.parse(response.getContentText()));
}


// ===== メール送信 =====
function send_mail(mail_to, mail_subject, mail_body) {
  const payload = {
    mail_to: mail_to,
    mail_subject: mail_subject,
    mail_body: mail_body
  };

  const options = {
    method: "post",
    contentType: "application/json",
    headers: { "api-key": API_KEY },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(API_URL + "/mail/send", options);
  return JSON.parse(response.getContentText());
}
```

実際に使用する際は以下の要領で使用してください。
```使用例.js
function test() {
  // メール送信
  const mail_result = send_mail(
    "user@example.com",
    "テスト件名",
    "テスト本文"
  );
  Logger.log("Mail:", mail_result);
}
