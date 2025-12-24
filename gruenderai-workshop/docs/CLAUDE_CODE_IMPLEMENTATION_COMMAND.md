# CLAUDE CODE IMPLEMENTIERUNGSBEFEHL: WORKSHOP BRANCHING & TEXT-FIX

## 🎯 ÜBERBLICK

Implementiere geschäftstyp-spezifisches Branching und fixe die Text-Generierung für den GründerAI Workshop basierend auf dem Referenzdokument: `/home/claude/WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md`

---

## 📋 KONTEXT & PROBLEM

### Aktuelle Situation:
1. **Alle User bekommen gleiche Fragen** → Irrelevante Fragen (z.B. "Räumlichkeiten" bei Online-Business)
2. **Text-Generierung ist kaputt** → Zeigt rechtliche Paragrafen statt Geschäftsmodell
3. **Keine Typ-Spezifität** → System weiß nicht welche Fragen für welchen Geschäftstyp relevant sind

### Ziel nach Implementierung:
1. ✅ User wird nach Geschäftstyp klassifiziert (Frage 1-2)
2. ✅ Nur relevante Fragen werden gestellt
3. ✅ Text-Generierung produziert konkreten, typ-spezifischen Businessplan-Text
4. ✅ Ausgeschlossene Fragen werden übersprungen

---

## 📚 REFERENZDOKUMENT

**WICHTIG:** Lies ZUERST das komplette Referenzdokument:
```bash
/home/claude/WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md
```

Dieses Dokument enthält:
- Alle 8 Geschäftstypen mit Definitionen
- Pflichtfelder pro Typ
- Ausgeschlossene Fragen pro Typ
- Typ-spezifische Fragenabfolgen
- Text-Generierungs-Templates
- System-Prompt-Templates

**Alle Implementierungen müssen diesem Dokument folgen!**

---

---

## 🏗️ AUFGABE 1: GESCHÄFTSTYP-KLASSIFIKATOR

### 1.1 Erstelle Business Type Classifier Service

**Datei:** `/backend/app/workshop/services/business_type_classifier.py`

```python
"""
Business Type Classifier Service

Klassifiziert User-Geschäft in einen von 8 Typen und gibt 
passende Konfiguration zurück.
"""

from enum import Enum
from typing import Dict, List
import json

class BusinessCategory(Enum):
    """Haupt-Geschäftskategorien"""
    GASTRONOMIE = "gastronomie"
    DIENSTLEISTUNG_LOKAL = "dienstleistung_lokal"
    DIENSTLEISTUNG_MOBIL = "dienstleistung_mobil"
    DIENSTLEISTUNG_ONLINE = "dienstleistung_online"
    HANDEL_STATIONAER = "handel_stationaer"
    HANDEL_ONLINE = "handel_online"
    PRODUKTION = "produktion"
    HYBRID = "hybrid"

class BusinessTypeClassifier:
    """
    Klassifiziert Geschäftstyp und gibt passende Konfiguration zurück
    """
    
    def __init__(self):
        # Lade Konfigurationen aus Referenzdokument
        self.type_configs = self._load_type_configurations()
    
    def _load_type_configurations(self) -> Dict:
        """
        Lädt Typ-Konfigurationen aus dem Referenzdokument
        
        In Produktion: Parse WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md
        Für jetzt: Hardcode basierend auf Dokument
        """
        
        return {
            BusinessCategory.GASTRONOMIE: {
                "label": "☕ Gastronomie",
                "beschreibung": "Café, Restaurant, Bar, Imbiss, Food Truck, Catering",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "gastro_subtyp",
                    "standort_konkret",
                    "groesse_qm",
                    "sitzplaetze_innen",
                    "oeffnungszeiten",
                    "produktpalette",
                    "zielgruppe_primaer",
                    "usp",
                    "preismodell_typ",
                    "preis_hauptprodukt"
                ],
                "excluded_questions": [
                    "einsatzradius_km",
                    "mobile_ausstattung",
                    "fahrzeug_typ",
                    "delivery_methode",
                    "tools_geplant",
                    "shop_plattform",
                    "versandlogistik",
                    "zielmarkt_international"
                ],
                "question_blocks": [
                    "geschaeftsidee",
                    "raeumlichkeiten",
                    "betriebszeiten",
                    "angebot",
                    "zielgruppen",
                    "usp",
                    "preismodell"
                ]
            },
            
            BusinessCategory.DIENSTLEISTUNG_ONLINE: {
                "label": "💻 Online-Dienstleistung",
                "beschreibung": "Beratung, Coaching, SaaS, Online-Kurse",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "dienstleistungstyp",
                    "spezialisierung",
                    "zielmarkt",
                    "beratungsformat",
                    "delivery_methode",
                    "session_dauer",
                    "plattform_typ",
                    "tools_geplant",
                    "max_kunden_pro_monat",
                    "zielgruppe_primaer",
                    "usp",
                    "preismodell_typ",
                    "preis_hauptprodukt"
                ],
                "excluded_questions": [
                    "groesse_qm",
                    "sitzplaetze",
                    "oeffnungszeiten",
                    "standort_konkret",
                    "raumaufteilung",
                    "gastgewerbe_erlaubnis",
                    "warenlager",
                    "durchgangsverkehr"
                ],
                "question_blocks": [
                    "geschaeftsidee",
                    "delivery_methode",
                    "plattform_tools",
                    "kapazitaet_skalierung",
                    "zielgruppen",
                    "usp",
                    "preismodell"
                ]
            },
            
            BusinessCategory.DIENSTLEISTUNG_MOBIL: {
                "label": "🚗 Mobiler Service",
                "beschreibung": "Handwerker, Mobile Massage, Haushaltsservice",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "service_typ",
                    "einsatzgebiet_stadt",
                    "einsatzradius_km",
                    "mobilität_typ",
                    "fahrzeug_status",
                    "mobile_ausstattung",
                    "durchschnittliche_einsatzzeit",
                    "einsaetze_pro_tag_realistisch",
                    "anfahrtskosten_modell",
                    "zielgruppe_primaer",
                    "usp",
                    "preismodell_typ",
                    "preis_hauptprodukt"
                ],
                "excluded_questions": [
                    "groesse_qm",
                    "sitzplaetze",
                    "oeffnungszeiten",
                    "raumaufteilung",
                    "gastgewerbe_erlaubnis",
                    "speisekarte_umfang",
                    "delivery_methode",
                    "tools_geplant",
                    "shop_plattform"
                ],
                "question_blocks": [
                    "geschaeftsidee",
                    "einsatzgebiet",
                    "mobilitaet",
                    "ausstattung_lager",
                    "einsatzplanung",
                    "zielgruppen",
                    "usp",
                    "preismodell"
                ]
            },
            
            BusinessCategory.HANDEL_STATIONAER: {
                "label": "🏪 Laden/Geschäft",
                "beschreibung": "Boutique, Einzelhandel, Spezialgeschäft",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "laden_typ",
                    "sortiment",
                    "standort_konkret",
                    "groesse_qm",
                    "verkaufsflaeche_vs_lager",
                    "oeffnungszeiten",
                    "zielgruppe_primaer",
                    "usp",
                    "preismodell_typ",
                    "durchschnittlicher_bon"
                ],
                "excluded_questions": [
                    "einsatzradius_km",
                    "delivery_methode",
                    "tools_geplant",
                    "mobile_ausstattung",
                    "session_dauer"
                ],
                "question_blocks": [
                    "geschaeftsidee",
                    "standort_raeumlichkeiten",
                    "sortiment",
                    "betriebszeiten",
                    "zielgruppen",
                    "usp",
                    "preismodell"
                ]
            },
            
            BusinessCategory.HANDEL_ONLINE: {
                "label": "📦 Online-Shop",
                "beschreibung": "E-Commerce, Dropshipping, Amazon FBA",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "ecommerce_modell",
                    "produktkatalog",
                    "shop_plattform",
                    "versandlogistik",
                    "lagerbestand",
                    "zielmarkt",
                    "zielgruppe_primaer",
                    "usp",
                    "preismodell_typ",
                    "durchschnittlicher_warenkorb"
                ],
                "excluded_questions": [
                    "groesse_qm",
                    "sitzplaetze",
                    "oeffnungszeiten",
                    "standort_konkret",
                    "raumaufteilung",
                    "einsatzradius_km"
                ],
                "question_blocks": [
                    "geschaeftsidee",
                    "ecommerce_modell",
                    "produktkatalog",
                    "plattform_logistik",
                    "zielgruppen",
                    "usp",
                    "preismodell"
                ]
            },
            
            BusinessCategory.PRODUKTION: {
                "label": "🏭 Produktion/Manufaktur",
                "beschreibung": "Werkstatt, Manufaktur, Handwerk",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "produkt_typ",
                    "produktionsweise",
                    "produktionsraeume_groesse",
                    "maschinen_ausstattung",
                    "produktionskapazitaet",
                    "vertriebsweg",
                    "zielgruppe_primaer",
                    "usp",
                    "preismodell_typ"
                ],
                "excluded_questions": [
                    "sitzplaetze",
                    "delivery_methode",
                    "tools_geplant",
                    "session_dauer"
                ],
                "question_blocks": [
                    "geschaeftsidee",
                    "produktion",
                    "vertrieb",
                    "zielgruppen",
                    "usp",
                    "preismodell"
                ]
            },
            
            BusinessCategory.DIENSTLEISTUNG_LOKAL: {
                "label": "💼 Dienstleistung vor Ort",
                "beschreibung": "Friseur, Studio, Werkstatt, Praxis",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "dienstleistungstyp",
                    "standort_konkret",
                    "groesse_qm",
                    "anzahl_arbeitsplaetze",
                    "ausstattung",
                    "durchschnittliche_behandlungszeit",
                    "oeffnungszeiten",
                    "zielgruppe_primaer",
                    "usp",
                    "preismodell_typ"
                ],
                "excluded_questions": [
                    "einsatzradius_km",
                    "fahrzeug_typ",
                    "delivery_methode",
                    "skalierung_automatisierung"
                ],
                "question_blocks": [
                    "geschaeftsidee",
                    "standort_raeumlichkeiten",
                    "betrieb",
                    "zielgruppen",
                    "usp",
                    "preismodell"
                ]
            },
            
            BusinessCategory.HYBRID: {
                "label": "🔄 Hybrid",
                "beschreibung": "Kombination aus Online + Offline",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "hybrid_kombination",
                    "hauptfokus",
                    "sekundaerfokus"
                    # Rest wird dynamisch basierend auf Kombination geladen
                ],
                "excluded_questions": [],  # Wird dynamisch bestimmt
                "question_blocks": [
                    "geschaeftsidee",
                    "hybrid_struktur",
                    # Rest dynamisch
                ]
            }
        }
    
    def get_classification_question(self) -> Dict:
        """
        Gibt die erste Klassifikationsfrage zurück
        """
        return {
            "question_id": "business_category_classification",
            "text": """Willkommen beim GründerAI Businessplan-Workshop!

Bevor wir loslegen: Welche Art von Geschäft planst du?

(Das hilft mir, dir die richtigen Fragen zu stellen)""",
            "typ": "single_choice",
            "optionen": [
                {
                    "value": "gastronomie",
                    "label": "☕ Gastronomie (Café, Restaurant, Bar, Imbiss)"
                },
                {
                    "value": "dienstleistung_lokal",
                    "label": "💼 Dienstleistung vor Ort (Friseur, Studio, Werkstatt)"
                },
                {
                    "value": "dienstleistung_mobil",
                    "label": "🚗 Mobiler Service (Handwerker, Pflege, Mobile Massage)"
                },
                {
                    "value": "dienstleistung_online",
                    "label": "💻 Online-Dienstleistung (Beratung, SaaS, Coaching)"
                },
                {
                    "value": "handel_stationaer",
                    "label": "🏪 Laden/Geschäft (Boutique, Einzelhandel)"
                },
                {
                    "value": "handel_online",
                    "label": "📦 Online-Shop (E-Commerce, Dropshipping)"
                },
                {
                    "value": "produktion",
                    "label": "🏭 Produktion/Manufaktur (Werkstatt, Handwerk)"
                },
                {
                    "value": "hybrid",
                    "label": "🔄 Hybrid (Mehrere Bereiche kombiniert)"
                }
            ],
            "required": True
        }
    
    def classify(self, business_category: str) -> Dict:
        """
        Klassifiziert basierend auf User-Auswahl und gibt Konfiguration zurück
        
        Args:
            business_category: String wie "gastronomie", "dienstleistung_online", etc.
        
        Returns:
            Dict mit:
            - category: BusinessCategory Enum
            - label: Anzeige-Name
            - beschreibung: Beschreibung
            - required_fields: Liste von Pflichtfeldern
            - excluded_questions: Liste von ausgeschlossenen Fragen
            - question_blocks: Reihenfolge der Fragenblöcke
        """
        try:
            category = BusinessCategory(business_category)
        except ValueError:
            raise ValueError(f"Unbekannte Business Category: {business_category}")
        
        config = self.type_configs[category]
        
        return {
            "category": category,
            "category_value": category.value,
            "label": config["label"],
            "beschreibung": config["beschreibung"],
            "required_fields": config["required_fields"],
            "excluded_questions": config["excluded_questions"],
            "question_blocks": config["question_blocks"]
        }
    
    def is_question_excluded(self, question_id: str, business_category: str) -> bool:
        """
        Prüft ob eine Frage für den gegebenen Geschäftstyp ausgeschlossen ist
        """
        try:
            category = BusinessCategory(business_category)
        except ValueError:
            return False
        
        excluded = self.type_configs[category]["excluded_questions"]
        return question_id in excluded
```

**Testing:**
```python
# /backend/app/workshop/tests/test_business_type_classifier.py

def test_gastronomie_classification():
    classifier = BusinessTypeClassifier()
    result = classifier.classify("gastronomie")
    
    assert result["category"] == BusinessCategory.GASTRONOMIE
    assert "groesse_qm" in result["required_fields"]
    assert "einsatzradius_km" in result["excluded_questions"]

def test_online_dienstleistung_classification():
    classifier = BusinessTypeClassifier()
    result = classifier.classify("dienstleistung_online")
    
    assert "tools_geplant" in result["required_fields"]
    assert "groesse_qm" in result["excluded_questions"]

def test_question_exclusion():
    classifier = BusinessTypeClassifier()
    
    # Gastronomie: groesse_qm ist relevant
    assert not classifier.is_question_excluded("groesse_qm", "gastronomie")
    
    # Online: groesse_qm ist irrelevant
    assert classifier.is_question_excluded("groesse_qm", "dienstleistung_online")
```

---

---

## 🏗️ AUFGABE 2: DYNAMISCHER FRAGEN-GENERATOR

### 2.1 Erstelle Dynamic Question Generator

**Datei:** `/backend/app/workshop/services/dynamic_question_generator.py`

```python
"""
Dynamic Question Generator

Generiert typ-spezifische Fragen basierend auf Geschäftskategorie
"""

from typing import Dict, Optional
from .business_type_classifier import BusinessTypeClassifier, BusinessCategory

class DynamicQuestionGenerator:
    """
    Generiert die nächste relevante Frage basierend auf:
    - Geschäftstyp
    - Bereits erfassten Feldern
    - Ausgeschlossenen Fragen
    """
    
    def __init__(self, classifier: BusinessTypeClassifier):
        self.classifier = classifier
        self.question_templates = self._load_question_templates()
    
    def _load_question_templates(self) -> Dict:
        """
        Lädt Fragen-Templates aus Referenzdokument
        
        Format:
        {
            "question_id": {
                "gastronomie": {
                    "text": "Typ-spezifische Frage...",
                    "typ": "single_choice",
                    "optionen": [...]
                },
                "dienstleistung_online": {
                    "text": "Andere Formulierung...",
                    ...
                },
                "default": {
                    "text": "Generische Frage...",
                    ...
                }
            }
        }
        """
        
        return {
            "standort_konkret": {
                "gastronomie": {
                    "text": "Wo genau planst du dein {gastro_subtyp}? (Straße, Kiez)",
                    "typ": "open_text",
                    "hint": "Für Gastronomie ist die Lage KRITISCH! Bitte so konkret wie möglich."
                },
                "handel_stationaer": {
                    "text": "Wo soll dein Laden sein? (Einkaufsstraße, Mall)",
                    "typ": "open_text",
                    "hint": "Laufkundschaft ist entscheidend!"
                },
                "dienstleistung_lokal": {
                    "text": "Wo planst du dein Studio/deine Praxis?",
                    "typ": "open_text",
                    "hint": "Erreichbarkeit und Parkplätze sind wichtig"
                },
                # Für Online: Diese Frage wird übersprungen!
            },
            
            "groesse_qm": {
                "gastronomie": {
                    "text": "Wie groß sollten deine Räume sein?",
                    "typ": "single_choice_with_custom",
                    "optionen": [
                        {"value": "40-60", "label": "40-60 qm (klein & gemütlich, ~15 Plätze)"},
                        {"value": "70-100", "label": "70-100 qm (mittel, ~30 Plätze)"},
                        {"value": "100+", "label": "100+ qm (groß, 40+ Plätze)"}
                    ]
                },
                "produktion": {
                    "text": "Wie groß muss deine Werkstatt/Produktion sein?",
                    "typ": "single_choice_with_custom",
                    "optionen": [
                        {"value": "50-100", "label": "50-100 qm (kleine Werkstatt)"},
                        {"value": "100-250", "label": "100-250 qm (mittlere Produktion)"},
                        {"value": "250+", "label": "250+ qm (Fabrikhalle)"}
                    ]
                },
                # Für Online/Mobil: Wird übersprungen
            },
            
            "delivery_methode": {
                "dienstleistung_online": {
                    "text": "Wie lieferst du deine Dienstleistung?",
                    "typ": "multiple_choice",
                    "optionen": [
                        {"value": "video_live", "label": "Live Video-Calls (Zoom, Teams)"},
                        {"value": "async", "label": "Asynchron (Email, Voice Notes)"},
                        {"value": "hybrid", "label": "Beides möglich"}
                    ]
                }
                # NUR für Online-Dienstleistung!
            },
            
            "einsatzradius_km": {
                "dienstleistung_mobil": {
                    "text": "Wie weit fährst du maximal?",
                    "typ": "single_choice_with_custom",
                    "optionen": [
                        {"value": "5", "label": "5 km (sehr lokal, Kiez)"},
                        {"value": "10", "label": "10 km (Stadtbezirk)"},
                        {"value": "20", "label": "20 km (ganze Stadt)"},
                        {"value": "50", "label": "50 km (Stadt + Umland)"}
                    ],
                    "hint": "Bedenke: Fahrtzeit = weniger Einsätze pro Tag"
                }
                # NUR für Mobile Services!
            },
            
            # ... weitere Fragen aus Referenzdokument
        }
    
    def get_next_question(
        self,
        business_category: str,
        collected_fields: Dict,
        current_block: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Gibt nächste relevante Frage zurück
        
        Args:
            business_category: z.B. "gastronomie"
            collected_fields: Dict der bereits erfassten Felder
            current_block: Aktueller Fragenblock (optional)
        
        Returns:
            Dict mit Frage oder None wenn Sektion komplett
        """
        
        # Hole Typ-Konfiguration
        config = self.classifier.classify(business_category)
        required_fields = config["required_fields"]
        excluded_questions = config["excluded_questions"]
        
        # Finde nächstes fehlendes Pflichtfeld
        for field_id in required_fields:
            
            # Skip wenn bereits erfasst
            if field_id in collected_fields:
                continue
            
            # Skip wenn excluded (sollte nicht passieren, aber Sicherheit)
            if field_id in excluded_questions:
                continue
            
            # Hole typ-spezifisches Template
            question_template = self._get_question_template(
                field_id,
                business_category
            )
            
            if question_template:
                return {
                    "question_id": field_id,
                    "business_category": business_category,
                    **question_template
                }
        
        # Alle Pflichtfelder erfasst
        return None
    
    def _get_question_template(
        self,
        question_id: str,
        business_category: str
    ) -> Optional[Dict]:
        """
        Holt typ-spezifisches Fragen-Template
        """
        
        if question_id not in self.question_templates:
            # Fallback: Generisches Template
            return self._get_generic_template(question_id)
        
        variants = self.question_templates[question_id]
        
        # Typ-spezifische Variante vorhanden?
        if business_category in variants:
            return variants[business_category]
        
        # Fallback auf default
        if "default" in variants:
            return variants["default"]
        
        return None
    
    def _get_generic_template(self, question_id: str) -> Dict:
        """
        Generiert generisches Template wenn keine typ-spezifische Version existiert
        """
        
        # Konvertiere field_id zu lesbarem Text
        readable_label = question_id.replace("_", " ").title()
        
        return {
            "text": f"{readable_label}:",
            "typ": "open_text",
            "hint": ""
        }
    
    def format_question_for_prompt(self, question: Dict) -> str:
        """
        Formatiert Frage für System Prompt
        """
        
        formatted = f"{question['text']}\n"
        
        if question.get("hint"):
            formatted += f"\nℹ️ {question['hint']}\n"
        
        if question["typ"] == "single_choice":
            formatted += "\nOptionen:\n"
            for opt in question.get("optionen", []):
                formatted += f"- {opt['label']}\n"
        
        elif question["typ"] == "multiple_choice":
            formatted += "\n(Mehrfachauswahl möglich)\n"
            for opt in question.get("optionen", []):
                formatted += f"□ {opt['label']}\n"
        
        return formatted
```

**Testing:**
```python
# /backend/app/workshop/tests/test_dynamic_question_generator.py

def test_gastronomie_gets_raumgroesse_question():
    classifier = BusinessTypeClassifier()
    generator = DynamicQuestionGenerator(classifier)
    
    question = generator.get_next_question(
        business_category="gastronomie",
        collected_fields={"geschaeftsidee_kurz": "Café"}
    )
    
    # Sollte groesse_qm fragen (relevant für Gastronomie)
    assert question is not None
    # Prüfe ob groesse_qm irgendwann kommt

def test_online_skips_raumgroesse_question():
    classifier = BusinessTypeClassifier()
    generator = DynamicQuestionGenerator(classifier)
    
    question = generator.get_next_question(
        business_category="dienstleistung_online",
        collected_fields={"geschaeftsidee_kurz": "Coaching"}
    )
    
    # Sollte groesse_qm NICHT fragen (excluded!)
    # Stattdessen delivery_methode oder andere Online-spezifische Fragen
    assert question["question_id"] != "groesse_qm"
```

---

---

## 🏗️ AUFGABE 3: TEXT-GENERIERUNG FIXEN

### 3.1 Erstelle Section Text Generator (TYP-SPEZIFISCH!)

**Datei:** `/backend/app/workshop/services/section_text_generator.py`

```python
"""
Section Text Generator

Generiert BA GZ 04-konforme Businessplan-Abschnitte 
aus strukturierten Daten - TYP-SPEZIFISCH!
"""

from anthropic import Anthropic
from typing import Dict
import json

class SectionTextGenerator:
    """
    Generiert typ-spezifische Businessplan-Texte
    """
    
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-sonnet-4-20250514"
    
    async def generate_modul_1_text(
        self,
        business_category: str,
        extracted_data: Dict
    ) -> str:
        """
        Generiert Modul 1 Text basierend auf Geschäftstyp
        """
        
        # Wähle typ-spezifischen Generator
        if business_category == "gastronomie":
            return await self._generate_gastronomie_text(extracted_data)
        
        elif business_category == "dienstleistung_online":
            return await self._generate_online_dienstleistung_text(extracted_data)
        
        elif business_category == "dienstleistung_mobil":
            return await self._generate_mobiler_service_text(extracted_data)
        
        elif business_category == "handel_stationaer":
            return await self._generate_handel_stationaer_text(extracted_data)
        
        elif business_category == "handel_online":
            return await self._generate_handel_online_text(extracted_data)
        
        elif business_category == "produktion":
            return await self._generate_produktion_text(extracted_data)
        
        elif business_category == "dienstleistung_lokal":
            return await self._generate_dienstleistung_lokal_text(extracted_data)
        
        else:
            # Fallback: Generischer Generator
            return await self._generate_generic_text(extracted_data)
    
    async def _generate_gastronomie_text(self, data: Dict) -> str:
        """
        Generiert Businessplan-Text für GASTRONOMIE
        
        Nutzt Template aus Referenzdokument:
        WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md
        Sektion: "Text-Generierung Template: Gastronomie"
        """
        
        prompt = f"""Du bist ein professioneller Businessplan-Autor für deutsche Gründungszuschuss-Anträge (BA GZ 04).

**AUFGABE:**
Schreibe den Abschnitt "2. GESCHÄFTSMODELL" für ein GASTRONOMIE-Geschäft.

**WICHTIG - WAS DU SCHREIBEN SOLLST:**
- Konkrete Geschäftsbeschreibung mit Zahlen (qm, Plätze, Öffnungszeiten)
- Zielgruppen mit demografischen Details
- Alleinstellungsmerkmal klar herausgearbeitet
- Preismodell mit konkreten Preisen

**WICHTIG - WAS DU NICHT SCHREIBEN DARFST:**
- KEINE rechtlichen Paragrafen (§ 93 SGB III etc.)
- KEINE "40 Stunden hauptberuflich"-Texte
- KEINE Gründungszuschuss-Anforderungen
- NUR das konkrete Geschäftsmodell!

**EXTRAHIERTE DATEN:**
```json
{json.dumps(data, indent=2, ensure_ascii=False)}
```

**STRUKTUR:**
```markdown
## 2. GESCHÄFTSMODELL

### 2.1 Geschäftsidee und Konzept

{{geschaeftsidee_beschreibung}}

**Standort:**
{{standort_konkret}}

**Räumlichkeiten:**
{{groesse_beschreibung}}

**Raumaufteilung:**
{{raumaufteilung}}

### 2.2 Angebotsbeschreibung

**Produktpalette:**
{{produktpalette}}

**Speisekarte:**
{{speisekarte_umfang}}

### 2.3 Betriebskonzept

**Öffnungszeiten:**
{{oeffnungszeiten}}

### 2.4 Zielgruppen

**Primäre Zielgruppe:**
{{zielgruppe_primaer_detailliert}}

### 2.5 Alleinstellungsmerkmale

**Marktlücke:**
{{marktluecke}}

**USP:**
{{usp}}

### 2.6 Preismodell

{{preismodell_beschreibung}}

**Preise:**
{{preisliste}}
```

**WICHTIG:**
- Nutze ALLE konkreten Zahlen aus den Daten!
- Keine Platzhalter wie [TBD] oder [Name]!
- Nur Fakten aus extracted_data verwenden!
- Länge: 600-900 Wörter

Schreibe jetzt den fertigen Businessplan-Abschnitt:
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_online_dienstleistung_text(self, data: Dict) -> str:
        """
        Generiert Businessplan-Text für ONLINE-DIENSTLEISTUNG
        """
        
        prompt = f"""Du bist ein professioneller Businessplan-Autor für deutsche Gründungszuschuss-Anträge (BA GZ 04).

**AUFGABE:**
Schreibe den Abschnitt "2. GESCHÄFTSMODELL" für eine ONLINE-DIENSTLEISTUNG.

**WICHTIG - FOKUS FÜR ONLINE-BUSINESS:**
- WIE wird die Dienstleistung geliefert? (Video/Async/Hybrid)
- Welche Technologie/Tools werden genutzt?
- Wie skaliert das Geschäft? (Kapazität, Automatisierung)
- NICHT: Räumlichkeiten, Öffnungszeiten (irrelevant!)

**WICHTIG - WAS DU NICHT SCHREIBEN DARFST:**
- KEINE rechtlichen Paragrafen
- KEINE Räumlichkeiten-Beschreibungen
- KEINE Öffnungszeiten
- NUR das konkrete Online-Geschäftsmodell!

**EXTRAHIERTE DATEN:**
```json
{json.dumps(data, indent=2, ensure_ascii=False)}
```

**STRUKTUR:**
```markdown
## 2. GESCHÄFTSMODELL

### 2.1 Geschäftsidee und Dienstleistung

{{geschaeftsidee}}

**Zielmarkt:**
{{zielmarkt}}

### 2.2 Service-Delivery und Format

**Beratungsformat:**
{{beratungsformat}}

**Delivery-Methode:**
{{delivery_methode}}

**Session-Struktur:**
{{session_details}}

**Technische Infrastruktur:**
{{tools_liste}}

### 2.3 Zielgruppe

{{zielgruppe_detailliert}}

### 2.4 Kapazität und Skalierbarkeit

{{kapazitaet_beschreibung}}

{{automatisierung_strategie}}

### 2.5 Alleinstellungsmerkmale

{{usp}}

### 2.6 Preismodell

{{preismodell}}
```

Schreibe jetzt den fertigen Businessplan-Abschnitt:
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_mobiler_service_text(self, data: Dict) -> str:
        """
        Generiert Businessplan-Text für MOBILEN SERVICE
        """
        
        prompt = f"""Du bist ein professioneller Businessplan-Autor für deutsche Gründungszuschuss-Anträge (BA GZ 04).

**AUFGABE:**
Schreibe den Abschnitt "2. GESCHÄFTSMODELL" für einen MOBILEN SERVICE.

**WICHTIG - FOKUS FÜR MOBILE SERVICES:**
- EINSATZGEBIET (wo aktiv?)
- MOBILITÄT (wie unterwegs?)
- EINSATZPLANUNG (wie viele Kunden pro Tag?)
- ANFAHRTSKOSTEN (wie berechnet?)
- NICHT: Feste Räumlichkeiten, Öffnungszeiten

**EXTRAHIERTE DATEN:**
```json
{json.dumps(data, indent=2, ensure_ascii=False)}
```

**STRUKTUR:**
```markdown
## 2. GESCHÄFTSMODELL

### 2.1 Geschäftsidee und Service

{{geschaeftsidee}}

### 2.2 Einsatzgebiet und Mobilität

**Einsatzgebiet:**
{{einsatzgebiet}}

**Mobilität:**
{{mobilität}}

**Fahrzeugausstattung:**
{{fahrzeug_ausstattung}}

### 2.3 Mobile Ausstattung

{{mobile_ausstattung_liste}}

### 2.4 Einsatzplanung und Kapazität

{{einsatzplanung}}

**Anfahrtskosten:**
{{anfahrtskosten_modell}}

### 2.5 Zielgruppe

{{zielgruppe}}

### 2.6 Alleinstellungsmerkmale

{{usp}}

### 2.7 Preismodell

{{preismodell}}
```

Schreibe jetzt den fertigen Businessplan-Abschnitt:
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    # ... weitere typ-spezifische Generatoren für andere Geschäftstypen
```

**Testing:**
```python
# /backend/app/workshop/tests/test_section_text_generator.py

async def test_gastronomie_text_no_legal_paragraphs():
    generator = SectionTextGenerator()
    
    data = {
        "geschaeftsidee_kurz": "Kiez-Café mit Co-Working",
        "standort_konkret": "Schillerkiez, Berlin-Neukölln",
        "groesse_qm": "70-100",
        # ... weitere Felder
    }
    
    text = await generator.generate_modul_1_text("gastronomie", data)
    
    # KRITISCH: Keine Rechtstexte!
    assert "§ 93 SGB III" not in text
    assert "40 Stunden hauptberuflich" not in text
    assert "Gründungszuschuss" not in text
    
    # MUSS enthalten: Konkrete Geschäftsdaten
    assert "Schillerkiez" in text
    assert "70-100" in text or "qm" in text

async def test_online_text_no_raeumlichkeiten():
    generator = SectionTextGenerator()
    
    data = {
        "geschaeftsidee_kurz": "Business-Coaching",
        "delivery_methode": "video_live",
        # ... weitere Online-spezifische Felder
    }
    
    text = await generator.generate_modul_1_text("dienstleistung_online", data)
    
    # KRITISCH: Keine Räumlichkeiten-Infos!
    assert "qm" not in text
    assert "Öffnungszeiten" not in text
    
    # MUSS enthalten: Online-spezifische Infos
    assert "Video" in text or "Zoom" in text or "Online" in text
```

---

---

## 🏗️ AUFGABE 4: CONVERSATION SERVICE ANPASSEN

### 4.1 Update Conversation Service mit Branching

**Datei:** `/backend/app/workshop/services/conversation_service.py`

```python
"""
Conversation Service mit Geschäftstyp-Branching
"""

from .business_type_classifier import BusinessTypeClassifier
from .dynamic_question_generator import DynamicQuestionGenerator
from .section_text_generator import SectionTextGenerator

class ConversationService:
    
    def __init__(self):
        self.classifier = BusinessTypeClassifier()
        self.question_generator = DynamicQuestionGenerator(self.classifier)
        self.text_generator = SectionTextGenerator()
    
    async def send_message(self, session_id: str, user_message: str, db):
        """
        Hauptlogik mit Branching
        """
        
        session = db.query(WorkshopSession).filter_by(id=session_id).first()
        
        # --- SCHRITT 1: KLASSIFIKATION (nur beim ersten Mal) ---
        if not session.business_category:
            
            # Allererste Nachricht: Klassifikationsfrage stellen
            if session.message_count == 0:
                classification_question = self.classifier.get_classification_question()
                
                return {
                    "assistant_message": self._format_classification_question(
                        classification_question
                    ),
                    "requires_classification": True
                }
            
            # Zweite Nachricht: Klassifiziere basierend auf Antwort
            try:
                classification_result = self.classifier.classify(user_message)
                
                # Speichere Klassifikation
                session.business_category = classification_result["category_value"]
                session.required_fields = classification_result["required_fields"]
                session.excluded_questions = classification_result["excluded_questions"]
                db.commit()
                
                return {
                    "assistant_message": f"""Perfekt! Du planst: {classification_result['label']}

{classification_result['beschreibung']}

Lass uns jetzt die Details deines Geschäfts erfassen!

Beschreibe deine Geschäftsidee in 1-2 Sätzen:
(So einfach, dass es jeder versteht)""",
                    "business_category": classification_result["category_value"]
                }
            
            except ValueError:
                return {
                    "assistant_message": "Hmm, das habe ich nicht verstanden. Bitte wähle eine der Optionen aus der Liste.",
                    "error": "invalid_classification"
                }
        
        # --- SCHRITT 2: TYP-SPEZIFISCHE FRAGEN STELLEN ---
        
        # Extrahiere Daten aus User-Nachricht
        extracted_data = await self._extract_data_from_message(
            user_message,
            session.current_question_id,
            session.business_category
        )
        
        # Speichere extrahierte Daten
        session.collected_fields.update(extracted_data)
        db.commit()
        
        # Hole nächste Frage (typ-spezifisch!)
        next_question = self.question_generator.get_next_question(
            business_category=session.business_category,
            collected_fields=session.collected_fields
        )
        
        # --- SCHRITT 3: PRÜFE OB SEKTION KOMPLETT ---
        if next_question is None:
            # Alle Pflichtfelder erfasst → Text generieren!
            return await self._complete_section(session, db)
        
        # --- SCHRITT 4: STELLE NÄCHSTE FRAGE ---
        session.current_question_id = next_question["question_id"]
        db.commit()
        
        formatted_question = self.question_generator.format_question_for_prompt(
            next_question
        )
        
        return {
            "assistant_message": formatted_question,
            "question_id": next_question["question_id"],
            "question_type": next_question["typ"]
        }
    
    async def _complete_section(self, session, db):
        """
        Sektion ist komplett → Generiere Text
        """
        
        # Generiere typ-spezifischen Text!
        generated_text = await self.text_generator.generate_modul_1_text(
            business_category=session.business_category,
            extracted_data=session.collected_fields
        )
        
        # Speichere
        section_completion = db.query(SectionCompletion).filter(
            SectionCompletion.session_id == session.id,
            SectionCompletion.section_id == "modul_1_geschaeftsmodell"
        ).first()
        
        section_completion.generated_text = generated_text
        section_completion.section_completed = True
        db.commit()
        
        # Zeige User den generierten Text
        return {
            "assistant_message": f"""🎉 SEKTION 1: GESCHÄFTSMODELL - ABGESCHLOSSEN!

Großartig! Hier ist dein formulierter Businessplan-Abschnitt:

---

{generated_text}

---

Bist du zufrieden mit diesem Abschnitt?
- ✅ **"Ja"** oder **"Weiter"** → Nächste Sektion
- ✏️ **"Änderungen"** → Was möchtest du anpassen?
""",
            "section_completed": True,
            "generated_text": generated_text
        }
    
    def _format_classification_question(self, question: Dict) -> str:
        """
        Formatiert Klassifikationsfrage für User
        """
        
        formatted = f"{question['text']}\n\n"
        
        for opt in question["optionen"]:
            formatted += f"{opt['label']}\n"
        
        return formatted
    
    async def _extract_data_from_message(
        self,
        user_message: str,
        question_id: str,
        business_category: str
    ) -> Dict:
        """
        Extrahiert strukturierte Daten aus User-Nachricht
        
        Nutzt Claude für Extraktion
        """
        
        # TODO: Implement mit Claude
        # Für jetzt: Simple Extraktion
        
        return {
            question_id: user_message
        }
```

---

---

## 🏗️ AUFGABE 5: SYSTEM PROMPT MIT BRANCHING

### 5.1 Update System Prompt Generator

**Datei:** `/backend/app/workshop/prompts/system_prompt_builder.py`

```python
"""
System Prompt Builder mit Geschäftstyp-Awareness
"""

def build_modul_1_system_prompt(
    business_category: str,
    required_fields: list,
    collected_fields: dict,
    excluded_questions: list
) -> str:
    """
    Baut typ-spezifischen System Prompt für Modul 1
    """
    
    # Berechne Progress
    progress = int((len(collected_fields) / len(required_fields)) * 100)
    
    # Formatiere Listen
    collected_list = "\n".join([f"✅ {k}: {v[:50]}..." for k, v in collected_fields.items()])
    missing_list = "\n".join([f"❌ {f}" for f in required_fields if f not in collected_fields])
    excluded_list = "\n".join([f"⛔ {q}" for q in excluded_questions])
    
    # Typ-spezifische Hinweise
    type_specific_notes = get_type_specific_notes(business_category)
    
    prompt = f"""Du führst den Nutzer durch Modul 1: GESCHÄFTSMODELL.

**GESCHÄFTSTYP:** {business_category}

---

**MODUL-ZIEL:**
Erfasse WAS, FÜR WEN, WARUM, WIE (Preismodell-Grundidee)

**TYP-SPEZIFISCHE HINWEISE:**
{type_specific_notes}

**KRITISCH - FRAGEN DIE DU NICHT STELLEN DARFST:**
{excluded_list}

**GRUND:** Diese Fragen sind für {business_category} NICHT relevant 
oder werden in späteren Modulen behandelt.

Wenn der User nach diesen Themen fragt, erkläre freundlich:
"Das besprechen wir später in Modul X" oder "Das ist für dein 
Geschäftsmodell nicht relevant, weil..."

---

**PFLICHTFELDER FÜR {business_category}:**
{len(required_fields)} Felder insgesamt

**AKTUELLER FORTSCHRITT: {progress}%**

**BEREITS ERFASST:**
{collected_list}

**NOCH FEHLEND:**
{missing_list}

---

**WENN >=90% DER PFLICHTFELDER ERFASST:**
1. STELLE KEINE WEITEREN FRAGEN
2. Erstelle Zusammenfassung aller erfassten Daten
3. Setze validation_status auf "complete"
4. System wird automatisch typ-spezifischen Text generieren

**STRUCTURED DATA FORMAT:**

Nach JEDER User-Antwort extrahiere strukturierte Daten:

<structured_data>
{{
  "section_id": "modul_1_geschaeftsmodell",
  "business_category": "{business_category}",
  "extracted_fields": {{
    "{next_field}": "... extrahierter Wert ..."
  }},
  "validation_status": "incomplete|complete",
  "progress_percent": {progress}
}}
</structured_data>

---

**WICHTIG:**
- Passe Fragen an den Geschäftstyp an!
- Nutze typ-spezifische Beispiele
- Überspringe automatisch excluded questions
- Halte Fragen konkret und praxisnah
"""
    
    return prompt

def get_type_specific_notes(business_category: str) -> str:
    """
    Gibt typ-spezifische Hinweise für System Prompt
    """
    
    notes = {
        "gastronomie": """
        - FOKUS: Räumlichkeiten, Standort, Öffnungszeiten
        - WICHTIG: qm, Sitzplätze, Angebot-Details
        - KRITISCH: Lage ist bei Gastro entscheidend!
        """,
        
        "dienstleistung_online": """
        - FOKUS: Delivery-Methode, Tools, Skalierbarkeit
        - WICHTIG: WIE wird Service geliefert?
        - NICHT FRAGEN: Räumlichkeiten, Öffnungszeiten
        """,
        
        "dienstleistung_mobil": """
        - FOKUS: Einsatzgebiet, Mobilität, Anfahrtskosten
        - WICHTIG: Wie weit fährst du? Was ist im Auto?
        - NICHT FRAGEN: Feste Räumlichkeiten
        """,
        
        # ... weitere Typen
    }
    
    return notes.get(business_category, "")
```

---

---

## 🧪 AUFGABE 6: TESTING

### 6.1 Integration Tests

```python
# /backend/app/workshop/tests/test_workshop_branching_integration.py

import pytest

@pytest.mark.asyncio
async def test_gastronomie_full_flow():
    """
    Test: Gastronomie-User durchläuft kompletten Flow
    """
    
    # 1. Start Workshop
    response = await conversation_service.send_message(
        session_id="test123",
        user_message="",  # Erste Nachricht
        db=db
    )
    
    assert "Welche Art von Geschäft" in response["assistant_message"]
    
    # 2. Wähle Gastronomie
    response = await conversation_service.send_message(
        session_id="test123",
        user_message="gastronomie",
        db=db
    )
    
    session = db.query(WorkshopSession).filter_by(id="test123").first()
    assert session.business_category == "gastronomie"
    
    # 3. Beantworte Fragen
    # ... mehrere Frage-Antwort-Runden
    
    # 4. Check: Keine excluded questions wurden gestellt
    all_questions_asked = [...]  # Liste aller gestellten Fragen
    assert "einsatzradius_km" not in all_questions_asked
    assert "delivery_methode" not in all_questions_asked
    
    # 5. Check: Relevante Fragen wurden gestellt
    assert "groesse_qm" in all_questions_asked
    assert "oeffnungszeiten" in all_questions_asked
    
    # 6. Check: Text wurde generiert
    assert session.section_completions[0].generated_text is not None
    
    # 7. Check: Text enthält keine Rechtsinfos
    generated_text = session.section_completions[0].generated_text
    assert "§ 93 SGB III" not in generated_text
    assert "40 Stunden" not in generated_text

@pytest.mark.asyncio
async def test_online_dienstleistung_skips_raeumlichkeiten():
    """
    Test: Online-Dienstleistung bekommt keine Räumlichkeiten-Fragen
    """
    
    # Setup
    session = create_test_session(business_category="dienstleistung_online")
    
    # Simuliere Fragen-Flow
    all_questions = []
    while True:
        next_question = question_generator.get_next_question(
            business_category="dienstleistung_online",
            collected_fields=session.collected_fields
        )
        
        if next_question is None:
            break
        
        all_questions.append(next_question["question_id"])
        
        # Simuliere Antwort
        session.collected_fields[next_question["question_id"]] = "test_value"
    
    # Assertions
    assert "groesse_qm" not in all_questions
    assert "sitzplaetze" not in all_questions
    assert "oeffnungszeiten" not in all_questions
    
    # Aber diese sollten gefragt worden sein:
    assert "delivery_methode" in all_questions
    assert "tools_geplant" in all_questions
```

---

---

## 📋 AUFGABE 7: DATABASE MIGRATIONS

### 7.1 Add business_category to workshop_sessions

```python
# /backend/app/workshop/migrations/add_business_category.py

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column(
        'workshop_sessions',
        sa.Column('business_category', sa.String(50), nullable=True)
    )
    
    op.add_column(
        'workshop_sessions',
        sa.Column('business_subtype', sa.String(50), nullable=True)
    )
    
    op.add_column(
        'workshop_sessions',
        sa.Column('required_fields', sa.JSON, nullable=True)
    )
    
    op.add_column(
        'workshop_sessions',
        sa.Column('excluded_questions', sa.JSON, nullable=True)
    )
    
    op.add_column(
        'workshop_sessions',
        sa.Column('current_question_id', sa.String(100), nullable=True)
    )

def downgrade():
    op.drop_column('workshop_sessions', 'business_category')
    op.drop_column('workshop_sessions', 'business_subtype')
    op.drop_column('workshop_sessions', 'required_fields')
    op.drop_column('workshop_sessions', 'excluded_questions')
    op.drop_column('workshop_sessions', 'current_question_id')
```

---

---

## 📦 ZUSAMMENFASSUNG: DEPLOYABLE CHECKLIST

Nach Implementierung müssen folgende Dinge funktionieren:

```bash
# 1. Backend Tests laufen durch
cd /backend
pytest app/workshop/tests/

# Erwartung:
✅ test_business_type_classifier.py - Alle Tests grün
✅ test_dynamic_question_generator.py - Alle Tests grün
✅ test_section_text_generator.py - Alle Tests grün
✅ test_workshop_branching_integration.py - Alle Tests grün

# 2. Database Migration
alembic upgrade head

# 3. Deploy to Railway
git add .
git commit -m "feat: Implement geschäftstyp-spezifisches Branching + Text-Generierung Fix"
git push origin main

# Railway deployed automatisch

# 4. Manuelle Tests
# Test Gastronomie-Flow:
- Start Workshop
- Wähle "☕ Gastronomie"
- Beantworte Fragen
- CHECK: "Wie groß sind deine Räume?" wird gefragt
- CHECK: "Wie weit fährst du?" wird NICHT gefragt
- CHECK: Am Ende wird konkreter Businessplan-Text angezeigt
- CHECK: Text enthält KEINE Rechtsinfos

# Test Online-Dienstleistung-Flow:
- Start Workshop
- Wähle "💻 Online-Dienstleistung"
- Beantworte Fragen
- CHECK: "Wie lieferst du die Dienstleistung?" wird gefragt
- CHECK: "Wie groß sind deine Räume?" wird NICHT gefragt
- CHECK: Am Ende wird Online-spezifischer Text angezeigt
```

---

---

## 🎯 ERWARTETE ERGEBNISSE

### Vor Implementierung:
```
User (Gastronomie): "Ich plane ein Café"
System: "Wie groß sind deine Räume?"
System: "Wie weit fährst du?" ❌ (irrelevant!)
System: "Welche Tools nutzt du?" ❌ (irrelevant!)

Nach Sektion 1:
Text: "Die geplante wöchentliche Arbeitszeit..." ❌ (Rechtsinfos!)
```

### Nach Implementierung:
```
User: Startet Workshop
System: "Welche Art von Geschäft planst du?"
User: "☕ Gastronomie"

System: "Beschreibe deine Geschäftsidee..."
User: "Kiez-Café mit Co-Working"

System: "Wo genau planst du das?" ✅
System: "Wie groß sollten die Räume sein?" ✅
System: "Öffnungszeiten?" ✅

System fragt NICHT:
- "Wie weit fährst du?" (nur für Mobil!)
- "Welche Tools?" (nur für Online!)

Nach Sektion 1:
Text: "## 2. GESCHÄFTSMODELL
Das geplante Kiez-Café kombiniert..." ✅ (Konkretes Geschäft!)
Keine Rechtsinfos! ✅
```

---

---

## 🚀 DEPLOY-BEFEHL

```bash
# Nachdem alle Änderungen gemacht wurden:

cd /backend

# Tests durchführen
pytest app/workshop/tests/ -v

# Wenn alles grün:
git add .
git commit -m "feat: Geschäftstyp-Branching + Text-Generierung Fix

- Implementiert BusinessTypeClassifier für 8 Geschäftstypen
- Implementiert DynamicQuestionGenerator mit typ-spezifischen Fragen
- Fixt SectionTextGenerator: Generiert konkreten Businessplan statt Rechtsinfos
- Updated ConversationService mit Branching-Logik
- Added Database Migrations für business_category
- Added comprehensive tests

Basierend auf: WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md"

git push origin main

# Railway deployed automatisch
# Monitoring:
railway logs --tail
```

---

**WICHTIG:** 
Lies ZUERST `/home/claude/WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md` vollständig durch!

Alle Implementierungen müssen diesem Referenzdokument folgen!
