from scapy.all import sniff, Dot11, Dot11Beacon, Dot11Elt

def scan_networks(interface, timeout=30):
    redes = {}
    def _pkt(pkt):
        if pkt.haslayer(Dot11Beacon):
            bssid = pkt[Dot11].addr3
            ssid = pkt[Dot11Elt].info.decode(errors="ignore")
            canal = int(ord(pkt[Dot11Elt:3].info))
            redes[bssid] = {"ssid": ssid, "bssid": bssid, "canal": canal}
    sniff(iface=interface, prn=_pkt, timeout=timeout, store=0)
    return list(redes.values())
