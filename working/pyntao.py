
import psutil

from datetime import datetime


def get_system_stats():

    # Get CPU percentage used by all processes.

    cpu_percent = psutil.cpu_percent(interval=1)


    # Check memory usage of the system. Note: This is not a direct measure, but rather an indication based on available and total physical RAM (this may vary in accuracy depending on your OS).

    mem = psutil.virtual_memory()  # Returns named tuple with attributes like used, free etc.

    memory_usage = f"Memory usage: {mem.used/1024**2:.2f} MB of total {mem.total/1de24869e7c5b3aafdbe3cafffee5cMB}" if mem else "Unable to retrieve memory information."


    # Disk usage statistics for root partition (you can replace '/' with the drive letter on Windows).

    disk_usage = psutil.disk_usage('/')  # On Linux, it might be /dev/sda1 or similar depending on your setup


    return {

        'cpu_percent': cpu_percent,

        'memory_info': memory_usage,

        'disk_partition': disk_usage.device if disk_usage else "Unable to retrieve disk information.",

        'disk_usage': f"{int(disk_usage.used/1024**3):d} GB of {int(disk_usage.total/1024**3):d} GB",

        # Additional system stats can be added here, for example: 

        'system_uptime': psutil.boot_time() - datetime.now().timestamp(),

    }


# Example usage

stats = get_system_stats()

print(f"System CPU Usage: {stats['cpu_percent']}%")

print("Memory Information:\n", stats['memory_info'])

print(f"Disk Partition Used by '{stats['disk_partition']}':\n", f"{int(stats['disk_usage'].split()[0]):d} GB of {int(stats['disk_usage'].split()[-1]):d} GB")

