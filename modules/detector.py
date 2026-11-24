from scapy.all import sniff, Dot11, Dot11Deauth
from collections import defaultdict
import time


class DeauthDetector:
    def __init__(self, threshold=10, window=10):
        self.threshold = threshold
        self.window = window
        self.alerts = []
        self._alert_keys = set()
        self.counts = defaultdict(list)

    def _cleanup(self, now):
        """Limpia BSSIDs sin actividad reciente para evitar fugas de memoria."""
        for bssid in list(self.counts.keys()):
            self.counts[bssid] = [t for t in self.counts[bssid] if now - t < self.window]
            if not self.counts[bssid]:
                del self.counts[bssid]

    def _handler(self, pkt):
        if not pkt.haslayer(Dot11Deauth):
            return
        bssid = pkt[Dot11].addr3
        if not bssid:
            return

        now = time.time()
        self.counts[bssid] = [t for t in self.counts[bssid] if now - t < self.window]
        self.counts[bssid].append(now)

        if len(self.counts[bssid]) >= self.threshold:
            # Bucket temporal para evitar alertas repetidas en la misma ventana
            bucket = int(now // self.window)
            key = (bssid, bucket)
            if key not in self._alert_keys:
                self._alert_keys.add(key)
                alert = (f"Posible ataque deauth en {bssid} "
                         f"({len(self.counts[bssid])} tramas en {self.window}s)")
                self.alerts.append(alert)
                print(f"[!] {alert}")

    def start(self, interface, timeout=60):
        print(f"[*] Detectando deauth en {interface} durante {timeout}s...")
        try:
            sniff(iface=interface, prn=self._handler, timeout=timeout, store=0)
        finally:
            self._cleanup(time.time())
        return self.alerts
