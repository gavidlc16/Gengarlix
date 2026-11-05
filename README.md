<div align="center">
  <h1>👻 Gengarlix 👻</h1> 
  <img src="docs/screenshots/banner.png" alt="Banner de Gengarlix" width="100%">
  <p><b>Suite de auditoría Wi-Fi pasiva con análisis local por IA</b></p>
  <p>
    <img src="https://img.shields.io/badge/python-3.10%2B-blue">
    <img src="https://img.shields.io/badge/license-MIT-green">
    <img src="https://img.shields.io/badge/status-beta-yellow">
  </p>
</div>

---

## 🚀 Instalación y Requisitos

<details>
<summary><b>📦 Dependencias requeridas</b> (clic para expandir)</summary>

### Dependencias del sistema
* **`python3`** (versión 3.10 o superior)[cite: 5]
* **`scapy`** (para la captura y análisis de paquetes de red)
* **`aircrack-ng`** (para la gestión de interfaces inalámbricas en modo monitor)
* **`iw`** y **`net-tools`** (para el control de tarjetas de red)

*Nota: La mayoría de estas herramientas vienen preinstaladas en distribuciones enfocadas en ciberseguridad como **Kali Linux** o **Parrot OS**.*

</details>

<details>
<summary><b>🧩 Extensiones y herramientas opcionales</b> (clic para expandir)</summary>

* **`ollama`** *(Opcional)*: Requerido si deseas utilizar el análisis local por Inteligencia Artificial para explicar los hallazgos del escaneo.
* **`macchanger`** *(Opcional)*: Útil para la suplantación de direcciones MAC durante las auditorías.

</details>

---

### 📥 Instalación rápida

Clona el repositorio e instala las dependencias de Python ejecutando los siguientes comandos en tu terminal:

```bash
# 1. Clonar el repositorio
git clone [https://github.com/gavidlc16/gengarlix.git](https://github.com/gavidlc16/gengarlix.git)

# 2. Entrar a la carpeta del proyecto
cd gengarlix

# 3. Instalar dependencias requeridas
pip3 install -r requirements.txt
