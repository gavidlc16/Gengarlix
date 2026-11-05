import os
import re

# Archivo de entrada (tu diccionario base)
INPUT_FILE = "wordlists/gengar_passwords.txt" 
# Archivo de salida (el diccionario expandido)
OUTPUT_FILE = "wordlists/gengar_passwords_mangled.txt"

# Patrones comunes que la gente le añade a sus contraseñas
numeros = ["1", "12", "123", "1234", "12345", "2023", "2024", "2025", "69", "99", "00", "007"]
simbolos = ["!", "@", "#", "$", ".", "_", "-"]
prefijos = ["El", "La", "The", "Mr", "Dr"]

def generar_mangling():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Error: No se encontró el archivo {INPUT_FILE}")
        return

    os.makedirs("wordlists", exist_ok=True)
    total = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        with open(INPUT_FILE, "r", encoding="utf-8") as infile:
            # Leemos las palabras ignorando espacios y líneas vacías
            palabras = [linea.strip() for linea in infile if linea.strip()]

            for palabra in palabras:
                # 1. Palabra original
                outfile.write(f"{palabra}\n")
                total += 1
                
                # 2. Capitalizada (Ej: Gengar en vez de gengar)
                cap = palabra.capitalize()
                if cap != palabra:
                    outfile.write(f"{cap}\n")
                    total += 1
                
                # 3. Mayúsculas completas (Ej: GENGAR)
                mayus = palabra.upper()
                if mayus != palabra and mayus != cap:
                    outfile.write(f"{mayus}\n")
                    total += 1

                # 4. Combinaciones con Números (Ej: gengar123, Gengar2024)
                for num in numeros:
                    outfile.write(f"{palabra}{num}\n")
                    outfile.write(f"{cap}{num}\n")
                    total += 2

                # 5. Combinaciones con Símbolos (Ej: gengar!, Gengar@)
                for sim in simbolos:
                    outfile.write(f"{palabra}{sim}\n")
                    outfile.write(f"{cap}{sim}\n")
                    total += 2

                # 6. Símbolo + Número (Ej: gengar!123)
                for sim in simbolos:
                    for num in numeros:
                        outfile.write(f"{palabra}{sim}{num}\n")
                        total += 1

                # 7. Números al principio (Ej: 123gengar)
                for num in ["123", "2024", "1"]:
                    outfile.write(f"{num}{palabra}\n")
                    total += 1

    print(f"[✓] ¡Éxito! Diccionario generado con {total} contraseñas.")
    print(f"[✓] Guardado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    generar_mangling()
