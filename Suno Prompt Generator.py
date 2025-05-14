import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import json
import pathlib
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import webbrowser
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FineTuningDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Speichere die Referenz zum Parent
        self.title(parent.t('fine_tuning_title'))
        self.geometry("800x900")
        self.resizable(True, True)
        
        # Modal-Dialog Konfiguration
        self.transient(parent)
        self.grab_set()
        
        # Ergebnis-Variable
        self.result = None
        
        # Hauptframe mit Scrollbar
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Einstellungen
        self.settings = {
            "genre": {
                "value": "",
                "label": parent.t('main_genre'),
                "placeholder": "z.B. Pop, Rock, Hip Hop",
                "options": [
                    "Avantgarde & Experimental", "Blues", "Classical", "Country", "Easy Listening",
                    "Electronic", "Folk", "Hip Hop", "Jazz", "Latin", "Metal", "Pop", "Punk",
                    "R&B & Soul", "Reggae", "Rock", "World Music", "Gospel & Christian",
                    "Indie & Alternative", "Soundtrack & Score", "Children's Music", "Holiday Music",
                    "New Age", "Spoken Word", "Comedy", "Traditional", "Fusion"
                ]
            },
            "subgenre": {
                "value": "",
                "label": parent.t('subgenre'),
                "placeholder": "z.B. Indie Pop, Synthwave",
                "options": {
                    "Avantgarde & Experimental": [
                        "Electroacoustic", "Industrial music", "Noise music", "Progressive music", 
                        "Psychedelic music", "Avant-garde jazz", "Experimental rock", "Sound art",
                        "Musique concrète", "Free improvisation", "Microtonal music", "Glitch",
                        "Drone music", "Field recordings", "Circuit bending", "Sound collage",
                        "Experimental pop", "Experimental electronic", "Experimental hip hop",
                        "Experimental metal", "Experimental folk", "Experimental classical"
                    ],
                    "Blues": [
                        "Chicago blues", "Delta blues", "Electric blues", "Gospel blues", 
                        "Rhythm and blues", "Texas blues", "Piedmont blues", "Jump blues",
                        "British blues", "Blues rock", "Soul blues", "Contemporary blues",
                        "Memphis blues", "Louisiana blues", "Swamp blues", "Hill country blues",
                        "Blues revival", "Blues fusion", "Blues punk", "Blues metal",
                        "Blues jazz", "Blues gospel", "Blues soul"
                    ],
                    "Classical": [
                        "Baroque", "Classical period", "Romantic", "Modern classical",
                        "Contemporary classical", "Chamber music", "Orchestral", "Opera",
                        "Choral", "Symphonic", "Minimalism", "Neoclassical",
                        "Renaissance", "Medieval", "Early music", "Post-minimalism",
                        "Experimental classical", "Classical crossover", "Classical fusion",
                        "Classical electronic", "Classical rock", "Classical jazz",
                        "Classical pop", "Classical metal"
                    ],
                    "Country": [
                        "Bluegrass", "Country blues", "Country pop", "Country rock",
                        "Nashville sound", "Outlaw country", "Progressive country",
                        "Texas country", "Western swing", "Honky-tonk", "Bakersfield sound",
                        "Alternative country", "Country folk", "Country gospel",
                        "Country soul", "Country jazz", "Country metal",
                        "Country punk", "Country rap", "Country electronic",
                        "Country classical", "Country fusion"
                    ],
                    "Easy Listening": [
                        "Adult contemporary music", "Elevator music", "Lounge music",
                        "Soft rock", "Smooth jazz", "Easy listening pop", "Background music",
                        "Light music", "Middle of the road", "Beautiful music",
                        "Easy listening classical", "Easy listening electronic",
                        "Easy listening jazz", "Easy listening folk",
                        "Easy listening world", "Easy listening fusion"
                    ],
                    "Electronic": [
                        "Ambient", "Breakbeat", "Disco", "Drum and bass", "Dub",
                        "Electro", "House music", "Techno", "Trance music", "IDM",
                        "Synthwave", "Vaporwave", "Future bass", "Glitch", "Industrial",
                        "Trip hop", "Downtempo", "Chillwave", "Lo-fi", "Experimental electronic",
                        "Electroclash", "Electro house", "Electro swing", "Electro pop",
                        "Electro rock", "Electro jazz", "Electro classical", "Electro folk",
                        "Electro metal", "Electro punk", "Electro soul", "Electro gospel"
                    ],
                    "Folk": [
                        "Americana", "Celtic music", "Folk rock", "Indie folk",
                        "Singer-songwriter", "Traditional folk", "Contemporary folk",
                        "Progressive folk", "Folk metal", "Folk punk", "World fusion",
                        "Ethnic fusion", "Neofolk", "Folk pop", "Folk jazz",
                        "Folk classical", "Folk electronic", "Folk soul",
                        "Folk gospel", "Folk blues", "Folk country",
                        "Folk punk", "Folk metal", "Folk fusion"
                    ],
                    "Hip Hop": [
                        "Alternative hip hop", "Gangsta rap", "Trap", "UK drill",
                        "Boom bap", "Conscious hip hop", "Experimental hip hop",
                        "Jazz rap", "Lo-fi hip hop", "Mumble rap", "Political hip hop",
                        "Cloud rap", "Drill", "Grime", "Horrorcore", "Trap metal",
                        "Hip hop soul", "Hip hop jazz", "Hip hop rock",
                        "Hip hop metal", "Hip hop punk", "Hip hop classical",
                        "Hip hop electronic", "Hip hop gospel", "Hip hop fusion"
                    ],
                    "Jazz": [
                        "Bebop", "Big band", "Cool jazz", "Jazz fusion", "Smooth jazz",
                        "Free jazz", "Hard bop", "Modal jazz", "Post-bop", "Soul jazz",
                        "Afro-Cuban jazz", "Latin jazz", "Jazz-funk", "Acid jazz",
                        "Nu jazz", "Jazz rap", "Jazz rock", "Jazz metal",
                        "Jazz punk", "Jazz classical", "Jazz electronic",
                        "Jazz soul", "Jazz gospel", "Jazz blues", "Jazz country",
                        "Jazz folk", "Jazz fusion"
                    ],
                    "Latin": [
                        "Salsa", "Merengue", "Bachata", "Reggaeton", "Latin pop",
                        "Bossa nova", "Samba", "Tango", "Flamenco", "Latin rock",
                        "Latin jazz", "Cumbia", "Ranchera", "Mariachi", "Latin alternative",
                        "Latin soul", "Latin gospel", "Latin blues", "Latin country",
                        "Latin folk", "Latin classical", "Latin electronic",
                        "Latin metal", "Latin punk", "Latin fusion"
                    ],
                    "Metal": [
                        "Black metal", "Death metal", "Heavy metal", "Industrial metal",
                        "Power metal", "Progressive metal", "Thrash metal", "Doom metal",
                        "Folk metal", "Symphonic metal", "Nu metal", "Metalcore",
                        "Deathcore", "Sludge metal", "Stoner metal", "Avant-garde metal",
                        "Metal jazz", "Metal classical", "Metal electronic",
                        "Metal soul", "Metal gospel", "Metal blues", "Metal country",
                        "Metal folk", "Metal fusion"
                    ],
                    "Pop": [
                        "Dance-pop", "Electropop", "Indie pop", "K-pop", "Synth-pop",
                        "Power pop", "Pop rock", "Pop punk", "Art pop", "Dream pop",
                        "Jangle pop", "Chamber pop", "Baroque pop", "Pop rap",
                        "Pop soul", "Pop metal", "Pop country", "Pop jazz",
                        "Pop classical", "Pop electronic", "Pop gospel",
                        "Pop blues", "Pop folk", "Pop fusion"
                    ],
                    "Punk": [
                        "Anarcho punk", "Hardcore punk", "Pop punk", "Punk rock",
                        "Skate punk", "Post-punk", "New wave", "Punk blues",
                        "Folk punk", "Crust punk", "Garage punk", "Psychobilly",
                        "Punk metal", "Emo", "Post-hardcore", "Punk jazz",
                        "Punk classical", "Punk electronic", "Punk soul",
                        "Punk gospel", "Punk blues", "Punk country",
                        "Punk folk", "Punk fusion"
                    ],
                    "R&B & Soul": [
                        "Contemporary R&B", "Funk", "Gospel music", "Neo soul",
                        "Quiet storm", "Soul blues", "Blue-eyed soul", "Northern soul",
                        "Southern soul", "Psychedelic soul", "Soul jazz", "Soul rock",
                        "Alternative R&B", "Progressive soul", "Soul metal",
                        "Soul punk", "Soul classical", "Soul electronic",
                        "Soul gospel", "Soul blues", "Soul country",
                        "Soul folk", "Soul fusion"
                    ],
                    "Reggae": [
                        "Roots reggae", "Dancehall", "Dub", "Reggae fusion",
                        "Reggae rock", "Lovers rock", "Ragga", "Ska", "Rocksteady",
                        "Dub poetry", "Reggae pop", "Reggae fusion", "Reggae jazz",
                        "Reggae classical", "Reggae electronic", "Reggae soul",
                        "Reggae gospel", "Reggae blues", "Reggae country",
                        "Reggae folk", "Reggae metal", "Reggae punk"
                    ],
                    "Rock": [
                        "Alternative rock", "Classic rock", "Hard rock", "Indie rock",
                        "Punk rock", "Progressive rock", "Psychedelic rock",
                        "Art rock", "Blues rock", "Folk rock", "Glam rock",
                        "Grunge", "Post-rock", "Math rock", "Shoegaze",
                        "Stoner rock", "Surf rock", "Rock jazz", "Rock classical",
                        "Rock electronic", "Rock soul", "Rock gospel",
                        "Rock blues", "Rock country", "Rock folk", "Rock fusion"
                    ],
                    "World Music": [
                        "African music", "Asian music", "Middle Eastern music",
                        "Indian classical", "Flamenco", "Celtic music", "Balkan music",
                        "Latin music", "Caribbean music", "Pacific music",
                        "World fusion", "Ethnic fusion", "Global fusion",
                        "World jazz", "World classical", "World electronic",
                        "World soul", "World gospel", "World blues",
                        "World country", "World folk", "World rock",
                        "World metal", "World punk"
                    ],
                    "Gospel & Christian": [
                        "Contemporary gospel", "Traditional gospel", "Christian rock",
                        "Christian pop", "Christian metal", "Christian hip hop",
                        "Worship music", "Southern gospel", "Black gospel",
                        "Christian country", "Christian alternative", "Christian jazz",
                        "Christian classical", "Christian electronic", "Christian soul",
                        "Christian blues", "Christian folk", "Christian fusion"
                    ],
                    "Indie & Alternative": [
                        "Indie rock", "Indie pop", "Alternative rock", "Art rock",
                        "Dream pop", "Shoegaze", "Post-rock", "Math rock",
                        "Noise rock", "Lo-fi", "Chamber pop", "Baroque pop",
                        "Indie folk", "Indie electronic", "Alternative hip hop",
                        "Indie jazz", "Indie classical", "Indie soul",
                        "Indie gospel", "Indie blues", "Indie country",
                        "Indie metal", "Indie punk", "Indie fusion"
                    ],
                    "Soundtrack & Score": [
                        "Film score", "Video game music", "TV show music",
                        "Orchestral soundtrack", "Electronic soundtrack",
                        "Ambient soundtrack", "Thematic music", "Incidental music",
                        "Background music", "Trailer music", "Soundtrack jazz",
                        "Soundtrack classical", "Soundtrack electronic",
                        "Soundtrack soul", "Soundtrack gospel", "Soundtrack blues",
                        "Soundtrack country", "Soundtrack folk", "Soundtrack fusion"
                    ],
                    "Children's Music": [
                        "Educational music", "Nursery rhymes", "Children's pop",
                        "Children's folk", "Children's rock", "Children's classical",
                        "Lullabies", "Children's world music", "Children's jazz",
                        "Children's electronic", "Children's soul", "Children's gospel",
                        "Children's blues", "Children's country", "Children's fusion"
                    ],
                    "Holiday Music": [
                        "Christmas music", "Christmas carols", "Christmas pop",
                        "Christmas jazz", "Christmas classical", "Christmas rock",
                        "Christmas country", "Christmas R&B", "Christmas gospel",
                        "Christmas blues", "Christmas folk", "Christmas electronic",
                        "Christmas soul", "Christmas metal", "Christmas punk",
                        "Christmas fusion"
                    ],
                    "New Age": [
                        "Ambient", "Meditation music", "Healing music",
                        "Nature sounds", "Spiritual music", "World fusion",
                        "Electronic new age", "Acoustic new age", "Celtic new age",
                        "New age jazz", "New age classical", "New age soul",
                        "New age gospel", "New age blues", "New age country",
                        "New age folk", "New age rock", "New age metal",
                        "New age punk", "New age fusion"
                    ],
                    "Spoken Word": [
                        "Poetry", "Storytelling", "Audiobook", "Radio drama",
                        "Sound poetry", "Performance poetry", "Beat poetry",
                        "Political speech", "Motivational speech", "Spoken word jazz",
                        "Spoken word classical", "Spoken word electronic",
                        "Spoken word soul", "Spoken word gospel", "Spoken word blues",
                        "Spoken word country", "Spoken word folk", "Spoken word fusion"
                    ],
                    "Comedy": [
                        "Musical comedy", "Comedy rock", "Comedy pop",
                        "Comedy rap", "Comedy country", "Comedy metal",
                        "Parody music", "Novelty songs", "Comedy folk",
                        "Comedy jazz", "Comedy classical", "Comedy electronic",
                        "Comedy soul", "Comedy gospel", "Comedy blues",
                        "Comedy punk", "Comedy fusion"
                    ],
                    "Traditional": [
                        "Folk music", "Classical traditional", "World traditional",
                        "Religious traditional", "Regional traditional",
                        "Historical music", "Early music", "Medieval music",
                        "Renaissance music", "Traditional jazz", "Traditional classical",
                        "Traditional electronic", "Traditional soul", "Traditional gospel",
                        "Traditional blues", "Traditional country", "Traditional fusion"
                    ],
                    "Fusion": [
                        "Jazz fusion", "Rock fusion", "World fusion",
                        "Electronic fusion", "Classical fusion", "Folk fusion",
                        "Metal fusion", "Hip hop fusion", "Experimental fusion",
                        "Soul fusion", "Gospel fusion", "Blues fusion",
                        "Country fusion", "Pop fusion", "Punk fusion"
                    ]
                }
            },
            "tempo": {
                "value": "",
                "label": parent.t('tempo'),
                "placeholder": "z.B. 120",
                "min": 40,
                "max": 200,
                "default": 120
            },
            "key": {
                "value": "",
                "label": parent.t('key'),
                "placeholder": "z.B. C-Dur"
            },
            "mood": {
                "value": "",
                "label": parent.t('mood'),
                "placeholder": "z.B. melancholisch, euphorisch"
            },
            "instruments": {
                "value": "",
                "label": parent.t('instruments'),
                "placeholder": "z.B. Gitarre, Klavier, Drums"
            },
            "vocal_style": {
                "value": "",
                "label": parent.t('vocal_style'),
                "placeholder": "z.B. klar, rau, geflüstert",
                "options": [
                    parent.t('vocal_style_male'),
                    parent.t('vocal_style_female'),
                    parent.t('vocal_style_child'),
                    parent.t('vocal_style_choir'),
                    parent.t('vocal_style_duet'),
                    parent.t('vocal_style_multi'),
                    parent.t('vocal_style_spoken'),
                    parent.t('vocal_style_rap')
                ]
            },
            "effects": {
                "value": "",
                "label": parent.t('effects'),
                "placeholder": "z.B. Reverb, Delay, Distortion"
            },
            "production": {
                "value": "",
                "label": parent.t('production'),
                "placeholder": "z.B. Lo-Fi, High-End, Vintage"
            },
            "special": {
                "value": "",
                "label": parent.t('special'),
                "placeholder": "z.B. spezielle Effekte oder Techniken"
            }
        }
        
        # Erstelle Eingabefelder für jede Einstellung
        self.entries = {}
        for key, setting in self.settings.items():
            frame = ctk.CTkFrame(self.main_frame)
            frame.pack(fill="x", pady=5)
            
            # Hauptlabel
            label = ctk.CTkLabel(frame, text=setting["label"], width=120)
            label.pack(side="left", padx=5)
            
            # Beschreibungs-Label
            desc_frame = ctk.CTkFrame(frame, fg_color="transparent")
            desc_frame.pack(side="left", fill="x", expand=True)
            
            desc_label = ctk.CTkLabel(desc_frame, text=setting["placeholder"], text_color="gray", anchor="w")
            desc_label.pack(fill="x", pady=(0, 2))
            
            if "options" in setting:
                if isinstance(setting["options"], list):
                    entry = ctk.CTkOptionMenu(desc_frame, values=setting["options"], width=400)
                    entry.set(setting["value"] if setting["value"] else setting["options"][0])
                    if key == "genre":
                        entry.configure(command=lambda v: self.update_subgenre_options("subgenre", v))
                else:  # Dictionary für Subgenres
                    entry = ctk.CTkOptionMenu(desc_frame, values=list(setting["options"].keys()), width=400)
                    entry.set(setting["value"] if setting["value"] else list(setting["options"].keys())[0])
                    if key == "subgenre":
                        # Initial die Subgenres basierend auf dem ausgewählten Hauptgenre setzen
                        main_genre = self.entries["genre"].get()
                        if main_genre in setting["options"]:
                            entry.configure(values=setting["options"][main_genre])
                            entry.set(setting["options"][main_genre][0])
            elif key == "tempo":
                # Spezieller Fall für BPM-Schieberegler
                entry = ctk.CTkSlider(desc_frame, from_=setting["min"], to=setting["max"], 
                                    number_of_steps=setting["max"]-setting["min"],
                                    width=400)
                entry.set(setting["default"])
                # Label für den aktuellen Wert
                value_label = ctk.CTkLabel(desc_frame, text=str(setting["default"]))
                value_label.pack(side="right", padx=5)
                # Callback für Wertänderung
                def update_tempo_label(value):
                    value_label.configure(text=str(int(value)))
                    self.settings[key]["value"] = str(int(value))
                entry.configure(command=update_tempo_label)
            else:
                entry = ctk.CTkEntry(desc_frame, width=400)
                entry.insert(0, setting["value"])
            
            entry.pack(fill="x", expand=True)
            self.entries[key] = entry
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        save_btn = ctk.CTkButton(button_frame, text="Speichern", command=self.save_settings)
        save_btn.pack(side="right", padx=5)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Abbrechen", command=self.destroy)
        cancel_btn.pack(side="right", padx=5)
    
    def update_subgenre_options(self, key, main_genre):
        """Aktualisiert die Subgenre-Optionen basierend auf dem ausgewählten Hauptgenre."""
        if key == "subgenre" and main_genre in self.settings["subgenre"]["options"]:
            subgenre_menu = self.entries["subgenre"]
            subgenre_menu.configure(values=self.settings["subgenre"]["options"][main_genre])
            subgenre_menu.set(self.settings["subgenre"]["options"][main_genre][0])
    
    def save_settings(self):
        """Speichert die Einstellungen und schließt den Dialog."""
        for key, entry in self.entries.items():
            self.settings[key]["value"] = entry.get()
        self.result = self.get_settings()
        self.destroy()
    
    def get_settings(self):
        """Gibt die aktuellen Einstellungen zurück."""
        settings = {}
        for key, setting in self.settings.items():
            value = setting["value"]
            if isinstance(value, (int, float)):
                if value != 0:  # Nur nicht-null Werte hinzufügen
                    settings[key] = str(int(value))
            elif isinstance(value, str) and value.strip():
                settings[key] = value
        return settings

class SunoPromptGenerator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Suno Prompt Generator")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.minsize(1200, 800)
        self.configure(bg="#23272a")
        self.languages = {
            "de": {
                "title": "Suno Prompt Generator",
                "album_title": "Album Titel:",
                "num_tracks": "Anzahl Tracks:",
                "lyrics_lang": "Sprache der Lyrics:",
                "narrative": "Albumstory (2–3 Sätze):",
                "global_style": "Globaler Musikstil:",
                "global_exclude": "Globale Excludes:",
                "tracks": "Tracks",
                "track_title": "Titel für Track",
                "track_excludes": "Excludes (optional)",
                "save_prompt": "Prompt generieren & speichern",
                "quit": "Beenden",
                "restore": "Letzte Sitzung wiederherstellen?",
                "template_save": "Track als Vorlage speichern",
                "template_apply": "Vorlage auf Track anwenden",
                "language": "Sprache:",
                "theme": "Farbschema:",
                "accent": "Akzentfarbe:",
                "footer": "© 2024 Suno Prompt Generator",
                "fine_tuning": "Feineinstellungen",
                "additional_options": "Zusatzoptionen",
                "generate_description": "Zu jedem Lied eine Beschreibung generieren",
                "generate_cover": "Zu jedem Lied ein Cover generieren",
                "song_title_in_cover": "Songtitel im Cover:",
                "with_song_title": "mit Songtitel",
                "without_song_title": "ohne Songtitel",
                "generate_album_cover": "Album-Cover generieren",
                "export_pdf": "Export als PDF",
                "copy_prompt": "Prompt kopieren",
                "preview": "Vorschau",
                "export_project": "Projekt exportieren",
                "import_project": "Projekt importieren",
                "help_faq": "Hilfe / FAQ",
                "music_style": "Musikstil:",
                "save": "Speichern",
                "cancel": "Abbrechen",
                "fine_tuning_title": "Feineinstellungen",
                "main_genre": "Hauptgenre:",
                "subgenre": "Subgenre:",
                "tempo": "Tempo (BPM):",
                "key": "Tonart:",
                "mood": "Stimmung:",
                "instruments": "Instrumentierung:",
                "vocal_style": "Gesangsstil:",
                "effects": "Effekte:",
                "production": "Produktion:",
                "special": "Besonderheiten:",
                "vocal_style_male": "Mann",
                "vocal_style_female": "Frau",
                "vocal_style_child": "Kind",
                "vocal_style_choir": "Chor",
                "vocal_style_duet": "Duett",
                "vocal_style_multi": "Mehrstimmig",
                "vocal_style_spoken": "Sprechgesang",
                "vocal_style_rap": "Rap",
                "help_title": "Hilfe",
                "help_text": """
Suno Prompt Generator - Hilfe

1. Grundlegende Funktionen
   - Albumtitel eingeben (optional)
   - Anzahl der Tracks festlegen (1-30)
   - Sprache für die Lyrics auswählen
   - Albumstory beschreiben (2-3 Sätze)
   - Globalen Musikstil definieren
   - Ausgeschlossene Stile angeben

2. Track-Management
   - Individuelle Tracktitel vergeben
   - Spezifische Stile pro Track definieren
   - Track-spezifische Excludes festlegen
   - Track-Vorlagen speichern und anwenden
   - Tracks mit Mausrad scrollen

3. Feineinstellungen
   - Genre und Subgenre auswählen
   - Tempo (BPM) einstellen
   - Tonart festlegen
   - Stimmung definieren
   - Instrumentierung spezifizieren
   - Gesangsstil wählen
   - Effekte hinzufügen
   - Produktionsstil festlegen
   - Besonderheiten angeben

4. Export & Import
   - Prompt als Text speichern
   - Als PDF exportieren
   - In Zwischenablage kopieren
   - Vorschau anzeigen
   - Projekt exportieren/importieren
   - Automatisches Speichern

5. Zusatzfunktionen
   - Beschreibungen für Songs generieren
   - Cover für einzelne Songs erstellen
   - Album-Cover generieren
   - Songtitel im Cover einbinden
   - Mehrsprachige Unterstützung (DE/EN)
   - Dark/Light Mode
   - Akzentfarben anpassen

6. Tipps & Tricks
   - Nutzen Sie die Feineinstellungen für präzise Kontrolle
   - Speichern Sie häufig verwendete Stile als Vorlagen
   - Verwenden Sie den globalen Stil als Basis
   - Nutzen Sie die Vorschau vor dem Export
   - Automatisches Speichern verhindert Datenverlust

7. Fehlerbehebung
   - Bei Problemen: Projekt exportieren und neu importieren
   - Konfiguration zurücksetzen: .suno_prompt_gui_config.json löschen
   - Autosave zurücksetzen: .suno_prompt_autosave.json löschen
   - Bei Abstürzen: Letzte Sitzung wiederherstellen

8. Updates
   - Automatische Update-Benachrichtigungen
   - GitHub-Repository für neue Versionen
   - Changelog in den Releases
""",
                "prompt_phase1": "PHASE 1: Album-Konzept",
                "prompt_metadata": "Metadaten",
                "prompt_version": "Version:",
                "prompt_generated": "Generiert am:",
                "prompt_warnings": "Warnungen",
                "prompt_instructions": "Anleitung für die KI",
                "prompt_ki_steps": """
[KI: Bitte folge diesen Schritten:
1. Analysiere die folgenden Informationen
2. Generiere ein Album-Konzept
3. Warte auf Bestätigung, bevor du fortfährst
4. Bei Fragen oder Unklarheiten, frage nach]""",
                "prompt_example": "Beispiel für ein gutes Album-Konzept:",
                "prompt_basic_info": "Grundlegende Informationen",
                "prompt_tracks": "Anzahl der Tracks:",
                "prompt_lyrics_lang": "Lyrics Sprache:",
                "prompt_narrative": "Narrative Overview:",
                "prompt_music_style": "Musikstil",
                "prompt_main_style": "Hauptstil",
                "prompt_excluded_styles": "Ausgeschlossene Stile",
                "prompt_empty": "[leer]",
                "prompt_ki_generate": """
[KI: Bitte generiere nun:]
1. Einen passenden Albumtitel
2. Einen passenden Titel für jeden Track
3. Eine kurze Beschreibung des Albums (2-3 Sätze)""",
                "prompt_ki_wait": "\n[KI: Warte nach der Generierung auf Bestätigung, bevor du fortfährst.]\n",
                "prompt_phase2": "PHASE 2: Track-Details",
                "prompt_track_steps": """
[KI: Bitte folge diesen Schritten für jeden Track:
1. Generiere passende Lyrics zur Sprache und zum Stil
2. Beachte die Stilvorgaben in der angegebenen Priorität
3. Stelle sicher, dass die Lyrics zur Stimmung passen
4. Warte auf Bestätigung nach jedem Track]""",
                "prompt_track_example": """
### Beispiel für einen guten Track:
- Titel: "Morgentau"
- Lyrics: [Passende Lyrics zur Stimmung]
- Style: [Klar definierter Stil mit allen Details]""",
                "prompt_track": "Track",
                "prompt_song_name": "Song Name",
                "prompt_song_lyrics": "Song Lyrics",
                "prompt_ki_important": """
[KI: WICHTIG - STRENGE ANWEISUNGEN:
1. Du MUSST den KOMPLETTEN Songtext in EINER EINZIGEN NACHRICHT ausgeben
2. Es ist VERBOTEN, den Text in mehrere Schritte oder Nachrichten aufzuteilen
3. Es ist VERBOTEN, nach Bestätigungen zwischen den Teilen zu fragen
4. Es ist VERBOTEN, den Text stückweise zu generieren
5. Du MUSST alle Teile (Intro, Verse, Chorus, etc.) SOFORT und VOLLSTÄNDIG ausgeben
6. Warte NICHT auf Bestätigungen zwischen den Teilen
7. Der Text muss zum Stil und zur Sprache passen]""",
                "song_style": "Song Stil (max. 1000 Zeichen)",
                "excluded_styles": "Ausgeschlossene Stile (max. 1000 Zeichen)",
                "no_style_defined": "[Kein spezifischer Stil definiert]",
                "no_excludes_defined": "[Keine ausgeschlossenen Stile definiert]",
                "style_placeholder": "z.B. Indie Pop mit elektronischen Elementen, Synthwave mit Retro-Atmosphäre, etc. (max. 1000 Zeichen)",
                "exclude_placeholder": "z.B. Metal, Schlager, etc. (max. 1000 Zeichen)",
                "lyrics_placeholder": "Songtext (max. 5000 Zeichen)",
                "prompt_style_limit": "Hinweis: Der Stil kann bis zu 1000 Zeichen lang sein. Nutzen Sie diese Möglichkeit für detaillierte Beschreibungen.",
                "prompt_exclude_limit": "Hinweis: Die ausgeschlossenen Stile können bis zu 1000 Zeichen lang sein. Listen Sie alle unerwünschten Stilelemente auf.",
                "prompt_lyrics_limit": "Hinweis: Der Songtext kann bis zu 5000 Zeichen lang sein. Nutzen Sie diese Möglichkeit für ausführliche Lyrics.",
                "fine_tuning_settings": "Feineinstellungen",
                "genre_settings": "Genre-Einstellungen",
                "tempo_settings": "Tempo-Einstellungen",
                "mood_settings": "Stimmungs-Einstellungen",
                "instrument_settings": "Instrumentierungs-Einstellungen",
                "vocal_settings": "Gesangs-Einstellungen",
                "effect_settings": "Effekt-Einstellungen",
                "production_settings": "Produktions-Einstellungen",
                "special_settings": "Besondere Einstellungen",
                "chatgpt_hint": "(nutze ChatGPT 4o)"
            },
            "en": {
                "title": "Suno Prompt Generator",
                "album_title": "Album Title:",
                "num_tracks": "Number of Tracks:",
                "lyrics_lang": "Lyrics Language:",
                "narrative": "Album Story (2-3 sentences):",
                "global_style": "Global Music Style:",
                "global_exclude": "Global Excludes:",
                "tracks": "Tracks",
                "track_title": "Track Title",
                "track_excludes": "Excludes (optional)",
                "save_prompt": "Generate & Save Prompt",
                "quit": "Quit",
                "restore": "Restore last session?",
                "template_save": "Save track as template",
                "template_apply": "Apply template to track",
                "language": "Language:",
                "theme": "Theme:",
                "accent": "Accent color:",
                "footer": "© 2024 Suno Prompt Generator",
                "fine_tuning": "Fine Tuning",
                "additional_options": "Additional Options",
                "generate_description": "Generate description for each song",
                "generate_cover": "Generate cover for each song",
                "song_title_in_cover": "Song title in cover:",
                "with_song_title": "with song title",
                "without_song_title": "without song title",
                "generate_album_cover": "Generate album cover",
                "export_pdf": "Export as PDF",
                "copy_prompt": "Copy Prompt",
                "preview": "Preview",
                "export_project": "Export Project",
                "import_project": "Import Project",
                "help_faq": "Help / FAQ",
                "music_style": "Music Style:",
                "save": "Save",
                "cancel": "Cancel",
                "fine_tuning_title": "Fine Tuning",
                "main_genre": "Main Genre:",
                "subgenre": "Subgenre:",
                "tempo": "Tempo (BPM):",
                "key": "Key:",
                "mood": "Mood:",
                "instruments": "Instruments:",
                "vocal_style": "Vocal Style:",
                "effects": "Effects:",
                "production": "Production:",
                "special": "Special Features:",
                "vocal_style_male": "Male",
                "vocal_style_female": "Female",
                "vocal_style_child": "Child",
                "vocal_style_choir": "Choir",
                "vocal_style_duet": "Duet",
                "vocal_style_multi": "Multi-voice",
                "vocal_style_spoken": "Spoken word",
                "vocal_style_rap": "Rap",
                "help_title": "Help",
                "help_text": """
Suno Prompt Generator - Help

1. Basic Functions
   - Enter album title (optional)
   - Set number of tracks (1-30)
   - Select lyrics language
   - Describe album story (2-3 sentences)
   - Define global music style
   - Specify excluded styles

2. Track Management
   - Assign individual track titles
   - Define specific styles per track
   - Set track-specific excludes
   - Save and apply track templates
   - Scroll tracks with mouse wheel

3. Fine Tuning
   - Select genre and subgenre
   - Set tempo (BPM)
   - Define key
   - Set mood
   - Specify instrumentation
   - Choose vocal style
   - Add effects
   - Set production style
   - Specify special features

4. Export & Import
   - Save prompt as text
   - Export as PDF
   - Copy to clipboard
   - Show preview
   - Export/import project
   - Auto-save functionality

5. Additional Features
   - Generate song descriptions
   - Create individual song covers
   - Generate album cover
   - Include song titles in covers
   - Multi-language support (DE/EN)
   - Dark/Light mode
   - Customize accent colors

6. Tips & Tricks
   - Use fine tuning for precise control
   - Save frequently used styles as templates
   - Use global style as base
   - Preview before export
   - Auto-save prevents data loss

7. Troubleshooting
   - For issues: Export and re-import project
   - Reset configuration: Delete .suno_prompt_gui_config.json
   - Reset autosave: Delete .suno_prompt_autosave.json
   - After crashes: Restore last session

8. Updates
   - Automatic update notifications
   - GitHub repository for new versions
   - Changelog in releases
""",
                "prompt_phase1": "PHASE 1: Album Concept",
                "prompt_metadata": "Metadata",
                "prompt_version": "Version:",
                "prompt_generated": "Generated on:",
                "prompt_warnings": "Warnings",
                "prompt_instructions": "Instructions for AI",
                "prompt_ki_steps": """
[AI: Please follow these steps:
1. Analyze the following information
2. Generate an album concept
3. Wait for confirmation before proceeding
4. Ask if you have any questions or uncertainties]""",
                "prompt_example": "Example of a good album concept:",
                "prompt_basic_info": "Basic Information",
                "prompt_tracks": "Number of Tracks:",
                "prompt_lyrics_lang": "Lyrics Language:",
                "prompt_narrative": "Narrative Overview:",
                "prompt_music_style": "Music Style",
                "prompt_main_style": "Main Style",
                "prompt_excluded_styles": "Excluded Styles",
                "prompt_empty": "[empty]",
                "prompt_ki_generate": """
[AI: Please generate now:]
1. A suitable album title
2. A suitable title for each track
3. A short description of the album (2-3 sentences)""",
                "prompt_ki_wait": "\n[AI: Wait for confirmation after generation before proceeding.]\n",
                "prompt_phase2": "PHASE 2: Track Details",
                "prompt_track_steps": """
[AI: Please follow these steps for each track:
1. Generate lyrics matching the language and style
2. Follow the style guidelines in the specified priority
3. Ensure the lyrics match the mood
4. Wait for confirmation after each track]""",
                "prompt_track_example": """
### Example of a good track:
- Title: "Morning Dew"
- Lyrics: [Matching lyrics for the mood]
- Style: [Clearly defined style with all details]""",
                "prompt_track": "Track",
                "prompt_song_name": "Song Name",
                "prompt_song_lyrics": "Song Lyrics",
                "prompt_ki_important": """
[AI: IMPORTANT - STRICT INSTRUCTIONS:
1. You MUST output the COMPLETE song text in a SINGLE message
2. It is FORBIDDEN to split the text into multiple steps or messages
3. It is FORBIDDEN to ask for confirmations between parts
4. It is FORBIDDEN to generate the text piece by piece
5. You MUST output all parts (Intro, Verse, Chorus, etc.) IMMEDIATELY and COMPLETELY
6. Do NOT wait for confirmations between parts
7. The text must match the style and language]""",
                "song_style": "Song Style (max. 1000 characters)",
                "excluded_styles": "Excluded Styles (max. 1000 characters)",
                "no_style_defined": "[No specific style defined]",
                "no_excludes_defined": "[No excluded styles defined]",
                "style_placeholder": "e.g. Indie Pop with electronic elements, Synthwave with retro atmosphere, etc. (max. 1000 characters)",
                "exclude_placeholder": "e.g. Metal, Schlager, etc. (max. 1000 characters)",
                "lyrics_placeholder": "Song lyrics (max. 5000 characters)",
                "prompt_style_limit": "Note: The style can be up to 1000 characters long. Use this opportunity for detailed descriptions.",
                "prompt_exclude_limit": "Note: Excluded styles can be up to 1000 characters long. List all unwanted style elements.",
                "prompt_lyrics_limit": "Note: The song lyrics can be up to 5000 characters long. Use this opportunity for extensive lyrics.",
                "fine_tuning_settings": "Fine Tuning Settings",
                "genre_settings": "Genre Settings",
                "tempo_settings": "Tempo Settings",
                "mood_settings": "Mood Settings",
                "instrument_settings": "Instrumentation Settings",
                "vocal_settings": "Vocal Settings",
                "effect_settings": "Effect Settings",
                "production_settings": "Production Settings",
                "special_settings": "Special Settings",
                "chatgpt_hint": "(use ChatGPT 4o)"
            }
        }
        self.lang = "de"
        self.track_template = None
        self.savefile = str(pathlib.Path.home() / ".suno_prompt_autosave.json")
        self.configfile = str(pathlib.Path.home() / ".suno_prompt_gui_config.json")
        self.last_dir = os.path.expanduser("~")
        self.last_global_style = ""
        self.last_global_exclude = ""
        self.current_color_theme = "blue"
        self.fine_tuning_settings = None
        self.load_config()
        self.create_widgets()
        self.load_autosave()
        self.check_for_update()

    def create_widgets(self):
        # Logo und Titelzeile
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 0), padx=30)
        self.logo = ctk.CTkLabel(header_frame, text="🎵", font=("Segoe UI Emoji", 36))
        self.logo.pack(side="left", padx=(0, 10))
        
        # Titel mit ChatGPT Hinweis
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left")
        
        self.header = ctk.CTkLabel(title_frame, text=self.t('title'), font=("Segoe UI", 32, "bold"), text_color="#60aaff")
        self.header.pack(side="left")
        
        self.chatgpt_label = ctk.CTkLabel(title_frame, text=self.t('chatgpt_hint'), font=("Segoe UI", 12), text_color="#ff6b6b")
        self.chatgpt_label.pack(side="left", padx=(10, 0), pady=(15, 0))

        # Farbschema- und Sprach-Auswahl
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.pack(fill="x", padx=30, pady=(0, 10))
        ctk.CTkLabel(theme_frame, text=self.t('theme')).pack(side="left", padx=(0, 10))
        self.theme_option = ctk.CTkOptionMenu(theme_frame, values=["dark", "light", "system"], command=self.change_theme)
        self.theme_option.set("dark")
        self.theme_option.pack(side="left")
        ctk.CTkLabel(theme_frame, text=self.t('accent')).pack(side="left", padx=(30, 10))
        self.color_option = ctk.CTkOptionMenu(theme_frame, values=["blue", "green", "dark-blue"], command=self.change_color)
        self.color_option.set("blue")
        self.color_option.pack(side="left")
        ctk.CTkLabel(theme_frame, text=self.t('language')).pack(side="left", padx=(30, 10))
        self.lang_option = ctk.CTkOptionMenu(theme_frame, values=["de", "en"], command=self.change_language)
        self.lang_option.set(self.lang)
        self.lang_option.pack(side="left")

        # Haupt-Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=20)

        # Linke Seite: Album Infos
        self.left_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.left_frame.pack(side="left", fill="y", padx=30, pady=30)

        self.title_entry = ctk.CTkEntry(self.left_frame, width=350, placeholder_text="z.B. Sommerträume")
        ctk.CTkLabel(self.left_frame, text=self.t('album_title'), anchor="w").pack(fill="x", pady=(10, 0))
        self.title_entry.pack(pady=5)

        self.num_tracks = tk.IntVar(value=5)
        self.num_tracks_spin = ctk.CTkSlider(self.left_frame, from_=1, to=30, number_of_steps=29, variable=self.num_tracks, width=300, command=self.update_tracks)
        ctk.CTkLabel(self.left_frame, text=self.t('num_tracks'), anchor="w").pack(fill="x", pady=(10, 0))
        self.num_tracks_spin.pack(pady=5)
        self.num_tracks_label = ctk.CTkLabel(self.left_frame, text="5")
        self.num_tracks_label.pack()
        self.num_tracks.trace_add('write', lambda *args: self.num_tracks_label.configure(text=str(self.num_tracks.get())))

        self.language_entry = ctk.CTkEntry(self.left_frame, width=350, placeholder_text="z.B. Deutsch")
        ctk.CTkLabel(self.left_frame, text=self.t('lyrics_lang'), anchor="w").pack(fill="x", pady=(10, 0))
        self.language_entry.pack(pady=5)

        self.narrative_text = ctk.CTkTextbox(self.left_frame, width=350, height=70)
        ctk.CTkLabel(self.left_frame, text=self.t('narrative'), anchor="w").pack(fill="x", pady=(10, 0))
        self.narrative_text.pack(pady=5)
        self.narrative_text.insert("1.0", "Kurze Beschreibung der Albumstory ...")

        self.global_style_entry = ctk.CTkEntry(self.left_frame, width=350, placeholder_text="z.B. Indie Pop, Synthwave")
        ctk.CTkLabel(self.left_frame, text=self.t('global_style'), anchor="w").pack(fill="x", pady=(10, 0))
        self.global_style_entry.pack(pady=5)
        self.global_style_entry.bind('<KeyRelease>', self.apply_global_style_to_tracks)
        self.last_global_style = self.global_style_entry.get()

        self.global_exclude_entry = ctk.CTkEntry(self.left_frame, width=350, placeholder_text="z.B. Schlager, Metal")
        ctk.CTkLabel(self.left_frame, text=self.t('global_exclude'), anchor="w").pack(fill="x", pady=(10, 0))
        self.global_exclude_entry.pack(pady=5)
        self.global_exclude_entry.bind('<KeyRelease>', self.apply_global_exclude_to_tracks)
        self.last_global_exclude = self.global_exclude_entry.get()

        # Zusatzoptionen-Frame
        self.options_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.options_frame.pack(side="left", fill="y", padx=10, pady=30)
        ctk.CTkLabel(self.options_frame, text=self.t('additional_options'), font=("Segoe UI", 16, "bold"), text_color="#60aaff").pack(pady=(10, 10))
        
        self.desc_var = tk.BooleanVar(value=False)
        self.cover_var = tk.BooleanVar(value=False)
        self.albumcover_var = tk.BooleanVar(value=False)
        self.cover_text_var = tk.StringVar(value="mit")
        self.desc_check = ctk.CTkCheckBox(self.options_frame, text=self.t('generate_description'), variable=self.desc_var)
        self.desc_check.pack(anchor="w", pady=5)
        self.cover_check = ctk.CTkCheckBox(self.options_frame, text=self.t('generate_cover'), variable=self.cover_var, command=self._toggle_cover_options)
        self.cover_check.pack(anchor="w", pady=5)
        self.cover_text_label = ctk.CTkLabel(self.options_frame, text=self.t('song_title_in_cover'))
        self.cover_text_radio1 = ctk.CTkRadioButton(self.options_frame, text=self.t('with_song_title'), variable=self.cover_text_var, value="mit")
        self.cover_text_radio2 = ctk.CTkRadioButton(self.options_frame, text=self.t('without_song_title'), variable=self.cover_text_var, value="ohne")
        self.cover_text_label.pack(anchor="w", padx=20)
        self.cover_text_radio1.pack(anchor="w", padx=30)
        self.cover_text_radio2.pack(anchor="w", padx=30)
        self.albumcover_check = ctk.CTkCheckBox(self.options_frame, text=self.t('generate_album_cover'), variable=self.albumcover_var)
        self.albumcover_check.pack(anchor="w", pady=5)

        # Rechte Seite: Tracks mit Scrollbereich
        self.right_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        ctk.CTkLabel(self.right_frame, text=self.t('tracks'), font=("Segoe UI", 20, "bold"), text_color="#60aaff").pack(pady=(10, 10))

        self.tracks_canvas = tk.Canvas(self.right_frame, bg="#23272a", highlightthickness=0)
        self.tracks_scrollbar = ctk.CTkScrollbar(self.right_frame, orientation="vertical", command=self.tracks_canvas.yview)
        self.tracks_scrollbar.pack(side="right", fill="y")
        self.tracks_canvas.pack(side="left", fill="both", expand=True)
        self.tracks_canvas.configure(yscrollcommand=self.tracks_scrollbar.set)
        self.tracks_inner = ctk.CTkFrame(self.tracks_canvas)
        self.tracks_window = self.tracks_canvas.create_window((0, 0), window=self.tracks_inner, anchor="nw")
        self.tracks_inner.bind("<Configure>", lambda e: self.tracks_canvas.configure(scrollregion=self.tracks_canvas.bbox("all")))
        self.tracks_canvas.bind('<Configure>', self.resize_tracks_window)
        # Mousewheel-Binding für Scrollen
        self.tracks_canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.tracks_canvas.bind_all('<Button-4>', self._on_mousewheel)  # Linux

        self.track_data = []  # Track-Daten als Liste von Dicts
        self.track_entries = []
        self.update_tracks(init=True)

        # Button-Leiste unten
        self.button_frame = ctk.CTkFrame(self, fg_color="#23272a")
        self.button_frame.pack(fill="x", pady=(0, 30))
        self.generate_btn = ctk.CTkButton(self.button_frame, text=self.t('save_prompt'), command=self.generate_prompt, width=220, height=50, font=("Segoe UI", 16, "bold"))
        self.generate_btn.pack(side="left", padx=20)
        self.fine_tuning_btn = ctk.CTkButton(self.button_frame, text=self.t('fine_tuning'), command=self.show_fine_tuning, width=160, height=50)
        self.fine_tuning_btn.pack(side="left", padx=10)
        self.pdf_btn = ctk.CTkButton(self.button_frame, text=self.t('export_pdf'), command=self.export_pdf, width=160, height=50)
        self.pdf_btn.pack(side="left", padx=10)
        self.copy_btn = ctk.CTkButton(self.button_frame, text=self.t('copy_prompt'), command=self.copy_prompt, width=160, height=50)
        self.copy_btn.pack(side="left", padx=10)
        self.preview_btn = ctk.CTkButton(self.button_frame, text=self.t('preview'), command=self.show_preview, width=120, height=50)
        self.preview_btn.pack(side="left", padx=10)
        self.export_btn = ctk.CTkButton(self.button_frame, text=self.t('export_project'), command=self.export_project, width=160, height=50)
        self.export_btn.pack(side="left", padx=10)
        self.import_btn = ctk.CTkButton(self.button_frame, text=self.t('import_project'), command=self.import_project, width=160, height=50)
        self.import_btn.pack(side="left", padx=10)
        self.help_btn = ctk.CTkButton(self.button_frame, text=self.t('help_faq'), command=self.show_help, width=120, height=50)
        self.help_btn.pack(side="right", padx=10)
        self.quit_btn = ctk.CTkButton(self.button_frame, text=self.t('quit'), command=self.destroy, width=120, height=50, font=("Segoe UI", 16))
        self.quit_btn.pack(side="right", padx=20)

        # Footer
        self.footer = ctk.CTkLabel(self, text=self.t('footer'), font=("Segoe UI", 12), text_color="#99aab5")
        self.footer.pack(side="bottom", pady=(0, 10))

    def t(self, key):
        return self.languages[self.lang][key]

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)
        self.save_config()
        gui_state = self._get_gui_state()
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self._restore_gui_state(gui_state)
        self.update_language_and_theme()
    def change_color(self, color):
        ctk.set_default_color_theme(color)
        self.current_color_theme = color
        self.save_config()
        # Eingaben zwischenspeichern
        gui_state = self._get_gui_state()
        # Alle Widgets neu aufbauen, damit die Akzentfarbe global übernommen wird
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self._restore_gui_state(gui_state)
        self.update_language_and_theme()
    def change_language(self, lang):
        """Ändert die Sprache der Anwendung."""
        self.lang = lang
        self.save_config()
        
        # Speichere den aktuellen GUI-Zustand
        gui_state = self._get_gui_state()
        
        # Baue die GUI neu auf
        for widget in self.winfo_children():
            widget.destroy()
        
        # Erstelle die GUI neu
        self.create_widgets()
        
        # Stelle den GUI-Zustand wieder her
        self._restore_gui_state(gui_state)
        
        # Aktualisiere die Sprache und das Theme
        self.update_language_and_theme()
    def resize_tracks_window(self, event):
        self.tracks_canvas.itemconfig(self.tracks_window, width=event.width)
    def update_tracks(self, *args, init=False):
        """Aktualisiert die Track-Liste."""
        try:
            for widget in self.tracks_inner.winfo_children():
                widget.destroy()
                
            num = self.num_tracks.get() if isinstance(self.num_tracks.get(), int) else int(float(self.num_tracks.get()))
                
            # Initialisierung oder Anpassung der Datenliste
            if init or len(self.track_data) != num:
                old_data = self.track_data if hasattr(self, 'track_data') else []
                self.track_data = []
                for i in range(num):
                    if i < len(old_data):
                        # Kompatibilität: ggf. style nachrüsten
                        d = old_data[i]
                        if "style" not in d:
                            d["style"] = ""
                        self.track_data.append(d)
                    else:
                        self.track_data.append({"title": "", "style": "", "exclude": ""})
                
            self.track_entries.clear()
            for i in range(num):
                row_frame = ctk.CTkFrame(self.tracks_inner)
                row_frame.pack(fill="x", pady=6, padx=10)
                    
                title_entry = ctk.CTkEntry(row_frame, width=180, placeholder_text=f"{self.t('track_title')} {i+1}")
                ctk.CTkLabel(row_frame, text=f"{self.t('track_title')} {i+1}:", width=110).pack(side="left")
                title_entry.pack(side="left", padx=5)
                title_entry.insert(0, self.track_data[i]["title"])
                    
                # Musikstil-Feld
                style_entry = ctk.CTkEntry(row_frame, width=140, placeholder_text=self.t('style_placeholder'))
                ctk.CTkLabel(row_frame, text=self.t('music_style'), width=80).pack(side="left", padx=(10,0))
                style_entry.pack(side="left", padx=5)
                style_entry.insert(0, self.track_data[i]["style"])
                    
                # Excludes-Feld
                exclude_entry = ctk.CTkEntry(row_frame, width=140, placeholder_text=self.t('exclude_placeholder'))
                ctk.CTkLabel(row_frame, text=self.t('track_excludes'), width=80).pack(side="left", padx=(10,0))
                exclude_entry.pack(side="left", padx=5)
                exclude_entry.insert(0, self.track_data[i]["exclude"])
                    
                # Track-Vorlagen Buttons
                btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                btn_frame.pack(side="left", padx=10)
                    
                save_tpl_btn = ctk.CTkButton(btn_frame, text=self.t('template_save'), width=40, 
                                           command=lambda e=title_entry, s=style_entry, x=exclude_entry: 
                                           self.save_track_template(e, s, x))
                save_tpl_btn.pack(side="top", pady=2)
                    
                apply_tpl_btn = ctk.CTkButton(btn_frame, text=self.t('template_apply'), width=40,
                                            command=lambda e=title_entry, s=style_entry, x=exclude_entry: 
                                            self.apply_track_template(e, s, x))
                apply_tpl_btn.pack(side="top", pady=2)
                    
                # Callback zum Speichern der Eingaben
                def save_entry(event=None, idx=i, t=title_entry, s=style_entry, e=exclude_entry):
                    self.track_data[idx]["title"] = t.get()
                    self.track_data[idx]["style"] = s.get()
                    self.track_data[idx]["exclude"] = e.get()
                    self.autosave()
                    
                title_entry.bind('<KeyRelease>', save_entry)
                style_entry.bind('<KeyRelease>', save_entry)
                exclude_entry.bind('<KeyRelease>', save_entry)
                    
                self.track_entries.append((title_entry, style_entry, exclude_entry))
                
            self.autosave()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren der Tracks: {str(e)}")
    def autosave(self):
        data = {
            "title": self.title_entry.get(),
            "num_tracks": self.num_tracks.get(),
            "language": self.language_entry.get(),
            "narrative": self.narrative_text.get('1.0', 'end').strip(),
            "global_style": self.global_style_entry.get(),
            "global_exclude": self.global_exclude_entry.get(),
            "tracks": self.track_data
        }
        try:
            with open(self.savefile, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass
    def save_track_template(self, title_entry, style_entry, exclude_entry):
        self.track_template = {
            "title": title_entry.get(),
            "style": style_entry.get(),
            "exclude": exclude_entry.get()
        }
    def apply_track_template(self, title_entry, style_entry, exclude_entry):
        if self.track_template:
            title_entry.delete(0, 'end')
            title_entry.insert(0, self.track_template.get("title", ""))
            style_entry.delete(0, 'end')
            style_entry.insert(0, self.track_template.get("style", ""))
            exclude_entry.delete(0, 'end')
            exclude_entry.insert(0, self.track_template.get("exclude", ""))
    def load_autosave(self):
        if os.path.exists(self.savefile):
            try:
                with open(self.savefile, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.title_entry.insert(0, data.get("title", ""))
                self.num_tracks.set(data.get("num_tracks", 5))
                self.language_entry.insert(0, data.get("language", ""))
                self.narrative_text.delete('1.0', 'end')
                self.narrative_text.insert('1.0', data.get("narrative", ""))
                self.global_style_entry.insert(0, data.get("global_style", ""))
                self.global_exclude_entry.insert(0, data.get("global_exclude", ""))
                self.track_data = data.get("tracks", [])
                self.update_tracks()
            except Exception:
                pass
    def validate_inputs(self):
        """Validiert die Eingaben und gibt Warnungen zurück."""
        warnings = []
        
        # Prüfe Album-Titel
        if not self.title_entry.get().strip():
            warnings.append("Kein Albumtitel eingegeben. Die KI wird einen passenden Titel generieren.")
        
        # Prüfe Anzahl der Tracks
        num_tracks = self.num_tracks.get()
        if num_tracks < 1 or num_tracks > 30:
            warnings.append("Die Anzahl der Tracks sollte zwischen 1 und 30 liegen.")
        
        # Prüfe Sprache
        if not self.language_entry.get().strip():
            warnings.append("Keine Sprache für die Lyrics angegeben.")
        
        # Prüfe Narrative
        narrative = self.narrative_text.get('1.0', 'end').strip()
        if len(narrative) < 10:
            warnings.append("Die Albumstory ist sehr kurz. Bitte geben Sie mehr Details ein.")
        
        # Prüfe auf Widersprüche in den Stilen
        global_style = self.global_style_entry.get().strip()
        global_exclude = self.global_exclude_entry.get().strip()
        if global_style and global_exclude:
            # Prüfe ob ausgeschlossene Stile im Hauptstil vorkommen
            for exclude in global_exclude.split(','):
                if exclude.strip() in global_style:
                    warnings.append(f"Widerspruch: '{exclude.strip()}' ist sowohl im Hauptstil als auch in den Excludes.")
        
        return warnings

    def generate_prompt(self):
        self.autosave()
        
        # Validiere Eingaben
        warnings = self.validate_inputs()
        if warnings:
            if not messagebox.askyesno("Warnungen", 
                "Es wurden folgende Warnungen gefunden:\n\n" + 
                "\n".join(f"- {w}" for w in warnings) + 
                "\n\nMöchten Sie trotzdem fortfahren?"):
                return
        
        # Sammle Metadaten
        import datetime
        metadata = {
            "version": "1.0.0",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_tags": [],
            "warnings": warnings
        }
        
        title = self.title_entry.get().strip()
        if not title:
            title = "[Die KI soll einen passenden Albumtitel wählen]"
        num_tracks = self.num_tracks.get() if isinstance(self.num_tracks.get(), int) else int(float(self.num_tracks.get()))
        language = self.language_entry.get()
        narrative = self.narrative_text.get('1.0', 'end').strip()
        global_style = self.global_style_entry.get()
        global_exclude = self.global_exclude_entry.get()
        
        # Phase 1: Album-Konzept
        output_phase1 = []
        output_phase1.append("# PHASE 1: Album-Konzept\n")
        output_phase1.append("## Metadaten")
        output_phase1.append(f"- Version: {metadata['version']}")
        output_phase1.append(f"- Generiert am: {metadata['timestamp']}")
        if metadata['warnings']:
            output_phase1.append("\n### Warnungen")
            for warning in metadata['warnings']:
                output_phase1.append(f"- {warning}")
        output_phase1.append("\n## Anleitung für die KI")
        output_phase1.append("""
[KI: Bitte folge diesen Schritten:
1. Analysiere die folgenden Informationen
2. Generiere ein Album-Konzept
3. Warte auf Bestätigung, bevor du fortfährst
4. Bei Fragen oder Unklarheiten, frage nach]

### Beispiel für ein gutes Album-Konzept:
- Albumtitel: "Sommerträume"
- Beschreibung: "Eine Reise durch die verschiedenen Facetten des Sommers, von erfrischenden Morgentönen bis zu warmen Abendklängen."
- Tracktitel: ["Morgentau", "Sonnenschein", "Abendbrisen", ...]
- Inspiration: [inspiration] (z.B. John Lennon's Songwriting, David Bowie's Experimentierfreude)
""")
        output_phase1.append("\n## Grundlegende Informationen")
        output_phase1.append(f"- Anzahl der Tracks: {num_tracks}")
        output_phase1.append(f"- Lyrics Sprache: {language}")
        output_phase1.append(f"- Narrative Overview: {narrative}\n")
        output_phase1.append("## Musikstil")
        output_phase1.append("### Hauptstil")
        output_phase1.append("```style")
        output_phase1.append(global_style)
        output_phase1.append("```\n")
        output_phase1.append("### Ausgeschlossene Stile")
        output_phase1.append("```excludes")
        output_phase1.append(global_exclude if global_exclude else "[leer]")
        output_phase1.append("```\n")
        output_phase1.append("\n[KI: Bitte generiere nun:]")
        output_phase1.append("1. Einen passenden Albumtitel")
        output_phase1.append("2. Einen passenden Titel für jeden Track")
        output_phase1.append("3. Eine kurze Beschreibung des Albums (2-3 Sätze)")
        output_phase1.append("\n[KI: Warte nach der Generierung auf Bestätigung, bevor du fortfährst.]\n")
        
        # Phase 2: Track-Details
        output_phase2 = []
        output_phase2.append("# PHASE 2: Track-Details\n")
        output_phase2.append("""
[KI: Bitte folge diesen Schritten für jeden Track:
1. Generiere passende Lyrics zur Sprache und zum Stil
2. Beachte die Stilvorgaben in der angegebenen Priorität
3. Stelle sicher, dass die Lyrics zur Stimmung passen
4. Warte auf Bestätigung nach jedem Track]

### Beispiel für einen guten Track:
- Titel: "Morgentau"
- Lyrics: [Passende Lyrics zur Stimmung]
- Style: [Klar definierter Stil mit allen Details]
""")
        
        for i, track in enumerate(self.track_data, 1):
            track_title = track["title"]
            track_style = track["style"]
            track_exclude = track["exclude"]
            
            # Markdown-Format für jeden Track
            output_phase2.append(f"\n## Track {i}\n")
            
            # Song Name
            output_phase2.append("### Song Name")
            output_phase2.append(f"{track_title if track_title else '[Die KI soll einen passenden Titel wählen]'}\n")
            
            # Song Style
            output_phase2.append("### Song Style")
            output_phase2.append("```style")
            output_phase2.append(track_style if track_style else self.t('no_style_defined'))
            output_phase2.append("```\n")
            
            # Excluded Styles
            output_phase2.append("### Excluded Styles")
            output_phase2.append("```excludes")
            if track_exclude:
                output_phase2.append(track_exclude)
            else:
                output_phase2.append("[KI: Bitte schlage passende ausgeschlossene Stile basierend auf dem definierten Musikstil vor]")
            output_phase2.append("```\n")

            # Song Lyrics
            output_phase2.append("### Song Lyrics")
            output_phase2.append("```lyrics")
            output_phase2.append("[Intro]")
            output_phase2.append("[Verse 1]")
            output_phase2.append("[Pre-Chorus]")
            output_phase2.append("[Chorus]")
            output_phase2.append("[Verse 2]")
            output_phase2.append("[Bridge]")
            output_phase2.append("[Chorus]")
            output_phase2.append("[Outro]")
            output_phase2.append("```\n")
        
        # Kombiniere die Phasen
        output = output_phase1 + output_phase2
        
        # Erstelle das Prompt-Objekt
        prompt = {
            "version": metadata["version"],
            "timestamp": metadata["timestamp"],
            "user_tags": metadata["user_tags"],
            "warnings": metadata["warnings"],
            "title": title,
            "num_tracks": num_tracks,
            "language": language,
            "narrative": narrative,
            "global_style": global_style,
            "global_exclude": global_exclude,
            "tracks": self.track_data,
            "prompt": "\n".join(output)
        }
        
        # Speichern des Prompts
        self.save_prompt(prompt)
        
        # Generiere Bilder wenn ausgewählt
        if self.cover_var.get() or self.albumcover_var.get():
            self.generate_images(prompt)
    
    def generate_images(self, prompt):
        """Generiert die ausgewählten Bilder basierend auf dem Prompt."""
        try:
            # Album Cover
            if self.albumcover_var.get():
                album_cover_prompt = f"""
                Erstelle ein Album-Cover für:
                Titel: {prompt['title']}
                Stil: {prompt['global_style']}
                Beschreibung: {prompt['narrative']}
                """
                # TODO: Hier die tatsächliche Bildgenerierung implementieren
                messagebox.showinfo("Album Cover", "Album Cover Generierung wird implementiert...")
            
            # Track Covers und Beschreibungen
            if self.cover_var.get() or self.desc_var.get():
                for i, track in enumerate(prompt['tracks'], 1):
                    track_title = track['title'] if track['title'] else f"Track {i}"
                    
                    # Track Cover
                    if self.cover_var.get():
                        cover_prompt = f"""
                        Erstelle ein Cover für:
                        Titel: {track_title}
                        Stil: {track['style']}
                        Mit Songtitel: {self.cover_text_var.get() == 'mit'}
                        """
                        # TODO: Hier die tatsächliche Bildgenerierung implementieren
                        messagebox.showinfo("Track Cover", f"Cover Generierung für {track_title} wird implementiert...")
                    
                    # Track Beschreibung
                    if self.desc_var.get():
                        desc_prompt = f"""
                        Erstelle eine Beschreibung für:
                        Titel: {track_title}
                        Stil: {track['style']}
                        Ausgeschlossene Stile: {track['exclude']}
                        """
                        # TODO: Hier die tatsächliche Beschreibungsgenerierung implementieren
                        messagebox.showinfo("Track Beschreibung", f"Beschreibung für {track_title} wird implementiert...")
                    
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Bildgenerierung: {str(e)}")

    def save_prompt(self, prompt):
        """Speichert den generierten Prompt in einer Datei."""
        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Prompt speichern unter"
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(prompt["prompt"])
                
                # Generiere Bilder und Beschreibungen nach dem Speichern
                if self.cover_var.get() or self.albumcover_var.get() or self.desc_var.get():
                    self.generate_images(prompt)
                
                messagebox.showinfo("Erfolg", "Prompt wurde erfolgreich gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Prompts: {str(e)}")

    def show_fine_tuning(self):
        """Zeigt den Dialog für Feineinstellungen an."""
        try:
            # Lösche den globalen Stil vor dem Öffnen der Feineinstellungen
            self.global_style_entry.delete(0, 'end')
            self.last_global_style = ""
            
            # Lösche auch die Stile in den Tracks
            for _, style_entry, _ in self.track_entries:
                style_entry.delete(0, 'end')
            
            dialog = FineTuningDialog(self)
            self.wait_window(dialog)
            if hasattr(dialog, 'result') and dialog.result is not None:
                self.fine_tuning_settings = dialog.result
                
                # Erstelle einen formatierten Text aus den Feineinstellungen
                style_parts = []
                
                # Sammle alle Teile mit ihren Längen
                parts_with_length = []
                
                # Genre & Subgenre
                if any(key in self.fine_tuning_settings for key in ['genre', 'subgenre']):
                    genre_part = ["Genre & Subgenre:"]
                    if 'genre' in self.fine_tuning_settings:
                        genre_part.append(f"- Genre: {self.fine_tuning_settings['genre']}")
                    if 'subgenre' in self.fine_tuning_settings:
                        genre_part.append(f"- Subgenre: {self.fine_tuning_settings['subgenre']}")
                    parts_with_length.append(("\n".join(genre_part), len("\n".join(genre_part))))
                
                # Tempo & Tonart
                if 'tempo' in self.fine_tuning_settings or 'key' in self.fine_tuning_settings:
                    tempo_part = ["\nTempo & Tonart:"]
                    if 'tempo' in self.fine_tuning_settings:
                        tempo_part.append(f"- Tempo: {self.fine_tuning_settings['tempo']} BPM")
                    if 'key' in self.fine_tuning_settings:
                        tempo_part.append(f"- Key: {self.fine_tuning_settings['key']}")
                    parts_with_length.append(("\n".join(tempo_part), len("\n".join(tempo_part))))
                
                # Stimmung
                if 'mood' in self.fine_tuning_settings:
                    mood_part = f"\nStimmung: {self.fine_tuning_settings['mood']}"
                    parts_with_length.append((mood_part, len(mood_part)))
                
                # Instrumentierung
                if 'instruments' in self.fine_tuning_settings:
                    instruments_part = f"\nInstrumentierung: {self.fine_tuning_settings['instruments']}"
                    parts_with_length.append((instruments_part, len(instruments_part)))
                
                # Gesangsstil
                if 'vocal_style' in self.fine_tuning_settings:
                    vocal_part = f"\nGesangsstil: {self.fine_tuning_settings['vocal_style']}"
                    parts_with_length.append((vocal_part, len(vocal_part)))
                
                # Effekte
                if 'effects' in self.fine_tuning_settings:
                    effects_part = f"\nEffekte: {self.fine_tuning_settings['effects']}"
                    parts_with_length.append((effects_part, len(effects_part)))
                
                # Produktion
                if 'production' in self.fine_tuning_settings:
                    production_part = f"\nProduktion: {self.fine_tuning_settings['production']}"
                    parts_with_length.append((production_part, len(production_part)))
                
                # Besonderheiten
                if 'special' in self.fine_tuning_settings:
                    special_part = f"\nBesonderheiten: {self.fine_tuning_settings['special']}"
                    parts_with_length.append((special_part, len(special_part)))
                
                # Baue den Text zusammen, ohne die 1000 Zeichen zu überschreiten
                current_length = 0
                final_parts = []
                
                for part, length in parts_with_length:
                    if current_length + length <= 1000:
                        final_parts.append(part)
                        current_length += length
                    else:
                        # Wenn der Teil zu lang ist, versuche ihn zu kürzen
                        remaining_chars = 1000 - current_length
                        if remaining_chars > 20:  # Nur kürzen wenn genug Platz für sinnvollen Text
                            # Kürze den Text und füge "..." hinzu
                            shortened_part = part[:remaining_chars-3] + "..."
                            final_parts.append(shortened_part)
                        break
                
                # Füge die formatierten Feineinstellungen zum globalen Stil hinzu
                formatted_style = "".join(final_parts)
                self.global_style_entry.insert(0, formatted_style)
                
                # Aktualisiere die Tracks mit dem neuen globalen Stil
                self.apply_global_style_to_tracks()
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen der Feineinstellungen: {str(e)}")

    def export_pdf(self):
        """Exportiert den generierten Prompt als PDF."""
        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                title="Als PDF speichern"
            )
            if save_path:
                prompt = self.get_prompt_text()
                c = canvas.Canvas(save_path, pagesize=A4)
                width, height = A4
                lines = prompt.split("\n")
                y = height - 40
                for line in lines:
                    if y < 40:
                        c.showPage()
                        y = height - 40
                    c.setFont("Helvetica", 10)
                    c.drawString(40, y, line)
                    y -= 15
                c.save()
                messagebox.showinfo("Erfolg", "PDF wurde erfolgreich erstellt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen der PDF: {str(e)}")

    def copy_prompt(self):
        """Kopiert den generierten Prompt in die Zwischenablage."""
        try:
            prompt = self.get_prompt_text()
            self.clipboard_clear()
            self.clipboard_append(prompt)
            messagebox.showinfo("Erfolg", "Prompt wurde in die Zwischenablage kopiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Kopieren des Prompts: {str(e)}")

    def show_preview(self):
        """Zeigt eine Vorschau des generierten Prompts an."""
        try:
            preview_window = tk.Toplevel(self)
            preview_window.title("Prompt Vorschau")
            preview_window.geometry("800x600")
            
            text_widget = tk.Text(preview_window, wrap=tk.WORD, padx=10, pady=10)
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            prompt = self.get_prompt_text()
            text_widget.insert("1.0", prompt)
            text_widget.config(state="disabled")
            
            scrollbar = ttk.Scrollbar(preview_window, command=text_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)

            # Füge Mausrad-Scrolling für das Vorschaufenster hinzu
            def on_mousewheel(event):
                text_widget.yview_scroll(int(-1*(event.delta/120)), "units")
            
            text_widget.bind('<MouseWheel>', on_mousewheel)  # Windows
            text_widget.bind('<Button-4>', lambda e: text_widget.yview_scroll(-1, "units"))  # Linux
            text_widget.bind('<Button-5>', lambda e: text_widget.yview_scroll(1, "units"))  # Linux

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Anzeigen der Vorschau: {str(e)}")

    def export_project(self):
        """Exportiert das aktuelle Projekt als JSON-Datei."""
        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")],
                title="Projekt exportieren"
            )
            if save_path:
                project_data = {
                    "title": self.title_entry.get(),
                    "num_tracks": self.num_tracks.get(),
                    "language": self.language_entry.get(),
                    "narrative": self.narrative_text.get("1.0", "end-1c"),
                    "global_style": self.global_style_entry.get(),
                    "global_exclude": self.global_exclude_entry.get(),
                    "tracks": self.track_data,
                    "fine_tuning": self.fine_tuning_settings
                }
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(project_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Erfolg", "Projekt wurde erfolgreich exportiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Exportieren des Projekts: {str(e)}")

    def import_project(self):
        """Importiert ein Projekt aus einer JSON-Datei."""
        try:
            open_path = filedialog.askopenfilename(
                filetypes=[("JSON Files", "*.json")],
                title="Projekt importieren"
            )
            if open_path:
                with open(open_path, "r", encoding="utf-8") as f:
                    project_data = json.load(f)
                
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, project_data.get("title", ""))
                
                self.num_tracks.set(project_data.get("num_tracks", 5))
                
                self.language_entry.delete(0, tk.END)
                self.language_entry.insert(0, project_data.get("language", ""))
                
                self.narrative_text.delete("1.0", tk.END)
                self.narrative_text.insert("1.0", project_data.get("narrative", ""))
                
                self.global_style_entry.delete(0, tk.END)
                self.global_style_entry.insert(0, project_data.get("global_style", ""))
                
                self.global_exclude_entry.delete(0, tk.END)
                self.global_exclude_entry.insert(0, project_data.get("global_exclude", ""))
                
                self.track_data = project_data.get("tracks", [])
                self.fine_tuning_settings = project_data.get("fine_tuning", {})
                
                self.update_tracks()
                messagebox.showinfo("Erfolg", "Projekt wurde erfolgreich importiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Importieren des Projekts: {str(e)}")

    def show_help(self):
        """Zeigt die Hilfe-Seite an."""
        help_window = tk.Toplevel(self)
        help_window.title(self.t('help_title'))
        help_window.geometry("600x400")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", self.t('help_text'))
        text_widget.config(state="disabled")
        
        scrollbar = ttk.Scrollbar(help_window, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        # Füge Mausrad-Scrolling für das Hilfe-Fenster hinzu
        def on_mousewheel(event):
            text_widget.yview_scroll(int(-1*(event.delta/120)), "units")
        
        text_widget.bind('<MouseWheel>', on_mousewheel)  # Windows
        text_widget.bind('<Button-4>', lambda e: text_widget.yview_scroll(-1, "units"))  # Linux
        text_widget.bind('<Button-5>', lambda e: text_widget.yview_scroll(1, "units"))  # Linux

    def _toggle_cover_options(self):
        """Schaltet die Cover-Optionen ein/aus."""
        if self.cover_var.get():
            self.cover_text_label.configure(state="normal")
            self.cover_text_radio1.configure(state="normal")
            self.cover_text_radio2.configure(state="normal")
        else:
            self.cover_text_label.configure(state="disabled")
            self.cover_text_radio1.configure(state="disabled")
            self.cover_text_radio2.configure(state="disabled")

    def _on_mousewheel(self, event):
        """Behandelt das Mausrad-Scrollen."""
        # Prüfe, ob das Event vom Tracks-Canvas kommt
        if str(event.widget) == str(self.tracks_canvas):
            if hasattr(event, 'delta'):
                self.tracks_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif hasattr(event, 'num'):
                if event.num == 4:
                    self.tracks_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.tracks_canvas.yview_scroll(1, "units")

    def _get_gui_state(self):
        """Gibt den aktuellen GUI-Zustand zurück."""
        return {
            "title": self.title_entry.get(),
            "num_tracks": self.num_tracks.get(),
            "language": self.language_entry.get(),
            "narrative": self.narrative_text.get("1.0", "end-1c"),
            "global_style": self.global_style_entry.get(),
            "global_exclude": self.global_exclude_entry.get(),
            "tracks": self.track_data,
            "fine_tuning": self.fine_tuning_settings
        }

    def _restore_gui_state(self, gui_state):
        """Stellt den GUI-Zustand wieder her."""
        try:
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, gui_state.get("title", ""))
            
            self.num_tracks.set(gui_state.get("num_tracks", 5))
            
            self.language_entry.delete(0, tk.END)
            self.language_entry.insert(0, gui_state.get("language", ""))
            
            self.narrative_text.delete("1.0", tk.END)
            self.narrative_text.insert("1.0", gui_state.get("narrative", ""))
            
            self.global_style_entry.delete(0, tk.END)
            self.global_style_entry.insert(0, gui_state.get("global_style", ""))
            
            self.global_exclude_entry.delete(0, tk.END)
            self.global_exclude_entry.insert(0, gui_state.get("global_exclude", ""))
            
            self.track_data = gui_state.get("tracks", [])
            self.fine_tuning_settings = gui_state.get("fine_tuning", {})
            
            self.update_tracks()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Wiederherstellen des GUI-Zustands: {str(e)}")

    def update_language_and_theme(self):
        """Aktualisiert die Sprache und das Farbschema."""
        self.title(self.t('title'))
        self.update_tracks()
        
        # Aktualisiere die Labels
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                if widget.cget("text") in self.languages["de"].values():
                    for key, value in self.languages["de"].items():
                        if value == widget.cget("text"):
                            widget.configure(text=self.t(key))
                            break
        
        # Aktualisiere die Buttons
        self.generate_btn.configure(text=self.t('save_prompt'))
        self.quit_btn.configure(text=self.t('quit'))
        self.fine_tuning_btn.configure(text=self.t('fine_tuning'))
        
        # Aktualisiere den Footer
        self.footer.configure(text=self.t('footer'))

    def load_config(self):
        """Lädt die Konfiguration aus der Datei."""
        try:
            if os.path.exists(self.configfile):
                with open(self.configfile, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.lang = config.get("lang", "de")
                    self.current_color_theme = config.get("color", "blue")
                    self.last_dir = config.get("last_dir", os.path.expanduser("~"))
        except Exception:
            pass

    def save_config(self):
        """Speichert die Konfiguration in der Datei."""
        try:
            config = {
                "lang": self.lang,
                "color": self.current_color_theme,
                "last_dir": self.last_dir
            }
            with open(self.configfile, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def check_for_update(self):
        """Überprüft auf verfügbare Updates."""
        try:
            import urllib.request
            import json
            
            url = "https://api.github.com/repos/suno-ai/suno-prompt-generator/releases/latest"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                latest_version = data["tag_name"]
                
                if latest_version > "1.0.0":  # Aktuelle Version
                    if messagebox.askyesno("Update verfügbar", 
                        f"Version {latest_version} ist verfügbar. Möchten Sie die GitHub-Seite öffnen?"):
                        webbrowser.open("https://github.com/suno-ai/suno-prompt-generator/releases/latest")
        except Exception:
            pass

    def get_prompt_text(self):
        """Generiert den aktuellen Prompt-Text basierend auf den Eingaben."""
        # Sammle Metadaten
        import datetime
        metadata = {
            "version": "1.0.0",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_tags": [],
            "warnings": self.validate_inputs()
        }
        
        title = self.title_entry.get().strip()
        if not title:
            title = "[Die KI soll einen passenden Albumtitel wählen]"
        num_tracks = self.num_tracks.get() if isinstance(self.num_tracks.get(), int) else int(float(self.num_tracks.get()))
        language = self.language_entry.get()
        narrative = self.narrative_text.get('1.0', 'end').strip()
        global_style = self.global_style_entry.get()
        global_exclude = self.global_exclude_entry.get()
        
        # Phase 1: Album-Konzept
        output_phase1 = []
        output_phase1.append(f"# {self.t('prompt_phase1')}\n")
        output_phase1.append(f"## {self.t('prompt_metadata')}")
        output_phase1.append(f"- {self.t('prompt_version')} {metadata['version']}")
        output_phase1.append(f"- {self.t('prompt_generated')} {metadata['timestamp']}")
        if metadata['warnings']:
            output_phase1.append(f"\n### {self.t('prompt_warnings')}")
            for warning in metadata['warnings']:
                output_phase1.append(f"- {warning}")
        output_phase1.append(f"\n## {self.t('prompt_instructions')}")
        output_phase1.append(self.t('prompt_ki_steps'))
        output_phase1.append(f"\n### {self.t('prompt_example')}")
        output_phase1.append("""
- Albumtitel: "Sommerträume"
- Beschreibung: "Eine Reise durch die verschiedenen Facetten des Sommers, von erfrischenden Morgentönen bis zu warmen Abendklängen."
- Tracktitel: ["Morgentau", "Sonnenschein", "Abendbrisen", ...]
- Inspiration: [inspiration] (z.B. John Lennon's Songwriting, David Bowie's Experimentierfreude)
""")
        output_phase1.append("\n## Grundlegende Informationen")
        output_phase1.append(f"- Anzahl der Tracks: {num_tracks}")
        output_phase1.append(f"- Lyrics Sprache: {language}")
        output_phase1.append(f"- Narrative Overview: {narrative}\n")
        output_phase1.append("## Musikstil")
        output_phase1.append("### Hauptstil")
        output_phase1.append("```style")
        output_phase1.append(global_style)
        output_phase1.append("```\n")
        output_phase1.append("### Ausgeschlossene Stile")
        output_phase1.append("```excludes")
        output_phase1.append(global_exclude if global_exclude else "[leer]")
        output_phase1.append("```\n")
        output_phase1.append("\n[KI: Bitte generiere nun:]")
        output_phase1.append("1. Einen passenden Albumtitel")
        output_phase1.append("2. Einen passenden Titel für jeden Track")
        output_phase1.append("3. Eine kurze Beschreibung des Albums (2-3 Sätze)")
        output_phase1.append("\n[KI: Warte nach der Generierung auf Bestätigung, bevor du fortfährst.]\n")
        
        # Phase 2: Track-Details
        output_phase2 = []
        output_phase2.append("# PHASE 2: Track-Details\n")
        output_phase2.append("""
[KI: Bitte folge diesen Schritten für jeden Track:
1. Generiere passende Lyrics zur Sprache und zum Stil
2. Beachte die Stilvorgaben in der angegebenen Priorität
3. Stelle sicher, dass die Lyrics zur Stimmung passen
4. Warte auf Bestätigung nach jedem Track]

### Beispiel für einen guten Track:
- Titel: "Morgentau"
- Lyrics: [Passende Lyrics zur Stimmung]
- Style: [Klar definierter Stil mit allen Details]
""")
        
        for i, track in enumerate(self.track_data, 1):
            track_title = track["title"]
            track_style = track["style"]
            track_exclude = track["exclude"]
            
            # Markdown-Format für jeden Track
            output_phase2.append(f"\n## {self.t('prompt_track')} {i}\n")
            
            # Song Name
            output_phase2.append(f"### {self.t('prompt_song_name')}")
            output_phase2.append(f"{track_title if track_title else '[Die KI soll einen passenden Titel wählen]'}\n")
            
            # Song Style
            output_phase2.append(f"### {self.t('song_style')}")
            output_phase2.append(self.t('prompt_style_limit'))
            output_phase2.append("```style")
            output_phase2.append(track_style if track_style else self.t('no_style_defined'))
            output_phase2.append("```\n")
            
            # Excluded Styles
            output_phase2.append(f"### {self.t('excluded_styles')}")
            output_phase2.append(self.t('prompt_exclude_limit'))
            output_phase2.append("```excludes")
            if track_exclude:
                output_phase2.append(track_exclude)
            else:
                output_phase2.append("[KI: Bitte schlage passende ausgeschlossene Stile basierend auf dem definierten Musikstil vor]")
            output_phase2.append("```\n")

            # Song Lyrics
            output_phase2.append(f"### {self.t('prompt_song_lyrics')}")
            output_phase2.append(self.t('prompt_lyrics_limit'))
            output_phase2.append(self.t('prompt_ki_important'))
            output_phase2.append("```lyrics")
            lyrics_template = """
[Intro]
[Verse 1]
[Pre-Chorus]
[Chorus]
[Verse 2]
[Bridge]
[Chorus]
[Outro]
"""
            output_phase2.append(validate_lyrics_format(lyrics_template))
            output_phase2.append("```\n")
        
        # Kombiniere die Phasen
        output = output_phase1 + output_phase2
        
        prompt_text = "\n".join(output)
        return replace_parentheses_outside_lyrics(prompt_text)

    def apply_global_style_to_tracks(self, event=None):
        """Wendet den globalen Stil auf alle Tracks an."""
        global_style = self.global_style_entry.get()
        if global_style != self.last_global_style:
            self.last_global_style = global_style
            for _, style_entry, _ in self.track_entries:
                style_entry.delete(0, 'end')
                style_entry.insert(0, global_style)
        self.autosave()

    def apply_global_exclude_to_tracks(self, event=None):
        """Wendet die globalen Excludes auf alle Tracks an."""
        global_exclude = self.global_exclude_entry.get()
        if global_exclude != self.last_global_exclude:
            self.last_global_exclude = global_exclude
            for _, _, exclude_entry in self.track_entries:
                if not exclude_entry.get():  # Nur leere Felder überschreiben
                    exclude_entry.delete(0, 'end')
                    exclude_entry.insert(0, global_exclude)
        self.autosave()

def replace_parentheses_outside_lyrics(prompt_text: str) -> str:
    """
    Ersetzt alle runden Klammern außerhalb von Songtext-Blöcken (```lyrics ... ```)
    durch eckige Klammern. Songtext-Blöcke bleiben unverändert.
    """
    # Splitte den Prompt in Abschnitte, getrennt durch ```lyrics ... ```
    parts = re.split(r'(```lyrics[\s\S]*?```)', prompt_text)
    for i in range(len(parts)):
        # Nur außerhalb von Songtext-Blöcken ersetzen (gerade Indizes)
        if i % 2 == 0:
            # Ersetze (text) durch [text], aber nur wenn es kein Markdown-Link ist
            parts[i] = re.sub(r'\(([^\)\[]+)\)', r'[\1]', parts[i])
    return ''.join(parts)

def validate_lyrics_format(lyrics_text: str) -> str:
    """
    Validiert und korrigiert das Format von Songtexten:
    - Ersetzt runde Klammern () durch eckige Klammern []
    - Stellt sicher, dass alle Anweisungen/Effekte in eckigen Klammern stehen
    - Validiert Bandnamen
    """
    # Ersetze alle runden Klammern durch eckige
    lyrics_text = re.sub(r'\(([^\)]+)\)', r'[\1]', lyrics_text)
    
    # Validiere Bandnamen
    lyrics_text = validate_band_names(lyrics_text)
    
    # Liste von typischen Anweisungen/Effekten
    instructions = [
        # Gesang und Stimme
        'singen', 'sprechen', 'flüstern', 'schreien', 'weinen', 'lachen',
        'atmen', 'seufzen', 'stöhnen', 'jubeln', 'jammern', 'klagen',
        'schreien', 'brüllen', 'heulen', 'schluchzen', 'giggeln', 'kichern',
        'grunzen', 'knurren', 'zischen', 'pfeifen', 'summen', 'brummen',
        'murmeln', 'raunen', 'tuscheln', 'flüstern', 'schreien', 'brüllen',
        'heulen', 'schluchzen', 'giggeln', 'kichern', 'grunzen', 'knurren',
        'zischen', 'pfeifen', 'summen', 'brummen', 'murmeln', 'raunen',
        'tuscheln', 'flüstern', 'schreien', 'brüllen', 'heulen', 'schluchzen',
        
        # Instrumente und Soli
        'gitarrensolo', 'pianosolo', 'saxophonsolo', 'trompetensolo',
        'schlagzeugsolo', 'basssolo', 'violinsolo', 'cellosolo',
        'flötensolo', 'klarinettensolo', 'trommelwirbel', 'trompetenfanfare',
        'gitarrenriff', 'bassriff', 'synthriff', 'keyboardriff',
        'drumfill', 'drumbreak', 'drumroll', 'drumbeat',
        
        # Soundeffekte
        'echo', 'reverb', 'delay', 'distortion', 'fuzz', 'wahwah',
        'phaser', 'flanger', 'chorus', 'tremolo', 'vibrato',
        'feedback', 'noise', 'static', 'crackle', 'pop',
        'scratch', 'vinyl', 'tape', 'lo-fi', 'hi-fi',
        
        # Rhythmus und Beat
        'beat', 'rhythm', 'groove', 'swing', 'shuffle',
        'waltz', 'march', 'samba', 'bossa', 'tango',
        'breakbeat', 'drumbeat', 'backbeat', 'offbeat',
        'syncopation', 'polyrhythm', 'cross-rhythm',
        
        # Dynamik und Tempo
        'crescendo', 'decrescendo', 'forte', 'piano',
        'fortissimo', 'pianissimo', 'accelerando', 'ritardando',
        'rubato', 'tempo', 'speed', 'slow', 'fast',
        
        # Stimmung und Atmosphäre
        'dramatic', 'mysterious', 'romantic', 'tragic',
        'happy', 'sad', 'angry', 'peaceful', 'tense',
        'relaxed', 'energetic', 'calm', 'chaotic',
        
        # Chor und Ensemble
        'chorus', 'choir', 'ensemble', 'harmony',
        'unison', 'counterpoint', 'polyphony', 'homophony',
        'call-and-response', 'round', 'canon', 'fugue',
        
        # Technische Anweisungen
        'fade-in', 'fade-out', 'crossfade', 'mix',
        'overdub', 'layering', 'panning', 'stereo',
        'mono', 'surround', 'spatial', 'ambient',
        
        # Genre-spezifische Elemente
        'breakdown', 'drop', 'build-up', 'drop-out',
        'bridge', 'outro', 'intro', 'verse', 'chorus',
        'hook', 'riff', 'lick', 'fill', 'break',
        
        # Emotionale und expressive Elemente
        'passionate', 'intense', 'gentle', 'powerful',
        'delicate', 'rough', 'smooth', 'harsh', 'soft',
        'loud', 'quiet', 'whisper', 'shout', 'cry',
        
        # Spezielle Effekte
        'reverb', 'delay', 'echo', 'distortion',
        'fuzz', 'wah-wah', 'phaser', 'flanger',
        'chorus', 'tremolo', 'vibrato', 'feedback',
        'noise', 'static', 'crackle', 'pop',
        
        # Akustische Elemente
        'acoustic', 'electric', 'electronic', 'digital',
        'analog', 'synthetic', 'organic', 'natural',
        'artificial', 'mechanical', 'industrial',
        
        # Performance-Anweisungen
        'live', 'studio', 'concert', 'recording',
        'rehearsal', 'soundcheck', 'soundcheck',
        'monitoring', 'mixing', 'mastering',
        
        # Spezielle Techniken
        'looping', 'sampling', 'sequencing', 'programming',
        'arranging', 'orchestrating', 'composing', 'improvising',
        'jamming', 'soloing', 'accompanying', 'backing'
    ]
    
    # Ersetze alle Anweisungen, die nicht in eckigen Klammern stehen
    for instruction in instructions:
        pattern = r'(?<![\[\w])' + re.escape(instruction) + r'(?![\]\w])'
        lyrics_text = re.sub(pattern, f'[{instruction}]', lyrics_text, flags=re.IGNORECASE)
    
    return lyrics_text

def validate_band_names(text: str) -> str:
    """
    Validiert und korrigiert Bandnamen in Texten:
    - Ersetzt Bandnamen durch [inspiration]
    - Erlaubt die Nennung von Bandmitgliedern
    """
    # Ersetze "the" gefolgt von einem oder mehreren Wörtern durch [inspiration]
    text = re.sub(r'\bthe\s+[a-zA-Z\s&]+(?:s)?\b', '[inspiration]', text, flags=re.IGNORECASE)
    
    # Ersetze einzelne oder mehrere Wörter, die auf "band", "group" oder ähnliches enden
    text = re.sub(r'\b[a-zA-Z\s&]+(?:band|group|collective|ensemble)\b', '[inspiration]', text, flags=re.IGNORECASE)
    
    # Ersetze bekannte Bandnamen-Muster (z.B. "Band A & Band B")
    text = re.sub(r'\b[a-zA-Z\s&]+(?:and|&)\s+[a-zA-Z\s&]+\b', '[inspiration]', text, flags=re.IGNORECASE)
    
    return text

def main():
    """Hauptfunktion zum Starten der Anwendung."""
    app = SunoPromptGenerator()
    app.mainloop()

if __name__ == "__main__":
    main()