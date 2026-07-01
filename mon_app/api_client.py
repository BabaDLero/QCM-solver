import requests
import config
import logging

logger = logging.getLogger(__name__)


def ask_deepseek(img):
    if not config.API_KEY:
        return "Erreur : clé API non définie. Définissez OPCODE_API_KEY dans .env"

    import pytesseract
    import os
    import sys

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    os.environ["TESSDATA_PREFIX"] = os.path.join(base, "tessdata")

    try:
        text = pytesseract.image_to_string(img, lang="fra")
        if not text.strip():
            return "Aucun texte détecté dans la capture"
    except Exception as e:
        logger.error(f"OCR error: {e}")
        return f"Erreur OCR : {e}"

    url = config.API_URL
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = (
        "Analyse le texte extrait d'une capture d'écran ci-dessous.\n"
        "Si c'est un QCM (questions à choix multiples), réponds UNIQUEMENT par "
        "le numéro ou la lettre de la bonne réponse, rien d'autre.\n"
        "Si c'est une question ouverte, réponds de façon très courte et concise "
        "(1 phrase maximum).\n\n"
        f"Texte :\n{text}"
    )

    payload = {
        "model": config.MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", str(result))
    except requests.exceptions.Timeout:
        logger.error("API timeout")
        return "Erreur : délai d'attente dépassé"
    except requests.exceptions.HTTPError as e:
        logger.error(f"API HTTP error: {e} | Response: {e.response.text}")
        return f"Erreur API : {e.response.text}"
    except Exception as e:
        logger.error(f"API error: {e}")
        return f"Erreur : {e}"
