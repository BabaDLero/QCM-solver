import os
import sys
import logging

import requests
import pytesseract
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import config

logger = logging.getLogger(__name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if getattr(sys, 'frozen', False):
    _base = sys._MEIPASS
else:
    _base = os.path.dirname(__file__)
os.environ["TESSDATA_PREFIX"] = os.path.join(_base, "tessdata")

_retry_strategy = Retry(
    total=0,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=0.3,
)
_adapter = HTTPAdapter(
    pool_connections=4,
    pool_maxsize=8,
    max_retries=_retry_strategy,
)
_session = requests.Session()
_session.mount("https://", _adapter)
_session.headers.update({
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate",
})

try:
    _empty = pytesseract.image_to_string(
        pytesseract.pytesseract.tesseract_cmd, lang="fra"
    )
except Exception:
    pass


def ask_deepseek(img):
    if not config.API_KEY:
        return "Erreur : clé API non définie. Définissez OPCODE_API_KEY dans .env"

    _session.headers.update({"Authorization": f"Bearer {config.API_KEY}"})

    try:
        text = pytesseract.image_to_string(img, lang="fra")
        if not text.strip():
            return "Aucun texte détecté dans la capture"
    except Exception as e:
        logger.error(f"OCR error: {e}")
        return f"Erreur OCR : {e}"

    prompt = (
        "Analyse le texte extrait d'une capture d'écran ci-dessous.\n"
        "Si c'est un QCM, réponds UNIQUEMENT par le numéro ou la lettre "
        "de la bonne réponse, rien d'autre.\n"
        "Si c'est une question ouverte, réponds de façon très courte et "
        "concise (1 phrase maximum).\n\n"
        f"Texte :\n{text}"
    )

    payload = {
        "model": config.MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": config.API_MAX_TOKENS,
    }

    try:
        response = _session.post(
            config.API_URL,
            json=payload,
            timeout=config.API_TIMEOUT,
        )
        response.raise_for_status()
        result = response.json()
        logger.debug(f"API raw response: {response.text[:500]}")
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            logger.warning(f"Empty content in API response. Full result: {result}")
            return f"Reponse API vide. Resultat brut: {str(result)[:200]}"
        return content
    except requests.exceptions.Timeout:
        logger.error("API timeout")
        return "Erreur : délai d'attente dépassé"
    except requests.exceptions.HTTPError as e:
        logger.error(f"API HTTP error: {e} | Response: {e.response.text}")
        return f"Erreur API : {e.response.text}"
    except Exception as e:
        logger.error(f"API error: {e}")
        return f"Erreur : {e}"
