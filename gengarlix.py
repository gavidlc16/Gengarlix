import os
import sys

PURPLE, BOLD = "\033[35m", "\033[1m"
CYAN, RED, GREEN, YELLOW, RESET = "\033[36m", "\033[31m", "\033[32m", "\033[33m", "\033[0m"

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
    "", "", "", "", "", "", "", "", "", "", "", # 11 líneas de margen para alinear con la cabeza de Gengar

    # Título GENGAR
    r"    ██████╗ ███████╗███╗   ██╗ ██████╗  █████╗ ██████╗",
    r"    ██╔════╝ ██╔════╝████╗  ██║██╔════╝ ██╔══██╗██╔══██╗",
    r"    ██║  ███╗█████╗  ██╔██╗ ██║██║  ███╗███████║██████╔╝",
    r"    ██║   ██║██╔══╝  ██║╚██╗██║██║   ██║██╔══██║██╔══██╗",
    r"    ╚██████╔╝███████╗██║ ╚████║╚██████╔╝██║  ██║██║  ██║",
    r"     ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝",

    # Título LIX
    r"    ██╗     ██╗██╗  ██╗",
    r"    ██║     ██║╚██╗██╔╝",
    r"    ██║     ██║ ╚███╔╝",
    r"    ██║     ██║ ██╔██╗",
    r"    ███████╗██║██╔╝ ██╗",
    r"    ╚══════╝╚═╝╚═╝  ╚═╝",

    "",
    f"    {BOLD}Gengarlix v1.0{RESET}",
    f"    {CYAN}Wireless Audit Suite{RESET}",
    "",
    f"    {YELLOW}•{RESET} Escaneo 802.11, Handshake y PMKID",
    f"    {YELLOW}•{RESET} Deauth activo y pasivo",
    f"    {YELLOW}•{RESET} Análisis con IA local (Ollama)",
    f"    {YELLOW}•{RESET} Reportes en Markdown",
    "",
    f"  {PURPLE}{BOLD}gengarlix >{RESET} ",
]

def imprimir_banner():
    try:
        ancho_terminal = os.get_terminal_size().columns
    except OSError:
        ancho_terminal = 80

    max_gengar_len = max(len(line) for line in gengar)
    max_derecha_len = max(len(line) for line in derecha)
    
    # Calculamos si realmente caben lado a lado (dejando 5 espacios de separación)
    ancho_necesario = max_gengar_len + max_derecha_len + 5

    if ancho_terminal >= ancho_necesario:
        # MODO LADO A LADO (Tu idea original)
        for i in range(max(len(gengar), len(derecha))):
            raw = gengar[i] if i < len(gengar) else ""
            pad = " " * max(0, max_gengar_len - len(raw) + 5)
            line_g = f"{PURPLE}{BOLD}{raw}{RESET}{pad}" if raw.strip() else pad
            line_d = f"{PURPLE}{BOLD}{derecha[i]}{RESET}" if i < len(derecha) and derecha[i] else ""
            print(f"{line_g}{line_d}")
    else:
        # MODO VERTICAL (Si la terminal es angosta, ej. 100 columnas)
        for linea in gengar:
            print(f"{PURPLE}{BOLD}{linea}{RESET}" if linea.strip() else "")
        print("\n")
        for linea in derecha:
            print(f"{PURPLE}{BOLD}{linea}{RESET}" if linea.strip() else "")
    print()
