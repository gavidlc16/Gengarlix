import subprocess
import os


def validate_capture(pcap):
    if not os.path.exists(pcap):
        return False, "El archivo pcap no existe."
    result = subprocess.run(['aircrack-ng', pcap],
                            capture_output=True, text=True)
    return True, result.stdout[-500:]


def crack_handshake(pcap, wordlist, tool='aircrack-ng', bssid=None):
    if not os.path.exists(wordlist):
        return False, "Wordlist no encontrada."
    if not os.path.exists(pcap):
        return False, "Archivo pcap no encontrado."

    if tool == 'aircrack-ng':
        cmd = ['aircrack-ng', '-w', wordlist]
        if bssid:
            cmd += ['-b', bssid]
        cmd.append(pcap)
    elif tool == 'hashcat':
        hccapx = pcap.rsplit('.', 1)[0] + '.hccapx'
        subprocess.run(['hcxpcapngtool', '-o', hccapx, pcap],
                       capture_output=True)
        if not os.path.exists(hccapx):
            return False, "No se pudo convertir el pcap a hccapx."
        cmd = ['hashcat', '-m', '22000', '-a', '0', hccapx, wordlist, '--force']
    else:
        return False, f"Herramienta desconocida: {tool}"

    print(f"[*] Ejecutando: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=7200)
        return True, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout alcanzado."
