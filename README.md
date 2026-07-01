# QCM Solver

Application Windows qui capture l'écran, extrait le texte par OCR, et envoie la question à une API IA pour obtenir la réponse.

## Prérequis

- Python 3.8+
- [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) installé (avec la langue française)

## Installation

```bash
# Cloner le repo
git clone https://github.com/BabaDLero/QCM-solver.git
cd QCM-solver/mon_app

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer le fichier .env
cp .env.example .env
```

## Configuration

Éditez `.env` :

| Variable | Description |
|---|---|
| `OPCODE_API_KEY` | Clé API pour le service d'IA |
| `OPCODE_API_URL` | URL de l'API (défaut : OpenCode API) |

Modifiez les réglages dans `config.py` :

- `TRIGGER_KEY` : touche de raccourci (défaut : `*`)
- `OVERLAY_WIDTH` / `OVERLAY_HEIGHT` : taille de la fenêtre de réponse

## Utilisation

```bash
python main.py
```

1. Lancez l'application — une icône apparaît dans la barre système
2. Ouvrez ou affichez un QCM à l'écran
3. Appuyez sur la touche `*` (ou la touche configurée)
4. L'application capture l'écran, extrait le texte, et l'envoie à l'IA
5. La réponse s'affiche dans une fenêtre en bas de l'écran

La touche de raccourci sert aussi à masquer la fenêtre de réponse.

## Build exécutable

```bash
pip install pyinstaller
pyinstaller ScreenScraperAI.spec
```

L'exécutable sera dans le dossier `dist/`.
