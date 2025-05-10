# Installation

## Systemanforderungen

- Python 3.8 oder höher
- Windows 10/11, macOS oder Linux
- Mindestens 4GB RAM
- Internetverbindung für Updates

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/Trunkenbold/suno-prompt-generator.git
cd suno-prompt-generator
```

### 2. Virtuelle Umgebung erstellen

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Programm starten

```bash
python "Suno Prompt Generator.py"
```

## Fehlerbehebung

### Häufige Probleme

1. **Python nicht gefunden**
   - Stellen Sie sicher, dass Python installiert ist
   - Fügen Sie Python zum PATH hinzu

2. **Abhängigkeiten können nicht installiert werden**
   - Aktualisieren Sie pip: `python -m pip install --upgrade pip`
   - Prüfen Sie Ihre Internetverbindung

3. **Programm startet nicht**
   - Prüfen Sie die Python-Version: `python --version`
   - Stellen Sie sicher, dass alle Abhängigkeiten installiert sind

### Support

Bei weiteren Problemen:
- Erstellen Sie ein Issue auf GitHub
- Prüfen Sie die [FAQ](FAQ.md)
- Kontaktieren Sie die Maintainer 