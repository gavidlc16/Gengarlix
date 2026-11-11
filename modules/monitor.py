import subprocess
import re
import os


def check_root():
    if os.geteuid() != 0:
        raise PermissionError("Este módulo requiere permisos de root (sudo).")


def list_interfaces():
    result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
    return re.findall(r'Interface (\w+)', result.stdout)


def enable_monitor(interface):
    check_root()
    # Mata procesos que interfieren (NetworkManager, wpa_supplicant...)
    subprocess.run(['airmon-ng', 'check', 'kill'],
                   capture_output=True, text=True)

    result = subprocess.run(['airmon-ng', 'start', interface],
                            capture_output=True, text=True)
    print(result.stdout)

    match = re.search(r'(wlan\d+mon|\w+mon)', result.stdout)
    if match:
        mon_iface = match.group(1)
        subprocess.run(['ip', 'link', 'set', mon_iface, 'up'],
                       capture_output=True)
        return mon_iface

    # Fallback con iw
    subprocess.run(['ip', 'link', 'set', interface, 'down'], capture_output=True)
    subprocess.run(['iw', interface, 'set', 'type', 'monitor'], capture_output=True)
    subprocess.run(['ip', 'link', 'set', interface, 'up'], capture_output=True)
    return interface


def disable_monitor(interface):
    check_root()
    if interface.endswith('mon'):
        subprocess.run(['airmon-ng', 'stop', interface],
                       capture_output=True, text=True)
    else:
        subprocess.run(['ip', 'link', 'set', interface, 'down'], capture_output=True)
        subprocess.run(['iw', interface, 'set', 'type', 'managed'], capture_output=True)
        subprocess.run(['ip', 'link', 'set', interface, 'up'], capture_output=True)
    print(f"[+] Modo monitor desactivado en {interface}")
