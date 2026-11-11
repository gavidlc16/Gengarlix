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
- **Modo Monitor:** Gestión de interfaces con `airmon-ng` e `iw`.
- **Escaneo:** Detección de redes y clientes (Scapy).
- **Ataques de Handshake:** Captura WPA/WPA2 forzando reconexión (Deauth).
- **Ataque PMKID:** Captura *clientless* sin esperar a que un cliente se conecte.
- **Cracking:** Integración con `aircrack-ng` y `hashcat`.
- **Análisis IA:** Consultas a Ollama local para resumir auditorías.
- **Reportes:** Generación automática de reportes en Markdown.
- **Wordlists:** Incluye un diccionario base y un script generador de contraseñas (mangling).

---

## 📦 Instalación y Requisitos

### 1. Dependencias del sistema (Kali Linux / Parrot OS)
* **`python3`** (versión 3.10 o superior)
* **`scapy`** (captura y análisis de paquetes)
* **`aircrack-ng`** (gestión de interfaces y crackeo)
* **`hcxtools`** y **`hashcat`** (para PMKID y crackeo avanzado)
* **`iw`** y **`net-tools`** (control de tarjetas de red)

### 2. Instalación Automática (Recomendada)
Hemos creado un script de instalación que configura el entorno virtual (para no romper tu Kali) e instala las dependencias y el comando global.

    git clone https://github.com/gavidlc16/Gengarlix.git
    cd Gengarlix
    chmod +x install.sh
    sudo ./install.sh

*Este script creará un comando global llamado `gengarlix` para que puedas usarlo desde cualquier carpeta.*

### 3. Instalación Manual (Si prefieres hacerlo paso a paso)
Si no quieres usar el script, puedes hacerlo manualmente:

    git clone https://github.com/gavidlc16/Gengarlix.git
    cd Gengarlix
    sudo apt update
    sudo apt install aircrack-ng hcxtools hashcat iw net-tools python3-venv -y
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

*(Nota: Si instalas manualmente, tendrás que activar el entorno virtual con `source venv/bin/activate` cada vez que uses la herramienta).*

### 4. Instalación de Ollama (Opcional, para Análisis IA)
Si deseas usar la función `--ai` para analizar los resultados automáticamente, necesitas tener **Ollama** instalado. Es un software 100% gratuito y open-source que ejecuta modelos de IA locales en tu propia computadora.

Instálalo en Kali Linux con el siguiente comando:

    curl -fsSL https://ollama.com/install.sh | sh

Luego, descarga un modelo de lenguaje (recomendamos `llama3` por su equilibrio entre rendimiento y velocidad):

    ollama pull llama3
    
*(Nota: El análisis con IA se ejecutará de forma local sin enviar datos a la nube, lo cual es ideal para la privacidad en auditorías).*

---

## 💀 Guía de Uso (Pentesting Autorizado en Linux)

Todas las herramientas de captura e inyección de paquetes requieren permisos de superusuario (`sudo`). Asegúrate de tener tu adaptador Wi-Fi conectado y compatible con modo monitor.

**Para ver el menú de ayuda en cualquier momento:**
    sudo gengarlix --help

### 1. Gestión del Modo Monitor
Para iniciar un pentest, primero debes poner tu tarjeta en modo monitor. Esto matará los procesos de red normales y creará una nueva interfaz (ej. `wlan0mon`).

    sudo gengarlix --monitor wlan0

*(Nota: Reemplaza `wlan0` por el nombre real de tu interfaz. Para volver a la normalidad, puedes usar `sudo airmon-ng stop wlan0mon`).*

### 2. Escaneo de Redes y Clientes
Escanea el espectro para encontrar objetivos (redes Wi-Fi y dispositivos conectados).

    # Escanear redes disponibles (BSSID, SSID, Canal, Señal)
    sudo gengarlix -i wlan0mon --scan --timeout 30

    # Ver clientes conectados a un AP específico
    sudo gengarlix -i wlan0mon --bssid AA:BB:CC:DD:EE:FF --clients

### 3. Ataques de Inyección (Deauth y Captura)
Fuerza la desconexión de los clientes para interceptar el saludo de autenticación (Handshake) o capturar el PMKID.

    # Enviar tramas de desautenticación manuales (Ataque de fuerza bruta)
    sudo gengarlix -i wlan0mon --bssid AA:BB:CC:DD:EE:FF --deauth

    # Capturar Handshake (incluye deauth automático para forzar reconexión)
    sudo gengarlix -i wlan0mon --bssid AA:BB:CC:DD:EE:FF --capture --timeout 120

    # Ataque PMKID (No necesita clientes conectados, es "Clientless")
    sudo gengarlix -i wlan0mon --bssid AA:BB:CC:DD:EE:FF --pmkid --timeout 60

### 4. Crackeo de Contraseñas
Una vez capturado el archivo `.pcap`, usa el ataque de diccionario con tu propia lista de contraseñas.

    # Crackear un Handshake capturado (usando aircrack-ng)
    sudo gengarlix --crack reports/handshake_AABBCCDDEEFF.pcap --wordlist wordlists/gengar_passwords_mangled.txt

    # Crackear un PMKID capturado (usando hashcat)
    sudo gengarlix --pmkid-crack reports/pmkid_AABBCCDDEEFF.pcap --wordlist wordlists/gengar_passwords_mangled.txt

### 5. Análisis con IA y Reportes
Genera un reporte final en Markdown con los hallazgos. Asegúrate de tener Ollama corriendo (`ollama serve`).

    # Escanear y analizar con IA (guardando reporte)
    sudo gengarlix -i wlan0mon --scan --ai --report reports/auditoria_final.md

---

## 🔤 Generación de Diccionarios (Wordlists)
El repositorio incluye un script llamado `mangler.py` que toma una lista de palabras base y la expande automáticamente con números, símbolos y mayúsculas (ej. `gengar` -> `Gengar2024!`).

    # Para generar tu propio diccionario masivo:
    python3 mangler.py

*(El resultado se guardará en `wordlists/gengar_passwords_mangled.txt`)*

---

## 📄 Licencia
Este proyecto está bajo la Licencia MIT.
