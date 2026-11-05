#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gengarlix v1.0 - Wireless Audit Suite
Auditoría Wi-Fi pasiva para entornos controlados y autorizados.
"""

import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PURPLE = "\033[35m"
BOLD   = "\033[1m"
CYAN   = "\033[36m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RESET  = "\033[0m"

# ══════════════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════════════
gengar = [
"@@@@@@@@@@@@@@@@@@*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@%-=*#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@#-=+++*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@%--=***+*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@%--=++*****#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@%--==+******+*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@##@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@%----=++++*++==*#@%*-+%@@%@@@@@@@@%*+-----#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@@==---====++=======-::-==--=**+=-:::::::=%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@#@@@@@@@@@@@@*=----=======-----------------::::::::+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@%#*===*%@@@@@@@@#+--------=====++++++++++++====-----::-----=*@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@#==---==++***@@@@#+-----==++*****************+++==--------::=+*********+*************++#%",
"@@@*=---==+***++*#%+-----=+************++******+++====--------==+*****++******++++++====%@",
"@@#+---=====+*++=-:::--==+*********************+++++===---------=+++*+++****++++==-==*%@@@",
"@@@@%+=========+=-----==++*********************+++++====--------===++*+++====-----+%@@@@@@",
"@@@@@@#=----=====-----=++***+****************++*++++===---------======---------=*@@@@@@@@@",
"@@@@@@@%=----=-------========************+++++++++===------------------------+%@@@@@@@@@@@",
"@@@@@@@@#+-----------=---+#**+*****+*++++++++++===------------------------=#@@@@@@@@@@@@@@",
"@@@@@@@@@%=-------------+#%#*==+++++++++++++===------------------------=*%@@@@@@@@@@@@@@@@",
"@@@@@@@@@@#=------------*%%%#+=-===========------------:----------::-+#@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@%=-------:-----*%%%*--:-----------====------+++=---------:*@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@#==------------=+###*+=-----------===---=++**+=----------:::-=+*#%%@@@@@@@@@@@@@@",
"@@@@@@@@%*++=-----=#%+=----==----------------==+####**+-----------:-----------====-=*@@@@@",
"@@@@@@@@#+++==-----%@@%=-------------------*%%%%%%##*+=----------------------------==+#@@@",
"@@@@@@@@*+====---::#@@@#**+----------------=++**++===------------------------------=*%@@@@",
"@@@@@@@@#+====--:::=#@@@@@@@#+-:-----------------------:------------------------=+:*@@@@@@",
"@@@@@@@@#+====-::::.:=%@@@@@@%@@@%*=---------------=-..--------------------==%@@@@@@@@@@@@",
"@@@@@@@@#=-----::::::.-*%@@@@@@@@@@@@@@%%##*****##@%#=--::::::::::::-=**#%@@@@@@@@@@@@@@@@",
"@@@@@@@%-..:--::........:=##%@@@@@@@@@@%@@@@@@@#@@%+:::::::::::.=#@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@*:...:::..............-*%@@@@@@@@#@@@@@@@%*=:...........:=@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@+::...::..               .:-=+====+*+++=-...............+@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@%+--::.....                  ... .................   . :*@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@*----::.....                      ...   .........    -*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@#=----::.......                     ...::------::...=%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@=::::..... .....                 ..:----------::::+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@*=:........:..........        ..:-----------:::::#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@#:.....:+%#=:................:::---------:::::.*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@%*-+%@@@@@@@+-:...........:::---------------:#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+:    .:+*#+------:---------=#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-..-*@@@@%=--::.....::--=*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#@@@@@@@%+:.........:=%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#=:.....:-+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*===+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
]

derecha = [
"", "", "", "", "", "", "", "", "", "", "",
r"    ██████╗ ███████╗███╗   ██╗ ██████╗  █████╗ ██████╗ ██╗     ██╗██╗  ██╗",
r"   ██╔════╝ ██╔════╝████╗  ██║██╔════╝ ██╔══██╗██╔══██╗██║     ██║╚██╗██╔╝",
r"   ██║  ███╗█████╗  ██╔██╗ ██║██║  ███╗███████║██████╔╝██║     ██║ ╚███╔╝ ",
r"   ██║   ██║██╔══╝  ██║╚██╗██║██║   ██║██╔══██║██╔══██╗██║     ██║ ██╔██╗ ",
r"   ╚██████╔╝███████╗██║ ╚████║╚██████╔╝██║  ██║██║  ██║███████╗██║██╔╝ ██╗",
r"    ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝",
"",
f"    {BOLD}Gengarlix v1.0{RESET}",
f"    {CYAN}Wireless Audit Suite{RESET}",
"",
f"    {YELLOW}•{RESET} Escaneo pasivo 802.11",
f"    {YELLOW}•{RESET} Detección de ataques deauth",
f"    {YELLOW}•{RESET} Análisis con IA local (Ollama)",
f"    {YELLOW}•{RESET} Reportes en Markdown / JSON",
"",
f"  {PURPLE}{BOLD}gengarlix >{RESET} ",
]

def imprimir_banner():
    # Esta versión adapta el banner para que no se rompa en pantallas pequeñas
    try:
        ancho_terminal = os.get_terminal_size().columns
    except OSError:
        ancho_terminal = 80

    for i in range(max(len(gengar), len(derecha))):
        if ancho_terminal > 130:
            raw = gengar[i] if i < len(gengar) else ""
            pad = " " * max(0, 95 - len(raw))
            line_g = f"{PURPLE}{raw}{RESET}{pad}"
            line_d = f"{PURPLE}{BOLD}{derecha[i]}{RESET}" if i < len(derecha) and derecha[i] else ""
            print(f"{line_g}   {line_d}")
        else:
            if i < len(gengar):
                print(f"{PURPLE}{gengar[i]}{RESET}")
            if i == len(gengar) - 1:
                for linea in derecha:
                    if linea:
                        print(f"{PURPLE}{BOLD}{linea:^80}{RESET}")
    print()

# ══════════════════════════════════════════════════════════════
# REPORTES
# ══════════════════════════════════════════════════════════════
def generar_reporte(path, redes, alertas, ai_text=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Gengarlix - Reporte de auditoría\n\n")
        f.write(f"**Fecha:** {datetime.now().isoformat(timespec='seconds')}\n\n")
        f.write("## Redes detectadas\n\n")
        if redes:
            f.write("| SSID | BSSID | Señal (dBm) | Seguridad |\n|---|---|---|---|\n")
            for r in redes:
                f.write(f"| {r['ssid']} | `{r['bssid']}` | {r['signal']} | {r['security']} |\n")
        else:
            f.write("_No se detectaron redes._\n")
        f.write("\n## Alertas de seguridad\n\n")
        if alertas:
            for a in alertas:
                f.write(f"- ⚠️ Posible ataque deauth desde `{a['bssid']}` "
                        f"({a['count']} tramas en 1s).\n")
        else:
            f.write("_Sin alertas._\n")
        if ai_text:
            f.write("\n## Análisis con IA\n\n")
            f.write(ai_text + "\n")
    print(f"{GREEN}[✓] Reporte guardado en:{RESET} {path}")

# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
def main():
    p = argparse.ArgumentParser(
        prog="gengarlix",
        description="Gengarlix - Wireless Audit Suite (solo auditorías éticas autorizadas).",
    )
    p.add_argument("-i", "--interface", help="Interfaz (ej. wlan0mon para modo monitor)")
    p.add_argument("--scan", action="store_true", help="Escaneo pasivo de redes (pywifi)")
    p.add_argument("--detect-deauth", action="store_true",
                   help="Detectar ataques deauth (requiere modo monitor)")
    p.add_argument("--timeout", type=int, default=30,
                   help="Segundos de captura para detección (default: 30)")
    p.add_argument("--ai", action="store_true",
                   help="Análisis con IA local (requiere Ollama en :11434)")
    p.add_argument("--report", default="reports/audit.md", help="Ruta del reporte")
    p.add_argument("--no-banner", action="store_true", help="No imprimir banner")
    args = p.parse_args()

    if not args.no_banner:
        imprimir_banner()

    if not (args.scan or args.detect_deauth):
        p.print_help()
        return

    redes, alertas, ai_text = [], [], None

    # ---- Escaneo ----
    if args.scan:
        from modules.scanner import scan_networks
        print(f"{CYAN}[*] Escaneando redes cercanas...{RESET}")
        redes = scan_networks()
        print(f"{GREEN}[✓] {len(redes)} redes encontradas.{RESET}\n")
        for r in redes:
            print(f"  {r['ssid']:<30} {r['bssid']:<20} {r['signal']:>4} dBm   {r['security']}")
        print()

    # ---- Detección deauth ----
    if args.detect_deauth:
        if not args.interface:
            print(f"{RED}[!] --detect-deauth requiere --interface (modo monitor){RESET}")
            sys.exit(1)
        from modules.detector import DeauthDetector
        print(f"{CYAN}[*] Capturando {args.timeout}s en {args.interface}...{RESET}")
        det = DeauthDetector()
        det.start(args.interface, timeout=args.timeout)
        alertas = det.alerts
        if alertas:
            print(f"{RED}[!] {len(alertas)} alertas detectadas.{RESET}")
        else:
            print(f"{GREEN}[✓] Sin alertas.{RESET}")

    # ---- IA ----
    if args.ai:
        from modules.ai_analyzer import analyze
        print(f"{CYAN}[*] Consultando IA local...{RESET}")
        ai_text = analyze(redes, alertas)
        if ai_text:
            print(ai_text)
        else:
            print(f"{YELLOW}[!] IA no disponible (¿Ollama corriendo en :11434?){RESET}")

    # ---- Reporte ----
    generar_reporte(args.report, redes, alertas, ai_text)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Interrumpido por el usuario.{RESET}")
        sys.exit(0)
