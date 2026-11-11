import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze(scan_results, alerts=None, model="llama3"):
    alerts = alerts or []
    prompt = (
        "Eres un experto en ciberseguridad Wi-Fi. Analiza los siguientes "
        "resultados de auditoría y proporciona recomendaciones concretas "
        "y priorizadas.\n\n"
        f"Redes detectadas: {json.dumps(scan_results, indent=2)}\n"
        f"Alertas: {json.dumps(alerts, indent=2)}\n\n"
        "Responde en español, con viñetas, indicando riesgos y mitigaciones."
    )
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "Sin respuesta del modelo.")
    except requests.exceptions.ConnectionError:
        return ("[!] No se pudo conectar a Ollama. "
                "¿Está corriendo en http://localhost:11434?")
    except Exception as e:
        return f"[!] Error al analizar con IA: {e}"
