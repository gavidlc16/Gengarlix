"""Ataque de diccionario con aircrack-ng o hashcat."""
import os
import shutil
import subprocess
import re

def _has(binary):
    return shutil.which(binary) is not None

def crack_handshake_aircrack(pcap, wordlist, bssid=None):
    if not _has("aircrack-ng"):
        print("[!] aircrack-ng no instalado. sudo apt install aircrack-ng")
        return None
    if not os.path.exists(pcap) or not os.path.exists(wordlist):
        print("[!] Archivo no encontrado (pcap o wordlist)")
        return None

    cmd = ["aircrack-ng", "-w", wordlist, pcap]
    if bssid:
        cmd = ["aircrack-ng", "-b", bssid, "-w", wordlist, pcap]

    print(f"[*] Ejecutando: {' '.join(cmd)}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        out = r.stdout + r.stderr
        print(out)

        if "KEY FOUND" in out:
            m = re.search(r"KEY FOUND!\s*\[\s*(.+?)\s*\]", out)
            if m:
                pw = m.group(1)
                print(f"[✓] CONTRASEÑA: {pw}")
                return pw
        print("[!] No encontrada en la wordlist.")
        return None
    except subprocess.TimeoutExpired:
        print("[!] Timeout.")
        return None

def crack_pmkid_hashcat(pcap, wordlist):
    if not _has("hashcat"):
        print("[!] hashcat no instalado.")
        return None
    if not _has("hcxpcapngtool"):
        print("[!] hcxtools no instalado. sudo apt install hcxtools")
        return None

    hashfile = pcap.replace(".pcap", ".16800")
    subprocess.run(["hcxpcapngtool", "-o", hashfile, pcap], capture_output=True)

    if not os.path.exists(hashfile):
        print("[!] No se pudo generar hash PMKID.")
        return None

    print(f"[*] Crackeando {hashfile} con hashcat...")
    cmd = ["hashcat", "-m", "22000", hashfile, wordlist, "--force", "--potfile-disable", "--quiet"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        print(r.stdout)

        show = subprocess.run(["hashcat", "-m", "22000", hashfile, "--show"], capture_output=True, text=True)
        if show.stdout.strip():
            for line in show.stdout.splitlines():
                if ":" in line:
                    pw = line.rsplit(":", 1)[-1]
                    print(f"[✓] CONTRASEÑA: {pw}")
                    return pw
        return None
    except subprocess.TimeoutExpired:
        print("[!] Timeout.")
        return None
