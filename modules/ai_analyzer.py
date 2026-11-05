def analyze(redes, alertas):
    if not redes:
        return "No se detectaron redes para analizar."
    
    texto = "[*] Simulación de IA (Modo Demo)\n"
    texto += f"- Se analizaron {len(redes)} redes.\n"
    if alertas:
        texto += f"- ¡Cuidado! Se detectaron {len(alertas)} alertas de seguridad.\n"
    else:
        texto += "- Todo tranquilo en el espectro inalámbrico.\n"
    texto += "- Se recomienda usar contraseñas seguras en las redes WPA2/WPA3."
    return texto
