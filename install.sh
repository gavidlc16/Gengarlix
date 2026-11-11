#!/bin/bash

echo -e "\e[35m[*] Instalando Gengarlix...\e[0m"

# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install -y python3-full python3-venv aircrack-ng hashcat hcxtools iw wireless-tools

# 2. Crear el entorno virtual e instalar librerías
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 3. Crear el lanzador (Wrapper)
echo -e "\e[35m[*] Configurando el comando 'gengarlix'...\e[0m"
cat << EOF | sudo tee /usr/local/bin/gengarlix > /dev/null
#!/bin/bash
DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
sudo "\$DIR/venv/bin/python3" "\$DIR/gengarlix.py" "\$@"
EOF

# 4. Dar permisos
sudo chmod +x /usr/local/bin/gengarlix

echo -e "\e[32m[✓] ¡Instalación completada!\e[0m"
echo -e "Ahora puedes usar: \e[33msudo gengarlix --help\e[0m"
