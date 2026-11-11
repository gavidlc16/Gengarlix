from scapy.all import sniff, Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeResp
import subprocess


def set_channel(interface, channel):
    subprocess.run(['iw', 'dev', interface, 'set', 'channel', str(channel)],
                   capture_output=True)


def scan_networks(interface, timeout=30):
    networks = {}

    def packet_handler(pkt):
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            bssid = pkt[Dot11].addr3
            try:
                ssid = pkt[Dot11Elt].info.decode(errors='ignore') or '<oculta>'
            except Exception:
                ssid = '<oculta>'
            try:
                channel = int(ord(pkt[Dot11Elt:3].info))
            except Exception:
                channel = 0

            crypto = 'Desconocido'
            try:
                stats = pkt[Dot11Beacon].network_stats()
                crypto = str(stats.get('crypto', 'Abierta'))
            except Exception:
                pass

            if bssid not in networks:
                networks[bssid] = {
                    'ssid': ssid,
                    'bssid': bssid,
                    'channel': channel,
                    'crypto': crypto,
                }

    print(f"[*] Escaneando en {interface} durante {timeout}s...")
    sniff(iface=interface, prn=packet_handler, timeout=timeout, store=0)
    return list(networks.values())


def scan_clients(interface, bssid, timeout=30):
    clients = set()

    def packet_handler(pkt):
        if pkt.haslayer(Dot11) and pkt[Dot11].addr3 == bssid:
            a1, a2 = pkt[Dot11].addr1, pkt[Dot11].addr2
            if a1 != 'ff:ff:ff:ff:ff:ff' and a1 != bssid:
                clients.add(a1)
            if a2 != 'ff:ff:ff:ff:ff:ff' and a2 != bssid:
                clients.add(a2)

    print(f"[*] Buscando clientes conectados a {bssid} ({timeout}s)...")
    sniff(iface=interface, prn=packet_handler, timeout=timeout, store=0)
    return list(clients)
