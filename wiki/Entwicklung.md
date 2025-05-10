# Entwicklung

## Projektstruktur

```
suno-prompt-generator/
├── .github/                    # GitHub-spezifische Dateien
│   ├── ISSUE_TEMPLATE/        # Issue-Vorlagen
│   └── PULL_REQUEST_TEMPLATE.md
├── src/                       # Quellcode
│   ├── gui/                   # GUI-Komponenten
│   ├── core/                  # Kernfunktionalität
│   └── utils/                 # Hilfsfunktionen
├── tests/                     # Testdateien
├── docs/                      # Dokumentation
├── wiki/                      # Wiki-Dokumentation
└── examples/                  # Beispielprojekte
```

## Entwicklungsumgebung einrichten

1. Repository klonen:
```bash
git clone https://github.com/Trunkenbold/suno-prompt-generator.git
cd suno-prompt-generator
```

2. Virtuelle Umgebung erstellen:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Entwicklungsabhängigkeiten
```

## Codestandards

### Python
- PEP 8 Style Guide
- Docstrings für alle Funktionen und Klassen
- Typisierung mit Python Type Hints
- Maximale Zeilenlänge: 88 Zeichen

### Tests
- Unit Tests für alle Kernfunktionen
- Integration Tests für GUI-Komponenten
- Testabdeckung > 80%

### Dokumentation
- Docstrings im Google Style
- README.md für jedes Modul
- Wiki-Dokumentation aktuell halten

## Entwicklungsworkflow

1. Branch erstellen:
```bash
git checkout -b feature/neue-funktion
```

2. Änderungen entwickeln und testen:
```bash
pytest tests/
flake8 src/
mypy src/
```

3. Änderungen committen:
```bash
git add .
git commit -m "feat: neue Funktion hinzugefügt"
```

4. Pull Request erstellen:
- Beschreibung der Änderungen
- Tests durchgeführt
- Dokumentation aktualisiert

## Release-Prozess

1. Version aktualisieren:
- `setup.py`
- `__version__` in Hauptmodul
- Changelog aktualisieren

2. Release erstellen:
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. GitHub Release erstellen:
- Release Notes
- Assets hochladen
- Changelog einbinden

## Contributing

1. Issue erstellen für:
- Bug Reports
- Feature Requests
- Verbesserungsvorschläge

2. Pull Request einreichen:
- Branch von `main`
- Tests hinzugefügt
- Dokumentation aktualisiert

3. Code Review:
- Style Guide eingehalten
- Tests bestanden
- Dokumentation vollständig

## Nützliche Befehle

### Tests ausführen
```bash
pytest tests/              # Alle Tests
pytest tests/ -v          # Mit Details
pytest tests/ -k "test_name"  # Spezifischer Test
```

### Code-Qualität prüfen
```bash
flake8 src/               # Style Check
mypy src/                # Typ-Check
pylint src/              # Code-Analyse
```

### Dokumentation generieren
```bash
sphinx-build docs/ docs/_build/  # HTML-Dokumentation
```

## Support

- GitHub Issues für Bug Reports
- Discord für Entwickler-Diskussionen
- Wiki für Dokumentation 