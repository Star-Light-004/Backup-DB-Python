import os
import shutil
import smtplib
import schedule
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

#đường dẫn đọc file .env 
load_dotenv(dotenv_path='db.env')

#mail
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
#folder
DATABASE_FOLDER = r"D:\Dbtest"
BACKUP_FOLDER = './backup'      

def send_email(sender, receiver, subject, body, password):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        text = message.as_string()
        server.sendmail(sender, receiver, text)
        print(f"Email đã được gửi đến {receiver}")
        server.quit()
    except Exception as e:
        print("Lỗi khi gửi email:", e)


def backup_database():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)

        files = os.listdir(DATABASE_FOLDER)
        db_files = [f for f in files if f.endswith('.sql') or f.endswith('.sqlite3')]

        if not db_files:
            send_email(SENDER_EMAIL, RECEIVER_EMAIL, "Backup thất bại", 
                       f"[{now}] Không tìm thấy file database (.sql hoặc .sqlite3) để backup.",
                       APP_PASSWORD)
            return

        for file in db_files:
            src_path = os.path.join(DATABASE_FOLDER, file)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(BACKUP_FOLDER, f"{timestamp}_{file}")
            shutil.copy2(src_path, backup_path)

        send_email(SENDER_EMAIL, RECEIVER_EMAIL, "Backup thành công", 
                   f"[{now}] Đã backup {len(db_files)} file database thành công",
                   APP_PASSWORD)

    except Exception as e:
        send_email(SENDER_EMAIL, RECEIVER_EMAIL, "Backup thất bại", 
                   f"[{now}] Lỗi: {e}",
                   APP_PASSWORD)

# chạy vào lúc 0h
schedule.every().day.at("00:00").do(backup_database)

print("Đang chạy lịch backup tự động...")
# dòng code để kiểm tra backup ngay lập tức khi run code
# backup_database()
while True:
    schedule.run_pending()
    time.sleep(1)
