import os
import subprocess
import sys
import tempfile

INPUT_FILE = os.environ.get("MANGLE_INPUT", "wordlists/gengar_passwords.txt")
OUTPUT_FILE = os.environ.get("MANGLE_OUTPUT", "wordlists/gengar_passwords_mangled.txt")
CONFIG = os.environ.get("MANGLE_CONFIG", "medium")

ANIOS = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]
NUMEROS = ["1", "12", "123", "1234", "12345", "69", "99", "00", "007"]
SIMBOLOS = ["!", "@", "#", "$", ".", "_", "-"]
PREFIJOS = ["El", "La", "The", "Mr", "Dr"]
LEET = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"}

MAX_OUTPUT_LINES = 50_000_000
WARN_INPUT_LINES = 100_000


def _leet_variants(word):
    out = set()
    out.add("".join(LEET.get(c.lower(), c) for c in word))
    for i, c in enumerate(word):
        if c.lower() in LEET:
            out.add(word[:i] + LEET[c.lower()] + word[i + 1:])
    return out


def _generar_variantes(palabra, config):
    cap = palabra.capitalize()
    may = palabra.upper()
    bases = {palabra, cap, may}

    for b in bases:
        yield b

    # Nivel LOW (solo lo básico)
    if config == "low":
        for b in bases:
            for n in ["1", "123", "2025", "2026"]:
                yield b + n
            for s in ["!", "@"]:
                yield b + s
        return

    # Nivel MEDIUM (números, símbolos, años, prefijos)
    for b in bases:
        for n in NUMEROS + ANIOS:
            yield b + n
        for s in SIMBOLOS:
            yield b + s

    for b in (palabra, cap):
        for a in ANIOS:
            for s in SIMBOLOS:
                yield b + a + s

    for b in (palabra, cap):
        for s in SIMBOLOS:
            for n in ["1", "123", "1234"] + ANIOS:
                yield b + s + n

    for p in PREFIJOS:
        yield p + palabra
        yield p + cap

    # Nivel HIGH (añade Leetspeak)
    if config == "high":
        for lv in _leet_variants(palabra):
            yield lv
            for s in ["!", "@", "#"]:
                yield lv + s
            for a in ["2023", "2024", "2025", "2026"]:
                yield lv + a
                yield lv + a + "!"


def _estimar_lineas(input_file):
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for l in f if l.strip())


def _sort_u(in_path, out_path):
    if os.path.exists('/usr/bin/sort') or os.path.exists('/bin/sort'):
        try:
            with open(out_path, "w", encoding="utf-8") as out:
                subprocess.run(['sort', '-u', in_path], stdout=out, check=True)
            return True
        except Exception:
            pass
    seen = set()
    try:
        with open(in_path, "r", encoding="utf-8", errors="ignore") as f, \
             open(out_path, "w", encoding="utf-8") as out:
            for line in f:
                line = line.rstrip("\n")
                if line and line not in seen:
                    seen.add(line)
                    out.write(line + "\n")
        return True
    except MemoryError:
        print("[!] Sin memoria para deduplicar en Python.")
        return False


def generar_mangling():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Error: No se encontró el archivo {INPUT_FILE}")
        sys.exit(1)

    n_input = _estimar_lineas(INPUT_FILE)
    print(f"[*] Entrada: {n_input} palabras ({INPUT_FILE}) | Nivel: {CONFIG.upper()}")

    if n_input > WARN_INPUT_LINES:
        print(f"{chr(27)}[33m[!] ADVERTENCIA: la entrada tiene {n_input} palabras. "
              f"La salida puede superar los {MAX_OUTPUT_LINES} candidatos.{chr(27)}[0m")
        if not os.environ.get("MANGLE_INPUT"):
            resp = input("¿Continuar igualmente? (s/N) > ").strip().lower()
            if resp != 's':
                print("[i] Cancelado.")
                sys.exit(0)

    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT_FILE)), exist_ok=True)

    tmp = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt")
    tmp_path = tmp.name
    count = 0
    aborted = False

    try:
        with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as infile:
            for line in infile:
                palabra = line.strip()
                if not palabra:
                    continue
                # AQUI ESTA EL FIX: le pasamos CONFIG a la función
                for cand in _generar_variantes(palabra, CONFIG):
                    tmp.write(cand + "\n")
                    count += 1
                    if count >= MAX_OUTPUT_LINES:
                        aborted = True
                        break
                if aborted:
                    break
        tmp.close()

        if aborted:
            print(f"[!] Límite {MAX_OUTPUT_LINES} alcanzado. Abortando.")
            print(f"[!] Archivo parcial conservado en: {tmp_path}")
            return

        print(f"[*] {count} variantes generadas. Deduplicando...")
        if not _sort_u(tmp_path, OUTPUT_FILE):
            print("[!] No se pudo deduplicar.")
            os.replace(tmp_path, OUTPUT_FILE)
            return
    finally:
        if not aborted and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        final = sum(1 for _ in f)

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"[✓] Diccionario generado: {final} contraseñas únicas ({size_mb:.1f} MB)")
    print(f"[✓] Guardado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    generar_mangling()
