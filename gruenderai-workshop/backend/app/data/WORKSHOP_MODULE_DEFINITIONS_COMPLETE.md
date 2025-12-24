# GRUENDERAI WORKSHOP - VOLLSTÄNDIGE MODULE DEFINITIONEN
# Version: 2.0 - MIT GESCHÄFTSTYP-BRANCHING
# Letzte Aktualisierung: 2025-01-17

---

## 📖 ZWECK DIESES DOKUMENTS

Dieses Dokument ist die **verbindliche Referenz** für alle Workshop-Module und Geschäftstypen.

**Für Claude Code:**
- Definiert exakt WAS in jedem Modul erfasst wird
- Verhindert Überschneidungen zwischen Modulen
- Gibt typ-spezifische Fragenabfolgen vor
- Definiert Validierungsregeln pro Geschäftstyp
- Zeigt wie User-Antworten → BA GZ 04-konformer Text transformiert werden

**Für Entwickler:**
- Klärt Scope und Boundaries jedes Moduls
- Zeigt Branching-Logik basierend auf Geschäftstyp
- Definiert Pflichtfelder pro Typ und Modul
- Gibt System-Prompt-Templates vor

---

## 🎯 WORKSHOP-STRUKTUR ÜBERSICHT

```
Workshop (4-6 Stunden)
│
├─ Modul 1: GESCHÄFTSMODELL (35-45 Min)
│   └─ WAS, FÜR WEN, WARUM, WIE (Preismodell-Idee)
│      ├─ Typ-Klassifikation (Frage 1-2)
│      └─ Typ-spezifische Fragen
│
├─ Modul 2: DEIN UNTERNEHMEN (25-35 Min)
│   └─ WER (Gründerprofil, Qualifikationen, Rechtsform, Standort)
│
├─ Modul 3: MARKT & WETTBEWERB (40-50 Min)
│   └─ WIE GROSS (TAM/SAM/SOM, Konkurrenz, Positionierung)
│
├─ Modul 4: MARKETING & VERTRIEB (30-40 Min)
│   └─ WIE GEWINNEN (Kundenakquise, Kanäle, Erstkunden)
│
├─ Modul 5: FINANZPLANUNG (60-90 Min)
│   └─ RECHNET ES SICH (Kapital, Umsatz, Kosten, Break-Even)
│
├─ Modul 6: SWOT-ANALYSE (30-40 Min)
│   └─ STÄRKEN, SCHWÄCHEN, CHANCEN, RISIKEN
│
└─ Modul 7: MEILENSTEINE & ZEITPLAN (20-30 Min)
    └─ WANN WAS (Timeline, KPIs, Erfolgsmessung)
```

---

---

# 🏗️ GESCHÄFTSTYP-TAXONOMIE

## 📊 HAUPT-KATEGORIEN

```yaml
geschaeftstypen:
  
  typ_1_gastronomie:
    id: "gastronomie"
    label: "☕ Gastronomie"
    beschreibung: "Café, Restaurant, Bar, Imbiss, Food Truck, Catering"
    merkmale:
      - stationaere_raeumlichkeiten: true
      - personal_wahrscheinlich: true
      - gastgewerbe_erlaubnis: true
      - oeffnungszeiten_relevant: true
      - warenlager: true
    beispiele:
      - "Kiez-Café mit Co-Working"
      - "Fine-Dining Restaurant"
      - "Food Truck mit Street Food"
      - "Catering-Service"
  
  typ_2_dienstleistung_lokal:
    id: "dienstleistung_lokal"
    label: "💼 Dienstleistung vor Ort"
    beschreibung: "Friseur, Studio, Werkstatt, Praxis, Atelier"
    merkmale:
      - stationaere_raeumlichkeiten: true
      - personal_moeglich: true
      - terminbasiert: true
      - oeffnungszeiten_relevant: true
      - laufkundschaft: true
    beispiele:
      - "Friseursalon"
      - "Yoga-Studio"
      - "Fahrradwerkstatt"
      - "Tattoo-Studio"
  
  typ_3_dienstleistung_mobil:
    id: "dienstleistung_mobil"
    label: "🚗 Mobiler Service"
    beschreibung: "Handwerker, Mobile Massage, Haushaltsservice"
    merkmale:
      - keine_festen_raeumlichkeiten: true
      - fahrzeug_wichtig: true
      - einsatzradius: true
      - flexible_zeiten: true
      - anfahrt_relevant: true
    beispiele:
      - "Mobiler Friseur"
      - "Handwerker-Service"
      - "Mobile Massage"
      - "Haushaltsauflösung"
  
  typ_4_dienstleistung_online:
    id: "dienstleistung_online"
    label: "💻 Online-Dienstleistung"
    beschreibung: "Beratung, Coaching, SaaS, Online-Kurse"
    merkmale:
      - keine_physischen_raeumlichkeiten: true
      - ortsunabhaengig: true
      - technologie_wichtig: true
      - skalierbar: true
      - internationale_kunden_moeglich: true
    beispiele:
      - "Business-Coaching"
      - "SaaS-Plattform"
      - "Online-Sprachkurse"
      - "Unternehmensberatung (remote)"
  
  typ_5_handel_stationaer:
    id: "handel_stationaer"
    label: "🏪 Laden/Geschäft"
    beschreibung: "Boutique, Einzelhandel, Spezialgeschäft"
    merkmale:
      - stationaere_raeumlichkeiten: true
      - laufkundschaft: true
      - warenlager: true
      - oeffnungszeiten_relevant: true
      - verkaufsflaeche: true
    beispiele:
      - "Mode-Boutique"
      - "Unverpackt-Laden"
      - "Buchhandlung"
      - "Feinkostgeschäft"
  
  typ_6_handel_online:
    id: "handel_online"
    label: "📦 Online-Shop"
    beschreibung: "E-Commerce, Dropshipping, Amazon FBA"
    merkmale:
      - keine_physische_verkaufsflaeche: true
      - lager_oder_dropshipping: true
      - versandlogistik: true
      - shop_plattform: true
      - 24_7_verfuegbar: true
    beispiele:
      - "Fashion E-Commerce"
      - "Dropshipping-Shop"
      - "Amazon FBA Business"
      - "Etsy-Shop (Handmade)"
  
  typ_7_produktion:
    id: "produktion"
    label: "🏭 Produktion/Manufaktur"
    beschreibung: "Werkstatt, Manufaktur, Handwerk"
    merkmale:
      - produktionsraeume: true
      - maschinen_ausstattung: true
      - lagerflaeche: true
      - materialkosten: true
      - produktionszeit: true
    beispiele:
      - "Schmuck-Manufaktur"
      - "Schreinerei"
      - "Craft Beer Brauerei"
      - "Seifenmanufaktur"
  
  typ_8_hybrid:
    id: "hybrid"
    label: "🔄 Hybrid"
    beschreibung: "Kombination aus Online + Offline"
    merkmale:
      - mehrere_kanaele: true
      - komplexer: true
      - flexible_struktur: true
    beispiele:
      - "Laden + Online-Shop"
      - "Beratung vor Ort + Online"
      - "Restaurant + Catering + Lieferdienst"
```

---

---

# 📦 MODUL 1: GESCHÄFTSMODELL (MIT BRANCHING)

## 🎯 MODUL-ZIEL

Erfasse die **Kernidee** des Geschäfts:
- **WAS** wird angeboten?
- **FÜR WEN** ist es gedacht?
- **WARUM** sollten Kunden hier kaufen?
- **WIE** wird Geld verdient (Grundkonzept)?

## 🚫 WAS NICHT IN MODUL 1 GEHÖRT

| Gehört NICHT hierher | Richtige Sektion |
|---------------------|------------------|
| Finanzielle Berechnungen (Break-Even, ROI) | Modul 5: Finanzplanung |
| Marktgrößen-Berechnungen (TAM/SAM/SOM) | Modul 3: Markt & Wettbewerb |
| Detaillierte Kosten (Miete, Personal, Waren) | Modul 5: Finanzplanung |
| Gründerprofil & Qualifikationen | Modul 2: Dein Unternehmen |
| Marketing-Kanäle & Kampagnen | Modul 4: Marketing & Vertrieb |
| Konkurrenz-Analyse mit Zahlen | Modul 3: Markt & Wettbewerb |
| SWOT-Analyse | Modul 6: SWOT |
| Zeitplan & Meilensteine | Modul 7: Meilensteine |

---

## 🔀 GESCHÄFTSTYP-KLASSIFIKATION (FRAGE 1-2)

### Frage 1: Hauptkategorie (IMMER ERSTE FRAGE!)

```yaml
frage_1_geschaeftstyp:
  text: |
    Willkommen beim GründerAI Businessplan-Workshop!
    
    Bevor wir loslegen: Welche Art von Geschäft planst du?
    
    (Das hilft mir, dir die richtigen Fragen zu stellen)
  
  typ: "single_choice"
  
  optionen:
    - value: "gastronomie"
      label: "☕ Gastronomie (Café, Restaurant, Bar, Imbiss)"
      
    - value: "dienstleistung_lokal"
      label: "💼 Dienstleistung vor Ort (Friseur, Studio, Werkstatt)"
      
    - value: "dienstleistung_mobil"
      label: "🚗 Mobiler Service (Handwerker, Pflege, Mobile Massage)"
      
    - value: "dienstleistung_online"
      label: "💻 Online-Dienstleistung (Beratung, SaaS, Coaching)"
      
    - value: "handel_stationaer"
      label: "🏪 Laden/Geschäft (Boutique, Einzelhandel)"
      
    - value: "handel_online"
      label: "📦 Online-Shop (E-Commerce, Dropshipping)"
      
    - value: "produktion"
      label: "🏭 Produktion/Manufaktur (Werkstatt, Handwerk)"
      
    - value: "hybrid"
      label: "🔄 Hybrid (Mehrere Bereiche kombiniert)"
  
  validation:
    required: true
  
  next_step: "frage_2_subtyp"
```

### Frage 2: Subtyp (Typ-spezifisch)

```yaml
frage_2_subtyp:
  gastronomie:
    text: "Welche Art von Gastronomie genau?"
    optionen:
      - value: "cafe"
        label: "Café/Coffeeshop"
      - value: "restaurant"
        label: "Restaurant (Vollgastronomie)"
      - value: "bar_club"
        label: "Bar/Club"
      - value: "imbiss"
        label: "Imbiss/Schnellrestaurant"
      - value: "food_truck"
        label: "Food Truck/Mobil"
      - value: "catering"
        label: "Catering-Service"
  
  dienstleistung_online:
    text: "Welche Art von Online-Dienstleistung?"
    optionen:
      - value: "beratung"
        label: "Unternehmensberatung"
      - value: "coaching"
        label: "Business/Life Coaching"
      - value: "saas"
        label: "Software-as-a-Service (SaaS)"
      - value: "online_kurse"
        label: "Online-Kurse/E-Learning"
      - value: "kreativ"
        label: "Kreativdienstleistung (Design, Text, etc.)"
  
  handel_online:
    text: "Welches E-Commerce-Modell?"
    optionen:
      - value: "eigener_shop"
        label: "Eigener Online-Shop"
      - value: "marketplace"
        label: "Amazon/eBay/Etsy"
      - value: "dropshipping"
        label: "Dropshipping"
      - value: "print_on_demand"
        label: "Print-on-Demand"
  
  # ... weitere Subtypen
```

---

---

## 📋 TYP 1: GASTRONOMIE

### ✅ Pflichtfelder

```yaml
gastronomie_pflichtfelder:
  kern:
    - geschaeftsidee_kurz          # 1-2 Sätze
    - gastro_subtyp                # Café/Restaurant/Bar/etc.
    - konzept_typ                  # Quick Service / Sit-Down / Hybrid
    - standort_konkret             # Straße, Kiez, Stadt
    
  raeumlichkeiten:
    - raeumlichkeiten_status       # Gefunden/In Suche/Noch offen
    - groesse_qm                   # Geschätzte Größe
    - sitzplaetze_innen            # Anzahl
    - sitzplaetze_aussen           # Optional, wichtig für Kapazität
    - raumaufteilung               # Beschreibung (Vorne/Hinten/Etagen)
    - kueche_groesse               # Klein/Mittel/Groß/Keine (bei Café)
    - barrierefreiheit             # Ja/Nein/Teilweise
    
  betriebszeiten:
    - oeffnungszeiten              # Mo-So, Uhrzeiten
    - ruhetage                     # Welche Tage?
    - tageszeit_fokus              # Frühstück/Mittag/Abend/Ganztags
    - durchschnittliche_verweildauer # Wichtig für Kapazitätsplanung
    
  angebot:
    - produktpalette               # Was wird angeboten?
    - speisekarte_umfang           # Klein (<10 Gerichte) / Mittel / Groß
    - produktionsweise             # Selbst/Zulieferung/Hybrid
    - besonderheiten               # Spezielle Ausstattung (z.B. Röstmaschine)
    - alkohol_geplant              # Ja/Nein (Schankerlaubnis!)
    - aussenverkauf                # To-Go/Lieferdienst/Keins
    
  zielgruppen:
    - zielgruppe_primaer           # Hauptkunden mit Details
    - zielgruppe_sekundaer         # Zweite Gruppe
    - kundenbeduerfnis             # Was brauchen sie?
    
  alleinstellungsmerkmal:
    - usp                          # Was macht dich einzigartig?
    - marktluecke                  # Welches Problem löst du?
    - abgrenzung                   # Wovon grenzt du dich ab?
    
  preismodell:
    - preismodell_typ              # À la carte / Flatrate / Hybrid
    - preis_hauptprodukt           # Z.B. "Cappuccino: 3,50€"
    - durchschnittlicher_bon       # Geschätzt
    - preispositionierung          # Budget/Mittel/Premium
    
  regulierung:
    - gastgewerbe_erlaubnis_status # Geplant/In Beantragung/Vorhanden
    - hygiene_schulung_status      # Geplant/Absolviert
    - schankerlaubnis_benoetigt    # Ja/Nein
```

### ❌ Ausgeschlossene Fragen (für Gastronomie)

```yaml
gastronomie_excluded_questions:
  - einsatzradius_km              # Irrelevant für stationär
  - mobile_ausstattung            # Irrelevant
  - fahrzeug_typ                  # Irrelevant (außer Food Truck)
  - delivery_methode              # Hat eigenes Konzept (Dine-in/To-Go)
  - tools_geplant                 # Irrelevant (keine Software)
  - shop_plattform                # Irrelevant
  - versandlogistik               # Irrelevant
  - produktionszeit_pro_einheit   # Zu detailliert für Modul 1
  - zielmarkt_international       # Gastro ist lokal
```

### 📝 Fragenabfolge Gastronomie

```yaml
fragenabfolge_gastronomie:
  
  block_1_geschaeftsidee:
    frage_1:
      id: "geschaeftsidee_kurz"
      text: "Beschreibe deine Geschäftsidee in 1-2 Sätzen"
      typ: "open_text"
      beispiele:
        - "Kiez-Café mit Co-Working-Ecke in Neukölln"
        - "Fine-Dining Restaurant mit regionaler Küche"
        - "Food Truck mit asiatischer Streetfood"
    
    frage_2:
      id: "konzept_typ"
      text: "Welcher Service-Typ passt am besten?"
      typ: "single_choice"
      optionen:
        - value: "quick_service"
          label: "Quick Service (schnell, To-Go-fokussiert)"
          beispiel: "Imbiss, Coffee-Bar"
        - value: "sit_down"
          label: "Sit-Down (Gäste verweilen länger)"
          beispiel: "Restaurant, gemütliches Café"
        - value: "hybrid"
          label: "Hybrid (beide Konzepte)"
          beispiel: "Café mit To-Go + Sitzplätzen"
    
    frage_3:
      id: "standort_konkret"
      text: "Wo genau planst du dein {gastro_subtyp}?"
      typ: "open_text"
      validation:
        min_length: 10
        must_contain_city: true
      hint: |
        Für Gastronomie ist die Lage KRITISCH!
        Bitte so konkret wie möglich:
        - Straße/Kiez: "Weserstraße, Neukölln"
        - Viertel/Bezirk: "Prenzlauer Berg, nähe Kollwitzplatz"
        - Stadt: Falls noch unsicher, mindestens Stadt angeben
  
  block_2_raeumlichkeiten:
    intro: |
      Jetzt zu den Räumlichkeiten. Auch wenn du noch nicht konkret suchst,
      brauche ich eine Größenordnung für die Planung.
    
    frage_4:
      id: "raeumlichkeiten_status"
      text: "Wie weit bist du bei der Raumsuche?"
      typ: "single_choice"
      optionen:
        - value: "gefunden"
          label: "Ich habe bereits Räume gefunden"
          followup: "raeumlichkeiten_details_konkret"
        - value: "in_suche"
          label: "Ich suche aktiv"
          followup: "raeumlichkeiten_details_schaetzung"
        - value: "noch_offen"
          label: "Noch offen, ich plane erst"
          followup: "raeumlichkeiten_details_schaetzung"
    
    frage_5:
      id: "groesse_qm"
      text: "Wie groß sollten deine Räume sein?"
      typ: "single_choice_with_custom"
      optionen:
        - value: "40-60"
          label: "40-60 qm (klein & gemütlich)"
          kapazitaet: "~15-20 Gäste"
        - value: "70-100"
          label: "70-100 qm (mittel)"
          kapazitaet: "~25-35 Gäste"
        - value: "100-150"
          label: "100-150 qm (groß)"
          kapazitaet: "~40-60 Gäste"
        - value: "150+"
          label: "150+ qm (sehr groß)"
          kapazitaet: "60+ Gäste"
      hint: "Die Größe bestimmt Kapazität, Miete und Personal-Bedarf"
    
    frage_6:
      id: "sitzplaetze_innen"
      text: "Wie viele Sitzplätze im Innenbereich?"
      typ: "number_input"
      validation:
        min: 5
        max: 200
        plausibility_check: |
          Check gegen qm: ~1,5-2 qm pro Sitzplatz sind realistisch
          Falls Diskrepanz → Hinweis geben
    
    frage_7:
      id: "sitzplaetze_aussen"
      text: "Gibt es eine Außen-/Terrassenfläche?"
      typ: "conditional"
      optionen:
        - value: "ja"
          label: "Ja"
          followup: "Wie viele Außenplätze? (Zahl)"
        - value: "nein"
          label: "Nein"
        - value: "geplant"
          label: "Geplant/Möglich"
          followup: "Wie viele Außenplätze angestrebt? (Zahl)"
    
    frage_8:
      id: "raumaufteilung"
      text: "Wie stellst du dir die Raumaufteilung vor?"
      typ: "open_text"
      beispiele:
        - "Vorne: Café-Bereich, Hinten: Küche + Lager"
        - "Erdgeschoss: Gastraum, Keller: Küche + Kühlraum"
        - "Offenes Konzept: Küche sichtbar, Sitzbereich drumherum"
      hint: |
        Beschreibe grob die funktionale Aufteilung:
        - Wo ist der Gästebereich?
        - Wo Küche/Theke?
        - Gibt es Nebenräume? (Lager, Toiletten, Büro)
  
  block_3_betriebszeiten:
    intro: "Lass uns über deinen Betriebsablauf sprechen."
    
    frage_9:
      id: "oeffnungszeiten"
      text: "Welche Öffnungszeiten planst du?"
      typ: "structured_input"
      format: |
        Bitte gib an:
        Mo-Fr: [Uhrzeit] - [Uhrzeit]
        Sa: [Uhrzeit] - [Uhrzeit]
        So: [Uhrzeit] - [Uhrzeit]
        
        Oder wähle Vorlage:
      vorlagen:
        - label: "Klassisch (Café): 8-18 Uhr, Mo-Sa"
          value: "mo_fr: 08:00-18:00, sa: 09:00-18:00, so: geschlossen"
        - label: "Extended (Gastro): 11-23 Uhr, 7 Tage"
          value: "mo_so: 11:00-23:00"
        - label: "Frühstart (To-Go): 7-20 Uhr, Mo-Fr"
          value: "mo_fr: 07:00-20:00, sa: 09:00-18:00, so: geschlossen"
    
    frage_10:
      id: "ruhetage"
      text: "Hast du Ruhetage?"
      typ: "multiple_choice"
      optionen:
        - "Montag"
        - "Dienstag"
        - "Sonntag"
        - "Keine (7 Tage/Woche)"
        - "Andere: ___"
    
    frage_11:
      id: "tageszeit_fokus"
      text: "Auf welche Tageszeit fokussierst du dich?"
      typ: "multiple_choice"
      optionen:
        - value: "fruehstueck"
          label: "Frühstück (7-11 Uhr)"
        - value: "mittag"
          label: "Mittagsgeschäft (11-15 Uhr)"
        - value: "nachmittag"
          label: "Nachmittag/Kaffee (15-18 Uhr)"
        - value: "abend"
          label: "Abendgeschäft (18-23 Uhr)"
        - value: "ganztags"
          label: "Ganztags gleichmäßig"
      allow_multiple: true
  
  block_4_angebot:
    frage_12:
      id: "produktpalette"
      text: "Was genau bietest du an?"
      typ: "checklist_with_details"
      kategorien:
        kaffee_getraenke:
          label: "Kaffee & Getränke"
          optionen:
            - "Spezialitätenkaffee (Flat White, V60, etc.)"
            - "Standardkaffee (Espresso, Cappuccino)"
            - "Tee-Auswahl"
            - "Smoothies/Säfte"
            - "Softdrinks"
            - "Alkoholische Getränke"
        
        essen:
          label: "Essen"
          optionen:
            - "Frühstück"
            - "Mittagstisch/Hauptgerichte"
            - "Gebäck/Kuchen"
            - "Snacks/Sandwiches"
            - "Salate"
            - "Desserts"
      
      followup: "Beschreibe kurz dein Angebot (2-3 Sätze)"
    
    frage_13:
      id: "speisekarte_umfang"
      text: "Wie umfangreich ist deine Speisekarte?"
      typ: "single_choice"
      optionen:
        - value: "klein"
          label: "Klein (unter 10 Positionen)"
          beispiel: "Coffee Bar mit Gebäck"
        - value: "mittel"
          label: "Mittel (10-30 Positionen)"
          beispiel: "Café mit Frühstück + Mittagstisch"
        - value: "gross"
          label: "Groß (30+ Positionen)"
          beispiel: "Restaurant mit mehreren Gängen"
    
    frage_14:
      id: "produktionsweise"
      text: "Wie produzierst du dein Angebot?"
      typ: "single_choice"
      optionen:
        - value: "selbst"
          label: "Alles selbst gemacht (eigene Küche)"
        - value: "zulieferung"
          label: "Hauptsächlich Zulieferung (Bäcker, Großküche)"
        - value: "hybrid"
          label: "Hybrid (Teils selbst, teils Zulieferung)"
      hint: "Wichtig für Küchen-Ausstattung und Personal"
    
    frage_15:
      id: "alkohol_geplant"
      text: "Planst du Alkohol auszuschenken?"
      typ: "single_choice"
      optionen:
        - value: "ja"
          label: "Ja"
          hinweis: "⚠️ Schankerlaubnis erforderlich!"
        - value: "nein"
          label: "Nein"
        - value: "spaeter"
          label: "Erstmal nicht, vielleicht später"
  
  block_5_zielgruppen:
    frage_16:
      id: "zielgruppen_hauptgruppen"
      text: "WER sind deine Hauptkunden? (2-3 Gruppen)"
      typ: "multiple_choice_with_details"
      optionen:
        - label: "Anwohner/Nachbarschaft"
          followup: "Welche? (Familien, Studenten, Rentner, Young Professionals)"
        - label: "Berufstätige/Office-Worker"
          followup: "Mittagspause? Frühstück? After-Work?"
        - label: "Durchgangsverkehr (U-Bahn, Bahnhof)"
          followup: "Hauptsächlich To-Go?"
        - label: "Touristen"
          followup: "Welche Art? (Städtereise, Business, etc.)"
        - label: "Spezielle Nische"
          followup: "Beschreibe sie genau"
      
      min_auswahl: 1
      max_auswahl: 3
    
    frage_17:
      id: "zielgruppe_details"
      text: "Beschreibe deine HAUPT-Zielgruppe genauer"
      typ: "guided_text"
      template: |
        Beantworte für deine wichtigste Zielgruppe:
        
        1. Demografie: Alter, Beruf, Einkommen, Wohnort
        2. Bedürfnis: Welches Problem/Bedürfnis hast du?
        3. Verhalten: Wann/wie oft kommen sie? Wie lange bleiben sie?
        4. Ausgabebereitschaft: Was geben sie durchschnittlich aus?
      
      beispiel: |
        Beispiel:
        1. Freelancer, 28-45 Jahre, Designer/Entwickler, Berlin-Mitte
        2. Brauchen Arbeitsplatz außerhalb Wohnung + guten Kaffee
        3. 3-4x/Woche, 9-17 Uhr, bleiben 4-6 Stunden
        4. 15-25€/Tag (Kaffee + Essen)
  
  block_6_usp:
    frage_18:
      id: "marktluecke_eigene_beobachtung"
      text: "Was hat DIR in bestehenden Angeboten gefehlt?"
      typ: "open_text"
      hint: |
        Die besten Geschäftsideen kommen aus eigener Frustration!
        
        Denk an deine Erfahrungen:
        - Was war nervig/unbefriedigend?
        - Was hast du dir gewünscht?
        - Was machen andere falsch?
    
    frage_19:
      id: "usp_formulierung"
      text: "Was macht DICH einzigartig?"
      typ: "structured_sentence"
      template: |
        Vervollständige diesen Satz:
        
        "Im Gegensatz zu [Konkurrent/Alternative] bin ich der/die 
        Einzige, der/die [dein USP], was für Kunden bedeutet [Vorteil]."
      
      beispiel: |
        "Im Gegensatz zu Starbucks (will Dauersitzer nicht) und WeWork 
        (zu teuer) bin ich das einzige Café, das explizit Co-Working 
        zum Café-Preis anbietet, was Freelancern flexible, günstige 
        Arbeitsplätze mit Premium-Kaffee ermöglicht."
      
      validation:
        must_mention_konkurrent: true
        must_mention_vorteil: true
  
  block_7_preismodell:
    frage_20:
      id: "preismodell_typ"
      text: "Welches Preismodell passt zu dir?"
      typ: "single_choice"
      optionen:
        - value: "a_la_carte"
          label: "À la carte (jedes Produkt einzeln bezahlt)"
        - value: "flatrate"
          label: "Flatrate/Abo (Pauschalpreis für Zeitraum)"
          beispiel: "Membership für Coworking"
        - value: "hybrid"
          label: "Hybrid (Kombination)"
          beispiel: "Abo für Stammkunden + Einzelpreise für Laufkundschaft"
    
    frage_21:
      id: "hauptprodukt_preise"
      text: "Was kosten deine Hauptprodukte?"
      typ: "price_list"
      format: |
        Gib mindestens 3-5 Preisbeispiele:
        
        Produkt: Preis
        Cappuccino: 3,50€
        Frühstück: 8,90€
        Mittagstisch: 12,50€
      
      validation:
        min_entries: 3
        must_contain_euro_symbol: true
    
    frage_22:
      id: "durchschnittlicher_bon"
      text: "Was gibt ein typischer Kunde bei dir aus?"
      typ: "number_input_with_context"
      unit: "€"
      examples:
        - "Schneller Kaffee To-Go: 3-5€"
        - "Frühstück mit Kaffee: 10-15€"
        - "Mittag + Getränk: 15-20€"
        - "Abendessen mit Wein: 30-50€"
      
      validation:
        min: 2
        max: 200
        plausibility_check: true
    
    frage_23:
      id: "preispositionierung"
      text: "Wie positionierst du dich preislich im Vergleich zur Konkurrenz?"
      typ: "single_choice"
      optionen:
        - value: "budget"
          label: "Budget (günstiger als Durchschnitt)"
        - value: "mittelklasse"
          label: "Mittelklasse (Marktdurchschnitt)"
        - value: "premium"
          label: "Premium (teurer, aber höhere Qualität)"
```

### 📄 Text-Generierung Template: Gastronomie

```markdown
## 2. GESCHÄFTSMODELL

### 2.1 Geschäftsidee und Konzept

{geschaeftsidee_kurz}

Das geplante {gastro_subtyp} verfolgt ein {konzept_typ}-Konzept und 
richtet sich an {zielgruppe_primaer} sowie {zielgruppe_sekundaer}.

**Standort:**
{standort_konkret}

Die Wahl dieses Standorts begründet sich durch {standort_begruendung}.

**Räumlichkeiten:**
Die geplanten Räumlichkeiten umfassen ca. {groesse_qm} qm mit 
{sitzplaetze_innen} Innenplätzen{if sitzplaetze_aussen} und 
{sitzplaetze_aussen} Außenplätzen{endif}.

**Raumaufteilung:**
{raumaufteilung}

Diese Aufteilung ermöglicht {raumaufteilung_vorteil}.

### 2.2 Angebotsbeschreibung

**Produktpalette:**
{produktpalette_beschreibung}

**Produktionsweise:**
{produktionsweise_text}

**Speisekarte:**
{speisekarte_umfang_text} mit Fokus auf {tageszeit_fokus}.

{if alkohol_geplant}
**Getränkekonzept:**
Neben Kaffee und alkoholfreien Getränken ist auch der Ausschank von 
Alkohol geplant (Schankerlaubnis wird beantragt).
{endif}

### 2.3 Betriebskonzept

**Öffnungszeiten:**
{oeffnungszeiten_formatiert}

**Ruhetage:** {ruhetage}

{if durchschnittliche_verweildauer}
Die durchschnittliche Verweildauer der Gäste wird auf 
{durchschnittliche_verweildauer} geschätzt, was bei voller Auslastung 
eine Tischrotation von {tischrotation} Durchgängen pro Tag ermöglicht.
{endif}

### 2.4 Zielgruppen

**Primäre Zielgruppe: {zielgruppe_primaer_titel}**

{zielgruppe_primaer_demografie}

**Bedürfnis:** {kundenbeduerfnis_primaer}

**Verhalten:** {zielgruppe_primaer_verhalten}

**Ausgabebereitschaft:** {zielgruppe_primaer_ausgaben}

{if zielgruppe_sekundaer}
**Sekundäre Zielgruppe: {zielgruppe_sekundaer_titel}**

{zielgruppe_sekundaer_beschreibung}
{endif}

### 2.5 Alleinstellungsmerkmale

**Identifizierte Marktlücke:**
{marktluecke_beschreibung}

**Lösung und USP:**
{usp_formulierung}

**Konkrete Vorteile für Kunden:**
{usp_vorteile_liste}

**Abgrenzung zur Konkurrenz:**
{abgrenzung_text}

### 2.6 Preismodell und Umsatzstruktur

**Preisstrategie:**
Das Geschäft nutzt ein {preismodell_typ}-Modell.

**Preisgestaltung:**

{hauptprodukt_preise_tabelle}

**Durchschnittlicher Bon:** {durchschnittlicher_bon}€

**Preispositionierung:**
Das Preisniveau bewegt sich im {preispositionierung}-Segment des 
lokalen Marktes. {preispositionierung_begruendung}

### 2.7 Rechtliche Anforderungen

Für den Betrieb des {gastro_subtyp} sind folgende Genehmigungen erforderlich:
- Gastgewerbeerlaubnis (§ 1 GastG): {gastgewerbe_erlaubnis_status}
- Hygienebelehrung nach § 43 IfSG: {hygiene_schulung_status}
{if schankerlaubnis_benoetigt}
- Schankerlaubnis für Alkohol: {schankerlaubnis_status}
{endif}
```

---

---

## 📋 TYP 2: DIENSTLEISTUNG ONLINE

### ✅ Pflichtfelder

```yaml
dienstleistung_online_pflichtfelder:
  kern:
    - geschaeftsidee_kurz
    - dienstleistungstyp          # Beratung/SaaS/Coaching/Kreativ
    - spezialisierung             # Nische
    - zielmarkt                   # Deutschland/Europa/Global
    
  dienstleistung:
    - beratungsformat             # 1:1 / Gruppe / Hybrid
    - delivery_methode            # Video-Call / Async / Vor-Ort / Hybrid
    - session_dauer               # Typische Dauer einer Session
    - paket_struktur              # Einzelsession / Pakete / Abo
    
  plattform_technologie:
    - plattform_typ               # Eigene Website / Marketplace / Beides
    - hauptplattformen            # z.B. "Eigene Website + LinkedIn"
    - tools_geplant               # Zoom, Calendly, CRM, etc.
    - technische_voraussetzungen  # Was brauchst du?
    
  kapazitaet_skalierung:
    - max_kunden_pro_monat        # Realistisch schätzbar?
    - max_stunden_pro_woche       # Arbeitszeit-Budget
    - automatisierung_geplant     # Online-Kurse, Templates, etc.
    - skalierbarkeit_strategie    # Wie wächst du?
    
  zielgruppen:
    - zielgruppe_primaer
    - zielgruppe_industrie        # Welche Branchen?
    - kundenbeduerfnis
    - customer_pain_point         # Spezifisches Problem
    
  alleinstellungsmerkmal:
    - usp
    - marktluecke
    - abgrenzung
    - proof_of_concept            # Erste Projekte/Testimonials?
    
  preismodell:
    - preismodell_typ             # Stundensatz/Projekt/Retainer/Abo
    - preis_hauptprodukt          # z.B. "1-Stunden-Session: 150€"
    - pricing_strategie           # Value-based/Time-based/Hybrid
    - durchschnittsprojekt_wert   # Geschätzt
```

### ❌ Ausgeschlossene Fragen

```yaml
dienstleistung_online_excluded:
  - groesse_qm                    # Keine physischen Räume!
  - sitzplaetze                   # Irrelevant
  - oeffnungszeiten               # Flexibel nach Termin
  - standort_konkret              # Nur Firmensitz (Modul 2)
  - raumaufteilung                # Irrelevant
  - gastgewerbe_erlaubnis         # Irrelevant
  - warenlager                    # Keine physischen Produkte
  - durchgangsverkehr             # Kein Laufpublikum
  - sitzplaetze_aussen            # Irrelevant
  - kueche_groesse                # Irrelevant
  - parkplaetze                   # Irrelevant
```

### 📝 Fragenabfolge Online-Dienstleistung

```yaml
fragenabfolge_online_dienstleistung:
  
  block_1_geschaeftsidee:
    frage_1:
      id: "geschaeftsidee_kurz"
      text: "Beschreibe deine Online-Dienstleistung in 1-2 Sätzen"
      beispiele:
        - "Business-Coaching für Tech-Gründer in der Seed-Phase"
        - "SEO-Beratung für lokale Handwerksbetriebe"
        - "Online-Sprachkurse für Business-Englisch mit KI-Feedback"
    
    frage_2:
      id: "spezialisierung"
      text: "Auf welche Nische spezialisierst du dich?"
      typ: "open_text"
      hint: |
        Je spezifischer, desto besser!
        
        Nicht gut: "Unternehmensberatung"
        Gut: "Go-to-Market Strategie für B2B SaaS Startups"
        
        Nicht gut: "Coaching"
        Gut: "Leadership-Coaching für weibliche Führungskräfte in Tech"
    
    frage_3:
      id: "zielmarkt"
      text: "Wo sind deine Kunden?"
      typ: "single_choice"
      optionen:
        - value: "deutschland"
          label: "Hauptsächlich Deutschland"
        - value: "dach"
          label: "DACH-Region (D-A-CH)"
        - value: "europa"
          label: "Europa"
        - value: "global"
          label: "Global/International"
      
      followup_if_global: |
        "Arbeitest du mit verschiedenen Zeitzonen?"
        → Wichtig für Kapazitätsplanung!
  
  block_2_delivery_methode:
    intro: |
      Lass uns klären WIE du deine Dienstleistung lieferst.
      (Das ersetzt die "Räumlichkeiten"-Fragen!)
    
    frage_4:
      id: "beratungsformat"
      text: "In welchem Format bietest du deine Dienstleistung an?"
      typ: "single_choice"
      optionen:
        - value: "1_zu_1"
          label: "Nur 1:1 (Einzelpersonen)"
        - value: "gruppe"
          label: "Nur Gruppen/Workshops"
        - value: "hybrid"
          label: "Beides (1:1 und Gruppen)"
    
    frage_5:
      id: "delivery_methode"
      text: "WIE lieferst du die Dienstleistung?"
      typ: "multiple_choice"
      optionen:
        - value: "video_live"
          label: "Live Video-Calls (Zoom, Teams, etc.)"
        - value: "async"
          label: "Asynchron (Email, Loom, Voice Notes)"
        - value: "vor_ort"
          label: "Persönlich vor Ort (beim Kunden)"
        - value: "selbstlern"
          label: "Selbstlern-Kurse/Materialien"
      
      allow_multiple: true
      hint: "Du kannst mehrere Methoden kombinieren"
    
    frage_6:
      id: "session_dauer"
      text: "Wie lange dauert eine typische Session/ein Call?"
      typ: "single_choice_with_custom"
      optionen:
        - "30 Minuten"
        - "45 Minuten"
        - "60 Minuten (1 Stunde)"
        - "90 Minuten"
        - "2 Stunden"
        - "Halbtags-Workshop (4h)"
        - "Ganztags-Workshop (8h)"
        - "Andere: ___"
    
    frage_7:
      id: "paket_struktur"
      text: "Wie strukturierst du dein Angebot?"
      typ: "single_choice"
      optionen:
        - value: "einzelsession"
          label: "Einzelne Sessions (Kunden buchen pro Session)"
        - value: "pakete"
          label: "Pakete (z.B. 5er/10er-Pack)"
        - value: "programm"
          label: "Feste Programme (z.B. '12-Wochen-Programm')"
        - value: "retainer"
          label: "Retainer/Monatspauschale"
        - value: "abo"
          label: "Abo-Modell (monatlich kündbar)"
  
  block_3_plattform_tools:
    frage_8:
      id: "plattform_typ"
      text: "Wo findest du deine Kunden?"
      typ: "multiple_choice"
      optionen:
        - value: "eigene_website"
          label: "Eigene Website"
        - value: "linkedin"
          label: "LinkedIn"
        - value: "marketplace"
          label: "Marketplace (Upwork, Fiverr, etc.)"
        - value: "empfehlungen"
          label: "Nur Empfehlungen/Netzwerk"
        - value: "andere"
          label: "Andere: ___"
      
      allow_multiple: true
    
    frage_9:
      id: "tools_geplant"
      text: "Welche Tools/Software brauchst du für deinen Betrieb?"
      typ: "checklist"
      kategorien:
        kommunikation:
          - "Zoom/Teams (Video-Calls)"
          - "Slack/Discord (Chat)"
          - "Email-Tool (Gmail, Outlook)"
        
        terminierung:
          - "Calendly/Acuity (Buchungstool)"
          - "Google Calendar"
        
        zahlung:
          - "Stripe/PayPal (Payment)"
          - "Rechnungstool (Lexoffice, sevDesk)"
        
        crm_projekt:
          - "CRM (HubSpot, Pipedrive)"
          - "Projektmanagement (Asana, Notion)"
        
        content:
          - "Website (Wordpress, Webflow)"
          - "Email-Marketing (Mailchimp)"
        
        andere:
          - "Andere: ___"
    
    frage_10:
      id: "technische_voraussetzungen"
      text: "Was brauchst du technisch für den Start?"
      typ: "open_text"
      beispiel: |
        z.B.:
        - Laptop mit Webcam
        - Professionelles Mikrofon
        - Ruhiger Raum für Calls
        - Stabile Internetverbindung (50 Mbit+)
        - Zweiter Monitor für Screen-Sharing
  
  block_4_kapazitaet_skalierung:
    intro: |
      Wichtig für Online-Dienstleistung: Kapazitätsgrenzen verstehen!
    
    frage_11:
      id: "max_stunden_pro_woche"
      text: "Wie viele Stunden kannst/willst du pro Woche arbeiten?"
      typ: "number_input_with_slider"
      range: [10, 60]
      default: 40
      hint: |
        Bedenke: Nicht nur Client-Calls, sondern auch:
        - Vorbereitung
        - Nachbereitung
        - Marketing/Akquise
        - Admin/Buchhaltung
    
    frage_12:
      id: "max_kunden_parallel"
      text: "Wie viele Kunden kannst du parallel betreuen?"
      typ: "number_input"
      hint: |
        Denk an:
        - Wie viel Zeit braucht jeder Kunde?
        - Wie oft treffen/kontakten?
        - Wie viel Vorbereitung/Nachbereitung?
      
      validation:
        plausibility_check: |
          Check gegen max_stunden_pro_woche:
          Wenn 40h/Woche und 10 Kunden → 4h pro Kunde
          Wenn Session nur 1h → Rest für Prep/Nachber ok?
          Wenn Session 1h aber keine Zeit für Prep → Warnung!
    
    frage_13:
      id: "automatisierung_geplant"
      text: "Planst du dein Angebot zu automatisieren/skalieren?"
      typ: "single_choice"
      optionen:
        - value: "nein"
          label: "Nein, ich bleibe bei 1:1 Dienstleistung"
        - value: "spaeter"
          label: "Ja, aber erst später (nach 1-2 Jahren)"
        - value: "von_anfang_an"
          label: "Ja, von Anfang an parallel aufbauen"
      
      followup_if_ja:
        text: "Was genau planst du? (Mehrfachauswahl)"
        optionen:
          - "Online-Kurse (aufgezeichnet)"
          - "Gruppen-Programme statt 1:1"
          - "Templates/Vorlagen verkaufen"
          - "Software/Tool entwickeln"
          - "Andere: ___"
  
  block_5_zielgruppen:
    frage_14:
      id: "zielgruppe_primaer"
      text: "WER ist dein idealer Kunde? (So spezifisch wie möglich!)"
      typ: "guided_text"
      template: |
        1. Titel/Rolle: (z.B. "Startup-Gründer", "HR-Manager")
        2. Unternehmensgröße: (z.B. "5-50 MA", "Konzern 1000+")
        3. Branche: (z.B. "Tech/SaaS", "Handel", "Gesundheit")
        4. Problem/Pain: (Was hält sie nachts wach?)
        5. Budget: (Was können sie ausgeben?)
      
      beispiel: |
        1. Titel: Tech-Startup-Gründer (CEO/CTO)
        2. Größe: Pre-Seed bis Series A (3-15 Mitarbeiter)
        3. Branche: B2B SaaS
        4. Problem: Produkt fertig, aber keine GTM-Strategie. Wissen nicht wie ersten Kunden gewinnen
        5. Budget: 2.000-5.000€ für 3-Monats-Programm
    
    frage_15:
      id: "customer_pain_point"
      text: "Was ist DAS zentrale Problem deiner Kunden?"
      typ: "open_text"
      hint: |
        Nicht technisch, sondern emotional:
        
        Statt: "Keine Marketing-Strategie"
        Besser: "Angst, Geld in die falsche Marketing-Maßnahme zu stecken"
        
        Statt: "Schlechtes Zeitmanagement"
        Besser: "Gefühl, den ganzen Tag beschäftigt aber nichts geschafft zu haben"
  
  block_6_usp:
    frage_16:
      id: "usp_formulierung"
      text: "Was macht DICH als Berater/Coach/Dienstleister einzigartig?"
      typ: "structured_sentence"
      template: |
        "Im Gegensatz zu [andere Berater/Coaches] bin ich der/die 
        Einzige, der/die [dein USP], was für Kunden bedeutet [Vorteil]."
      
      beispiel: |
        "Im Gegensatz zu klassischen Unternehmensberatern (teuer, abstrakt) 
        bin ich der einzige Ex-Startup-CTO, der technische und kommerzielle 
        Go-to-Market-Strategie kombiniert, was Tech-Gründern ermöglicht, 
        sowohl Produkt als auch Vertrieb zu optimieren."
    
    frage_17:
      id: "proof_of_concept"
      text: "Hast du bereits erste Kunden/Projekte/Testimonials?"
      typ: "conditional"
      optionen:
        - value: "ja"
          label: "Ja"
          followup: "Beschreibe kurz 1-2 Erfolgsgeschichten"
        - value: "teilweise"
          label: "Teilweise (habe pro-bono/Test-Projekte gemacht)"
          followup: "Was waren die Ergebnisse?"
        - value: "nein"
          label: "Nein, ich starte von null"
  
  block_7_preismodell:
    frage_18:
      id: "preismodell_typ"
      text: "Wie berechnest du deine Preise?"
      typ: "single_choice"
      optionen:
        - value: "stundensatz"
          label: "Stundensatz (X€ pro Stunde)"
        - value: "tagessatz"
          label: "Tagessatz (X€ pro Tag)"
        - value: "projektpauschale"
          label: "Projektpauschale (Festpreis pro Projekt)"
        - value: "retainer"
          label: "Retainer (Monatspauschale)"
        - value: "value_based"
          label: "Value-based (Preis basierend auf Ergebnis)"
        - value: "abo"
          label: "Abo-Modell (monatlich)"
    
    frage_19:
      id: "preis_hauptprodukt"
      text: "Was kostet dein Haupt-Angebot?"
      typ: "price_input"
      examples:
        - "1-Stunden-Call: 150€"
        - "5er-Paket Sessions: 650€"
        - "3-Monats-Programm: 3.000€"
        - "Monatlicher Retainer: 2.500€"
      
      validation:
        min: 50
        must_contain_euro: true
    
    frage_20:
      id: "pricing_strategie"
      text: "Wie positionierst du dich preislich?"
      typ: "single_choice"
      optionen:
        - value: "budget"
          label: "Budget (günstiger als Durchschnitt)"
          beispiel: "50-100€/h"
        - value: "mittelklasse"
          label: "Mittelklasse (Marktdurchschnitt)"
          beispiel: "100-200€/h"
        - value: "premium"
          label: "Premium (deutlich über Durchschnitt)"
          beispiel: "200-500€/h"
        - value: "enterprise"
          label: "Enterprise (Top-Tier)"
          beispiel: "500€+/h oder Projektsummen 10.000€+"
    
    frage_21:
      id: "durchschnittsprojekt_wert"
      text: "Was ist der durchschnittliche Wert eines Kunden-Projekts?"
      typ: "number_input"
      unit: "€"
      hint: |
        Denk an die gesamte Kundenbeziehung:
        
        Wenn Session 150€ kostet und Kunde durchschnittlich 
        8 Sessions bucht → 1.200€
        
        Wenn 3-Monats-Programm 3.000€ und 50% verlängern 
        → Ø 4.500€ Customer Lifetime Value
```

### 📄 Text-Generierung Template: Online-Dienstleistung

```markdown
## 2. GESCHÄFTSMODELL

### 2.1 Geschäftsidee und Dienstleistung

{geschaeftsidee_kurz}

Die Dienstleistung richtet sich an {zielgruppe_primaer} mit dem 
Fokus auf {spezialisierung}.

**Zielmarkt:**
{zielmarkt_beschreibung}

{if zielmarkt_global}
Durch die digitale Natur des Geschäfts können Kunden weltweit 
bedient werden, wobei {zeitzonen_handling} berücksichtigt wird.
{endif}

### 2.2 Service-Delivery und Format

**Beratungsformat:**
Die Dienstleistung wird im {beratungsformat}-Format angeboten.

**Delivery-Methode:**
{delivery_methode_beschreibung}

**Session-Struktur:**
Eine typische Session dauert {session_dauer}. Das Angebot ist 
strukturiert als {paket_struktur}.

{if paket_struktur == "programm"}
**Programm-Aufbau:**
{programm_details}
{endif}

**Technische Infrastruktur:**
Für die Durchführung werden folgende Tools/Plattformen genutzt:
{tools_liste}

### 2.3 Platform-Strategie

**Kundenakquise-Kanäle:**
{plattform_typ_beschreibung}

**Online-Präsenz:**
{online_praesenz_strategie}

### 2.4 Zielgruppe und Kundenprofil

**Idealer Kunde:**
{zielgruppe_detailliert}

**Zentrales Kundenproblem:**
{customer_pain_point}

**Lösung:**
{problemloesung_beschreibung}

### 2.5 Alleinstellungsmerkmale

**USP:**
{usp_formulierung}

**Differenzierung:**
{differenzierung_text}

{if proof_of_concept}
**Validierung:**
{proof_of_concept_beschreibung}
{endif}

### 2.6 Kapazität und Skalierbarkeit

**Aktuelle Kapazität:**
Bei {max_stunden_pro_woche} Arbeitsstunden pro Woche können 
maximal {max_kunden_parallel} Kunden parallel betreut werden.

**Skalierungsstrategie:**
{automatisierung_strategie}

{if automatisierung_geplant}
Langfristig ist geplant, das Geschäftsmodell durch 
{automatisierung_massnahmen} zu skalieren, um die Abhängigkeit 
von direkter Arbeitszeit zu reduzieren.
{endif}

### 2.7 Preismodell

**Pricing-Strategie:**
Das Preismodell basiert auf {preismodell_typ}.

**Preisgestaltung:**
{preis_hauptprodukt}

**Positionierung:**
Die Preise bewegen sich im {pricing_strategie}-Segment des 
Marktes. {pricing_begruendung}

**Durchschnittlicher Kundenwert:**
Der durchschnittliche Projekt- bzw. Customer Lifetime Value liegt 
bei ca. {durchschnittsprojekt_wert}€.
```

---

---

## 📋 TYP 3: MOBILER SERVICE

### ✅ Pflichtfelder

```yaml
mobiler_service_pflichtfelder:
  kern:
    - geschaeftsidee_kurz
    - service_typ                 # Handwerk/Pflege/Beauty/Catering
    - spezialisierung
    
  einsatzgebiet:
    - einsatzgebiet_stadt         # In welcher Stadt/Region?
    - einsatzradius_km            # Wie weit fährst du?
    - haupteinsatzgebiet          # Wo konzentrierst du dich?
    - einsatzgebiete_erweitert    # Mehrere Städte? Bundesland?
    
  mobilitaet:
    - mobilität_typ               # Auto/Transporter/Fahrrad/ÖPNV
    - fahrzeug_vorhanden          # Ja/Nein/Geplant
    - fahrzeug_typ                # PKW/Transporter/Kastenwagen
    - fahrzeug_ausstattung        # Was ist im Auto?
    
  mobile_ausstattung:
    - ausstattung_liste           # Was bringst du mit?
    - lager_benoetigt             # Für Equipment/Material
    - lagerort                    # Zuhause/Gemieteter Raum
    
  einsatzplanung:
    - einsaetze_pro_tag           # Realistisch schätzbar
    - durchschnittliche_einsatzzeit # Pro Kunde
    - anfahrtszeit_durchschnitt   # Fahrzeit
    - anfahrtskosten_modell       # Pauschal/Pro km/Inklusive
    
  zielgruppen:
    - zielgruppe_primaer
    - kundentyp                   # B2B/B2C/Beides
    - kundenbeduerfnis
    
  alleinstellungsmerkmal:
    - usp
    - marktluecke
    - abgrenzung
    
  preismodell:
    - preismodell_typ             # Stundensatz/Pauschale/Projekt
    - preis_hauptprodukt
    - anfahrt_berechnung          # Wie kalkuliert?
    - mindestauftragswert         # Falls relevant
```

### ❌ Ausgeschlossene Fragen

```yaml
mobiler_service_excluded:
  - groesse_qm                    # Keine festen Räume
  - sitzplaetze                   # Irrelevant
  - oeffnungszeiten               # Flexibel nach Termin
  - raumaufteilung                # Irrelevant
  - gastgewerbe_erlaubnis         # Irrelevant (außer Catering)
  - speisekarte_umfang            # Irrelevant
  - delivery_methode              # Hat eigenes Konzept
  - tools_geplant                 # Irrelevant (außer Termin-Tool)
  - shop_plattform                # Kein E-Commerce
```

### 📝 Fragenabfolge Mobiler Service

```yaml
fragenabfolge_mobiler_service:
  
  block_1_geschaeftsidee:
    frage_1:
      id: "geschaeftsidee_kurz"
      text: "Beschreibe deinen mobilen Service in 1-2 Sätzen"
      beispiele:
        - "Mobiler Friseur für Senioren und Menschen mit eingeschränkter Mobilität"
        - "Fahrrad-Reparatur vor Ort für Berufspendler"
        - "Mobile Massage für Firmenkunden (Corporate Wellness)"
    
    frage_2:
      id: "spezialisierung"
      text: "Auf was spezialisierst du dich?"
      typ: "open_text"
      hint: "Was macht dich anders als andere mobile Dienstleister?"
  
  block_2_einsatzgebiet:
    intro: |
      Für mobile Services ist das Einsatzgebiet KRITISCH!
      (Ersetzt die "Standort"-Fragen bei stationären Geschäften)
    
    frage_3:
      id: "einsatzgebiet_stadt"
      text: "In welcher Stadt/Region bist du tätig?"
      typ: "open_text"
      validation:
        min_length: 5
      beispiel: "Berlin-Neukölln und Kreuzberg"
    
    frage_4:
      id: "einsatzradius_km"
      text: "Wie weit fährst du maximal?"
      typ: "single_choice_with_custom"
      optionen:
        - value: "5"
          label: "5 km (sehr lokal, Kiez)"
        - value: "10"
          label: "10 km (Stadtbezirk)"
        - value: "20"
          label: "20 km (ganze Stadt)"
        - value: "50"
          label: "50 km (Stadt + Umland)"
        - value: "100"
          label: "100 km (Region)"
        - value: "custom"
          label: "Andere Regelung: ___"
      
      hint: |
        Bedenke:
        - Fahrtzeit kostet Zeit = weniger Einsätze pro Tag
        - Benzinkosten steigen
        - Kunden außerhalb zahlen oft Aufschlag
    
    frage_5:
      id: "haupteinsatzgebiet"
      text: "Wo konzentrierst du dich hauptsächlich?"
      typ: "open_text"
      beispiel: |
        "Hauptsächlich Berlin-Mitte, Prenzlauer Berg, Friedrichshain.
        Bei größeren Aufträgen auch Brandenburg."
  
  block_3_mobilitaet:
    frage_6:
      id: "mobilität_typ"
      text: "WIE bist du mobil?"
      typ: "single_choice"
      optionen:
        - value: "auto"
          label: "Auto/PKW"
        - value: "transporter"
          label: "Transporter/Kastenwagen"
        - value: "fahrrad_ebike"
          label: "Fahrrad/E-Bike (+ ÖPNV für größere Distanzen)"
        - value: "oepnv"
          label: "Nur ÖPNV"
        - value: "andere"
          label: "Andere: ___"
    
    frage_7:
      id: "fahrzeug_status"
      text: "Hast du bereits ein Fahrzeug?"
      typ: "single_choice"
      optionen:
        - value: "vorhanden"
          label: "Ja, vorhanden"
          followup: "Welches? (Marke, Typ, Baujahr)"
        - value: "geplant"
          label: "Nein, muss ich noch anschaffen"
          followup: "Was planst du? (Neu/Gebraucht, Budget?)"
        - value: "nicht_noetig"
          label: "Nicht nötig (Fahrrad/ÖPNV reicht)"
    
    frage_8:
      id: "fahrzeug_ausstattung"
      text: "Was befindet sich in deinem Fahrzeug/bei dir?"
      typ: "open_text"
      beispiel: |
        z.B. bei mobilem Handwerker:
        - Werkzeugkoffer (Bosch Professional Set)
        - Akkuschrauber + Ersatzakkus
        - Leiter (3-teilig)
        - Kleinmaterial (Schrauben, Dübel, etc.)
        - Staubsauger
  
  block_4_ausstattung_lager:
    frage_9:
      id: "mobile_ausstattung"
      text: "Was bringst du zu deinen Kunden mit?"
      typ: "checklist_with_text"
      hint: "Liste alle Tools/Geräte/Materialien auf"
    
    frage_10:
      id: "lager_benoetigt"
      text: "Brauchst du einen Lagerraum?"
      typ: "conditional"
      optionen:
        - value: "ja"
          label: "Ja"
          followup: "Wo? (Zuhause/Gemietet) Wie groß?"
        - value: "nein"
          label: "Nein, alles passt ins Auto/Zuhause"
        - value: "spaeter"
          label: "Erstmal nicht, bei Wachstum dann ja"
  
  block_5_einsatzplanung:
    intro: |
      Wichtig für Kapazitätsplanung: Wie viele Kunden pro Tag?
    
    frage_11:
      id: "durchschnittliche_einsatzzeit"
      text: "Wie lange dauert ein typischer Einsatz?"
      typ: "time_input"
      optionen:
        - "30 Minuten"
        - "1 Stunde"
        - "2 Stunden"
        - "Halber Tag (4h)"
        - "Ganzer Tag (8h)"
        - "Variiert stark"
      
      if_variiert:
        followup: "Nenne Beispiele für kurze und lange Einsätze"
    
    frage_12:
      id: "anfahrtszeit_durchschnitt"
      text: "Wie lange fährst du durchschnittlich zum Kunden?"
      typ: "time_input"
      hint: "Im Schnitt innerhalb deines Einsatzgebiets"
    
    frage_13:
      id: "einsaetze_pro_tag_realistisch"
      text: "Wie viele Einsätze schaffst du realistisch pro Tag?"
      typ: "number_input"
      range: [1, 10]
      calculation_hint: |
        Rechnung:
        Arbeitstag: 8h
        - Einsatzzeit: {durchschnittliche_einsatzzeit}
        - Anfahrt hin + zurück: {anfahrtszeit_durchschnitt} × 2
        - Pause: 30-60 Min
        = Realistisch {calculated_einsaetze} Einsätze
      
      validation:
        plausibility_check: true
    
    frage_14:
      id: "anfahrtskosten_modell"
      text: "Wie berechnest du die Anfahrt?"
      typ: "single_choice"
      optionen:
        - value: "inklusive"
          label: "Inklusive im Preis (keine extra Berechnung)"
        - value: "pauschal"
          label: "Pauschale Anfahrt (z.B. 15€)"
        - value: "pro_km"
          label: "Pro km (z.B. 0,50€/km)"
        - value: "gestaffelt"
          label: "Gestaffelt nach Entfernung"
          beispiel: "0-10km: 0€, 10-20km: 10€, 20+km: 20€"
  
  block_6_zielgruppen:
    frage_15:
      id: "kundentyp"
      text: "Wen bedienst du hauptsächlich?"
      typ: "single_choice"
      optionen:
        - value: "b2c"
          label: "Privatkunden (B2C)"
        - value: "b2b"
          label: "Geschäftskunden (B2B)"
        - value: "beide"
          label: "Beide"
    
    frage_16:
      id: "zielgruppe_primaer"
      text: "Wer ist dein idealer Kunde?"
      typ: "guided_text"
      template: |
        1. Wer? (z.B. "Berufstätige 30-50J", "Kleine Büros 5-20 MA")
        2. Wo? (Wohngebiet/Büroviertel/etc.)
        3. Problem? (Was brauchen sie?)
        4. Warum mobil? (Warum kommen sie nicht zu dir?)
      
      beispiel: |
        1. Berufstätige Homeoffice-Worker, 30-45J
        2. Wohnen in Neukölln/Kreuzberg
        3. Rückenprobleme durch schlechte Homeoffice-Ausstattung
        4. Keine Zeit in Praxis zu fahren + wollen nicht raus
  
  block_7_usp:
    frage_17:
      id: "marktluecke"
      text: "WARUM mobil? Was ist der Vorteil für Kunden?"
      typ: "open_text"
      hint: |
        Gute Antworten:
        - "Kunden haben keine Zeit zur Werkstatt zu fahren"
        - "Senioren können nicht mehr raus"
        - "Firmen wollen Service direkt im Büro"
    
    frage_18:
      id: "usp_formulierung"
      text: "Was macht DICH anders als andere mobile Dienstleister?"
      typ: "structured_sentence"
      template: |
        "Im Gegensatz zu [andere Mobile/Stationäre Anbieter] bin 
        ich der/die Einzige, der/die [dein USP], was Kunden 
        [Vorteil] bringt."
  
  block_8_preismodell:
    frage_19:
      id: "preismodell_typ"
      text: "Wie berechnest du deine Preise?"
      typ: "single_choice"
      optionen:
        - value: "stundensatz"
          label: "Stundensatz (X€ pro Stunde)"
        - value: "pauschale"
          label: "Pauschale pro Einsatz (Festpreis)"
        - value: "projekt"
          label: "Projektbasis (je nach Umfang)"
        - value: "hybrid"
          label: "Hybrid (Pauschalpreis + Zusatzleistungen extra)"
    
    frage_20:
      id: "preis_hauptprodukt"
      text: "Was kostet dein Hauptangebot?"
      typ: "price_input"
      beispiele:
        - "1 Stunde Massage: 80€"
        - "Friseurbesuch: 45€ (+ 15€ Anfahrt)"
        - "Fahrrad-Reparatur: ab 50€"
    
    frage_21:
      id: "mindestauftragswert"
      text: "Hast du einen Mindestauftragswert?"
      typ: "conditional"
      optionen:
        - value: "ja"
          label: "Ja"
          followup: "Wie viel? (€)"
        - value: "nein"
          label: "Nein"
      
      hint: |
        Viele mobile Services haben Mindestauftragswert,
        da Anfahrt sonst nicht lohnt.
        
        z.B. "Mindestens 50€, sonst +20€ Anfahrtspauschale"
```

### 📄 Text-Generierung Template: Mobiler Service

```markdown
## 2. GESCHÄFTSMODELL

### 2.1 Geschäftsidee und Service

{geschaeftsidee_kurz}

Der Service richtet sich an {zielgruppe_primaer} und wird mobil 
direkt vor Ort beim Kunden erbracht.

**Spezialisierung:**
{spezialisierung_beschreibung}

### 2.2 Einsatzgebiet und Mobilität

**Einsatzgebiet:**
Haupt-Einsatzgebiet ist {einsatzgebiet_stadt} mit einem maximalen 
Einsatzradius von {einsatzradius_km} km. Der Fokus liegt auf 
{haupteinsatzgebiet}.

**Mobilität:**
Die Anfahrt zu Kunden erfolgt per {mobilität_typ}. 
{fahrzeug_status_beschreibung}

**Fahrzeugausstattung:**
{fahrzeug_ausstattung_liste}

### 2.3 Mobile Ausstattung und Equipment

Für die Erbringung der Dienstleistung wird folgendes Equipment 
zum Kunden mitgebracht:

{mobile_ausstattung_liste}

{if lager_benoetigt}
**Lagerung:**
{lager_beschreibung}
{endif}

### 2.4 Einsatzplanung und Kapazität

**Einsatzdauer:**
Ein typischer Einsatz dauert ca. {durchschnittliche_einsatzzeit}, 
bei einer durchschnittlichen Anfahrtszeit von 
{anfahrtszeit_durchschnitt}.

**Kapazität:**
Bei einem 8-Stunden-Arbeitstag sind realistisch 
{einsaetze_pro_tag_realistisch} Einsätze pro Tag möglich, unter 
Berücksichtigung von Anfahrtszeiten, Pausen und Vorbereitung.

**Anfahrtskosten:**
{anfahrtskosten_modell_beschreibung}

### 2.5 Zielgruppe

**Kundentyp:** {kundentyp}

**Hauptzielgruppe:**
{zielgruppe_detailliert}

**Bedürfnis:**
{kundenbeduerfnis_beschreibung}

**Warum mobil?**
{mobile_vorteil_fuer_kunden}

### 2.6 Alleinstellungsmerkmale

**USP:**
{usp_formulierung}

**Marktlücke:**
{marktluecke_beschreibung}

Im Gegensatz zu stationären Anbietern bietet der mobile Ansatz 
folgende Vorteile: {mobile_vorteile_liste}

### 2.7 Preismodell

**Preisgestaltung:**
{preismodell_typ_beschreibung}

**Hauptangebot:**
{preis_hauptprodukt}

{if anfahrtskosten != "inklusive"}
**Anfahrtskosten:**
{anfahrtskosten_berechnung}
{endif}

{if mindestauftragswert}
**Mindestauftragswert:** {mindestauftragswert}€

Dieser Mindestauftragswert stellt sicher, dass die Anfahrt 
wirtschaftlich tragbar ist.
{endif}

**Durchschnittlicher Auftragswert:**
{durchschnittlicher_auftragswert_schaetzung}
```

---

---

## 📋 WEITERE TYPEN (KOMPAKT)

### TYP 4: HANDEL STATIONÄR

```yaml
handel_stationaer_pflichtfelder:
  - geschaeftsidee
  - laden_typ                     # Boutique/Fachgeschäft/Concept Store
  - sortiment                     # Was verkaufst du?
  - standort_konkret              # Einkaufsstraße kritisch!
  - groesse_qm
  - verkaufsflaeche_vs_lager      # Aufteilung
  - oeffnungszeiten
  - laufkundschaft_vs_stammkunden # Ratio
  - zielgruppe
  - usp
  - preismodell
  - durchschnittlicher_bon

ausgeschlossen:
  - einsatzradius_km
  - delivery_methode
  - tools_geplant
  - mobile_ausstattung
```

### TYP 5: HANDEL ONLINE

```yaml
handel_online_pflichtfelder:
  - geschaeftsidee
  - ecommerce_modell              # Eigener Shop/Marketplace/Dropshipping
  - produktkatalog                # Wie viele Produkte?
  - shop_plattform                # Shopify/WooCommerce/Amazon
  - versandlogistik               # Wie verschickst du?
  - lagerbestand                  # Eigenlager/Dropshipping
  - zielmarkt                     # Deutschland/International
  - zielgruppe
  - usp
  - preismodell
  - durchschnittlicher_warenkorb

ausgeschlossen:
  - groesse_qm
  - sitzplaetze
  - oeffnungszeiten
  - standort_konkret
  - raumaufteilung
```

### TYP 6: PRODUKTION

```yaml
produktion_pflichtfelder:
  - geschaeftsidee
  - produkt_typ                   # Was stellst du her?
  - produktionsweise              # Handarbeit/Maschinen/Hybrid
  - produktionsraeume_groesse
  - maschinen_ausstattung
  - produktionskapazitaet         # Einheiten pro Tag/Woche
  - materialkosten_pro_einheit
  - produktionszeit_pro_einheit
  - vertriebsweg                  # Direktverkauf/B2B/Online/Handel
  - zielgruppe
  - usp
  - preismodell

ausgeschlossen:
  - sitzplaetze
  - oeffnungszeiten               # Produktionszeiten ≠ Öffnungszeiten
  - delivery_methode
  - tools_geplant
```

### TYP 7: DIENSTLEISTUNG LOKAL

```yaml
dienstleistung_lokal_pflichtfelder:
  - geschaeftsidee
  - dienstleistungstyp            # Friseur/Studio/Werkstatt/Praxis
  - standort_konkret
  - groesse_qm
  - anzahl_arbeitsplaetze         # Behandlungsräume/Stühle
  - ausstattung
  - terminbasiert                 # Ja/Nein
  - durchschnittliche_behandlungszeit
  - kapazitaet_pro_tag
  - oeffnungszeiten
  - zielgruppe
  - usp
  - preismodell

ausgeschlossen:
  - einsatzradius_km
  - fahrzeug_typ
  - delivery_methode
  - skalierung_automatisierung
```

### TYP 8: HYBRID

```yaml
hybrid_pflichtfelder:
  # Kombination der relevanten Pflichtfelder aus beiden Typen
  - geschaeftsidee
  - hybrid_kombination            # Welche Bereiche?
  - hauptfokus                    # Was ist primär?
  - sekundaerfokus                # Was ist sekundär?
  
  # Dann je nach Kombination relevante Felder aus beiden Typen

hinweis: |
  Bei Hybrid-Modellen: 
  1. Erst Hauptfokus identifizieren
  2. Fragen für Hauptfokus stellen
  3. Dann Sekundärfokus mit reduzierten Fragen

  Beispiel: "Laden + Online-Shop"
  → Hauptfokus: Handel Stationär (vollständige Fragen)
  → Sekundärfokus: Online (reduzierte Fragen)
```

---

---

## 🔧 IMPLEMENTIERUNGS-LOGIK

### Pseudo-Code: Geschäftstyp-Klassifikation

```python
class WorkshopFlowController:
    
    def start_modul_1(self, session_id):
        """
        Startet Modul 1 mit Typ-Klassifikation
        """
        # SCHRITT 1: Frage nach Geschäftstyp
        return {
            "message": CLASSIFICATION_QUESTION,
            "expects": "business_category_selection"
        }
    
    def handle_classification(self, session_id, user_answer):
        """
        Verarbeitet Typ-Auswahl und lädt passende Fragen
        """
        business_category = user_answer  # z.B. "gastronomie"
        
        # Speichere Typ in Session
        session = get_session(session_id)
        session.business_category = business_category
        session.save()
        
        # Lade typ-spezifische Konfiguration
        config = load_business_type_config(business_category)
        
        session.required_fields = config['required_fields']
        session.excluded_questions = config['excluded_questions']
        session.question_flow = config['question_flow']
        session.save()
        
        # Starte mit ersten typ-spezifischen Fragen
        first_question = self.get_next_question(session_id)
        
        return {
            "message": f"Perfekt! Du planst {business_category}. Lass uns die Details erfassen.",
            "next_question": first_question
        }
    
    def get_next_question(self, session_id):
        """
        Gibt nächste relevante Frage basierend auf Typ zurück
        """
        session = get_session(session_id)
        
        # Hole Fragenabfolge für diesen Typ
        question_flow = session.question_flow
        collected_fields = session.collected_fields
        excluded_questions = session.excluded_questions
        
        # Finde nächste offene Frage
        for block in question_flow:
            for question_id in block['questions']:
                
                # Skip wenn bereits beantwortet
                if question_id in collected_fields:
                    continue
                
                # Skip wenn excluded für diesen Typ
                if question_id in excluded_questions:
                    continue
                
                # Hole typ-spezifisches Fragen-Template
                question_template = self.get_question_template(
                    question_id,
                    session.business_category
                )
                
                return question_template
        
        # Alle Fragen beantwortet → Text generieren
        return {"status": "section_complete"}
    
    def get_question_template(self, question_id, business_category):
        """
        Gibt typ-spezifische Fragen-Formulierung zurück
        """
        # Lade Fragen-Definitionen
        question_definitions = load_question_definitions()
        
        # Prüfe ob typ-spezifische Variante existiert
        if question_id in question_definitions:
            variants = question_definitions[question_id]
            
            if business_category in variants:
                return variants[business_category]
            else:
                return variants['default']
        
        return None
```

---

---

## 📚 SYSTEM PROMPT TEMPLATE (MIT BRANCHING)

```python
MODUL_1_SYSTEM_PROMPT_WITH_BRANCHING = """
Du führst den Nutzer durch Modul 1: GESCHÄFTSMODELL.

**GESCHÄFTSTYP:** {business_category}
**SUBTYP:** {business_subtype}

---

**MODUL-ZIEL:**
Erfasse WAS, FÜR WEN, WARUM, WIE (Preismodell-Grundidee)

**FÜR DIESEN GESCHÄFTSTYP RELEVANTE THEMEN:**
{relevant_topics}

**KRITISCH - FRAGEN DIE DU NICHT STELLEN DARFST:**
{excluded_questions_list}

**GRUND:** Diese Fragen gehören nicht zu diesem Geschäftstyp oder 
werden in späteren Modulen behandelt.

---

**PFLICHTFELDER FÜR {business_category}:**
{required_fields_list}

**AKTUELL ERFASST ({progress}%):**
{collected_fields}

**NOCH FEHLEND:**
{missing_fields}

---

**FRAGENABFOLGE:**
Du befindest dich in Block: {current_block}
Nächste Frage: {next_question_id}

**BEISPIELE FÜR DIESEN TYP:**
{type_specific_examples}

---

**WICHTIG:**
1. Stelle NUR Fragen, die für {business_category} relevant sind
2. Überspringe automatisch Fragen in {excluded_questions_list}
3. Passe Frage-Formulierung an den Typ an
4. Nutze typ-spezifische Beispiele

**WENN >=90% DER PFLICHTFELDER ERFASST:**
Setze validation_status auf "complete" und generiere 
typ-spezifischen Businessplan-Text.

**STRUCTURED DATA FORMAT:**
<structured_data>
{{
  "section_id": "modul_1_geschaeftsmodell",
  "business_category": "{business_category}",
  "business_subtype": "{business_subtype}",
  "extracted_fields": {{
    {field_template}
  }},
  "validation_status": "incomplete|complete",
  "progress_percent": {progress}
}}
</structured_data>
"""
```

---

---

# 📄 FINALES DOKUMENT ENDE

**Dieses Dokument definiert:**
✅ Alle 8 Geschäftstypen mit Pflichtfeldern
✅ Typ-spezifische Fragenabfolgen
✅ Ausgeschlossene Fragen pro Typ
✅ Text-Generierungs-Templates pro Typ
✅ Branching-Logik Implementierung
✅ System-Prompt-Templates mit Typ-Awareness

**Verwendung:**
1. Dieses Dokument ist die Single Source of Truth
2. Claude Code implementiert basierend auf diesen Definitionen
3. Alle Änderungen nur hier dokumentieren
4. System Prompts werden aus diesem Dokument generiert

---

**Version:** 2.0
**Status:** Production-Ready
**Nächste Schritte:** Implementierung in Claude Code
