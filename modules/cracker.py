import os
import re
import shutil
import subprocess

_KEY_RE = re.compile(r'KEY FOUND!\s*\[\s*(.+?)\s*\]', re.IGNORECASE)
_HASHCAT_CRACKED_RE = re.compile(r'^([0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:.+?):(.+)$')


def _tool_available(name):
    return shutil.which(name) is not None

def validate_capture(pcap):
    if not os.path.exists(pcap):
        return False, "El archivo pcap no existe."
    if not _tool_available('aircrack-ng'):
        return False, "aircrack-ng no está instalado."
    try:
        r = subprocess.run(['aircrack-ng', pcap], capture_output=True, text=True, timeout=30)
        return True, r.stdout[-500:]
    except Exception as e:
        return False, f"Error al validar pcap: {e}"

def _run_streaming(cmd, on_line=None):
    output_lines = []
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert process.stdout is not None
    for line in process.stdout:
        output_lines.append(line)
        print(line, end='')
        if on_line: on_line(line)
    process.wait()
    return process.returncode, "".join(output_lines)


def crack_handshake_aircrack(pcap, wordlist, bssid=None, rules=None):
    if not os.path.exists(pcap): return "[!] Archivo pcap no encontrado."
    if not os.path.exists(wordlist): return "[!] Wordlist no encontrada."
    if not _tool_available('aircrack-ng'): return "[!] aircrack-ng no está instalado."

    if rules:
        print("[i] aircrack-ng no soporta reglas hashcat; se ignora --rules.")

    cmd = ['aircrack-ng', '-w', os.path.abspath(wordlist)]
    if bssid: cmd += ['-b', bssid]
    cmd.append(os.path.abspath(pcap))

    print(f"[*] Ejecutando aircrack-ng...")
    found = {"key": None}

    def on_line(line):
        m = _KEY_RE.search(line)
        if m: found["key"] = m.group(1)

    try:
        rc, _ = _run_streaming(cmd, on_line=on_line)
    except Exception as e:
        return f"[!] Error al ejecutar aircrack-ng: {e}"

    if found["key"]: return f"[+] Contraseña encontrada: {found['key']}"
    if rc != 0: return "[!] aircrack-ng falló o fue interrumpido."
    return "[-] Ataque finalizado sin encontrar la clave."


def crack_pmkid_hashcat(pcap, wordlist, rules=None, combinator=None, hybrid_mask=None, hybrid_mode="suffix"):
    if not os.path.exists(pcap): return "[!] Archivo pcap no encontrado."
    if not os.path.exists(wordlist): return "[!] Wordlist no encontrada."
    if not _tool_available('hashcat'): return "[!] hashcat no está instalado."
    if not _tool_available('hcxpcapngtool'): return "[!] hcxpcapngtool no está instalado."

    # FIX: Extraer extensión correctamente
    base, _ = os.path.splitext(pcap)
    hash_file = base + '.16800'
    
    print("[*] Extrayendo hash PMKID con hcxpcapngtool...")
    subprocess.run(['hcxpcapngtool', '-o', hash_file, pcap], capture_output=True)

    if not os.path.exists(hash_file) or os.path.getsize(hash_file) == 0:
        return "[!] No se pudo extraer el hash PMKID."

    cmd = ['hashcat', '-m', '22000']
    hash_abs, wl_abs = os.path.abspath(hash_file), os.path.abspath(wordlist)

    if hybrid_mask:
        if hybrid_mode == "prefix":
            cmd += ['-a', '7', hash_abs, hybrid_mask, wl_abs]
        else:
            cmd += ['-a', '6', hash_abs, wl_abs, hybrid_mask]
    elif combinator:
        if not os.path.exists(combinator):
            return "[!] Wordlist de combinator no encontrada."
        cmd += ['-a', '1', hash_abs, wl_abs, os.path.abspath(combinator)]
    else:
        cmd += ['-a', '0', hash_abs, wl_abs]
        for rule_file in (rules or []):
            if not os.path.exists(rule_file):
                print(f"[!] Regla no encontrada, se omite: {rule_file}")
                continue
            cmd += ['-r', os.path.abspath(rule_file)]

    cmd.append('--force')
    print(f"[*] Ejecutando hashcat...")
    found = {"hash": None, "plain": None}

    def on_line(line):
        m = _HASHCAT_CRACKED_RE.search(line.strip())
        if m: found["hash"], found["plain"] = m.group(1), m.group(2)

    try:
        rc, _ = _run_streaming(cmd, on_line=on_line)
    except Exception as e:
        return f"[!] Error al ejecutar hashcat: {e}"

    # FIX: Buscar potfile en varias ubicaciones comunes
    potfiles = [
        os.path.expanduser("~/.local/share/hashcat/hashcat.potfile"),
        os.path.expanduser("~/Library/hashcat/hashcat.potfile"),
        os.path.expandvars(r"%APPDATA%\hashcat\hashcat.potfile")
    ]
    
    if not found["plain"]:
        for pot in potfiles:
            if os.path.exists(pot):
                try:
                    with open(pot, "r", errors="ignore") as f:
                        for line in f:
                            if ':' in line:
                                _, plain = line.rstrip("\n").split(':', 1)
                                found["plain"] = plain
                    break
                except Exception:
                    pass

    if found["plain"]: return f"[+] Contraseña encontrada: {found['plain']}"
    if rc != 0: return "[!] hashcat falló o fue interrumpido."
    return "[-] Ataque finalizado sin encontrar la clave."
