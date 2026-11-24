from scapy.all import (sniff, Dot11, Dot11Beacon, Dot11Elt,
                       Dot11ProbeResp, RadioTap)
import subprocess
import threading

DEFAULT_CHANNELS_24 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
DEFAULT_CHANNELS_5 = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112,
                      116, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161, 165]

def set_channel(interface, channel):
    try:
        subprocess.run(['iw', 'dev', interface, 'set', 'channel', str(channel)],
                       capture_output=True, check=False, timeout=15)
    except Exception:
        pass

def _hopper(interface, channels, stop_event, dwell=0.25):
    i = 0
    while not stop_event.is_set():
        set_channel(interface, channels[i % len(channels)])
        i += 1
        stop_event.wait(dwell)

def _freq_to_channel(freq):
    if 2412 <= freq <= 2484:
        return 14 if freq == 2484 else (freq - 2407) // 5
    if 5000 <= freq <= 5900:
        return (freq - 5000) // 5
    if 5955 <= freq <= 7115:
        return (freq - 5950) // 5
    return 0

def _obtener_canal(pkt):
    elt = pkt.getlayer(Dot11Elt)
    while elt:
        try:
            if elt.ID == 3 and len(elt.info) == 1:
                return ord(elt.info)
        except Exception:
            pass
        elt = elt.payload.getlayer(Dot11Elt)

    try:
        if pkt.haslayer(RadioTap):
            freq = getattr(pkt[RadioTap], 'ChannelFrequency', None)
            if freq:
                ch = _freq_to_channel(freq)
                if ch: return ch
    except Exception:
        pass
    return 0

def _detectar_crypto(pkt):
    crypto = set()
    elt = pkt.getlayer(Dot11Elt)
    while elt:
        try:
            if elt.ID == 48:  # RSN
                info = bytes(elt.info)
                if len(info) >= 8:
                    pair_count = int.from_bytes(info[6:8], 'little')
                    offset = 8 + pair_count * 4
                    akm_count = 0
                    if offset + 2 <= len(info):
                        akm_count = int.from_bytes(info[offset:offset+2], 'little')
                    crypto.add("WPA2")
                    akm_offset = offset + 2
                    for _ in range(akm_count):
                        if akm_offset + 4 <= len(info):
                            suite = info[akm_offset + 3]
                            if suite == 8: crypto.add("WPA3")
                            akm_offset += 4
            elif elt.ID == 221:  # Vendor WPA
                info = bytes(elt.info)
                if info.startswith(b'\x00\x50\xf2\x01'):
                    crypto.add("WPA")
        except Exception:
            pass
        elt = elt.payload.getlayer(Dot11Elt)

    if not crypto:
        try:
            if pkt[Dot11Beacon].cap & 0x10: crypto.add("WEP")
        except Exception:
            pass

    return '/'.join(sorted(crypto)) if crypto else "Abierta"


def scan_networks(interface, timeout=30, channels=None):
    channels = channels or (DEFAULT_CHANNELS_24 + DEFAULT_CHANNELS_5)
    networks = {}
    stop = threading.Event()
    hopper = threading.Thread(target=_hopper, args=(interface, channels, stop), daemon=True)
    hopper.start()

    def packet_handler(pkt):
        if not pkt.haslayer(Dot11): return
        dot11 = pkt[Dot11]

        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            bssid = dot11.addr3
            if not bssid: return
            bssid = bssid.lower()

            try:
                ssid = pkt[Dot11Elt].info.decode(errors='ignore') or '<oculta>'
            except Exception:
                ssid = '<oculta>'

            channel = _obtener_canal(pkt)
            crypto = _detectar_crypto(pkt)

            signal = 0
            try:
                if pkt.haslayer(RadioTap) and pkt.dBm_AntSignal is not None:
                    signal = pkt.dBm_AntSignal
            except Exception:
                pass

            if bssid not in networks:
                networks[bssid] = {
                    'ssid': ssid, 'bssid': bssid, 'channel': channel,
                    'crypto': crypto, 'signal': signal, 'clientes': 0,
                    '_clientes_set': set(),
                }
            else:
                # FIX: La señal más cercana a 0 es la MÁS FUERTE en dBm
                if signal != 0 and (networks[bssid]['signal'] == 0 or signal > networks[bssid]['signal']):
                    networks[bssid]['signal'] = signal

        # Contar clientes observando tramas Data (type=2)
        if dot11.type == 2:
            bssid_t = (dot11.addr3 or '').lower()
            a1 = (dot11.addr1 or '').lower()
            a2 = (dot11.addr2 or '').lower()
            if bssid_t in networks:
                for addr in (a1, a2):
                    if not addr or addr == 'ff:ff:ff:ff:ff:ff' or addr == bssid_t:
                        continue
                    try:
                        if int(addr.split(':')[0], 16) & 0x01: continue # multicast
                    except Exception:
                        continue
                    networks[bssid_t]['_clientes_set'].add(addr)

    print(f"[*] Escaneando en {interface} durante {timeout}s (hopping {len(channels)} canales)...")
    try:
        sniff(iface=interface, prn=packet_handler, timeout=timeout, store=0)
    finally:
        stop.set()
        hopper.join(timeout=2)

    result = []
    for n in networks.values():
        n['clientes'] = len(n.pop('_clientes_set', set()))
        result.append(n)
    return result


def scan_clients(interface, bssid, timeout=30, channels=None):
    channels = channels or (DEFAULT_CHANNELS_24 + DEFAULT_CHANNELS_5)
    clients = set()
    bssid_l = bssid.lower()

    stop = threading.Event()
    hopper = threading.Thread(target=_hopper, args=(interface, channels, stop), daemon=True)
    hopper.start()

    def packet_handler(pkt):
        if not pkt.haslayer(Dot11): return
        dot11 = pkt[Dot11]
        
        # FIX: Revisar todas las direcciones, no solo addr3
        addrs = [(dot11.addr1 or '').lower(), (dot11.addr2 or '').lower(), (dot11.addr3 or '').lower()]
        if bssid_l not in addrs:
            return
            
        for addr in addrs:
            if not addr or addr == 'ff:ff:ff:ff:ff:ff' or addr == bssid_l:
                continue
            try:
                if int(addr.split(':')[0], 16) & 0x01: continue # multicast
            except Exception:
                continue
            clients.add(addr)

    print(f"[*] Buscando clientes conectados a {bssid} ({timeout}s, hopping...)...")
    try:
        sniff(iface=interface, prn=packet_handler, timeout=timeout, store=0)
    finally:
        stop.set()
        hopper.join(timeout=2)
    return list(clients)
