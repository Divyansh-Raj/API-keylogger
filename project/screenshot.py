import pyautogui
import os

# File path
screenshot_information = "logs/screenshot.png"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_information)

take_screenshot()