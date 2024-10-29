import subprocess
import re

wifi_networks = re.findall(r'ssid="([^"]+)"',subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode().strip())
for network in wifi_networks:
    print(network)