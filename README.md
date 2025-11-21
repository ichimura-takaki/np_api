# np_api
## send_mail.py
```
//apiの使い方は以下の通り
//メールの送り方
const mail = MailClient(mail_from, password, smtp_host, smtp_port, use_ssl); //送信側の設定
const result = mail.send(mail_to, mail_subject, mail_body); //メールの送り方

//結果を見る方法
const status = result.status; //送信成功でtrue ,送信失敗でfalse を返す
const msg = result.msg; //送信成功で"success" ,送信失敗でエラーメッセージ を返す

Logger.log(status,msg) //結果表示してます。(本番は書かなくてOK)
//-----------------------------------------------------------------------------------------

//以下の方法でも結果を見れます
const mail = MailClient(mail_from, password, smtp_host, smtp_port, use_ssl); //送信側の設定
const {status,msg} = mail.send(mail_to, mail_subject, mail_body); //メール送って即見れる
Logger.log(status,msg) //結果表示してます。(本番は書かなくてOK)
```
```
//引数は以下の要素を満たしくてください。
    mail_from = r"送信するアドレスを入れてください"
    password = r"ログインパスワードを入れてください"
    smtp_host = r"実際の SMTP ホスト名に置き換えてください"
    smtp_port = "465" #省略可( SSL の場合は通常 465、TLS の場合は 587)
    use_ssl = True #省略可( SSL を使う場合は True、TLS の場合は False)

    mail_to = r"宛先のアドレスを入れてください"
    mail_subject = r"件名テスト"
    mail_body = r"本文テスト"
```
