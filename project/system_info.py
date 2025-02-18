import platform
import os

# File path
system_information = "logs/system.txt"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def get_system_info():
    with open(system_information, "a") as f:
        f.write(f"System: {platform.system()} {platform.version()}\n")
        f.write(f"Machine: {platform.machine()}\n")
        f.write(f"Processor: {platform.processor()}\n")
        f.write(f"Node Name: {platform.node()}\n")
        f.write(f"Release: {platform.release()}\n\n")

get_system_info()
