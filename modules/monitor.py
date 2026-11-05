"""Gestión de modo monitor con airmon-ng (Linux/Kali)."""
import subprocess
import re

def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def list_interfaces():
    out = _run(["iwconfig"]).stdout
    return re.findall(r"^(\w+)\s+IEEE 802\.11", out, re.MULTILINE)

def enable_monitor(interface):
    print(f"[*] Deteniendo servicios que interfieren (NetworkManager, wpa_supplicant)...")
    _run(["sudo", "airmon-ng", "check", "kill"])

    print(f"[*] Activando modo monitor en {interface}...")
    r = _run(["sudo", "airmon-ng", "start", interface])
    print(r.stdout)

    m = re.search(r"monitor mode (?:vif )?enabled on (\w+)", r.stdout)
    if m:
        mon_iface = m.group(1)
        print(f"[✓] Interfaz en modo monitor: {mon_iface}")
        return mon_iface
    print("[!] No se pudo activar modo monitor.")
    return None

def disable_monitor(interface):
    print(f"[*] Deteniendo modo monitor en {interface}...")
    _run(["sudo", "airmon-ng", "stop", interface])
    _run(["sudo", "systemctl", "restart", "NetworkManager"])
    print("[✓] Modo monitor desactivado.")
