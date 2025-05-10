# Suno Prompt Generator

Ein leistungsstarkes Tool zur Generierung von Prompts für Suno AI, mit einer benutzerfreundlichen GUI-Oberfläche.

## Features

- 🎵 Erstellen von Album-Konzepten mit mehreren Tracks
- 🎨 Detaillierte Musikstil-Definitionen
- 🎹 Feineinstellungen für Genre, Tempo, Tonart und mehr
- 🌍 Mehrsprachige Unterstützung (Deutsch/Englisch)
- 🎨 Anpassbare Benutzeroberfläche (Dark/Light Mode)
- 💾 Automatisches Speichern
- 📝 Export als Text oder PDF
- 🖼️ Cover-Generierung (in Entwicklung)
- 🔄 Projekt-Import/Export

## Installation

1. Klonen Sie das Repository:
```bash
git clone https://github.com/Trunkenbold/suno-prompt-generator.git
cd suno-prompt-generator
```

2. Erstellen Sie eine virtuelle Umgebung:
```bash
python -m venv .venv
```

3. Aktivieren Sie die virtuelle Umgebung:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. Installieren Sie die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

## Verwendung

Starten Sie das Programm:
```bash
python "Suno Prompt Generator.py"
```

### Grundlegende Funktionen

1. **Album-Konzept erstellen**
   - Geben Sie einen Albumtitel ein (optional)
   - Legen Sie die Anzahl der Tracks fest (1-30)
   - Wählen Sie die Sprache für die Lyrics
   - Beschreiben Sie die Albumstory (2-3 Sätze)
   - Definieren Sie den globalen Musikstil
   - Geben Sie ausgeschlossene Stile an

2. **Track-Management**
   - Vergeben Sie individuelle Tracktitel
   - Definieren Sie spezifische Stile pro Track
   - Legen Sie Track-spezifische Excludes fest
   - Speichern und anwenden von Track-Vorlagen
   - Scrollen Sie durch die Tracks mit dem Mausrad

3. **Feineinstellungen**
   - Genre und Subgenre auswählen
   - Tempo (BPM) einstellen
   - Tonart festlegen
   - Stimmung definieren
   - Instrumentierung spezifizieren
   - Gesangsstil wählen
   - Effekte hinzufügen
   - Produktionsstil festlegen
   - Besonderheiten angeben

4. **Export & Import**
   - Prompt als Text speichern
   - Als PDF exportieren
   - In Zwischenablage kopieren
   - Vorschau anzeigen
   - Projekt exportieren/importieren
   - Automatisches Speichern

## Abhängigkeiten

- customtkinter >= 5.2.0
- reportlab >= 4.0.0
- tkinter (Python Standard Library)
- json (Python Standard Library)
- os (Python Standard Library)
- pathlib (Python Standard Library)
- webbrowser (Python Standard Library)

## Entwicklung

Das Projekt verwendet:
- Python 3.x
- customtkinter für die moderne GUI
- JSON für die Datenspeicherung

### Projektstruktur

```
suno-prompt-generator/
├── Suno Prompt Generator.py    # Hauptprogramm
├── requirements.txt            # Abhängigkeiten
├── README.md                  # Dokumentation
├── LICENSE                    # MIT Lizenz
├── CHANGELOG.md              # Änderungshistorie
└── .gitignore                # Git Ignore-Datei
```

## Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## Beitragen

Beiträge sind willkommen! Bitte folgen Sie diesen Schritten:

1. Forken Sie das Repository
2. Erstellen Sie einen neuen Branch (`git checkout -b feature/amazing-feature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some amazing feature'`)
4. Pushen Sie zum Branch (`git push origin feature/amazing-feature`)
5. Öffnen Sie einen Pull Request

## Autor

David Melchior (Trunkenbold)

## Danksagung

- Suno AI für die Inspiration
- customtkinter für die großartige GUI-Bibliothek
- Allen Beitragenden und Testern 