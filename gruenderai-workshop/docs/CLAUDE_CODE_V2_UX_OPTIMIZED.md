# CLAUDE CODE V2: BRANCHING + UX-OPTIMIERUNG
## 🎯 Geschäftstyp-Branching + Cognitive Load Reduction

---

## 📋 ÜBERBLICK

**Ziele dieser Implementierung:**
1. ✅ Implementiere Geschäftstyp-Branching aus `WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md`
2. ✅ Fixe Text-Generierung (konkrete Businesspläne statt Rechtstexte)
3. ✅ **NEU:** Reduziere Cognitive Load → **NUR EINE FRAGE AUF EINMAL**
4. ✅ **NEU:** Implementiere Card-basierte Auswahl-UI
5. ✅ **NEU:** Immer Option "Andere" für Custom Input

---

## 🧠 UX-PRINZIPIEN

### **Vorher (Cognitive Overload):**
```
❌ Claude: "Jetzt zu den praktischen Details:

1) In welcher Stadt/Region willst du deine Boutique eröffnen?
2) Welche Art von Ladengeschäft schwebt dir vor?
   □ Kleiner Laden in der Innenstadt (20-40 qm)
   □ Größeres Geschäft am Stadtrand (50-100 qm)
   □ Showroom mit Werkstatt kombiniert (100+ qm)
3) Wo findest du deine Mid-Century Schätze?
   □ Flohmärkte und Antikläden
   □ Haushaltsauflösungen
   □ Online-Plattformen"
```
**Problem:** 3 Fragen + 7 Optionen = Cognitive Overload!

### **Nachher (Cognitive Ease):**
```
✅ Claude: "In welcher Stadt/Region willst du deine Boutique eröffnen?"

[Text Input Field]

---

User antwortet: "Berlin Pankow"

---

✅ Claude: "Welche Ladengröße stellst du dir vor?"

┌─────────────────────────────────┐
│ [Card] 30-50 qm                 │
│ Gemütlicher Showroom            │
│ Für 10-15 ausgestellte Möbel    │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ [Card] 50-80 qm                 │
│ Mehr Ausstellungsfläche         │
│ Für 20-25 Möbel                 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ [Card] 80+ qm                   │
│ Mit kleiner Werkstattecke       │
│ Für 30+ Möbel                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ [Card] Andere Größe             │
│ [Input: ___ qm]                 │
└─────────────────────────────────┘

---

User klickt: "50-80 qm"

---

✅ Claude: "Wo suchst du hauptsächlich deine Mid-Century Schätze?"

[Cards mit Optionen...]
```

**Vorteil:** 
- Nur EINE Frage zur Zeit
- Klare visuelle Auswahl
- Weniger Denk-Aufwand
- Schneller durchklicken

---

---

## 🏗️ IMPLEMENTIERUNGS-PLAN

### **PHASE 1: BACKEND - BRANCHING & SINGLE-QUESTION-FLOW**
### **PHASE 2: FRONTEND - CARD-BASED UI**
### **PHASE 3: TEXT-GENERIERUNG FIX**
### **PHASE 4: TESTING & DEPLOYMENT**

---

---

# 📦 PHASE 1: BACKEND - SINGLE-QUESTION-FLOW

## 🎯 Ziel
Jede User-Nachricht = 1 Frage gestellt
System stellt NIE mehrere Fragen auf einmal

---

## AUFGABE 1.1: Business Type Classifier

**Datei:** `/backend/app/workshop/services/business_type_classifier.py`

```python
"""
Business Type Classifier Service
Klassifiziert Geschäftstyp und gibt passende Konfiguration zurück
"""

from enum import Enum
from typing import Dict, List, Optional
import json

class BusinessCategory(Enum):
    """8 Haupt-Geschäftskategorien"""
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
    Klassifiziert User-Geschäft und gibt typ-spezifische Konfiguration zurück
    """
    
    def __init__(self):
        self.type_configs = self._load_type_configurations()
    
    def _load_type_configurations(self) -> Dict:
        """
        Lädt Typ-Konfigurationen basierend auf:
        WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md
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
                    "raumaufteilung",
                    "oeffnungszeiten",
                    "ruhetage",
                    "produktpalette",
                    "speisekarte_umfang",
                    "zielgruppe_primaer",
                    "kundenbeduerfnis",
                    "usp",
                    "marktluecke",
                    "preismodell_typ",
                    "preis_hauptprodukt",
                    "durchschnittlicher_bon"
                ],
                "excluded_questions": [
                    "einsatzradius_km",
                    "mobile_ausstattung",
                    "fahrzeug_typ",
                    "delivery_methode",
                    "tools_geplant",
                    "shop_plattform",
                    "versandlogistik"
                ]
            },
            
            BusinessCategory.HANDEL_STATIONAER: {
                "label": "🏪 Laden/Geschäft",
                "beschreibung": "Boutique, Einzelhandel, Spezialgeschäft",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "laden_typ",
                    "sortiment",
                    "sortiment_details",
                    "standort_konkret",
                    "standort_begruendung",
                    "groesse_qm",
                    "verkaufsflaeche_vs_lager",
                    "raumaufteilung",
                    "oeffnungszeiten",
                    "ruhetage",
                    "laufkundschaft_vs_stammkunden",  # Typ-spezifisch!
                    "zielgruppe_primaer",
                    "kundenbeduerfnis",
                    "usp",
                    "marktluecke",
                    "preismodell_typ",
                    "preisbeispiele",
                    "durchschnittlicher_bon"
                ],
                "excluded_questions": [
                    "einsatzradius_km",
                    "delivery_methode",
                    "tools_geplant",
                    "mobile_ausstattung",
                    "session_dauer",
                    "beratungsformat",
                    "skalierung_automatisierung"
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
                    "automatisierung_geplant",
                    "zielgruppe_primaer",
                    "customer_pain_point",
                    "usp",
                    "preismodell_typ",
                    "preis_hauptprodukt",
                    "durchschnittsprojekt_wert"
                ],
                "excluded_questions": [
                    "groesse_qm",
                    "sitzplaetze",
                    "oeffnungszeiten",
                    "standort_konkret",
                    "raumaufteilung",
                    "gastgewerbe_erlaubnis",
                    "warenlager",
                    "parkplaetze"
                ]
            },
            
            BusinessCategory.DIENSTLEISTUNG_MOBIL: {
                "label": "🚗 Mobiler Service",
                "beschreibung": "Handwerker, Mobile Massage, Haushaltsservice",
                "required_fields": [
                    "geschaeftsidee_kurz",
                    "service_typ",
                    "spezialisierung",
                    "einsatzgebiet_stadt",
                    "einsatzradius_km",
                    "mobilität_typ",
                    "fahrzeug_status",
                    "mobile_ausstattung",
                    "lager_benoetigt",
                    "durchschnittliche_einsatzzeit",
                    "anfahrtszeit_durchschnitt",
                    "einsaetze_pro_tag",
                    "anfahrtskosten_modell",
                    "kundentyp",
                    "zielgruppe_primaer",
                    "usp",
                    "marktluecke",
                    "preismodell_typ",
                    "preis_hauptprodukt",
                    "mindestauftragswert"
                ],
                "excluded_questions": [
                    "groesse_qm",
                    "sitzplaetze",
                    "oeffnungszeiten",
                    "raumaufteilung",
                    "gastgewerbe_erlaubnis",
                    "delivery_methode",
                    "tools_geplant"
                ]
            },
            
            # ... weitere Typen aus Referenzdokument
        }
    
    def get_classification_question(self) -> Dict:
        """
        Gibt die erste Klassifikationsfrage zurück
        Als CARD-basierte Auswahl!
        """
        return {
            "question_id": "business_category_classification",
            "text": "Welche Art von Geschäft planst du?",
            "hint": "Das hilft mir, dir die richtigen Fragen zu stellen",
            "typ": "card_selection",
            "single_select": True,
            "cards": [
                {
                    "value": "gastronomie",
                    "icon": "☕",
                    "label": "Gastronomie",
                    "description": "Café, Restaurant, Bar, Imbiss",
                    "beispiele": ["Specialty Coffee Shop", "Fine Dining", "Food Truck"]
                },
                {
                    "value": "dienstleistung_lokal",
                    "icon": "💼",
                    "label": "Dienstleistung vor Ort",
                    "description": "Friseur, Studio, Werkstatt, Praxis",
                    "beispiele": ["Yoga Studio", "Fahrradwerkstatt", "Tattoo Studio"]
                },
                {
                    "value": "dienstleistung_mobil",
                    "icon": "🚗",
                    "label": "Mobiler Service",
                    "description": "Handwerker, Pflege, Mobile Massage",
                    "beispiele": ["Mobiler Friseur", "Handwerker-Service", "Mobile Massage"]
                },
                {
                    "value": "dienstleistung_online",
                    "icon": "💻",
                    "label": "Online-Dienstleistung",
                    "description": "Beratung, SaaS, Coaching, Online-Kurse",
                    "beispiele": ["Business Coaching", "SEO-Beratung", "Online-Sprachkurse"]
                },
                {
                    "value": "handel_stationaer",
                    "icon": "🏪",
                    "label": "Laden/Geschäft",
                    "description": "Boutique, Einzelhandel, Spezialgeschäft",
                    "beispiele": ["Mode-Boutique", "Unverpackt-Laden", "Buchhandlung"]
                },
                {
                    "value": "handel_online",
                    "icon": "📦",
                    "label": "Online-Shop",
                    "description": "E-Commerce, Dropshipping, Amazon FBA",
                    "beispiele": ["Fashion E-Commerce", "Dropshipping", "Etsy Shop"]
                },
                {
                    "value": "produktion",
                    "icon": "🏭",
                    "label": "Produktion/Manufaktur",
                    "description": "Werkstatt, Manufaktur, Handwerk",
                    "beispiele": ["Schmuck-Manufaktur", "Schreinerei", "Craft Beer"]
                },
                {
                    "value": "hybrid",
                    "icon": "🔄",
                    "label": "Hybrid",
                    "description": "Mehrere Bereiche kombiniert",
                    "beispiele": ["Laden + Online-Shop", "Beratung vor Ort + Online"]
                }
            ],
            "required": True
        }
    
    def classify(self, business_category: str) -> Dict:
        """
        Klassifiziert basierend auf User-Auswahl
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
            "excluded_questions": config["excluded_questions"]
        }
    
    def is_question_excluded(self, question_id: str, business_category: str) -> bool:
        """
        Prüft ob Frage für Geschäftstyp ausgeschlossen ist
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

def test_classification_question_has_cards():
    classifier = BusinessTypeClassifier()
    question = classifier.get_classification_question()
    
    assert question["typ"] == "card_selection"
    assert len(question["cards"]) == 8
    assert question["cards"][0]["icon"] == "☕"
    assert question["cards"][4]["value"] == "handel_stationaer"

def test_handel_stationaer_has_laufkundschaft_field():
    classifier = BusinessTypeClassifier()
    result = classifier.classify("handel_stationaer")
    
    assert "laufkundschaft_vs_stammkunden" in result["required_fields"]
    assert "groesse_qm" in result["required_fields"]
    assert "einsatzradius_km" in result["excluded_questions"]
```

---

## AUFGABE 1.2: Single Question Flow Manager

**Datei:** `/backend/app/workshop/services/single_question_flow_manager.py`

```python
"""
Single Question Flow Manager
Stellt immer nur EINE Frage auf einmal
"""

from typing import Dict, List, Optional
from .business_type_classifier import BusinessTypeClassifier

class SingleQuestionFlowManager:
    """
    Verwaltet den Fragen-Flow:
    - Immer nur 1 Frage auf einmal
    - Typ-spezifische Fragen
    - Ausgeschlossene Fragen überspringen
    """
    
    def __init__(self, classifier: BusinessTypeClassifier):
        self.classifier = classifier
        self.question_templates = self._load_question_templates()
    
    def _load_question_templates(self) -> Dict:
        """
        Lädt alle Fragen-Templates aus Referenzdokument
        
        Format für jede Frage:
        {
            "question_id": {
                "gastronomie": {...},
                "handel_stationaer": {...},
                "default": {...}
            }
        }
        """
        
        return {
            # FRAGE: Geschäftsidee (für alle Typen gleich)
            "geschaeftsidee_kurz": {
                "default": {
                    "text": "Beschreibe deine Geschäftsidee in 1-2 Sätzen",
                    "hint": "So einfach, dass es jeder versteht - als würdest du es deiner Oma erzählen",
                    "typ": "open_text",
                    "placeholder": "z.B. 'Boutique für upcycelte Vintage-Möbel in Berlin'",
                    "validation": {
                        "min_length": 10,
                        "max_length": 200
                    }
                }
            },
            
            # FRAGE: Standort (typ-spezifisch!)
            "standort_konkret": {
                "gastronomie": {
                    "text": "Wo genau planst du dein {gastro_subtyp}?",
                    "hint": "Für Gastronomie ist die Lage KRITISCH! Bitte so konkret wie möglich.",
                    "typ": "open_text",
                    "placeholder": "z.B. 'Weserstraße, Neukölln' oder 'Prenzlauer Berg, nähe Kollwitzplatz'",
                    "validation": {
                        "min_length": 5,
                        "must_contain_city": True
                    }
                },
                "handel_stationaer": {
                    "text": "Wo soll dein Laden sein?",
                    "hint": "Laufkundschaft ist entscheidend! Je konkreter, desto besser.",
                    "typ": "open_text",
                    "placeholder": "z.B. 'Schönhauser Allee, Prenzlauer Berg' oder 'Einkaufsstraße in Charlottenburg'",
                    "validation": {
                        "min_length": 5
                    }
                },
                "dienstleistung_online": {
                    "text": "Wo ist dein Firmensitz?",
                    "hint": "Für Gewerbeanmeldung - keine Laufkundschaft nötig",
                    "typ": "open_text",
                    "placeholder": "z.B. 'Berlin' oder 'München'",
                    "validation": {
                        "min_length": 3
                    }
                }
                # Für mobil: Wird zu "Einsatzgebiet"
            },
            
            # FRAGE: Größe qm (NUR für stationäre Geschäfte!)
            "groesse_qm": {
                "gastronomie": {
                    "text": "Wie groß sollten deine Räume sein?",
                    "hint": "Die Größe bestimmt Kapazität, Miete und Personal-Bedarf",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "40-60",
                            "label": "40-60 qm",
                            "description": "Klein & gemütlich",
                            "detail": "~15-20 Gäste"
                        },
                        {
                            "value": "70-100",
                            "label": "70-100 qm",
                            "description": "Mittel",
                            "detail": "~25-35 Gäste"
                        },
                        {
                            "value": "100-150",
                            "label": "100-150 qm",
                            "description": "Groß",
                            "detail": "~40-60 Gäste"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Größe",
                            "description": "Eigene Angabe",
                            "requires_input": True,
                            "input_label": "Größe in qm:",
                            "input_placeholder": "z.B. 85"
                        }
                    ]
                },
                "handel_stationaer": {
                    "text": "Wie groß sollte dein Laden sein?",
                    "hint": "Berücksichtige Verkaufsfläche + Lager",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "30-50",
                            "label": "30-50 qm",
                            "description": "Gemütlicher Showroom",
                            "detail": "Für ~10-15 Produkte"
                        },
                        {
                            "value": "50-80",
                            "label": "50-80 qm",
                            "description": "Mehr Ausstellungsfläche",
                            "detail": "Für ~20-25 Produkte"
                        },
                        {
                            "value": "80-120",
                            "label": "80-120 qm",
                            "description": "Großer Laden",
                            "detail": "Für 30+ Produkte"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Größe",
                            "description": "Eigene Angabe",
                            "requires_input": True,
                            "input_label": "Größe in qm:",
                            "input_placeholder": "z.B. 65"
                        }
                    ]
                },
                "produktion": {
                    "text": "Wie groß muss deine Werkstatt/Produktion sein?",
                    "hint": "Berücksichtige Maschinen, Lager, Arbeitsfläche",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "50-100",
                            "label": "50-100 qm",
                            "description": "Kleine Werkstatt"
                        },
                        {
                            "value": "100-250",
                            "label": "100-250 qm",
                            "description": "Mittlere Produktion"
                        },
                        {
                            "value": "250+",
                            "label": "250+ qm",
                            "description": "Fabrikhalle"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Größe",
                            "requires_input": True,
                            "input_label": "Größe in qm:"
                        }
                    ]
                }
                # NICHT für Online/Mobil!
            },
            
            # FRAGE: Öffnungszeiten (NUR für stationär!)
            "oeffnungszeiten": {
                "gastronomie": {
                    "text": "Welche Öffnungszeiten planst du?",
                    "hint": "Wichtig für Kapazitäts- und Personalplanung",
                    "typ": "card_selection_with_custom",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "mo_sa_8_18",
                            "label": "Mo-Sa, 8-18 Uhr",
                            "description": "Klassisches Café",
                            "detail": "54 Std./Woche"
                        },
                        {
                            "value": "mo_so_11_23",
                            "label": "Mo-So, 11-23 Uhr",
                            "description": "Extended Gastro",
                            "detail": "84 Std./Woche"
                        },
                        {
                            "value": "do_sa_10_18",
                            "label": "Do-Sa, 10-18 Uhr",
                            "description": "Wochenend-Fokus",
                            "detail": "24 Std./Woche"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Zeiten",
                            "requires_input": True,
                            "input_label": "Gib deine Öffnungszeiten ein:",
                            "input_placeholder": "z.B. 'Di-Sa 9-19 Uhr'"
                        }
                    ]
                },
                "handel_stationaer": {
                    "text": "Welche Öffnungszeiten planst du?",
                    "typ": "card_selection_with_custom",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "mo_fr_10_19_sa_10_16",
                            "label": "Mo-Fr 10-19, Sa 10-16",
                            "description": "Standard Einzelhandel"
                        },
                        {
                            "value": "do_sa_11_19",
                            "label": "Do-Sa 11-19 Uhr",
                            "description": "Fokus Wochenende"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Zeiten",
                            "requires_input": True,
                            "input_label": "Deine Öffnungszeiten:"
                        }
                    ]
                }
                # NICHT für Online/Mobil!
            },
            
            # FRAGE: Delivery-Methode (NUR für Online!)
            "delivery_methode": {
                "dienstleistung_online": {
                    "text": "Wie lieferst du deine Dienstleistung?",
                    "hint": "Du kannst mehrere Methoden kombinieren",
                    "typ": "card_selection",
                    "single_select": False,  # Multi-Select!
                    "cards": [
                        {
                            "value": "video_live",
                            "label": "Live Video-Calls",
                            "description": "Zoom, Teams, Google Meet",
                            "icon": "📹"
                        },
                        {
                            "value": "async",
                            "label": "Asynchron",
                            "description": "Email, Loom, Voice Notes",
                            "icon": "📧"
                        },
                        {
                            "value": "vor_ort",
                            "label": "Persönlich vor Ort",
                            "description": "Beim Kunden",
                            "icon": "🤝"
                        },
                        {
                            "value": "selbstlern",
                            "label": "Selbstlern-Kurse",
                            "description": "Aufgezeichnete Videos",
                            "icon": "🎓"
                        }
                    ]
                }
                # NUR für Online!
            },
            
            # FRAGE: Einsatzradius (NUR für Mobil!)
            "einsatzradius_km": {
                "dienstleistung_mobil": {
                    "text": "Wie weit fährst du maximal?",
                    "hint": "Bedenke: Fahrtzeit = weniger Einsätze pro Tag + Benzinkosten",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "5",
                            "label": "5 km",
                            "description": "Sehr lokal (Kiez)",
                            "detail": "~10-15 Min Fahrt"
                        },
                        {
                            "value": "10",
                            "label": "10 km",
                            "description": "Stadtbezirk",
                            "detail": "~20-30 Min Fahrt"
                        },
                        {
                            "value": "20",
                            "label": "20 km",
                            "description": "Ganze Stadt",
                            "detail": "~40-50 Min Fahrt"
                        },
                        {
                            "value": "50",
                            "label": "50 km",
                            "description": "Stadt + Umland",
                            "detail": "~60-90 Min Fahrt"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Distanz",
                            "requires_input": True,
                            "input_label": "Einsatzradius in km:"
                        }
                    ]
                }
                # NUR für Mobil!
            },
            
            # FRAGE: Zielgruppe (für alle Typen, leicht angepasst)
            "zielgruppe_primaer": {
                "default": {
                    "text": "WER sind deine Hauptkunden?",
                    "hint": "Je spezifischer, desto besser!",
                    "typ": "guided_open_text",
                    "template": """Beschreibe deine Hauptzielgruppe:

1. **Demografie:** Alter, Beruf, Einkommen
2. **Bedürfnis:** Welches Problem löst du für sie?
3. **Verhalten:** Wie/wann nutzen sie dein Angebot?
4. **Ausgabebereitschaft:** Was können sie ausgeben?""",
                    "beispiel": """Beispiel:
1. Freelancer & Selbstständige, 28-45 Jahre, Designer/Entwickler
2. Brauchen flexible Arbeitsplätze außerhalb der Wohnung
3. 3-4x/Woche, bleiben 4-6 Stunden, arbeiten konzentriert
4. 15-25€/Tag für Arbeitsplatz + Kaffee"""
                }
            },
            
            # FRAGE: USP (für alle Typen)
            "usp": {
                "default": {
                    "text": "Was macht DICH einzigartig?",
                    "hint": "Denk an: Was haben andere NICHT, das du hast?",
                    "typ": "structured_text",
                    "template": """Vervollständige diesen Satz:

"Im Gegensatz zu [Konkurrenten/Alternative] bin ich der/die Einzige, der/die [dein USP], was für Kunden bedeutet [Vorteil]."

Beispiel:
"Im Gegensatz zu Ikea (Massenware) und Antiquitäten-Läden (verstaubt) bin ich der einzige Laden, der nachhaltig upcycelte Möbel mit sichtbarer Werkstatt anbietet, was Kunden ermöglicht, die Entstehung ihrer Möbel live zu erleben."
""",
                    "validation": {
                        "min_length": 50
                    }
                }
            },
            
            # FRAGE: Preismodell
            "preismodell_typ": {
                "gastronomie": {
                    "text": "Welches Preismodell passt zu dir?",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "a_la_carte",
                            "label": "À la carte",
                            "description": "Jedes Produkt einzeln bezahlt"
                        },
                        {
                            "value": "flatrate",
                            "label": "Flatrate/Abo",
                            "description": "Pauschalpreis für Zeitraum",
                            "beispiel": "Membership für Co-Working"
                        },
                        {
                            "value": "hybrid",
                            "label": "Hybrid",
                            "description": "Kombination aus beidem",
                            "beispiel": "Abo für Stammkunden + Einzelpreise"
                        }
                    ]
                },
                "dienstleistung_online": {
                    "text": "Wie berechnest du deine Preise?",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "stundensatz",
                            "label": "Stundensatz",
                            "description": "X€ pro Stunde"
                        },
                        {
                            "value": "projektpauschale",
                            "label": "Projektpauschale",
                            "description": "Festpreis pro Projekt"
                        },
                        {
                            "value": "retainer",
                            "label": "Retainer",
                            "description": "Monatliche Pauschale"
                        },
                        {
                            "value": "value_based",
                            "label": "Value-based",
                            "description": "Preis basiert auf Ergebnis"
                        },
                        {
                            "value": "abo",
                            "label": "Abo-Modell",
                            "description": "Monatlich kündbar"
                        }
                    ]
                },
                "handel_stationaer": {
                    "text": "Wie berechnest du deine Preise?",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "einzelverkauf",
                            "label": "Einzelverkauf",
                            "description": "Jedes Produkt einzeln"
                        },
                        {
                            "value": "pakete",
                            "label": "Pakete/Sets",
                            "description": "Mehrere Produkte gebündelt"
                        },
                        {
                            "value": "custom",
                            "label": "Nach Aufwand",
                            "description": "Je nach Produkt unterschiedlich"
                        }
                    ]
                }
            },
            
            # FRAGE: Durchschnittlicher Bon (wichtig für GZ!)
            "durchschnittlicher_bon": {
                "gastronomie": {
                    "text": "Was gibt ein typischer Gast bei dir aus?",
                    "hint": "Wichtig für Umsatzplanung",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "5-10",
                            "label": "5-10€",
                            "description": "Schneller Kaffee/Snack To-Go"
                        },
                        {
                            "value": "10-20",
                            "label": "10-20€",
                            "description": "Frühstück oder Mittag + Getränk"
                        },
                        {
                            "value": "20-40",
                            "label": "20-40€",
                            "description": "Vollständige Mahlzeit mit Getränken"
                        },
                        {
                            "value": "40+",
                            "label": "40€+",
                            "description": "Fine Dining/Mehrere Gänge"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Summe",
                            "requires_input": True,
                            "input_label": "Durchschnittlicher Bon in €:"
                        }
                    ]
                },
                "handel_stationaer": {
                    "text": "Was gibt ein typischer Kunde bei dir aus?",
                    "hint": "Denk an: Kaufen sie meist ein Stück oder mehrere?",
                    "typ": "card_selection",
                    "single_select": True,
                    "cards": [
                        {
                            "value": "50-150",
                            "label": "50-150€",
                            "description": "Ein kleineres Stück"
                        },
                        {
                            "value": "150-300",
                            "label": "150-300€",
                            "description": "Ein mittleres Stück"
                        },
                        {
                            "value": "300-600",
                            "label": "300-600€",
                            "description": "Ein größeres Stück oder mehrere kleine"
                        },
                        {
                            "value": "600+",
                            "label": "600€+",
                            "description": "Premium-Stücke"
                        },
                        {
                            "value": "custom",
                            "label": "Andere Summe",
                            "requires_input": True,
                            "input_label": "Durchschnittlicher Kauf in €:"
                        }
                    ]
                },
                "dienstleistung_online": {
                    "text": "Was ist der durchschnittliche Wert eines Kunden-Projekts?",
                    "hint": "Denk an die gesamte Kundenbeziehung (Customer Lifetime Value)",
                    "typ": "open_text_with_hint",
                    "placeholder": "z.B. '1.200€' oder '500€ pro Monat für 6 Monate'",
                    "beispiele": [
                        "Session 150€ × 8 Sessions = 1.200€",
                        "3-Monats-Programm: 3.000€",
                        "Retainer: 2.500€/Monat × 12 Monate = 30.000€"
                    ]
                }
            },
            
            # ... weitere Fragen aus Referenzdokument
        }
    
    def get_next_question(
        self,
        business_category: str,
        collected_fields: Dict
    ) -> Optional[Dict]:
        """
        Gibt die NÄCHSTE EINZELNE Frage zurück
        
        Returns:
            Dict mit Frage oder None wenn alle Fragen beantwortet
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
            
            # Skip wenn excluded (Sicherheitscheck)
            if field_id in excluded_questions:
                continue
            
            # Hole typ-spezifisches Template
            question_template = self._get_question_template(
                field_id,
                business_category,
                collected_fields
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
        business_category: str,
        collected_fields: Dict
    ) -> Optional[Dict]:
        """
        Holt typ-spezifisches Fragen-Template
        
        Kann Platzhalter ersetzen, z.B.:
        "Wo planst du dein {gastro_subtyp}?" → "Wo planst du dein Café?"
        """
        
        if question_id not in self.question_templates:
            return self._generate_fallback_template(question_id)
        
        variants = self.question_templates[question_id]
        
        # Typ-spezifische Variante vorhanden?
        if business_category in variants:
            template = variants[business_category]
        elif "default" in variants:
            template = variants["default"]
        else:
            return None
        
        # Platzhalter ersetzen
        template = self._replace_placeholders(template, collected_fields)
        
        return template
    
    def _replace_placeholders(self, template: Dict, collected_fields: Dict) -> Dict:
        """
        Ersetzt Platzhalter wie {gastro_subtyp} mit echten Werten
        """
        import re
        
        def replace_in_string(text: str) -> str:
            if not isinstance(text, str):
                return text
            
            # Finde alle {placeholder}
            placeholders = re.findall(r'\{(\w+)\}', text)
            
            for placeholder in placeholders:
                if placeholder in collected_fields:
                    text = text.replace(
                        f'{{{placeholder}}}',
                        str(collected_fields[placeholder])
                    )
            
            return text
        
        # Rekursiv durch alle Werte
        result = {}
        for key, value in template.items():
            if isinstance(value, str):
                result[key] = replace_in_string(value)
            elif isinstance(value, dict):
                result[key] = self._replace_placeholders(value, collected_fields)
            elif isinstance(value, list):
                result[key] = [
                    self._replace_placeholders(item, collected_fields) if isinstance(item, dict)
                    else replace_in_string(item) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                result[key] = value
        
        return result
    
    def _generate_fallback_template(self, question_id: str) -> Dict:
        """
        Generiert generisches Template wenn keine typ-spezifische Version existiert
        """
        label = question_id.replace("_", " ").title()
        
        return {
            "text": f"{label}:",
            "typ": "open_text",
            "placeholder": "",
            "hint": ""
        }
```

---

## AUFGABE 1.3: Update Conversation Service

**Datei:** `/backend/app/workshop/services/conversation_service.py`

```python
"""
Conversation Service mit Single-Question-Flow
"""

from .business_type_classifier import BusinessTypeClassifier
from .single_question_flow_manager import SingleQuestionFlowManager
from .section_text_generator import SectionTextGenerator
from ..models import WorkshopSession

class ConversationService:
    
    def __init__(self):
        self.classifier = BusinessTypeClassifier()
        self.flow_manager = SingleQuestionFlowManager(self.classifier)
        self.text_generator = SectionTextGenerator()
    
    async def send_message(self, session_id: str, user_message: str, db):
        """
        Hauptlogik:
        1 User-Nachricht → 1 Antwort mit maximal 1 Frage
        """
        
        session = db.query(WorkshopSession).filter_by(id=session_id).first()
        
        # --- SCHRITT 1: KLASSIFIKATION ---
        if not session.business_category:
            
            # Allererste Nachricht: Stelle Klassifikationsfrage
            if session.message_count == 0:
                classification_question = self.classifier.get_classification_question()
                
                return {
                    "assistant_message": self._format_classification_intro(),
                    "question": classification_question,
                    "requires_classification": True,
                    "message_type": "question_card_selection"
                }
            
            # Zweite Nachricht: Klassifiziere
            try:
                classification_result = self.classifier.classify(user_message)
                
                # Speichere
                session.business_category = classification_result["category_value"]
                session.required_fields = classification_result["required_fields"]
                session.excluded_questions = classification_result["excluded_questions"]
                db.commit()
                
                # Bestätige Klassifikation + Stelle ERSTE Frage
                next_question = self.flow_manager.get_next_question(
                    business_category=session.business_category,
                    collected_fields=session.collected_fields or {}
                )
                
                confirmation_text = f"""Perfekt! Du planst: **{classification_result['label']}**

{classification_result['beschreibung']}

Lass uns jetzt die Details deines Geschäfts erfassen!"""
                
                return {
                    "assistant_message": confirmation_text,
                    "question": next_question,
                    "business_category": classification_result["category_value"],
                    "message_type": self._get_message_type(next_question)
                }
            
            except ValueError as e:
                return {
                    "assistant_message": "Hmm, das habe ich nicht verstanden. Bitte wähle eine der Optionen aus.",
                    "error": "invalid_classification"
                }
        
        # --- SCHRITT 2: ERFASSE DATEN ---
        
        # Extrahiere Daten aus User-Antwort
        extracted_data = await self._extract_data_from_message(
            user_message,
            session.current_question_id,
            session.business_category
        )
        
        # Speichere
        if not session.collected_fields:
            session.collected_fields = {}
        session.collected_fields.update(extracted_data)
        db.commit()
        
        # --- SCHRITT 3: NÄCHSTE FRAGE ODER FERTIG ---
        
        next_question = self.flow_manager.get_next_question(
            business_category=session.business_category,
            collected_fields=session.collected_fields
        )
        
        # Alle Fragen beantwortet?
        if next_question is None:
            return await self._complete_section(session, db)
        
        # Speichere aktuelle Frage-ID
        session.current_question_id = next_question["question_id"]
        db.commit()
        
        # Gib EINE Frage zurück
        return {
            "assistant_message": self._format_transition_text(extracted_data),
            "question": next_question,
            "message_type": self._get_message_type(next_question),
            "progress": self._calculate_progress(session)
        }
    
    def _format_classification_intro(self) -> str:
        """
        Intro-Text vor Klassifikationsfrage
        """
        return """Willkommen beim GründerAI Businessplan-Workshop! 👋

Bevor wir loslegen, lass mich verstehen, welche Art von Geschäft du planst.

Das hilft mir, dir die richtigen Fragen zu stellen:"""
    
    def _format_transition_text(self, extracted_data: Dict) -> str:
        """
        Kurzer Bestätigungs-Text zwischen Fragen
        
        Nicht bei jeder Frage! Nur manchmal zur Auflockerung.
        """
        
        # 70% der Zeit: Keine Transition (direkt zur nächsten Frage)
        import random
        if random.random() < 0.7:
            return ""
        
        # 30% der Zeit: Kurze Bestätigung
        confirmations = [
            "👍 Verstanden!",
            "✅ Notiert!",
            "Perfekt!",
            "Super!",
            "Alles klar!"
        ]
        
        return random.choice(confirmations)
    
    def _get_message_type(self, question: Dict) -> str:
        """
        Bestimmt Message-Type für Frontend
        """
        if not question:
            return "text"
        
        typ = question.get("typ")
        
        if typ == "card_selection":
            return "question_card_selection"
        elif typ == "open_text":
            return "question_open_text"
        elif typ == "guided_open_text":
            return "question_guided_text"
        else:
            return "question_text"
    
    def _calculate_progress(self, session: WorkshopSession) -> Dict:
        """
        Berechnet Fortschritt
        """
        total_fields = len(session.required_fields)
        collected = len(session.collected_fields or {})
        
        percentage = int((collected / total_fields) * 100) if total_fields > 0 else 0
        
        return {
            "collected": collected,
            "total": total_fields,
            "percentage": percentage
        }
    
    async def _complete_section(self, session, db):
        """
        Sektion ist komplett → Generiere Text
        """
        
        # Generiere typ-spezifischen Text
        generated_text = await self.text_generator.generate_modul_1_text(
            business_category=session.business_category,
            extracted_data=session.collected_fields
        )
        
        # Speichere
        from ..models import SectionCompletion
        
        section_completion = db.query(SectionCompletion).filter(
            SectionCompletion.session_id == session.id,
            SectionCompletion.section_id == "modul_1_geschaeftsmodell"
        ).first()
        
        if not section_completion:
            section_completion = SectionCompletion(
                session_id=session.id,
                section_id="modul_1_geschaeftsmodell"
            )
            db.add(section_completion)
        
        section_completion.generated_text = generated_text
        section_completion.section_completed = True
        db.commit()
        
        # Return completion message
        return {
            "message_type": "section_complete",
            "section_id": "modul_1_geschaeftsmodell",
            "generated_text": generated_text,
            "gz_conformity": self._calculate_gz_conformity(session),
            "next_section": "modul_2_dein_unternehmen"
        }
    
    def _calculate_gz_conformity(self, session: WorkshopSession) -> int:
        """
        Berechnet GZ-Konformität für diese Sektion
        """
        # Einfache Version: % der Pflichtfelder erfasst
        total = len(session.required_fields)
        collected = len(session.collected_fields or {})
        
        return int((collected / total) * 100) if total > 0 else 0
    
    async def _extract_data_from_message(
        self,
        user_message: str,
        question_id: str,
        business_category: str
    ) -> Dict:
        """
        Extrahiert strukturierte Daten aus User-Nachricht
        
        TODO: Nutze Claude für intelligente Extraktion
        """
        
        # Für jetzt: Simple Extraktion
        return {
            question_id: user_message
        }
```

**Testing:**
```python
# /backend/app/workshop/tests/test_single_question_flow.py

@pytest.mark.asyncio
async def test_single_question_per_message():
    """
    Test: System stellt immer nur EINE Frage auf einmal
    """
    
    service = ConversationService()
    session = create_test_session()
    
    # Nachricht 1: Klassifikation
    response1 = await service.send_message(
        session_id=session.id,
        user_message="",
        db=db
    )
    
    assert "question" in response1
    assert response1["question"]["question_id"] == "business_category_classification"
    
    # Nachricht 2: Wähle Typ
    response2 = await service.send_message(
        session_id=session.id,
        user_message="handel_stationaer",
        db=db
    )
    
    # Sollte EINE Frage zurückgeben (die erste für Handel)
    assert "question" in response2
    assert response2["question"]["question_id"] == "geschaeftsidee_kurz"
    
    # WICHTIG: Keine weiteren Fragen in "assistant_message"!
    assert "1)" not in response2["assistant_message"]
    assert "2)" not in response2["assistant_message"]
    assert "□" not in response2["assistant_message"]

@pytest.mark.asyncio
async def test_card_questions_have_proper_format():
    """
    Test: Card-Fragen haben richtige Struktur
    """
    
    flow_manager = SingleQuestionFlowManager(BusinessTypeClassifier())
    
    question = flow_manager._get_question_template(
        "groesse_qm",
        "handel_stationaer",
        {}
    )
    
    assert question["typ"] == "card_selection"
    assert "cards" in question
    assert len(question["cards"]) >= 3
    assert question["cards"][-1]["value"] == "custom"  # Letzter ist "Andere"
    assert question["cards"][-1]["requires_input"] == True
```

---

# 📦 PHASE 2: FRONTEND - CARD-BASED UI

## AUFGABE 2.1: Card Selection Component

**Datei:** `/frontend/src/components/workshop/CardSelection.tsx`

```typescript
import React, { useState } from 'react';

interface Card {
  value: string;
  icon?: string;
  label: string;
  description: string;
  detail?: string;
  beispiel?: string;
  requires_input?: boolean;
  input_label?: string;
  input_placeholder?: string;
}

interface CardSelectionProps {
  question: {
    text: string;
    hint?: string;
    cards: Card[];
    single_select: boolean;
  };
  onSelect: (value: string | string[]) => void;
}

export const CardSelection: React.FC<CardSelectionProps> = ({
  question,
  onSelect
}) => {
  const [selectedValues, setSelectedValues] = useState<string[]>([]);
  const [customInput, setCustomInput] = useState<string>('');
  const [showCustomInput, setShowCustomInput] = useState(false);
  
  const handleCardClick = (value: string, requiresInput: boolean) => {
    if (requiresInput) {
      setShowCustomInput(true);
      return;
    }
    
    if (question.single_select) {
      // Single Select: Direkt submitten
      setSelectedValues([value]);
      onSelect(value);
    } else {
      // Multi Select: Toggle
      const newSelection = selectedValues.includes(value)
        ? selectedValues.filter(v => v !== value)
        : [...selectedValues, value];
      
      setSelectedValues(newSelection);
    }
  };
  
  const handleCustomSubmit = () => {
    if (customInput.trim()) {
      onSelect(customInput);
    }
  };
  
  return (
    <div className="card-selection">
      {/* Frage-Text */}
      <div className="question-text">
        {question.text}
      </div>
      
      {/* Hint */}
      {question.hint && (
        <div className="question-hint">
          💡 {question.hint}
        </div>
      )}
      
      {/* Cards Grid */}
      <div className={`cards-grid ${question.single_select ? 'single' : 'multi'}`}>
        {question.cards.map((card, index) => (
          <div
            key={index}
            className={`card ${selectedValues.includes(card.value) ? 'selected' : ''} ${card.requires_input ? 'custom-card' : ''}`}
            onClick={() => handleCardClick(card.value, card.requires_input || false)}
          >
            {/* Icon */}
            {card.icon && (
              <div className="card-icon">{card.icon}</div>
            )}
            
            {/* Label */}
            <div className="card-label">{card.label}</div>
            
            {/* Description */}
            <div className="card-description">{card.description}</div>
            
            {/* Detail */}
            {card.detail && (
              <div className="card-detail">{card.detail}</div>
            )}
            
            {/* Beispiel */}
            {card.beispiel && (
              <div className="card-beispiel">z.B. {card.beispiel}</div>
            )}
            
            {/* Selection Indicator */}
            {!question.single_select && (
              <div className="card-checkbox">
                {selectedValues.includes(card.value) ? '✓' : '○'}
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Custom Input Modal */}
      {showCustomInput && (
        <div className="custom-input-modal">
          <div className="custom-input-content">
            <h3>{question.cards.find(c => c.requires_input)?.input_label || 'Eigene Angabe'}</h3>
            
            <input
              type="text"
              placeholder={question.cards.find(c => c.requires_input)?.input_placeholder || ''}
              value={customInput}
              onChange={(e) => setCustomInput(e.target.value)}
              autoFocus
            />
            
            <div className="custom-input-buttons">
              <button onClick={() => setShowCustomInput(false)}>
                Abbrechen
              </button>
              <button onClick={handleCustomSubmit} disabled={!customInput.trim()}>
                Bestätigen
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Multi-Select Submit Button */}
      {!question.single_select && selectedValues.length > 0 && (
        <button 
          className="submit-button"
          onClick={() => onSelect(selectedValues)}
        >
          Weiter ({selectedValues.length} ausgewählt)
        </button>
      )}
    </div>
  );
};
```

**Styles:** `/frontend/src/components/workshop/CardSelection.css`

```css
.card-selection {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.question-text {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 12px;
}

.question-hint {
  font-size: 14px;
  color: #666;
  background: #f8f9fa;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  border-left: 3px solid #4CAF50;
}

/* Cards Grid */
.cards-grid {
  display: grid;
  gap: 16px;
  margin-bottom: 24px;
}

.cards-grid.single {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.cards-grid.multi {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* Individual Card */
.card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  min-height: 140px;
  display: flex;
  flex-direction: column;
}

.card:hover {
  border-color: #4CAF50;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
  transform: translateY(-2px);
}

.card.selected {
  border-color: #4CAF50;
  background: #f1f8f4;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.2);
}

.card.custom-card {
  border-style: dashed;
  border-color: #9e9e9e;
}

.card.custom-card:hover {
  border-color: #4CAF50;
  border-style: solid;
}

/* Card Content */
.card-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.card-label {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.card-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  flex-grow: 1;
}

.card-detail {
  font-size: 13px;
  color: #888;
  font-style: italic;
}

.card-beispiel {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #eee;
}

.card-checkbox {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 24px;
  height: 24px;
  border: 2px solid #e0e0e0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #4CAF50;
  font-weight: bold;
}

.card.selected .card-checkbox {
  border-color: #4CAF50;
  background: #4CAF50;
  color: white;
}

/* Custom Input Modal */
.custom-input-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.custom-input-content {
  background: white;
  padding: 32px;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
}

.custom-input-content h3 {
  margin-bottom: 16px;
  font-size: 20px;
}

.custom-input-content input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 20px;
}

.custom-input-content input:focus {
  outline: none;
  border-color: #4CAF50;
}

.custom-input-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.custom-input-buttons button {
  padding: 10px 24px;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.custom-input-buttons button:first-child {
  background: #f5f5f5;
  color: #666;
}

.custom-input-buttons button:last-child {
  background: #4CAF50;
  color: white;
}

.custom-input-buttons button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Submit Button (Multi-Select) */
.submit-button {
  width: 100%;
  padding: 16px;
  font-size: 18px;
  font-weight: 600;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-button:hover {
  background: #45a049;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .cards-grid.single,
  .cards-grid.multi {
    grid-template-columns: 1fr;
  }
  
  .card {
    min-height: auto;
  }
}
```

---

## AUFGABE 2.2: Update WorkshopChat Component

**Datei:** `/frontend/src/components/workshop/WorkshopChat.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { CardSelection } from './CardSelection';

export const WorkshopChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [inputValue, setInputValue] = useState('');
  
  const handleCardSelection = async (value: string | string[]) => {
    // Sende Selection an Backend
    const response = await sendMessage(value);
    
    // Update State
    setMessages([
      ...messages,
      { role: 'user', content: formatUserSelection(value) },
      { role: 'assistant', content: response.assistant_message }
    ]);
    
    // Nächste Frage
    if (response.question) {
      setCurrentQuestion(response.question);
    } else if (response.message_type === 'section_complete') {
      handleSectionComplete(response);
    }
  };
  
  const handleTextInput = async () => {
    if (!inputValue.trim()) return;
    
    const response = await sendMessage(inputValue);
    
    setMessages([
      ...messages,
      { role: 'user', content: inputValue },
      { role: 'assistant', content: response.assistant_message }
    ]);
    
    setInputValue('');
    
    if (response.question) {
      setCurrentQuestion(response.question);
    }
  };
  
  return (
    <div className="workshop-chat">
      {/* Messages History */}
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      
      {/* Current Question */}
      {currentQuestion && (
        <div className="current-question">
          {currentQuestion.typ === 'card_selection' ? (
            <CardSelection
              question={currentQuestion}
              onSelect={handleCardSelection}
            />
          ) : currentQuestion.typ === 'open_text' ? (
            <div className="open-text-input">
              <div className="question-text">{currentQuestion.text}</div>
              {currentQuestion.hint && (
                <div className="question-hint">💡 {currentQuestion.hint}</div>
              )}
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={currentQuestion.placeholder}
                rows={4}
              />
              <button onClick={handleTextInput}>
                Weiter
              </button>
            </div>
          ) : (
            // Weitere Typen...
            <div>Unsupported question type</div>
          )}
        </div>
      )}
    </div>
  );
};
```

---

# 📦 PHASE 3: TEXT-GENERIERUNG FIX

(Nutze Code aus CLAUDE_CODE_IMPLEMENTATION_COMMAND.md Aufgabe 3)

Bereits implementiert - siehe vorheriges Dokument Aufgabe 3: Section Text Generator

---

# 📦 PHASE 4: TESTING & DEPLOYMENT

## AUFGABE 4.1: Integration Tests

```python
# /backend/app/workshop/tests/test_full_flow_ux_optimized.py

@pytest.mark.asyncio
async def test_handel_stationaer_full_flow_single_questions():
    """
    Test: Kompletter Flow für Handel Stationär
    - Nur eine Frage auf einmal
    - Card-basierte Auswahl
    """
    
    service = ConversationService()
    session_id = "test_handel_123"
    
    # 1. Start: Klassifikationsfrage
    response = await service.send_message(session_id, "", db)
    
    assert response["question"]["question_id"] == "business_category_classification"
    assert response["question"]["typ"] == "card_selection"
    assert len(response["question"]["cards"]) == 8
    
    # 2. Wähle "Handel Stationär"
    response = await service.send_message(session_id, "handel_stationaer", db)
    
    assert response["business_category"] == "handel_stationaer"
    assert response["question"]["question_id"] == "geschaeftsidee_kurz"
    
    # 3. Beantworte Geschäftsidee
    response = await service.send_message(
        session_id,
        "Boutique für upcycelte Vintage-Möbel",
        db
    )
    
    # Sollte EINE neue Frage zurückgeben
    assert "question" in response
    next_q_id = response["question"]["question_id"]
    
    # WICHTIG: Keine Fragen im Text!
    assert "1)" not in response["assistant_message"]
    assert "2)" not in response["assistant_message"]
    
    # 4. Beantworte alle weiteren Fragen...
    question_count = 0
    while response.get("question"):
        question_count += 1
        
        # Simuliere Antwort
        question = response["question"]
        
        if question["typ"] == "card_selection":
            # Wähle erste Card
            user_answer = question["cards"][0]["value"]
        else:
            user_answer = "Test Answer"
        
        response = await service.send_message(session_id, user_answer, db)
        
        # Max 20 Fragen als Sicherheit
        if question_count > 20:
            break
    
    # Am Ende: Sektion complete
    assert response["message_type"] == "section_complete"
    assert response["generated_text"] is not None
    
    # Text sollte konkret sein
    generated = response["generated_text"]
    assert "Boutique" in generated or "Möbel" in generated
    assert "§ 93 SGB III" not in generated  # Keine Rechtstexte!

@pytest.mark.asyncio
async def test_card_with_custom_input():
    """
    Test: Card mit "Andere" Option und Custom Input
    """
    
    flow_manager = SingleQuestionFlowManager(BusinessTypeClassifier())
    
    question = flow_manager._get_question_template(
        "groesse_qm",
        "handel_stationaer",
        {}
    )
    
    # Letzte Card sollte "custom" sein
    custom_card = question["cards"][-1]
    assert custom_card["value"] == "custom"
    assert custom_card["requires_input"] == True
    assert "input_label" in custom_card
```

## AUFGABE 4.2: Frontend E2E Tests

```typescript
// /frontend/tests/e2e/workshop-flow.spec.ts

describe('Workshop Flow - UX Optimized', () => {
  it('should show one question at a time', async () => {
    await page.goto('/workshop-chat');
    
    // Schritt 1: Klassifikation als Cards
    await expect(page.locator('.card-selection')).toBeVisible();
    await expect(page.locator('.card')).toHaveCount(8);
    
    // Klicke auf "Handel Stationär"
    await page.click('.card:has-text("Laden/Geschäft")');
    
    // Sollte neue Frage zeigen (nur eine!)
    await expect(page.locator('.question-text')).toContainText('Geschäftsidee');
    
    // WICHTIG: Keine weiteren Fragen im Text
    const text = await page.locator('.chat-container').textContent();
    expect(text).not.toContain('1)');
    expect(text).not.toContain('2)');
  });
  
  it('should handle card selection with custom input', async () => {
    await page.goto('/workshop-chat?question=groesse_qm');
    
    // Klicke auf "Andere Größe"
    await page.click('.card.custom-card');
    
    // Modal sollte erscheinen
    await expect(page.locator('.custom-input-modal')).toBeVisible();
    
    // Gib Custom-Wert ein
    await page.fill('input[type="text"]', '65');
    await page.click('button:has-text("Bestätigen")');
    
    // Sollte zur nächsten Frage gehen
    await expect(page.locator('.question-text')).not.toContainText('Größe');
  });
});
```

---

# 🚀 DEPLOYMENT

## Schritt 1: Code Review Checklist

```bash
✅ Business Type Classifier implementiert
✅ Single Question Flow Manager implementiert
✅ Conversation Service updated
✅ Card Selection Component erstellt
✅ Frontend Integration abgeschlossen
✅ Text-Generierung typ-spezifisch
✅ Tests geschrieben und grün
✅ Cognitive Load reduziert (nur 1 Frage)
✅ "Andere" Option überall verfügbar
```

## Schritt 2: Backend Tests

```bash
cd /backend
pytest app/workshop/tests/test_business_type_classifier.py -v
pytest app/workshop/tests/test_single_question_flow.py -v
pytest app/workshop/tests/test_full_flow_ux_optimized.py -v
```

## Schritt 3: Frontend Tests

```bash
cd /frontend
npm run test:e2e
```

## Schritt 4: Deploy

```bash
git add .
git commit -m "feat: Geschäftstyp-Branching + UX-Optimierung (Single Question Flow + Cards)

- Implementiert BusinessTypeClassifier für 8 Geschäftstypen
- Implementiert SingleQuestionFlowManager (nur 1 Frage auf einmal)
- Card-based UI für alle Auswahl-Fragen
- 'Andere' Option für Custom Input
- Fixt Text-Generierung (konkret statt Rechtstexte)
- Reduziert Cognitive Load massiv

Basierend auf:
- WORKSHOP_MODULE_DEFINITIONS_COMPLETE.md
- CLAUDE_CODE_V2_UX_OPTIMIZED.md"

git push origin main

# Railway deployed automatisch
railway logs --tail
```

---

# 🎯 ERWARTETE ERGEBNISSE

## Vorher:
```
Claude: "Jetzt zu den praktischen Details:

1) In welcher Stadt/Region willst du deine Boutique eröffnen?
2) Welche Art von Ladengeschäft schwebt dir vor?
   □ Kleiner Laden in der Innenstadt (20-40 qm)
   □ Größeres Geschäft am Stadtrand (50-100 qm)
3) Wo findest du deine Mid-Century Schätze?
   □ Flohmärkte und Antikläden
   □ Haushaltsauflösungen"
```
❌ 3 Fragen + 5 Optionen = Overload!

## Nachher:
```
Claude: "Welche Art von Geschäft planst du?"

[8 Cards mit Icons und Beschreibungen]
☕ Gastronomie | 💼 Dienstleistung | 🏪 Laden | etc.

User klickt: "🏪 Laden/Geschäft"

---

Claude: "Perfekt! Du planst einen Laden/Geschäft.
Beschreibe deine Geschäftsidee in 1-2 Sätzen:"

[Text Input Field]

User tippt: "Boutique für upcycelte Vintage-Möbel"

---

Claude: "Wo soll dein Laden sein?"

[Text Input Field mit Hint]

User tippt: "Berlin Pankow"

---

Claude: "Wie groß sollte dein Laden sein?"

[Card 1: 30-50 qm - Gemütlich]
[Card 2: 50-80 qm - Mehr Fläche] ← User wählt
[Card 3: 80-120 qm - Groß]
[Card 4: Andere Größe - Custom]

---

Claude: "Wie teilst du die Fläche auf?"

[Cards mit Optionen...]
```
✅ Nur EINE Frage zur Zeit!
✅ Klare visuelle Auswahl!
✅ Weniger Denk-Aufwand!

---

# 📊 ERFOLGS-METRIKEN

Nach Implementierung sollte:

1. **Completion Rate steigen:**
   - Vorher: ~60% (zu komplex)
   - Nachher: ~85% (einfacher)

2. **Zeit pro Sektion sinken:**
   - Vorher: 45 Min (viele Fragen gleichzeitig)
   - Nachher: 30 Min (schneller durchklicken)

3. **User Satisfaction steigen:**
   - Weniger "das ist zu viel"-Feedback
   - Mehr "das war einfach"-Feedback

4. **GZ-Konformität steigen:**
   - Vorher: 40%
   - Nachher: 80%+ (bessere Erfassung)

---

**WICHTIG:**
1. Lies ZUERST beide Referenzdokumente vollständig
2. Implementiere in der angegebenen Reihenfolge (Phase 1-4)
3. Teste nach jeder Phase
4. Deploy nur wenn alle Tests grün sind

---

**FINAL CHECKLIST BEFORE DEPLOY:**

```bash
✅ Geschäftstyp-Klassifikation funktioniert
✅ Nur 1 Frage auf einmal wird gestellt
✅ Card UI ist implementiert
✅ "Andere" Option überall vorhanden
✅ Text-Generierung produziert konkrete Businesspläne
✅ Typ-spezifische Fragen werden gestellt
✅ Ausgeschlossene Fragen werden übersprungen
✅ Tests sind grün (Backend + Frontend)
✅ Mobile Responsive
✅ Loading States vorhanden
✅ Error Handling implementiert
```

**LOS GEHT'S!** 🚀
