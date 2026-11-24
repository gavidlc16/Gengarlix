#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gengarlix v1.1.0 - Suite ofensiva de auditoría Wi-Fi (pentesting ético)."""

import argparse
import os
import shutil
import sys
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PURPLE, BOLD = "\033[35m", "\033[1m"
CYAN, RED, GREEN, YELLOW, RESET = "\033[36m", "\033[31m", "\033[32m", "\033[33m", "\033[0m"


gengar = [
    "",
    "",
    "               =#*#+:",
    "               =*=+==*=.",
    "               =*=%@%+-*#-,",
    "               =#=#@@@@#-*%+:.",
    "               =#=#@@@@@@#==#%#*+:..:.     :=**+-=*.",
    "               :#-#@@@@@@@@%+-+-:=##-+%#%#*=-=*+-#+   ",
    "     -*+=:.    :#=*@@@@@@@@@@@*-*#=-*--=+#%@@@*=#%#+:",
    "   :#%#-=-=*#+.:#+=@@@@@@@@@@@@@@@@@@@@@@@@@@#.:---=#:",
    "   #=.+*%@@#+=-*%*:@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@%--+++++++++++++=======+#",
    "   %**-*@@@@@@@#=-:+==*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*==+-",
    "   :#*--*%@@@@@@@#-*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*-**.",
    "     :%%*=#@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#==*=",
    "       :#*-#@@@@@@@%+=%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*==--.",
    "         .*%-+-*@@@@@@@*+@#=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#==+.",
    "         =@#-+@@@@@@@%=%@@**@@@@@@@@@@@@@@@@@#=+%@@@@%-**:+=",
    "         +%++@@@@%+@@@+#@@*-#@@@@@@@@@@@@%*+*#+#@@@@@%::+##*+====-=:.",
    "         *%-#@@@@%--#@@*+#%#+%@@@@@@@@#+=#@@@%=%@@@@@%=+%##***+===--++:",
    "        .**=%@@@@%=#*=*%@@%%%@@@@@@#++**@@@@#=#@@@@@@@+#@@@@@@@@@@*::+#=",
    "        .*++@@@@@@*+#=**=*%@@@@@@@@@#==+*+=+#@@@@@@@@@@@@@@@@@@@@%*=#%#-,",
    "        .*+=%@@@@@@+-+@@@%====+#%@@@@@@@@@@@%+=%@@@@@@@@@@@@%+-=+*+**.",
    "        :##-%@@@@@@@#=*%@*+@@@@%#*:++++=-+++=+@@@@@@*#%%*+==**=-.",
    "       :%+--*@@@@@@@@@%==-#@@@@@@*+@@@@*+#*=%@@@@@@#--+**+:",
    "      :#=+%*=#@@@@@@@@@@@%*==#%@%=#%%%*--*%@@@@@@@%=++",
    "      =#-#@@%#@@@@@@@@@@@@@@@@%####%%%@@@@@@@@@@@%++=",
    "      -#=*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-++",
    "      .*%=*@@@@@@#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@+=%*",
    "       .**%*=+#@@@#+-*%@@@@@@@@@@@@@@@@@@@@@@@@@#-#-",
    "         -#@#-+##==:==-+%@@@@@@@@@@@@@@@@@@@@@@%-+:",
    "           :%+---##%@@%*=:=+**#***%@@@@@@@@@@@%-*:",
    "               .-+*##*++#@@#-+#*-#%#=*@%+=*++#%%+++",
    "                       :*@#=-+@%@#=*=%@@@%*--++",
    "                          .-=-. .*#-:*#*+-:*-",
    "                                 :#%#####+:",
 ]

derecha = [
    "", "", "", "", "", "", "", "", "", "", "",
    r"        ██████╗ ███████╗███╗   ██╗ ██████╗  █████╗ ██████╗ ",
    r"        ██╔════╝ ██╔════╝████╗  ██║██╔════╝ ██╔══██╗██╔══██╗",
    r"        ██║  ███╗█████╗  ██╔██╗ ██║██║  ███╗███████║██████╔╝",
    r"        ██║   ██║██╔══╝  ██║╚██╗██║██║   ██║██╔══██║██╔══██╗",
    r"        ╚██████╔╝███████╗██║ ╚████║╚██████╔╝██║  ██║██║  ██║",
    r"         ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝",
    r"        ██╗     ██╗██╗  ██╗",
    r"        ██║     ██║╚██╗██╔╝",
    r"        ██║     ██║ ╚███╔╝ ",
    r"        ██║     ██║ ██╔██╗ ",
    r"        ███████╗██║██╔╝ ██╗",
    r"        ╚══════╝╚═╝╚═╝  ╚═╝",
    "",
    f"        {BOLD}Gengarlix v1.0{RESET}",
    f"        {CYAN}Wireless Audit Suite{RESET}",
    "",
    f"        {YELLOW}•{RESET} Escaneo 802.11, Handshake y PMKID",
    f"        {YELLOW}•{RESET} Deauth activo y pasivo",
    f"        {YELLOW}•{RESET} Análisis con IA local (Ollama)",
    f"        {YELLOW}•{RESET} Reportes en Markdown",
    "",
    f"      {PURPLE}{BOLD}gengarlix >{RESET} ",
]


DISCLAIMER = f"""{YELLOW}{BOLD}AVISO LEGAL:{RESET} Uso exclusivo en redes propias o con
autorización escrita. El uso no autorizado es ilegal."""

REQUIRED_TOOLS = ["iw", "ip"]
OPTIONAL_TOOLS = ["airmon-ng", "aircrack-ng", "hashcat", "hcxpcapngtool"]


def check_dependencies():
    missing_required = [t for t in REQUIRED_TOOLS if shutil.which(t) is None]
    missing_optional = [t for t in OPTIONAL_TOOLS if shutil.which(t) is None]
    ok = True
    if missing_required:
        print(f"{RED}[!] Herramientas requeridas no encontradas: "
              f"{', '.join(missing_required)}{RESET}")
        ok = False
    if missing_optional:
        print(f"{YELLOW}[!] Herramientas opcionales no encontradas: "
              f"{', '.join(missing_optional)}{RESET}")
        print(f"{YELLOW}    Algunas funciones (monitor, cracking) "
              f"no estarán disponibles.{RESET}")
    return ok


def _safe_md_cell(text):
    if text is None:
        return "N/A"
    return str(text).replace("|", "\\|").replace("\n", " ")


def _safe_md_block(text):
    if text is None:
        return "N/A"
    return str(text)


def imprimir_banner():
    try:
        ancho_terminal = os.get_terminal_size().columns
    except OSError:
        ancho_terminal = 100
    ancho_terminal = max(ancho_terminal, 100)

    max_gengar_len = max(len(line) for line in gengar)
    max_derecha_len = max(len(line) for line in derecha)
    ancho_necesario = max_gengar_len + max_derecha_len + 8

    if ancho_terminal >= ancho_necesario:
        for i in range(max(len(gengar), len(derecha))):
            raw = gengar[i] if i < len(gengar) else ""
            pad = " " * max(0, max_gengar_len - len(raw) + 8)
            line_g = f"{PURPLE}{BOLD}{raw}{RESET}{pad}" if raw.strip() else pad
            line_d = (f"{PURPLE}{BOLD}{derecha[i]}{RESET}"
                      if i < len(derecha) and derecha[i] else "")
            print(f"{line_g}{line_d}")
    else:
        for linea in gengar:
            print(f"{PURPLE}{BOLD}{linea}{RESET}" if linea.strip() else "")
        print("\n")
        for linea in derecha:
            print(f"{PURPLE}{BOLD}{linea}{RESET}" if linea.strip() else "")
    print()


def imprimir_menu():
    menu = f"""
{CYAN}{BOLD}Uso:{RESET} sudo gengarlix [opciones]

{PURPLE}{BOLD} Opciones Principales:{RESET}
  {YELLOW}-h, --help{RESET}            Muestra este menú de ayuda
  {YELLOW}-i, --interface{RESET}       Interfaz de red (ej. wlan0, wlan0mon)
  {YELLOW}--monitor IFACE{RESET}       Activa el modo monitor en la interfaz
  {YELLOW}--no-banner{RESET}           Oculta el arte ASCII de Gengar

{PURPLE}{BOLD} Escaneo y Reconocimiento:{RESET}
  {YELLOW}--scan{RESET}                Escanea redes Wi-Fi cercanas (con hopping)
  {YELLOW}--bssid MAC{RESET}           Especifica el BSSID objetivo
  {YELLOW}--clients{RESET}             Escanea clientes conectados al BSSID

{PURPLE}{BOLD} Ataques Activos:{RESET}
  {YELLOW}--deauth{RESET}              Envía tramas deauth (requiere --bssid)
  {YELLOW}--client MAC{RESET}          MAC del cliente a atacar (opcional)
  {YELLOW}--capture{RESET}             Captura handshake WPA (requiere --bssid)
  {YELLOW}--pmkid{RESET}               Captura PMKID (clientless)
  {YELLOW}--channel N{RESET}           Canal del objetivo (recomendado)

{PURPLE}{BOLD} Cracking y Análisis:{RESET}
  {YELLOW}--crack PCAP{RESET}          Crackea un handshake con aircrack-ng
  {YELLOW}--pmkid-crack PCAP{RESET}    Crackea PMKID con hashcat
  {YELLOW}--wordlist RUTA{RESET}       Diccionario para cracking
  {YELLOW}--rules R1 [R2...]{RESET}    Reglas hashcat (-r)
  {YELLOW}--combinator LISTA{RESET}    Segunda wordlist (ataque -a 1)
  {YELLOW}--hybrid MASK{RESET}         Máscara para -a 6/7
  {YELLOW}--ai{RESET}                  Análisis con IA (corre DeauthDetector real)

{PURPLE}{BOLD} Expansión de Diccionario:{RESET}
  {YELLOW}--mangle{RESET}              Expande --wordlist con reglas locales
  {YELLOW}--mangle-out RUTA{RESET}     Salida del mangle
  {YELLOW}--mangle-config N{RESET}     low | medium | high

{PURPLE}{BOLD} Reportes:{RESET}
  {YELLOW}--report RUTA{RESET}         Ruta de salida del reporte Markdown
"""
    print(menu)


def generar_reporte(path, redes, pcap, password, ai_text=None, alerts=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Gengarlix — Reporte de auditoría\n\n")
        f.write(f"**Fecha:** {datetime.now().isoformat(timespec='seconds')}\n\n")

        f.write("## Redes detectadas\n\n")
        if redes:
            f.write("| SSID | BSSID | Canal | Señal | Clientes | Crypto |\n")
            f.write("|---|---|---|---|---|---|\n")
            for r in redes:
                f.write(f"| {_safe_md_cell(r.get('ssid'))} "
                        f"| `{_safe_md_cell(r.get('bssid'))}` "
                        f"| {_safe_md_cell(r.get('channel', '?'))} "
                        f"| {r.get('signal', 0)} dBm "
                        f"| {r.get('clientes', 0)} "
                        f"| {_safe_md_cell(r.get('crypto', '?'))} |\n")
        else:
            f.write("_Sin datos de escaneo._\n")

        if alerts:
            f.write("\n## Alertas de Deauth\n\n")
            for a in alerts:
                f.write(f"- {_safe_md_cell(a)}\n")

        f.write("\n## Captura\n\n")
        f.write(f"- PCAP: `{_safe_md_cell(pcap)}`\n"
                f"- Contraseña: `{_safe_md_cell(password) or 'no encontrada'}`\n")

        if ai_text:
            f.write("\n## Análisis IA\n\n" + _safe_md_block(ai_text) + "\n")

    print(f"{GREEN}[✓] Reporte: {path}{RESET}")


def _run_deauth_detector(interface, timeout=15):
    try:
        from modules.detector import DeauthDetector
        det = DeauthDetector(threshold=10, window=10)
        return det.start(interface, timeout=timeout)
    except Exception as e:
        print(f"{YELLOW}[!] No se pudo correr el detector de deauth: {e}{RESET}")
        return []


def main():
    p = argparse.ArgumentParser(prog="gengarlix",
                                description="Gengarlix — Suite ofensiva de auditoría Wi-Fi.",
                                add_help=False)

    p.add_argument("-h", "--help", action="store_true", help="Mostrar este menú de ayuda")
    p.add_argument("-i", "--interface", help="Interfaz (wlan0, wlan0mon...)")
    p.add_argument("--monitor", metavar="IFACE", help="Activar modo monitor en IFACE")
    p.add_argument("--scan", action="store_true", help="Escanear redes")
    p.add_argument("--bssid", help="BSSID objetivo")
    p.add_argument("--clients", action="store_true", help="Escanear clientes del BSSID")
    p.add_argument("--capture", action="store_true", help="Capturar handshake (usa --bssid)")
    p.add_argument("--pmkid", action="store_true", help="Capturar PMKID (clientless)")
    p.add_argument("--deauth", action="store_true", help="Enviar deauth (forzar reconexión)")
    p.add_argument("--client", default="ff:ff:ff:ff:ff:ff", help="MAC del cliente a atacar")
    p.add_argument("--crack", metavar="PCAP", help="Crackear handshake")
    p.add_argument("--pmkid-crack", metavar="PCAP", help="Crackear PMKID con hashcat")
    p.add_argument("--wordlist", default="wordlists/gengar_passwords.txt")
    p.add_argument("--channel", type=int, help="Canal del objetivo")
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--ai", action="store_true", help="Análisis IA (Ollama)")
    p.add_argument("--report", default="reports/audit.md")
    p.add_argument("--no-banner", action="store_true")

    p.add_argument("--mangle", action="store_true", help="Expande --wordlist con reglas locales")
    p.add_argument("--mangle-out", default=None, help="Salida del mangle")
    p.add_argument("--mangle-config", choices=["low", "medium", "high"], default="medium")
    p.add_argument("--rules", nargs="+", default=None, help="Reglas hashcat")
    p.add_argument("--combinator", default=None, help="Segunda wordlist (combinator)")
    p.add_argument("--hybrid", default=None, help="Máscara para -a 6/7")
    p.add_argument("--hybrid-mode", choices=["prefix", "suffix"], default="suffix")

    args = p.parse_args()

    if len(sys.argv) == 1:
        from modules.menu import iniciar
        print(DISCLAIMER)
        iniciar(banner_fn=None if args.no_banner else imprimir_banner)
        return

    if args.help:
        if not args.no_banner:
            imprimir_banner()
        imprimir_menu()
        return

    if not check_dependencies():
        sys.exit(1)

    if args.monitor:
        from modules.monitor import enable_monitor
        mon = enable_monitor(args.monitor)
        if mon:
            print(f"{GREEN}[✓] Usa: -i {mon}{RESET}")
        return

    redes, pcap, password, ai_text, alerts = [], None, None, None, []

    if args.scan:
        if not args.interface:
            print(f"{RED}[!] --scan requiere -i{RESET}"); sys.exit(1)
        from modules.scanner import scan_networks
        redes = scan_networks(args.interface, timeout=args.timeout)
        print(f"\n{GREEN}[✓] {len(redes)} redes:{RESET}\n")
        for r in redes:
            print(f"  {r['ssid']:<30} {r['bssid']:<20} "
                  f"ch:{r.get('channel','?'):<3} "
                  f"{r.get('signal',0):>4} dBm  "
                  f"clientes:{r.get('clientes', 0)}")

    if args.clients:
        if not (args.interface and args.bssid):
            print(f"{RED}[!] --clients requiere -i y --bssid{RESET}"); sys.exit(1)
        from modules.scanner import scan_clients
        cl = scan_clients(args.interface, args.bssid, timeout=args.timeout)
        print(f"\n{GREEN}[✓] {len(cl)} clientes:{RESET}")
        for c in cl:
            print(f"  {c}")

    if args.deauth:
        if not (args.interface and args.bssid):
            print(f"{RED}[!] --deauth requiere -i y --bssid{RESET}"); sys.exit(1)
        from modules.deauth import send_deauth
        send_deauth(args.interface, args.bssid, client=args.client, channel=args.channel)

    if args.capture:
        if not (args.interface and args.bssid):
            print(f"{RED}[!] --capture requiere -i y --bssid{RESET}"); sys.exit(1)
        from modules.capture import HandshakeCapture
        hc = HandshakeCapture(args.bssid)
        pcap = hc.capture(args.interface, timeout=args.timeout, deauth_every=5)

    if args.pmkid:
        if not (args.interface and args.bssid):
            print(f"{RED}[!] --pmkid requiere -i y --bssid{RESET}"); sys.exit(1)
        if not args.channel:
            print(f"{RED}[!] --pmkid requiere --channel{RESET}"); sys.exit(1)
        from modules.capture import capture_pmkid
        pcap = capture_pmkid(args.interface, args.bssid, args.channel, timeout=args.timeout)

    # FIX: Llamar a mangler.py en la raíz y actualizar la lista de cracking
    if args.mangle:
        if not os.path.exists(args.wordlist):
            print(f"{RED}[!] Wordlist no encontrada: {args.wordlist}{RESET}")
            sys.exit(1)
        
        out = args.mangle_out or args.wordlist.replace(".txt", "_mangled.txt")
        print(f"{CYAN}[*] Generando diccionario con mangler.py...{RESET}")
        
        env = os.environ.copy()
        env["MANGLE_INPUT"] = os.path.abspath(args.wordlist)
        env["MANGLE_OUTPUT"] = os.path.abspath(out)
        env["MANGLE_CONFIG"] = args.mangle_config
        
        res = subprocess.run([sys.executable, "mangler.py"], env=env)
        if res.returncode != 0:
            print(f"{RED}[!] Falló la generación del diccionario.{RESET}")
            sys.exit(1)
            
        if not any([args.crack, args.pmkid_crack]):
            return
        
        # El cracking usará el archivo expandido
        args.wordlist = out

    if args.crack:
        from modules.cracker import crack_handshake_aircrack
        password = crack_handshake_aircrack(
            args.crack, args.wordlist, args.bssid,
            rules=args.rules[0] if args.rules else None)

    if args.pmkid_crack:
        from modules.cracker import crack_pmkid_hashcat
        password = crack_pmkid_hashcat(
            args.pmkid_crack, args.wordlist,
            rules=args.rules, combinator=args.combinator,
            hybrid_mask=args.hybrid, hybrid_mode=args.hybrid_mode)

    if args.ai:
        from modules.ai_analyzer import analyze
        if args.interface:
            alerts = _run_deauth_detector(args.interface, timeout=15)
        ai_text = analyze(redes, alerts)

    if any([redes, pcap, password, ai_text, alerts]):
        generar_reporte(args.report, redes, pcap, password, ai_text, alerts)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Interrumpido.{RESET}"); sys.exit(0)
