class DeauthDetector:
    def __init__(self):
        self.alerts = []

    def start(self, interface, timeout):
        print(f"[*] Simulando detección de deauth en {interface} por {timeout}s...")
        # Simulamos que no encontramos ataques
        self.alerts = []
        print("[✓] Simulación terminada. Sin ataques detectados (modo demo).")
