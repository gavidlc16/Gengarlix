<div align="center">
  <h1>👻 Gengarlix 👻</h1>
  <img src="docs/screenshots/banner.png" alt="Banner de Gengarlix" width="100%">
  <p><b>Suite de auditoría Wi-Fi ofensiva con análisis local por IA</b></p>
  <p>
    <img src="https://img.shields.io/badge/python-3.10%2B-blue">
    <img src="https://img.shields.io/badge/license-MIT-green">
    <img src="https://img.shields.io/badge/status-beta-yellow">
    <img src="https://img.shields.io/badge/OS-Kali%20Linux-557C94">
  </p>
</div>

---

> [!WARNING]  
> **AVISO LEGAL:** Esta herramienta está diseñada exclusivamente para **auditorías éticas, laboratorios de práctica y entornos controlados**. El uso de estas funciones en redes sin autorización explícita es **ilegal**. El autor no se hace responsable del mal uso.

## 🚀 Características
- **Modo Monitor:** Gestión de interfaces con `airmon-ng`.
- **Escaneo:** Detección de redes y clientes (Scapy).
- **Ataques de Handshake:** Captura WPA/WPA2 forzando reconexión (Deauth).
- **Ataque PMKID:** Captura *clientless* sin esperar a que un cliente se conecte.
- **Cracking:** Integración con `aircrack-ng` y `hashcat`.
- **Análisis IA:** Consultas a Ollama local para resumir auditorías.
- **Reportes:** Generación automática de reportes en Markdown.

---

## 📦 Instalación y Requisitos

<details>
<summary><b>📦 Dependencias requeridas</b> (clic para expandir)</summary>

### Dependencias del sistema
* **`python3`** (versión 3.10 o superior)
* **`scapy`** (captura y análisis de paquetes)
* **`aircrack-ng`** (gestión de interfaces inalámbricas)
* **`hcxtools`** y **`hashcat`** (para PMKID y crackeo)
* **`iw`** y **`net-tools`** (control de tarjetas de red)

*Nota: Recomendado sobre sistemas operativos basados en Linux de ciberseguridad (Kali Linux / Parrot OS).*

</details>

### 📥 Instalación rápida

Clona el repositorio e instala las dependencias ejecutando:

    git clone https://github.com/gavidlc16/Gengarlix.git
    cd Gengarlix
    sudo apt update
    sudo apt install aircrack-ng hcxtools hashcat iw net-tools -y
    pip3 install -r requirements.txt

---

## 💀 Uso Ofensivo (Pentesting Autorizado)

| Flag | Descripción |
|---|---|
| `--monitor IFACE` | Activa modo monitor (ej. `--monitor wlan0`) |
| `--scan` | Escaneo de redes 802.11 |
| `--clients --bssid MAC` | Escaneo de clientes del AP |
| `--deauth --bssid MAC` | Envío manual de tramas deauth |
| `--capture --bssid MAC` | Captura de Handshake + deauth automático |
| `--pmkid --bssid MAC` | Captura PMKID (Clientless) |
| `--crack PCAP` | Crackeo de handshake (aircrack) |
| `--pmkid-crack PCAP` | Crackeo de PMKID (hashcat) |
| `--ai` | Análisis con IA local |

### ⚡ Flujo rápido de trabajo

    # 1. Activar modo monitor
    sudo python3 gengarlix.py --monitor wlan0

    # 2. Escanear redes
    sudo python3 gengarlix.py -i wlan0mon --scan

    # 3. Capturar handshake (automático con deauth)
    sudo python3 gengarlix.py -i wlan0mon --bssid AA:BB:CC:DD:EE:FF --capture

    # 4. Crackear
    python3 gengarlix.py --crack reports/handshake_AABBCCDDEEFF.pcap

---

## 📄 Licencia
Este proyecto está bajo la Licencia MIT.
