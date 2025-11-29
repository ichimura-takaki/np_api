# np_api

## アジェンダ
gas用のapiです。railwayをサーバとしています。→railwayでsmtp使えない！？
pythonのfastAPIを使用して記述されてます。
gas側での使い方を記述します。

## mail機能
プログラム横のコメントがある場合、そこは都度書き換え必須ポイントです。
```
//初期初期設定なので一回書けばOK
function config() {
  const apiUrl = "https://api-server_URL"; //apiサーバのURL
  const apiKey = "your_api_key"; // 設定した API_KEY
  
  const payload = {
    "mail_from": {
      "address": "send@api.com",//送信元メールアドレス
      "password": "password123",//送信元メールアドレスのパスワード
      "smtp_host": "smtp1234.smpt_server.jp",//SMTPサーバー
      "smtp_port": 465,//SMTPポート(デフォルト値)
      "use_ssl": true //SSL使用有無(true/false) (デフォルト値true)
    },
    "mail_to": {}
  };

  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    headers: {
      "x-api-key": apiKey
    },
    muteHttpExceptions: true
  };
  return {apiUrl,options,payload}
}

//実際の処理部分
function main(){

  //ループ前に書くおまじない
  const {apiUrl,options,payload}=config();

  //実際の処理はループするっしょ！？！？
  for(let i=0;i<1;i++){
    //送信先の更新
    payload.mail_to = {
      "address": "reception@gmail.com", //送信先メールアドレス
      "subject": "Test Subject", //メール件名
      "body": "This is a test email" //メール本文
    }
    //更新の保存
    options.payload = JSON.stringify(payload);

    //処理開始&結果の取得
    const response = UrlFetchApp.fetch(apiUrl, options);
    const result = JSON.parse(response.getContentText());
    
    //結果の表示
    Logger.log(result);
    return result;
  }
}
```
