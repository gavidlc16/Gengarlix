from scapy.all import sniff, Dot11, Dot11Deauth
from collections import defaultdict
import time


class DeauthDetector:
    def __init__(self, threshold=10, window=10):
        self.threshold = threshold
        self.window = window
        self.alerts = []
        self.counts = defaultdict(list)

    def _handler(self, pkt):
        if pkt.haslayer(Dot11Deauth):
            bssid = pkt[Dot11].addr3
            now = time.time()
            self.counts[bssid] = [t for t in self.counts[bssid]
                                  if now - t < self.window]
            self.counts[bssid].append(now)

            if len(self.counts[bssid]) >= self.threshold:
                alert = (f"Posible ataque deauth en {bssid} "
                         f"({len(self.counts[bssid])} tramas en {self.window}s)")
                if alert not in self.alerts:
                    self.alerts.append(alert)
                    print(f"[!] {alert}")

    def start(self, interface, timeout=60):
        print(f"[*] Detectando deauth en {interface} durante {timeout}s...")
        sniff(iface=interface, prn=self._handler, timeout=timeout, store=0)
        return self.alerts
