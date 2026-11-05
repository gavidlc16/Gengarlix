def scan_networks():
    print("[*] Simulando escaneo (modo demo)...")
    return [
        {"ssid": "Mi_WiFi_Casa", "bssid": "00:11:22:33:44:55", "signal": -45, "security": "WPA2"},
        {"ssid": "Vecino_5G", "bssid": "AA:BB:CC:DD:EE:FF", "signal": -70, "security": "WPA3"},
        {"ssid": "Cafeteria_Gratis", "bssid": "11:22:33:44:55:66", "signal": -80, "security": "Abierta"}
    ]
