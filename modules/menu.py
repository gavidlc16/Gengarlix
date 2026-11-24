#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

PURPLE, BOLD = "\033[35m", "\033[1m"
CYAN, RED, GREEN, YELLOW, ORANGE, RESET = (
    "\033[36m", "\033[31m", "\033[32m", "\033[33m", "\033[38;5;208m", "\033[0m"
)

ANCHO = 78

def limpiar():
    os.system("clear" if os.name != "nt" else "cls")

def linea(char="-", color=PURPLE):
    print(f"{color}{char * ANCHO}{RESET}")

def titulo(texto):
    relleno = max(0, (ANCHO - len(texto) - 2) // 2)
    print(f"{PURPLE}{BOLD}{'*' * relleno} {texto} {'*' * relleno}{RESET}")


class EstadoSesion:
    def __init__(self):
        self.reset()

    def reset(self):
        self.interface = None
        self.modo = "Managed"
        self.bandas = "2.4Ghz"
        self.bssid = None
        self.essid = None
        self.canal = None
        self.redes = []
        self.clientes = []
        self.pcap = None
        self.password = None
        self.ai_text = None
        self.alerts = []
        # FIX: Apuntar a la lista base real
        self.wordlist = "wordlists/gengar_passwords.txt"
        self.report = "reports/audit.md"

    def resumen(self):
        iface = self.interface if self.interface else f"{RED}ninguna{CYAN}"
        print(f"{CYAN}Interfaz {BOLD}{iface}{RESET}{CYAN} seleccionada. Modo: "
              f"{BOLD}{self.modo}{RESET}{CYAN}. Bandas: {self.bandas}{RESET}")
        print(f"{CYAN}BSSID seleccionado: {YELLOW + self.bssid if self.bssid else RESET + 'Ninguno'}{RESET}")
        print(f"{CYAN}Canal seleccionado: {YELLOW + str(self.canal) if self.canal else RESET + 'Ninguno'}{RESET}")
        print(f"{CYAN}ESSID seleccionado: {YELLOW + self.essid if self.essid else RESET + 'Ninguno'}{RESET}")
        print()


OPCIONES = [
    ("0", "Salir del script", None),
    ("1", "Seleccionar otra interfaz de red", "interfaz"),
    ("2", "Poner interfaz en modo monitor", "monitor_on"),
    ("3", "Poner interfaz en modo managed", "monitor_off"),
    ("4", "Explorar redes objetivo (necesita modo monitor)", "scan"),
    ("SEP", "Reconocimiento", None),
    ("5", "Escanear clientes conectados al objetivo", "clientes"),
    ("SEP", "Ataques activos", None),
    ("6", "Ataque deauth (forzar reconexión)", "deauth"),
    ("7", "Capturar handshake WPA/WPA2", "handshake"),
    ("8", "Capturar PMKID (clientless)", "pmkid"),
    ("SEP", "Cracking", None),
    ("9", "Crackear handshake con diccionario", "crack_handshake"),
    ("10", "Crackear PMKID con diccionario", "crack_pmkid"),
    ("SEP", "Análisis y reporte", None),
    ("11", "Detector de deauth (evidencia real)", "detect_deauth"),
    ("12", "Análisis con IA (Ollama)", "ai"),
    ("13", "Generar reporte en Markdown", "reporte"),
]


def mostrar_menu(estado, banner_fn=None):
    limpiar()
    if banner_fn: banner_fn()
    titulo("Gengarlix - Menú principal")
    estado.resumen()
    print(f"{CYAN}{BOLD}Selecciona una opción del menú:{RESET}")
    linea()
    for num, texto, _ in OPCIONES:
        if num == "SEP":
            print(f"{PURPLE}{'-' * 15} ({texto}) {'-' * 15}{RESET}")
            continue
        color = GREEN if num == "0" else YELLOW
        print(f"{color}{num}.{' ' if len(num) == 2 else '  '}{RESET}{texto}")
    linea()
    print(f"{ORANGE}*Hint*{RESET} Selecciona una interfaz y ponla en modo monitor antes de explorar.\n")
    try:
        return input(f"{PURPLE}{BOLD}gengarlix >{RESET} ").strip()
    except (KeyboardInterrupt, EOFError):
        return "0"


def listar_redes(redes):
    limpiar()
    titulo("Redes detectadas")
    print(f"{CYAN}{'#':<4}{'BSSID':<20}{'PWR':<6}{'CH':<4}{'ENC':<10}{'CLI':<5}ESSID{RESET}")
    linea()
    for i, r in enumerate(redes, start=1):
        tiene_clientes = r.get("clientes", 0) > 0
        marca = f"{ORANGE}*{RESET}" if tiene_clientes else " "
        pwr = r.get("signal", 0)
        color_essid = ORANGE if tiene_clientes else RESET
        print(f"{marca} {i:>2})  {r['bssid']:<20}{pwr!s:<6}"
              f"{r.get('channel', '?')!s:<4}{r.get('crypto', '?'):<10}"
              f"{r.get('clientes', 0)!s:<5}{color_essid}{r['ssid']}{RESET}")
    linea()
    print(f"{ORANGE}(*){RESET} Red con clientes detectados\n")
    sel = input(f"{CYAN}Selecciona la red objetivo (0 para volver) >{RESET} ").strip()
    try:
        idx = int(sel)
    except ValueError:
        return None
    if idx <= 0 or idx > len(redes):
        return None
    return redes[idx - 1]


def pausar():
    try:
        input(f"\n{CYAN}Presiona Enter para continuar...{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass


def _pedir_entero(mensaje, default, min_val=None, max_val=None):
    while True:
        try:
            val = input(f"{CYAN}{mensaje} [{default}] >{RESET} ").strip()
            if not val: return default
            n = int(val)
            if min_val is not None and n < min_val:
                print(f"{RED}[!] Valor mínimo: {min_val}{RESET}")
                continue
            if max_val is not None and n > max_val:
                print(f"{RED}[!] Valor máximo: {max_val}{RESET}")
                continue
            return n
        except ValueError:
            print(f"{RED}[!] Introduce un número entero.{RESET}")
        except (KeyboardInterrupt, EOFError):
            return default


def ejecutar_accion(accion, estado):
    if accion == "interfaz":
        from modules.monitor import list_interfaces
        ifaces = list_interfaces()
        if not ifaces:
            print(f"{RED}[!] No se detectaron interfaces Wi-Fi.{RESET}")
        else:
            for i, iface in enumerate(ifaces, 1):
                print(f"{YELLOW}{i}){RESET} {iface}")
            while True:
                try:
                    sel = input(f"{CYAN}Elige interfaz (0 cancela) >{RESET} ").strip()
                    if sel == "0": break
                    estado.interface = ifaces[int(sel) - 1]
                    estado.modo = ("Monitor" if estado.interface.endswith("mon") else "Managed")
                    break
                except (ValueError, IndexError):
                    print(f"{RED}[!] Selección inválida.{RESET}")
                except (KeyboardInterrupt, EOFError):
                    break
        pausar()
        return

    if accion == "monitor_on":
        if not estado.interface: print(f"{RED}[!] Selecciona antes una interfaz.{RESET}")
        else:
            from modules.monitor import enable_monitor
            mon = enable_monitor(estado.interface)
            if mon:
                estado.interface = mon
                estado.modo = "Monitor"
        pausar()
        return

    if accion == "monitor_off":
        if not estado.interface: print(f"{RED}[!] Selecciona antes una interfaz.{RESET}")
        else:
            from modules.monitor import disable_monitor
            disable_monitor(estado.interface)
            estado.modo = "Managed"
        pausar()
        return

    if accion == "scan":
        if not estado.interface:
            print(f"{RED}[!] Necesitas una interfaz en modo monitor.{RESET}")
            pausar()
            return
        from modules.scanner import scan_networks
        timeout = _pedir_entero("Duración del escaneo en segundos", 20, min_val=1)
        estado.redes = scan_networks(estado.interface, timeout=timeout)
        if not estado.redes:
            print(f"{RED}[!] No se detectaron redes.{RESET}")
            pausar()
            return
        objetivo = listar_redes(estado.redes)
        if objetivo:
            estado.bssid = objetivo["bssid"]
            estado.essid = objetivo["ssid"]
            estado.canal = objetivo.get("channel")
        return

    if accion == "clientes":
        if not (estado.interface and estado.bssid):
            print(f"{RED}[!] Necesitas interfaz y un objetivo seleccionado.{RESET}")
        else:
            from modules.scanner import scan_clients
            timeout = _pedir_entero("Duración del escaneo en segundos", 20, min_val=1)
            estado.clientes = scan_clients(estado.interface, estado.bssid, timeout=timeout)
            print(f"{GREEN}[✓] {len(estado.clientes)} cliente(s) detectado(s):{RESET}")
            for c in estado.clientes: print(f"  {c}")
        pausar()
        return

    if accion == "deauth":
        if not (estado.interface and estado.bssid):
            print(f"{RED}[!] Necesitas interfaz y un objetivo seleccionado.{RESET}")
        else:
            from modules.deauth import send_deauth
            try:
                cliente = input(f"{CYAN}MAC del cliente (Enter = broadcast) >{RESET} ").strip()
            except (KeyboardInterrupt, EOFError):
                cliente = ""
            send_deauth(estado.interface, estado.bssid, client=cliente or "ff:ff:ff:ff:ff:ff", channel=estado.canal)
        pausar()
        return

    if accion == "handshake":
        if not (estado.interface and estado.bssid):
            print(f"{RED}[!] Necesitas interfaz y un objetivo seleccionado.{RESET}")
        else:
            from modules.capture import HandshakeCapture
            timeout = _pedir_entero("Timeout de captura en segundos", 60, min_val=1)
            hc = HandshakeCapture(estado.bssid)
            estado.pcap = hc.capture(estado.interface, timeout=timeout, deauth_every=5)
        pausar()
        return

    if accion == "pmkid":
        if not (estado.interface and estado.bssid and estado.canal):
            print(f"{RED}[!] Necesitas interfaz, objetivo y canal.{RESET}")
        else:
            from modules.capture import capture_pmkid
            timeout = _pedir_entero("Timeout de captura en segundos", 60, min_val=1)
            estado.pcap = capture_pmkid(estado.interface, estado.bssid, estado.canal, timeout=timeout)
        pausar()
        return

    if accion == "crack_handshake":
        if not estado.pcap:
            print(f"{RED}[!] No hay ningún pcap capturado todavía.{RESET}")
        else:
            from modules.cracker import crack_handshake_aircrack
            try:
                wl = input(f"{CYAN}Wordlist [{estado.wordlist}] >{RESET} ").strip() or estado.wordlist
            except (KeyboardInterrupt, EOFError):
                wl = estado.wordlist
            estado.password = crack_handshake_aircrack(estado.pcap, wl, estado.bssid)
            print(f"{GREEN}{estado.password}{RESET}")
        pausar()
        return

    if accion == "crack_pmkid":
        if not estado.pcap:
            print(f"{RED}[!] No hay ningún pcap/hash capturado todavía.{RESET}")
        else:
            from modules.cracker import crack_pmkid_hashcat
            try:
                wl = input(f"{CYAN}Wordlist [{estado.wordlist}] >{RESET} ").strip() or estado.wordlist
            except (KeyboardInterrupt, EOFError):
                wl = estado.wordlist
            estado.password = crack_pmkid_hashcat(estado.pcap, wl)
            print(f"{GREEN}{estado.password}{RESET}")
        pausar()
        return

    if accion == "detect_deauth":
        if not estado.interface:
            print(f"{RED}[!] Necesitas una interfaz en modo monitor.{RESET}")
            pausar()
            return
        from modules.detector import DeauthDetector
        timeout = _pedir_entero("Duración de la detección en segundos", 20, min_val=1)
        # FIX: try/except para que no se caiga el menú
        try:
            det = DeauthDetector(threshold=10, window=10)
            estado.alerts = det.start(estado.interface, timeout=timeout)
            if estado.alerts:
                print(f"{GREEN}[✓] {len(estado.alerts)} alerta(s) registrada(s).{RESET}")
            else:
                print(f"{YELLOW}[i] No se detectaron ataques deauth.{RESET}")
        except Exception as e:
            print(f"{RED}[!] Error en el detector: {e}{RESET}")
        pausar()
        return

    if accion == "ai":
        from modules.ai_analyzer import analyze
        print(f"{CYAN}[*] Consultando a Ollama...{RESET}")
        if not estado.alerts and estado.interface:
            from modules.detector import DeauthDetector
            # FIX: try/except para que no se caiga
            try:
                det = DeauthDetector(threshold=10, window=10)
                estado.alerts = det.start(estado.interface, timeout=15)
            except Exception:
                pass
        estado.ai_text = analyze(estado.redes, estado.alerts)
        print(estado.ai_text)
        pausar()
        return

    if accion == "reporte":
        from gengarlix import generar_reporte
        try:
            ruta = input(f"{CYAN}Ruta del reporte [{estado.report}] >{RESET} ").strip() or estado.report
        except (KeyboardInterrupt, EOFError):
            ruta = estado.report
        generar_reporte(ruta, estado.redes, estado.pcap, estado.password, estado.ai_text, estado.alerts)
        pausar()
        return


def iniciar(banner_fn=None):
    estado = EstadoSesion()
    while True:
        opcion = mostrar_menu(estado, banner_fn=banner_fn)
        if opcion == "0":
            limpiar()
            print(f"{GREEN}[✓] ¡Hasta la próxima auditoría!{RESET}")
            break
        accion = next((a for n, _, a in OPCIONES if n == opcion), "__invalida__")
        if accion == "__invalida__":
            print(f"{RED}[!] Opción inválida.{RESET}")
            pausar()
            continue
        ejecutar_accion(accion, estado)
