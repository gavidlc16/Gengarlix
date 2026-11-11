from scapy.all import sniff, wrpcap, Dot11, EAPOL
import subprocess
import os

class HandshakeCapture:
    def __init__(self, bssid):
        self.bssid = bssid.lower()
        self.packets = []
        self.eapol_count = 0

    def _packet_handler(self, pkt):
        if pkt.haslayer(EAPOL) and (pkt[Dot11].addr3 == self.bssid or pkt[Dot11].addr1 == self.bssid):
            self.packets.append(pkt)
            self.eapol_count += 1
            print(f"[+] EAPOL capturado ({self.eapol_count}/4)")

    def capture(self, interface, timeout=60, deauth_every=5, output='handshake.pcap'):
        print(f"[*] Capturando handshake para {self.bssid} en {interface}...")
        try:
            sniff(iface=interface, prn=self._packet_handler, timeout=timeout, store=0,
                  stop_filter=lambda p: self.eapol_count >= 4)
        except Exception as e:
            print(f"[!] Error durante la captura: {e}")
            return None

        if self.packets:
            wrpcap(output, self.packets)
            print(f"[+] Handshake guardado en {output}")
            return output
        print("[-] No se capturó ningún handshake. Intenta forzar reconexión con --deauth.")
        return None

def capture_pmkid(interface, bssid, channel, timeout=60, output='pmkid.pcap'):
    print(f"[*] Capturando PMKID para {bssid} en canal {channel}...")
    subprocess.run(['iw', 'dev', interface, 'set', 'channel', str(channel)], capture_output=True)
    
    packets = []
    def handler(pkt):
        if pkt.haslayer(EAPOL) and pkt[Dot11].addr3 == bssid:
            packets.append(pkt)

    sniff(iface=interface, prn=handler, timeout=timeout, store=0)

    if not packets:
        print("[-] No se capturó PMKID.")
        return None

    wrpcap(output, packets)
    hash_file = output.replace('.pcap', '.16800')
    subprocess.run(['hcxpcapngtool', '-o', hash_file, output], capture_output=True)
    
    if os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
        print(f"[+] Hash PMKID extraído: {hash_file}")
        return hash_file
    print(f"[!] Capturado en {output} pero no se pudo extraer el hash.")
    return output
