import os
import re
import subprocess
from shutil import which

def check_root():
    if os.geteuid() != 0:
        raise PermissionError("Este módulo requiere permisos de root (sudo).")

def _run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError as e:
        return 127, "", str(e)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:
        return 1, "", str(e)

def list_interfaces():
    rc, out, _ = _run(['iw', 'dev'])
    if rc != 0: return []
    return re.findall(r'Interface (\w+)', out)

def supports_monitor(interface):
    rc, out, _ = _run(['iw', 'list'])
    if rc != 0: return True
    return '* monitor' in out

def enable_monitor(interface):
    check_root()

    if not supports_monitor(interface):
        print(f"[!] {interface} no reporta soporte de modo monitor.")

    if which('airmon-ng'):
        _run(['airmon-ng', 'check', 'kill'])
        rc, out, _ = _run(['airmon-ng', 'start', interface])
        print(out)
        
        # FIX: Aceptar formato viejo y nuevo (con [phy0] adelante)
        patrones = [
            r'monitor mode enabled on\s+(\S+?)\)?$',
            r'monitor mode vif enabled for \S+ on \[?\S*?\]?(\S+?)\)?$',
            r'\b(\w+mon\d*)\)',
        ]
        mon_iface = None
        for patron in patrones:
            m = re.search(patron, out, re.MULTILINE)
            if m:
                mon_iface = m.group(1).strip().rstrip(',')
                break
                
        if mon_iface:
            _run(['ip', 'link', 'set', mon_iface, 'up'])
            return mon_iface

    print(f"[*] Usando fallback iw para {interface}...")
    _run(['ip', 'link', 'set', interface, 'down'])
    rc, _, err = _run(['iw', 'dev', interface, 'set', 'type', 'monitor'])
    if rc != 0:
        print(f"[!] No se pudo poner en modo monitor: {err.strip()}")
        _run(['ip', 'link', 'set', interface, 'up'])
        return None
    _run(['ip', 'link', 'set', interface, 'up'])
    return interface


def disable_monitor(interface):
    check_root()
    if interface.endswith('mon') and which('airmon-ng'):
        _run(['airmon-ng', 'stop', interface])
        print(f"[+] Modo monitor desactivado en {interface}")
        return

    _run(['ip', 'link', 'set', interface, 'down'])
    rc, _, err = _run(['iw', 'dev', interface, 'set', 'type', 'managed'])
    _run(['ip', 'link', 'set', interface, 'up'])
    if rc == 0: print(f"[+] Modo managed restaurado en {interface}")
    else: print(f"[!] No se pudo restaurar managed: {err.strip()}")
