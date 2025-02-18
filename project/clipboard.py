import pyperclip
import os

# File path
clipboard_information = "logs/clipboard.txt"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def get_clipboard():
    with open(clipboard_information, "a") as f:
        clipboard_content = pyperclip.paste()
        f.write(f"Clipboard Data: {clipboard_content}\n\n")

get_clipboard()