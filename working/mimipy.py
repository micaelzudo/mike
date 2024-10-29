import psutil
import platform
import sys
import os

print("System Information:")
print("-------------------")
print(f"Platform: {platform.system()}")
print(f"Version: {platform.release()}")
print(f"Processor: {platform.processor()}")
print(f"Total Memory: {(psutil.virtual_memory().total / (1024.0 **3)): .2f} GB")

print("\nSystem Statistics:")
print("-------------------")
print(f"Uptime: {psutil.boot_time():.24f}") 
print(f"CPU Count: {psutil.cpu_count()}")
sys.stdout.flush()