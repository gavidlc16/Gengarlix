import json
import os
import requests

DEFAULT_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")


def _sanitize(obj, max_len=200):
    """Limita longitudes y normaliza tipos para evitar prompts gigantes."""
    if isinstance(obj, dict):
        return {str(k)[:64]: _sanitize(v, max_len) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v, max_len) for v in obj]
    if isinstance(obj, str):
        return obj[:max_len]
    return obj


def analyze(scan_results, alerts=None, model=None, url=None, timeout=120):
    alerts = alerts or []
    model = model or DEFAULT_MODEL
    url = url or DEFAULT_URL

    prompt = (
        "Eres un experto en ciberseguridad Wi-Fi. Analiza los siguientes "
        "resultados de auditoría y proporciona recomendaciones concretas "
        "y priorizadas.\n\n"
        f"Redes detectadas: {json.dumps(_sanitize(scan_results), indent=2)}\n"
        f"Alertas: {json.dumps(_sanitize(alerts), indent=2)}\n\n"
        "Responde en español, con viñetas, indicando riesgos y mitigaciones."
    )

    try:
        r = requests.post(url, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=timeout)
        r.raise_for_status()
        return r.json().get("response", "Sin respuesta del modelo.")
    except requests.exceptions.ConnectionError:
        return (f"[!] No se pudo conectar a Ollama en {url}. "
                "¿Está corriendo?")
    except requests.exceptions.Timeout:
        return f"[!] Timeout ({timeout}s) al consultar Ollama."
    except requests.exceptions.HTTPError as e:
        return f"[!] Ollama devolvió error HTTP: {e}"
    except Exception as e:
        return f"[!] Error al analizar con IA: {e}"
