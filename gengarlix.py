#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gengarlix v1.0 - Suite ofensiva de auditoría Wi-Fi (pentesting ético)."""

import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PURPLE, BOLD = "\033[35m", "\033[1m"
CYAN, RED, GREEN, YELLOW, RESET = "\033[36m", "\033[31m", "\033[32m", "\033[33m", "\033[0m"

# ─── Banner (Gengar con 2 líneas de margen superior) ───
gengar = [
    "",  # Margen superior 1
    "",  # Margen superior 2
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
    "", "", "", "", "", "", "", "", "", "", "", # 11 líneas de margen

    # Título GENGAR
    r"        ██████╗ ███████╗███╗   ██╗ ██████╗  █████╗ ██████╗",
    r"        ██╔════╝ ██╔════╝████╗  ██║██╔════╝ ██╔══██╗██╔══██╗",
    r"        ██║  ███╗█████╗  ██╔██╗ ██║██║  ███╗███████║██████╔╝",
    r"        ██║   ██║██╔══╝  ██║╚██╗██║██║   ██║██╔══██║██╔══██╗",
    r"        ╚██████╔╝███████╗██║ ╚████║╚██████╔╝██║  ██║██║  ██║",
    r"         ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝",

    # Título LIX
    r"        ██╗     ██╗██╗  ██╗",
    r"        ██║     ██║╚██╗██╔╝",
    r"        ██║     ██║ ╚███╔╝",
    r"        ██║     ██║ ██╔██╗",
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

def imprimir_banner():
    try:
        ancho_terminal = os.get_terminal_size().columns
    except OSError:
        ancho_terminal = 80

    max_gengar_len = max(len(line) for line in gengar)
    max_derecha_len = max(len(line) for line in derecha)
    ancho_necesario = max_gengar_len + max_derecha_len + 8

    if ancho_terminal >= ancho_necesario:
        for i in range(max(len(gengar), len(derecha))):
            raw = gengar[i] if i < len(gengar) else ""
            pad = " " * max(0, max_gengar_len - len(raw) + 8)
            line_g = f"{PURPLE}{BOLD}{raw}{RESET}{pad}" if raw.strip() else pad
            line_d = f"{PURPLE}{BOLD}{derecha[i]}{RESET}" if i < len(derecha) and derecha[i] else ""
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

{PURPLE}{BOLD}⚡ Opciones Principales:{RESET}
  {YELLOW}-h, --help{RESET}            Muestra este menú de ayuda
  {YELLOW}-i, --interface{RESET}       Interfaz de red (ej. wlan0, wlan0mon)
  {YELLOW}--monitor IFACE{RESET}       Activa el modo monitor en la interfaz
  {YELLOW}--no-banner{RESET}           Oculta el arte ASCII de Gengar

{PURPLE}{BOLD}📡 Escaneo y Reconocimiento:{RESET}
  {YELLOW}--scan{RESET}                Escanea redes Wi-Fi cercanas
  {YELLOW}--bssid MAC{RESET}           Especifica el BSSID objetivo
  {YELLOW}--clients{RESET}             Escanea clientes conectados al BSSID

{PURPLE}{BOLD}💥 Ataques Activos:{RESET}
  {YELLOW}--deauth{RESET}              Envía tramas deauth (requiere --bssid)
  {YELLOW}--capture{RESET}             Captura handshake WPA (requiere --bssid)
  {YELLOW}--pmkid{RESET}               Captura PMKID (clientless)

{PURPLE}{BOLD}🔓 Cracking y Análisis:{RESET}
  {YELLOW}--crack PCAP{RESET}          Crackea un handshake con aircrack-ng
  {YELLOW}--pmkid-crack PCAP{RESET}    Crackea PMKID con hashcat
  {YELLOW}--wordlist RUTA{RESET}       Diccionario para cracking
  {YELLOW}--ai{RESET}                  Análisis de seguridad con IA local (Ollama)

{PURPLE}{BOLD}📁 Reportes:{RESET}
  {YELLOW}--report RUTA{RESET}         Ruta de salida del reporte Markdown
"""
    print(menu)

def generar_reporte(path, redes, pcap, password, ai_text=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Gengarlix — Reporte de auditoría\n\n")
        f.write(f"**Fecha:** {datetime.now().isoformat(timespec='seconds')}\n\n")
        f.write("## Redes detectadas\n\n")
        if redes:
            f.write("| SSID | BSSID | Canal | Señal |\n|---|---|---|---|\n")
            for r in redes:
                f.write(f"| {r['ssid']} | `{r['bssid']}` | {r.get('channel','?')} | {r.get('signal',0)} dBm |\n")
        f.write("\n## Captura\n\n")
        f.write(f"- PCAP: `{pcap or 'N/A'}`\n- Contraseña: `{password or 'no encontrada'}`\n")
        if ai_text:
            f.write("\n## Análisis IA\n\n" + ai_text + "\n")
    print(f"{GREEN}[✓] Reporte: {path}{RESET}")

def main():
    p = argparse.ArgumentParser(prog="gengarlix", description="Gengarlix — Suite ofensiva de auditoría Wi-Fi.", add_help=False)
    
    p.add_argument("-h", "--help", action="store_true", help="Mostrar este menú de ayuda")
    p.add_argument("-i", "--interface", help="Interfaz (wlan0, wlan0mon...)")
    p.add_argument("--monitor", metavar="IFACE", help="Activar modo monitor en IFACE")
    p.add_argument("--scan", action="store_true", help="Escanear redes")
    p.add_argument("--bssid", help="BSSID objetivo")
    p.add_argument("--clients", action="store_true", help="Escanear clientes del BSSID")
    p.add_argument("--capture", action="store_true", help="Capturar handshake (usa --bssid)")
    p.add_argument("--pmkid", action="store_true", help="Capturar PMKID (clientless)")
    p.add_argument("--deauth", action="store_true", help="Enviar deauth (forzar reconexión)")
    p.add_argument("--crack", metavar="PCAP", help="Crackear handshake")
    p.add_argument("--pmkid-crack", metavar="PCAP", help="Crackear PMKID con hashcat")
    p.add_argument("--wordlist", default="wordlists/common_passwords.txt")
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--ai", action="store_true", help="Análisis IA (Ollama)")
    p.add_argument("--report", default="reports/audit.md")
    p.add_argument("--no-banner", action="store_true")

    args = p.parse_args()

    # BANNER SOLO SI: se pide ayuda o no hay argumentos
    if args.help or len(sys.argv) == 1:
        if not args.no_banner: 
            imprimir_banner()
        imprimir_menu()
        return

    # Si ejecuta una herramienta (--scan, --monitor, etc.), va directo a la acción (sin banner)
    
    if args.monitor:
        from modules.monitor import enable_monitor
        mon = enable_monitor(args.monitor)
        if mon: print(f"{GREEN}[✓] Usa: -i {mon}{RESET}")
        return

    redes, pcap, password, ai_text = [], None, None, None

    if args.scan:
        if not args.interface: print(f"{RED}[!] --scan requiere -i{RESET}"); sys.exit(1)
        from modules.scanner import scan_networks
        redes = scan_networks(args.interface, timeout=args.timeout)
        print(f"\n{GREEN}[✓] {len(redes)} redes:{RESET}\n")
        for r in redes:
            print(f"  {r['ssid']:<30} {r['bssid']:<20} ch:{r.get('channel','?'):<3} {r.get('signal',0):>4} dBm")

    if args.clients:
        if not (args.interface and args.bssid): print(f"{RED}[!] --clients requiere -i y --bssid{RESET}"); sys.exit(1)
        from modules.scanner import scan_clients
        cl = scan_clients(args.interface, args.bssid, timeout=args.timeout)
        print(f"\n{GREEN}[✓] {len(cl)} clientes:{RESET}")
        for c in cl: print(f"  {c}")

    if args.deauth:
        if not (args.interface and args.bssid): print(f"{RED}[!] --deauth requiere -i y --bssid{RESET}"); sys.exit(1)
        from modules.deauth import send_deauth
        send_deauth(args.interface, args.bssid, count=20)

    if args.capture:
        if not (args.interface and args.bssid): print(f"{RED}[!] --capture requiere -i y --bssid{RESET}"); sys.exit(1)
        from modules.capture import HandshakeCapture
        hc = HandshakeCapture(args.bssid)
        pcap = hc.capture(args.interface, timeout=args.timeout, deauth_every=5)

    if args.pmkid:
        if not (args.interface and args.bssid): print(f"{RED}[!] --pmkid requiere -i y --bssid{RESET}"); sys.exit(1)
        from modules.capture import capture_pmkid
        pcap = capture_pmkid(args.interface, args.bssid, timeout=args.timeout)

    if args.crack:
        from modules.cracker import crack_handshake_aircrack
        password = crack_handshake_aircrack(args.crack, args.wordlist, args.bssid)

    if args.pmkid_crack:
        from modules.cracker import crack_pmkid_hashcat
        password = crack_pmkid_hashcat(args.pmkid_crack, args.wordlist)

    if args.ai:
        from modules.ai_analyzer import analyze
        ai_text = analyze(redes, [{"bssid": args.bssid, "count": 1}] if pcap else [])

    if any([redes, pcap, password, ai_text]):
        generar_reporte(args.report, redes, pcap, password, ai_text)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Interrumpido.{RESET}"); sys.exit(0)
