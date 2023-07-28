from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import email.utils

# メール送信処理のメソッド
# 引数は宛先、件名、本文
def send_mail(to, subject, body):
# 送信に必要な情報を定数で定義
    ID='t.takahashi.sys22@morijyobi.ac.jp'
    PASS=os.environ['MAIL_PASS']
    HOST='smtp.gmail.com'
    PORT=587
    
    # MIME インスタンスを生成
    msg=MIMEMultipart()
    # HTML 形式の本文を設定
    msg.attach(MIMEText(body, 'html'))
    # 件名、送信元アドレス、送信先アドレスを設定
    msg['Subject'] =subject
    msg['From'] = email.utils.formataddr(('システムメール', ID))
    msg['To'] =to
    
    # SMTP サーバへ接続
    server=SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS) # ログイン認証
    server.send_message(msg) # 送信！！！
    server.quit() # サーバ切断