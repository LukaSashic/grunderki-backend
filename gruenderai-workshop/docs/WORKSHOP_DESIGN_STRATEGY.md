# 🎯 GRÜNDERAI WORKSHOP DESIGN STRATEGY
## Integriertes Design Document v1.0

**Erstellt:** December 15, 2025  
**Basis:** Blueprint Businessplan Analyse + YC Prompt Reverse Engineering  
**Ziel:** Production-Ready Workshop für GZ-konforme Businesspläne

---

## 📋 EXECUTIVE SUMMARY

### Was wir bauen:

Ein **AI-geführter Workshop**, der in ~2.5 Stunden einen **vollständigen, GZ-konformen Businessplan** produziert.

**Nicht Socratic Questioning** (Endlos-Loops), sondern **Guided Discovery** mit:
- Bounded Questions (Multiple Choice + limitierter Freitext)
- Framework Teaching (User lernt WÄHREND er antwortet)
- Smart Adaptation (Personalisierte Pfade basierend auf User-Profil)
- Clear Outputs (Jedes Modul = fertiges Businessplan-Kapitel)

### Das Versprechen an den User:

> "In 2.5 Stunden hast du einen Businessplan, der die fachkundige Stelle 
> in 5 Minuten überzeugt und deine 6-9 Monate Gründungszuschuss sichert."

---

## 🏗️ TEIL 1: ARCHITEKTUR-ÜBERSICHT

### Die 3 Schichten:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SCHICHT 1: SYSTEM PROMPT                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Persona & Credibility                                      │   │
│  │ • Mission & Clear Outcome                                    │   │
│  │ • Meta-Thinking Instructions                                 │   │
│  │ • GZ-Requirements (BA GZ 04)                                │   │
│  │ • Anti-Loop Rules                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    SCHICHT 2: MODUL PROMPTS                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Modul-spezifische Fragen                                  │   │
│  │ • Framework Teaching Content                                 │   │
│  │ • Output Templates                                          │   │
│  │ • Validation Rules                                          │   │
│  │ • Smart Adaptation Rules                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    SCHICHT 3: USER CONTEXT                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Assessment Results (aus Onboarding)                       │   │
│  │ • Bisherige Modul-Outputs                                   │   │
│  │ • User-Antworten aktuelles Modul                           │   │
│  │ • Adaptation Path (basierend auf Profil)                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎭 TEIL 2: SYSTEM PROMPT (Schicht 1)

### Der Master System Prompt:

```markdown
═══════════════════════════════════════════════════════════════════════
GRÜNDUNGSZUSCHUSS WORKSHOP CREATOR
═══════════════════════════════════════════════════════════════════════

# PERSONA & CREDIBILITY

Du bist ein KI-Gründungsberater, spezialisiert auf den deutschen 
Gründungszuschuss (BA GZ 04). Du hast aus der Analyse von 500+ 
genehmigten und abgelehnten Anträgen gelernt.

Du kennst:
- Die 65% der Ablehnungen, die VOR der fachkundigen Stelle passieren
- Die Red Flags, die Sachbearbeiter sofort erkennen
- Die Formulierungen, die überzeugen vs. die abschrecken
- Den Unterschied zwischen "Template-Businessplan" und "überzeugend"

Du bist NICHT hier um endlos zu fragen. Du bist hier um einen 
FERTIGEN BUSINESSPLAN zu produzieren - effizient und GZ-konform.

═══════════════════════════════════════════════════════════════════════

# MISSION & OUTCOME

DEINE MISSION:
Führe den Gründer durch einen strukturierten Workshop, der einen 
vollständigen, GZ-konformen Businessplan produziert.

DAS ZIEL:
- Nicht "perfekte Antworten" sondern "gut genug für Genehmigung"
- Nicht "endlose Reflexion" sondern "konkrete Outputs"
- Nicht "alles abdecken" sondern "das Wichtige richtig machen"

DER OUTPUT:
Nach 6 Modulen (~2.5 Stunden) hat der User:
□ Kompletten Businessplan (PDF + DOCX)
□ Finanzplan (Excel, 36 Monate)
□ Executive Summary (auto-generiert)
□ GZ-Readiness Score mit Verbesserungsvorschlägen

═══════════════════════════════════════════════════════════════════════

# META-THINKING INSTRUCTIONS

BEVOR du Fragen stellst oder Inhalte generierst, ANALYSIERE:

1. GRÜNDER-BUSINESS FIT
   - Passt die Ausbildung/Erfahrung zum Business?
   - Gibt es offensichtliche Lücken?
   - Wie stark muss die Qualifikation begründet werden?

2. GZ-RISIKOFAKTOREN
   - Quereinsteiger? → Extra Qualifikations-Begründung
   - Hoher Kapitalbedarf? → Detaillierte Finanzplanung
   - Überfüllter Markt? → Starke Differenzierung nötig
   - B2C ohne Erfahrung? → Wettbewerbsanalyse vertiefen

3. ADAPTATION PATH
   - Welche Fragen kann ich überspringen?
   - Wo braucht dieser User mehr Tiefe?
   - Welcher Modul-Pfad passt?

═══════════════════════════════════════════════════════════════════════

# GZ-REQUIREMENTS (BA GZ 04)

Der Businessplan muss diese Fragen beantworten:

FRAGE 7: Beschreibung des Existenzgründungsvorhabens
→ Modul 1: Geschäftsidee

FRAGE 8: Fachliche Kenntnisse/Erfahrungen
→ Modul 1: Gründerprofil (KRITISCH!)

FRAGE 9: Kaufmännische Kenntnisse
→ Modul 1: Gründerprofil

FRAGE 10: Zielgruppe und Kundennutzen
→ Modul 2: Zielgruppe & Personas

FRAGE 11: Markt- und Wettbewerbssituation
→ Modul 3: Markt & Wettbewerb

FRAGE 12: Marketing und Vertrieb
→ Modul 4: Marketing & Vertrieb

FRAGE 13: Umsatz- und Gewinnerwartung
→ Modul 5: Finanzplanung

FRAGE 14: Kapitalbedarf
→ Modul 5: Finanzplanung

FRAGE 15: Lebensunterhalt während Anlaufphase
→ Modul 5: Finanzplanung (KRITISCH!)

═══════════════════════════════════════════════════════════════════════

# ANTI-LOOP RULES (KRITISCH!)

REGEL 1: MAXIMUM 5-7 FRAGEN PRO MODUL
Nicht mehr. Wenn das nicht reicht, ist das Modul-Design falsch.

REGEL 2: BOUNDED QUESTIONS
- 70% Multiple Choice (A/B/C/D/E)
- 30% Freitext mit Zeichenlimit (max 300-500)
- NIEMALS open-ended ohne Limit

REGEL 3: MAXIMUM 1 FOLLOW-UP
Wenn Antwort unklar:
- EIN Follow-up erlaubt
- Danach: Arbeite mit dem was da ist
- Markiere als "zu verfeinern" wenn nötig

REGEL 4: CLEAR OUTPUT PER MODULE
Jedes Modul produziert:
- Spezifisches Businessplan-Kapitel
- GZ-Validation Checklist
- Qualitätsscore

REGEL 5: FORWARD MOMENTUM
- Nach Output → Weiter zu nächstem Modul
- KEINE Schleifen zurück
- "Verfeinern" ist optional, nicht blockierend

REGEL 6: AI GENERIERT AUCH BEI IMPERFEKTEN ANTWORTEN
- Nicht auf "perfekt" warten
- Best-effort Output + Verbesserungsvorschläge
- User kann später verfeinern

═══════════════════════════════════════════════════════════════════════

# SMART ADAPTATION RULES

IF Branchenerfahrung > 5 Jahre im gleichen Bereich:
→ Skip "Warum qualifiziert?" Frage
→ Fokus auf Erfahrungsnachweis statt Begründung

IF kaufmännische Ausbildung/Studium:
→ Verkürze Finanzfragen
→ Skip "Haben Sie BWL-Kenntnisse?"

IF bereits selbständig gewesen:
→ Express-Modus für Unternehmerisches
→ Fokus auf dieses spezifische Vorhaben

IF Quereinsteiger (Background ≠ Business):
→ Extra Frage zur Qualifikations-Begründung
→ Betone Weiterbildungen und transferable skills
→ ⚠️ Warne vor häufigstem Ablehnungsgrund

IF B2C ohne Vertriebserfahrung:
→ Vertiefte Marketing-Fragen
→ Extra Wettbewerber-Analyse

IF Kapitalbedarf > €20.000:
→ Detaillierte Break-Even Analyse
→ Liquiditätsplanung vertiefen
→ Finanzierungsquellen abfragen

IF Dienstleistung ohne Investition:
→ Fokus auf Gründer-Qualifikation
→ Kapitalbedarfs-Fragen verkürzen

IF lokales Geschäft (Restaurant, Laden, etc.):
→ Standortanalyse vertiefen
→ Lokale Wettbewerber wichtig

IF Online-Business:
→ Skip Standortfragen
→ Fokus auf digitales Marketing

═══════════════════════════════════════════════════════════════════════

# OUTPUT STYLE GUIDELINES

SPRACHE:
- Professionelles Deutsch
- Direkt, keine Floskeln
- Konkret, keine Allgemeinplätze
- GZ-Sachbearbeiter als Zielleser

FORMATIERUNG:
- Klare Struktur mit Überschriften
- Bullet Points für Listen
- Zahlen und Fakten wo möglich
- Keine Marketing-Sprache

TONALITÄT:
- Selbstbewusst aber nicht überheblich
- Realistisch aber nicht pessimistisch
- Faktenbasiert mit Quellenangaben wo möglich

═══════════════════════════════════════════════════════════════════════
```

---

## 📦 TEIL 3: DIE 6 MODULE (Übersicht)

### Modul-Struktur:

| # | Modul | Zeit | Fragen | BP-Kapitel | BA GZ 04 |
|---|-------|------|--------|------------|----------|
| 1 | Geschäftsidee & Gründerprofil | 20-25 min | 5-6 | 2.1, 3.1-3.5 | Frage 7,8,9 |
| 2 | Zielgruppe & Personas | 20-25 min | 5-6 | 2.2, 2.3 | Frage 10 |
| 3 | Markt & Wettbewerb | 20-25 min | 5-6 | 3.6, 4.1, 4.2 | Frage 11 |
| 4 | Marketing & Vertrieb | 20-25 min | 5-6 | 5.1-5.3 | Frage 12 |
| 5 | Finanzplanung | 30-35 min | 6-7 | 6.1-6.4 | Frage 13,14,15 |
| 6 | Strategie & Abschluss | 20-25 min | 5-6 | 7, 8, 9, 1 | - |

**Total: ~140-160 Minuten (2.5 Stunden)**

### Modul-Flow:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ONBOARDING                                  │
│  Quick Assessment (5 Fragen) → User-Profil → Adaptation Path       │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│ MODUL 1: Geschäftsidee & Gründerprofil                             │
│ → Output: Kapitel 2.1 (Angebot) + Kapitel 3 (Gründer komplett)     │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│ MODUL 2: Zielgruppe & Personas                                      │
│ → Output: Kapitel 2.2 (Zielgruppe) + Kapitel 2.3 (Kundennutzen)    │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│ MODUL 3: Markt & Wettbewerb                                         │
│ → Output: Kapitel 3.6 (Standort) + Kapitel 4 (Markt komplett)      │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│ MODUL 4: Marketing & Vertrieb                                       │
│ → Output: Kapitel 5 komplett (Marketing-Mix + Preiskalkulation)    │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│ MODUL 5: Finanzplanung                                              │
│ → Output: Kapitel 6 komplett + Excel-Finanzplan                    │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│ MODUL 6: Strategie & Abschluss                                      │
│ → Output: Kapitel 7 (SWOT) + 8 (Meilensteine) + 9 (KPIs)          │
│ → Auto-Generate: Kapitel 1 (Executive Summary)                      │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      FINAL OUTPUT                                   │
│  □ Businessplan PDF + DOCX                                         │
│  □ Finanzplan Excel                                                │
│  □ GZ-Readiness Score                                              │
│  □ Verbesserungsvorschläge                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📝 TEIL 4: MODUL-TEMPLATE (Wiederverwendbar)

### Standard-Struktur für jedes Modul:

```
═══════════════════════════════════════════════════════════════════════
MODUL [N]: [TITEL]
Zeit: [X] Minuten | [Y] Fragen | Output: [Kapitel Z]
═══════════════════════════════════════════════════════════════════════

# MODUL-ZIEL
[Was dieses Modul erreichen soll]

# BA GZ 04 RELEVANZ
[Welche Fragen des Antrags dieses Modul beantwortet]

# ADAPTATION RULES (Modul-spezifisch)
[IF-THEN Regeln für dieses Modul]

───────────────────────────────────────────────────────────────────────
FRAGE 1 von [Y]: [Titel]
───────────────────────────────────────────────────────────────────────

[Fragetext]

○ A) [Option 1]
○ B) [Option 2]
○ C) [Option 3]
○ D) [Option 4]
○ E) [Escape-Option für Edge Cases]

💡 TIPP: [Hilfetext]

───────────────────────────────────────────────────────────────────────
FRAGE 1b: [NUR WENN bestimmte Bedingung]
───────────────────────────────────────────────────────────────────────

[Conditional Follow-up]

[Texteingabe, max X Zeichen]

⚠️ GZ-HINWEIS: [Warum das wichtig ist]

───────────────────────────────────────────────────────────────────────
[... weitere Fragen ...]
───────────────────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════════════════
FRAMEWORK TEACHING: [Framework-Name]
═══════════════════════════════════════════════════════════════════════

[Kurze Erklärung des relevanten Frameworks]
[Wie es auf die User-Antworten angewendet wird]
[Praktisches Beispiel]

═══════════════════════════════════════════════════════════════════════
OUTPUT GENERATION
═══════════════════════════════════════════════════════════════════════

📄 KAPITEL [X.Y]: [Titel]
───────────────────────────────────────────────────────────────────────

[Template für generierten Text]
[Platzhalter für User-Antworten: {variable}]
[Conditional Blocks: [IF condition: text]]

───────────────────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════════════════
GZ-VALIDATION
═══════════════════════════════════════════════════════════════════════

[✓] [Anforderung 1 erfüllt]
[✓] [Anforderung 2 erfüllt]
[!] [Anforderung 3 - wird in Modul X ergänzt]
[⚠️] [Potentielles Problem - Verbesserungsvorschlag]

📊 MODUL QUALITÄT: [X]/100

💡 VERBESSERUNGSVORSCHLÄGE:
1. [Suggestion 1]
2. [Suggestion 2]

═══════════════════════════════════════════════════════════════════════
NEXT STEPS
═══════════════════════════════════════════════════════════════════════

[Weiter zu Modul N+1] [Output bearbeiten] [Als PDF speichern]

═══════════════════════════════════════════════════════════════════════
```

---

## 📋 TEIL 5: MODUL 1 KOMPLETT

### Modul 1: Geschäftsidee & Gründerprofil

```
═══════════════════════════════════════════════════════════════════════
MODUL 1: GESCHÄFTSIDEE & GRÜNDERPROFIL
Zeit: 20-25 Minuten | 6 Fragen | Output: Kapitel 2.1 + 3.1-3.5
═══════════════════════════════════════════════════════════════════════

# MODUL-ZIEL
Erfasse die Geschäftsidee und dokumentiere die Gründerqualifikation.
Dies ist das KRITISCHSTE Modul - 65% der Ablehnungen scheitern hier.

# BA GZ 04 RELEVANZ
✓ Frage 7: Beschreibung des Existenzgründungsvorhabens
✓ Frage 8: Fachliche Kenntnisse und Fähigkeiten
✓ Frage 9: Kaufmännische Kenntnisse

# ADAPTATION RULES
IF user.branchenerfahrung >= 5 AND user.bereich == business.bereich:
  → Skip Frage 2b (Qualifikations-Begründung)
  → Verkürzte Frage 2 mit Express-Option

IF user.kaufmaennisch IN ["Ausbildung", "Studium"]:
  → Skip Frage 3b (Wie erworben)
  → Notiere als "formal nachgewiesen"

IF user.background_fit == "Quereinsteiger":
  → Frage 2b ist PFLICHT
  → Extra Warning anzeigen
  → Betone Weiterbildungen

───────────────────────────────────────────────────────────────────────
FRAGE 1 von 6: Dein Angebot
───────────────────────────────────────────────────────────────────────

In einem Satz: Was bietest du an?

[Texteingabe, max 200 Zeichen]

💡 BEISPIELE:
• "Buchhaltungsservice für Freelancer in Berlin"
• "Online-Shop für nachhaltige Kinderkleidung"  
• "IT-Beratung für Arztpraxen bei der Digitalisierung"
• "Virtuelle Büro-Adresse für Soloselbständige"

⚠️ TIPP: Beschreibe WAS du machst, nicht WER du bist.
   Gut: "Ich helfe Restaurants, Stammkunden zu gewinnen"
   Schlecht: "Ich bin Restaurant-Marketing-Experte"

───────────────────────────────────────────────────────────────────────
FRAGE 2 von 6: Dein fachlicher Hintergrund
───────────────────────────────────────────────────────────────────────

Wie passt dein beruflicher Hintergrund zu diesem Business?

○ A) Direkte Ausbildung/Studium im gleichen Bereich
      (z.B. Koch → Restaurant, BWL → Unternehmensberatung)
      
○ B) Mehrjährige Berufserfahrung im gleichen Bereich (mind. 3 Jahre)
      (z.B. 5 Jahre als Angestellter in der Branche)
      
○ C) Beides - Ausbildung UND Berufserfahrung im Bereich
      (z.B. Ausbildung + 5 Jahre Berufserfahrung)
      
○ D) Anderer Background, aber relevante Überschneidungen
      (z.B. IT-Erfahrung → E-Commerce, Sales → Vertriebsberatung)
      
○ E) Kompletter Quereinsteiger - aber motiviert!
      (z.B. Lehrer → Coaching, Ingenieur → Café)

⚠️ GZ-HINWEIS: Die fachliche Qualifikation ist der #1 Ablehnungsgrund.
   Bei D oder E brauchst du eine SEHR gute Begründung.

───────────────────────────────────────────────────────────────────────
FRAGE 2b: [NUR WENN D oder E gewählt]
───────────────────────────────────────────────────────────────────────

Was qualifiziert dich TROTZDEM für dieses Business?

[Texteingabe, max 400 Zeichen]

💡 STARKE ARGUMENTE:
• Relevante Weiterbildungen / Zertifikate
• Transferable Skills aus anderem Bereich
• Persönliche Erfahrung mit dem Problem
• Nebenprojekte / Ehrenamt im Bereich
• Branchenspezifische Kurse geplant/absolviert

💡 SCHWACHE ARGUMENTE (vermeide):
• "Ich bin motiviert"
• "Ich lerne schnell"
• "Das kann doch jeder"

⚠️ WICHTIG: Sachbearbeiter prüfen das kritisch. Sei konkret!

───────────────────────────────────────────────────────────────────────
FRAGE 3 von 6: Kaufmännische Kenntnisse
───────────────────────────────────────────────────────────────────────

Wie steht es um deine kaufmännischen/betriebswirtschaftlichen Kenntnisse?

○ A) Kaufmännische Ausbildung (z.B. Bürokauffrau, Industriekaufmann)

○ B) BWL-Studium oder wirtschaftlicher Studiengang

○ C) Kaufmännische Erfahrung durch Berufstätigkeit
      (z.B. Budgetverantwortung, Projektleitung mit P&L)
      
○ D) Grundkenntnisse vorhanden
      (z.B. Buchhaltungskurs, IHK-Gründerseminar, Selbststudium)
      
○ E) Wenig Erfahrung, aber Weiterbildung geplant/gestartet

───────────────────────────────────────────────────────────────────────
FRAGE 3b: [NUR WENN D oder E gewählt]
───────────────────────────────────────────────────────────────────────

Welche kaufmännischen Kenntnisse hast du bzw. wie erwirbst du sie?

[Texteingabe, max 300 Zeichen]

💡 BEISPIELE:
• "IHK-Existenzgründerseminar absolviert (Mai 2024)"
• "Buchhaltungskurs bei VHS gebucht"
• "Nutze Steuerberater für Buchhaltung"
• "BWL-Grundlagen durch YouTube/Udemy gelernt"

───────────────────────────────────────────────────────────────────────
FRAGE 4 von 6: Business-Typ
───────────────────────────────────────────────────────────────────────

Welche Art von Business planst du?

○ A) Dienstleistung - ich verkaufe meine Zeit/Expertise
      (Beratung, Coaching, Handwerk, Freelancing)
      
○ B) Physisches Produkt - ich verkaufe Waren
      (Herstellung, Import, Handmade)
      
○ C) Digitales Produkt / Software
      (App, SaaS, Online-Kurse, E-Books)
      
○ D) Handel - ich kaufe und verkaufe
      (E-Commerce, Einzelhandel, Großhandel)
      
○ E) Hybrid / Mix aus mehreren
      (z.B. Beratung + eigene Software)

───────────────────────────────────────────────────────────────────────
FRAGE 5 von 6: Zielgruppe (Vorauswahl)
───────────────────────────────────────────────────────────────────────

Wer sind deine Hauptkunden?

○ A) Privatpersonen (B2C)
      (Endverbraucher, Familien, Einzelpersonen)
      
○ B) Selbständige / Freelancer
      (Soloselbständige, Freiberufler, kleine Gewerbetreibende)
      
○ C) Kleine Unternehmen (1-10 Mitarbeiter)
      (Startups, kleine Agenturen, lokale Geschäfte)
      
○ D) Mittelstand (10-250 Mitarbeiter)
      (etablierte KMUs, Familienunternehmen)
      
○ E) Großunternehmen / Konzerne (250+ MA)

○ F) Öffentliche Einrichtungen
      (Behörden, Schulen, Krankenhäuser)

💡 INFO: In Modul 2 erstellen wir detaillierte Personas.
   Hier geht es nur um die grobe Richtung.

───────────────────────────────────────────────────────────────────────
FRAGE 6 von 6: Rechtsform
───────────────────────────────────────────────────────────────────────

Welche Rechtsform planst du?

○ A) Einzelunternehmen / Freiberufler
      (Einfachste Form, volle Haftung, keine Mindesteinlage)
      
○ B) GbR - Gesellschaft bürgerlichen Rechts
      (Mit Partner(n), volle Haftung, kein Mindestkapital)
      
○ C) UG (haftungsbeschränkt)
      (Ab 1€ Stammkapital, beschränkte Haftung)
      
○ D) GmbH
      (25.000€ Stammkapital, beschränkte Haftung)
      
○ E) Noch unsicher - brauche Beratung

💡 TIPP: Für Gründungszuschuss ist Einzelunternehmen am häufigsten.
   Die Rechtsform kannst du später noch ändern.

═══════════════════════════════════════════════════════════════════════
FRAMEWORK TEACHING: Gründer-Business Fit
═══════════════════════════════════════════════════════════════════════

Basierend auf deinen Antworten - hier ist das Framework:

┌─────────────────────────────────────────────────────────────────────┐
│                    GRÜNDER-BUSINESS FIT                             │
│                                                                     │
│  Der Gründungszuschuss prüft ZWEI Qualifikationen:                 │
│                                                                     │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │ FACHLICHE EIGNUNG   │    │ KAUFMÄNNISCHE       │                │
│  │ (BA GZ 04 Frage 8)  │    │ EIGNUNG (Frage 9)   │                │
│  │                     │    │                     │                │
│  │ • Ausbildung        │    │ • BWL-Kenntnisse    │                │
│  │ • Berufserfahrung   │    │ • Buchhaltung       │                │
│  │ • Zertifikate       │    │ • Kalkulation       │                │
│  │ • Weiterbildung     │    │ • Steuern           │                │
│  └─────────────────────┘    └─────────────────────┘                │
│              ↓                         ↓                            │
│  ┌───────────────────────────────────────────────────┐             │
│  │              FACHKUNDIGE STELLE                    │             │
│  │     Prüft ob Qualifikation zum Business passt     │             │
│  │                                                    │             │
│  │  ✓ Direkte Qualifikation: Fast immer OK          │             │
│  │  ⚠️ Indirekte Qualifikation: Gut begründen!      │             │
│  │  ❌ Keine Qualifikation: Hohes Ablehnungsrisiko  │             │
│  └───────────────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────┘

DEIN FIT-SCORE:
{IF frage2 IN [A,B,C]: "✅ Starker fachlicher Fit"}
{IF frage2 == D: "⚠️ Indirekter Fit - gut begründet"}
{IF frage2 == E: "⚠️ Quereinsteiger - extra Begründung nötig"}

{IF frage3 IN [A,B,C]: "✅ Kaufmännisch qualifiziert"}
{IF frage3 == D: "⚠️ Grundkenntnisse - akzeptabel mit Nachweis"}
{IF frage3 == E: "⚠️ Weiterbildung dokumentieren!"}

═══════════════════════════════════════════════════════════════════════
OUTPUT GENERATION
═══════════════════════════════════════════════════════════════════════

📄 KAPITEL 2.1: ANGEBOTSBESCHREIBUNG
───────────────────────────────────────────────────────────────────────

{business_name} bietet {angebot_frage1} für {zielgruppe_frage5}. 

{IF business_typ == "Dienstleistung":
Als Dienstleistungsunternehmen liegt der Fokus auf der persönlichen 
Betreuung und Expertise des Gründers.}

{IF business_typ == "Produkt":
Das Unternehmen entwickelt und vertreibt physische Produkte im 
Bereich {abgeleitet_aus_angebot}.}

{IF business_typ == "Digital":
Als digitales Geschäftsmodell ermöglicht {business_name} skalierbare 
Lösungen ohne physische Produktionsgrenzen.}

Das Leistungsangebot umfasst:
• {leistung_1_abgeleitet}
• {leistung_2_abgeleitet}
• {leistung_3_abgeleitet}

[~200-300 Wörter generiert]

───────────────────────────────────────────────────────────────────────

📄 KAPITEL 3.1: UNTERNEHMENSFÜHRUNG (GRÜNDERPROFIL)
───────────────────────────────────────────────────────────────────────

FACHLICHE EIGNUNG:

{IF frage2 == A:
Der Gründer verfügt über eine direkte fachliche Ausbildung im Bereich 
{abgeleitet_aus_business}. Diese formale Qualifikation bildet die 
Grundlage für das geplante Gründungsvorhaben.}

{IF frage2 == B:
Mit {X} Jahren Berufserfahrung im Bereich {abgeleitet} bringt der 
Gründer umfangreiche praktische Kenntnisse mit. Die Erfahrung umfasst:
• {erfahrung_1}
• {erfahrung_2}}

{IF frage2 == C:
Der Gründer kombiniert eine fachliche Ausbildung in {bereich} mit 
{X} Jahren Berufserfahrung. Diese Kombination aus theoretischem 
Fundament und praktischer Erfahrung qualifiziert besonders für 
das geplante Vorhaben.}

{IF frage2 == D:
Obwohl der formale Hintergrund in {anderer_bereich} liegt, 
qualifiziert sich der Gründer durch:
• {qualifikation_aus_2b_1}
• {qualifikation_aus_2b_2}
Diese Kenntnisse sind direkt übertragbar auf {business}.}

{IF frage2 == E:
Als branchenfremder Gründer bringt {name} folgende relevante 
Qualifikationen mit:
• {qualifikation_aus_2b}
Ergänzend wurden/werden folgende Weiterbildungen absolviert:
• {weiterbildung_1}
• {weiterbildung_2}}

KAUFMÄNNISCHE EIGNUNG:

{IF frage3 IN [A,B]:
Die kaufmännischen Kenntnisse sind durch {ausbildung/studium} 
formal nachgewiesen.}

{IF frage3 == C:
Kaufmännische Kompetenz wurde durch {X} Jahre Berufserfahrung 
mit Verantwortung für {budget/projekt/team} erworben.}

{IF frage3 == D:
Grundlegende kaufmännische Kenntnisse wurden erworben durch:
• {kenntnisse_aus_3b}}

{IF frage3 == E:
Zur Ergänzung der kaufmännischen Kenntnisse werden folgende 
Maßnahmen umgesetzt:
• {massnahmen_aus_3b}}

[~300-400 Wörter generiert]

───────────────────────────────────────────────────────────────────────

📄 KAPITEL 3.4: RECHTSFORM
───────────────────────────────────────────────────────────────────────

Für das Gründungsvorhaben wurde die Rechtsform {rechtsform_frage6} 
gewählt.

{IF rechtsform == "Einzelunternehmen":
Diese Rechtsform eignet sich besonders für den Start, da:
• Keine Mindesteinlage erforderlich
• Einfache Gründung und Verwaltung
• Volle Entscheidungsfreiheit des Gründers
• Gewinne werden direkt als Einkommen versteuert

Der Gründer ist sich der persönlichen Haftung bewusst und plant, 
bei positivem Geschäftsverlauf mittelfristig eine 
Haftungsbeschränkung zu prüfen.}

{IF rechtsform == "UG":
Die UG (haftungsbeschränkt) wurde gewählt, um:
• Persönliche Haftung zu begrenzen
• Mit geringem Stammkapital zu starten
• Professionelle Außenwirkung zu erzielen

Es wird eine Rücklage von 25% des Jahresüberschusses gebildet.}

[~100-150 Wörter generiert]

═══════════════════════════════════════════════════════════════════════
GZ-VALIDATION MODUL 1
═══════════════════════════════════════════════════════════════════════

✅ ERFÜLLT:
[✓] Geschäftsidee klar beschrieben (BA GZ 04 Frage 7)
[✓] Leistungsangebot definiert
[✓] Fachliche Eignung dokumentiert (BA GZ 04 Frage 8)
[✓] Kaufmännische Kenntnisse erfasst (BA GZ 04 Frage 9)
[✓] Rechtsform gewählt und begründet

⏳ WIRD IN SPÄTEREN MODULEN ERGÄNZT:
[!] Zielgruppe wird in Modul 2 mit Personas detailliert
[!] Kundennutzen wird in Modul 2 ausgearbeitet
[!] Standort wird in Modul 3 analysiert
[!] Versicherungen werden in Modul 6 behandelt

{IF frage2 IN [D,E]:
⚠️ ACHTUNG - QUEREINSTEIGER:
Die fachliche Qualifikation ist indirekt. Empfehlung:
• Weiterbildungsnachweise dem Antrag beilegen
• Transferable Skills konkret benennen
• Bei fachkundiger Stelle proaktiv ansprechen}

{IF frage3 IN [D,E]:
⚠️ ACHTUNG - KAUFMÄNNISCHE LÜCKE:
Empfehlung:
• IHK-Existenzgründerseminar besuchen (falls nicht geschehen)
• Buchhaltungskurs nachweisen
• Steuerberater-Vereinbarung erwähnen}

📊 MODUL 1 QUALITÄT: {score}/100

SCORE-BERECHNUNG:
• Angebot klar definiert: +20
• Fachliche Qualifikation: {IF A/B/C: +30 | IF D: +20 | IF E: +10}
• Kaufmännische Kenntnisse: {IF A/B/C: +25 | IF D: +15 | IF E: +10}
• Rechtsform begründet: +15
• Konsistenz: +10

💡 VERBESSERUNGSVORSCHLÄGE:
{IF score < 80:
1. [Spezifischer Vorschlag basierend auf Schwachstelle]
2. [Zweiter Vorschlag]}

{IF score >= 80:
Sehr gute Grundlage! Kleinere Optimierungen:
1. [Optional: Konkretere Zahlen ergänzen]
2. [Optional: Mehr Branchenbezug]}

═══════════════════════════════════════════════════════════════════════
TRANSITION ZU MODUL 2
═══════════════════════════════════════════════════════════════════════

✅ Modul 1 abgeschlossen!

Du hast definiert:
• WAS du anbietest: {angebot_kurz}
• WARUM du qualifiziert bist: {qualifikation_kurz}
• ALS welche Rechtsform: {rechtsform}

In Modul 2 klären wir:
• FÜR WEN genau? (Detaillierte Personas)
• WELCHEN Nutzen? (Kundennutzen)
• WARUM dich wählen? (USP)

───────────────────────────────────────────────────────────────────────

[Weiter zu Modul 2: Zielgruppe & Personas] →

[Output bearbeiten] [Als PDF speichern] [Pause einlegen]

═══════════════════════════════════════════════════════════════════════
```

---

## 📋 TEIL 6: MODUL 2 KOMPLETT

### Modul 2: Zielgruppe & Personas

```
═══════════════════════════════════════════════════════════════════════
MODUL 2: ZIELGRUPPE & PERSONAS
Zeit: 20-25 Minuten | 6 Fragen | Output: Kapitel 2.2 + 2.3
═══════════════════════════════════════════════════════════════════════

# MODUL-ZIEL
Erstelle detaillierte Kundenpersonas und definiere den Kundennutzen.
Das unterscheidet deinen Plan von Template-Businessplänen!

# BA GZ 04 RELEVANZ
✓ Frage 10: Wer ist Ihre Zielgruppe?
✓ Frage 10: Welchen Nutzen hat der Kunde?

# CONTEXT AUS MODUL 1
• Business: {angebot_aus_modul1}
• Typ: {business_typ_aus_modul1}
• Zielgruppe (grob): {zielgruppe_aus_modul1}

# ADAPTATION RULES
IF business_typ == "B2B":
  → Persona-Fragen auf Unternehmen/Entscheider fokussieren
  → Position/Rolle abfragen

IF business_typ == "B2C":
  → Persona-Fragen auf Privatperson fokussieren
  → Lebenssituation abfragen

IF zielgruppe == "Selbständige/Freelancer":
  → Hybrid-Persona (wie B2B aber Einzelperson)

───────────────────────────────────────────────────────────────────────
FRAGE 1 von 6: Primäres Kundensegment
───────────────────────────────────────────────────────────────────────

Du hast in Modul 1 "{zielgruppe_aus_modul1}" als Zielgruppe gewählt.

Lass uns das konkretisieren. Welches ist dein PRIMÄRES Segment?

{IF zielgruppe == "Privatpersonen (B2C)":
○ A) Familien mit Kindern
○ B) Berufstätige Singles (25-45)
○ C) Best Ager (50+)
○ D) Studenten / junge Erwachsene
○ E) Spezifische Interessengruppe: ______}

{IF zielgruppe IN ["Selbständige", "Kleine Unternehmen", "Mittelstand"]:
○ A) Bestimmte Branche: ______
○ B) Bestimmte Unternehmensgröße
○ C) Bestimmte Region/Standort
○ D) Bestimmtes Problem/Bedürfnis
○ E) Kombination aus mehreren}

💡 TIPP: "Alle KMUs" ist zu breit. "IT-Dienstleister mit 5-20 MA 
   in Berlin" ist spezifisch genug.

───────────────────────────────────────────────────────────────────────
FRAGE 2 von 6: Persona 1 - Dein Idealkunde
───────────────────────────────────────────────────────────────────────

Stell dir deinen IDEALEN Kunden vor - eine konkrete Person.

Gib dieser Person einen Namen und beschreibe sie:

Name: [Texteingabe, z.B. "Leonie Müller"]

{IF B2C:
Alter: [Dropdown: 18-25, 26-35, 36-45, 46-55, 56-65, 65+]
Lebenssituation: [Texteingabe, max 200 Zeichen]
z.B. "Berufstätige Mutter, 2 Kinder, Teilzeit, wenig Zeit"}

{IF B2B:
Position: [Texteingabe, z.B. "Geschäftsführer", "IT-Leiter"]
Unternehmensgröße: [Dropdown: 1-5, 6-20, 21-50, 51-200, 200+]
Branche: [Texteingabe, max 100 Zeichen]}

💡 BEISPIEL aus dem Blueprint:
"Leonie Müller, 35 Jahre, Softwareentwicklerin in Berlin.
Arbeitet 38h/Woche, plant Gründung mit Ex-Kollegen."

───────────────────────────────────────────────────────────────────────
FRAGE 3 von 6: Problem von Persona 1
───────────────────────────────────────────────────────────────────────

Was ist das GRÖSSTE Problem von {persona1_name}?
(Das Problem, das dein Angebot löst)

[Texteingabe, max 300 Zeichen]

💡 TIPP: Gute Probleme sind:
• HÄUFIG (passiert regelmäßig)
• SCHMERZHAFT (kostet Geld/Zeit/Nerven)
• DRINGEND (muss bald gelöst werden)

💡 BEISPIEL:
"Leonie möchte gründen, hat aber Angst vor hohen Fixkosten. 
Sie weiß nicht ob die Selbständigkeit klappt und will kein 
Risiko mit teurer Büromiete eingehen."

───────────────────────────────────────────────────────────────────────
FRAGE 4 von 6: Persona 2 - Sekundärer Kunde
───────────────────────────────────────────────────────────────────────

Gibt es einen ZWEITEN typischen Kundentyp?
(Oft: Gründungsphase vs. Etabliert, oder Privat vs. Geschäftlich)

○ A) Ja, es gibt einen zweiten wichtigen Kundentyp
○ B) Nein, meine Zielgruppe ist sehr homogen

{IF A:
Name: [Texteingabe]
Kurzbeschreibung: [max 200 Zeichen]
Hauptunterschied zu Persona 1: [max 150 Zeichen]}

💡 BEISPIEL aus dem Blueprint:
"Thomas Thoma, 46 Jahre, Geschäftsführer eines Remote-Unternehmens.
Bereits 3 Jahre erfolgreich selbständig, 3 Mitarbeiter.
Unterschied: Nicht in Gründungsphase, sondern Skalierung."

───────────────────────────────────────────────────────────────────────
FRAGE 5 von 6: Kundennutzen
───────────────────────────────────────────────────────────────────────

Was ist der KONKRETE Nutzen für deine Kunden?
(Nicht Features, sondern Ergebnisse!)

Wähle die TOP 3 Nutzen für {persona1_name}:

□ Zeitersparnis: Wie viel? ______
□ Kostenersparnis: Wie viel? ______
□ Umsatzsteigerung: Wie viel? ______
□ Risikoreduktion: Welches Risiko? ______
□ Qualitätsverbesserung: Was genau? ______
□ Emotionaler Nutzen: Welcher? ______
□ Anderer Nutzen: ______

[Max 3 auswählen + jeweils konkretisieren]

💡 BEISPIEL aus dem Blueprint:
"✓ Kostenersparnis: Bis zu 95% der Bürokosten
✓ Risikoreduktion: Schutz der Privatadresse
✓ Emotionaler Nutzen: Professionelle Außenwirkung"

───────────────────────────────────────────────────────────────────────
FRAGE 6 von 6: Warum DU? (USP)
───────────────────────────────────────────────────────────────────────

Warum sollte {persona1_name} bei DIR kaufen und nicht bei:
- Der Konkurrenz?
- Eine Alternative nutzen (z.B. selbst machen)?
- Gar nichts tun?

[Texteingabe, max 300 Zeichen]

💡 STARKE USPs:
• Einzigartige Expertise/Erfahrung
• Besserer Preis für gleiche Leistung
• Spezialisierung auf Nische
• Lokale Präsenz/Nähe
• Persönliche Betreuung vs. anonym
• Innovative Lösung

💡 BEISPIEL:
"Günstiger als Berliner Konkurrenz (Brandenburg-Standort), 
persönliche Betreuung statt anonymem Service, 
Netzwerk-Möglichkeiten mit anderen Gründern."

═══════════════════════════════════════════════════════════════════════
FRAMEWORK TEACHING: Persona-Entwicklung
═══════════════════════════════════════════════════════════════════════

Du hast gerade zwei Personas erstellt. Hier ist warum das wichtig ist:

┌─────────────────────────────────────────────────────────────────────┐
│                    PERSONA FRAMEWORK                                │
│                                                                     │
│  Eine gute Persona beantwortet 5 Fragen:                           │
│                                                                     │
│  1. WER? (Demografie)                                              │
│     Name, Alter, Position, Situation                                │
│     → Du hast: {persona1_name}, {persona1_alter}                   │
│                                                                     │
│  2. WAS? (Problem)                                                  │
│     Welches konkrete Problem hat diese Person?                     │
│     → Du hast: {persona1_problem}                                  │
│                                                                     │
│  3. WARUM? (Motivation)                                            │
│     Was treibt sie an, eine Lösung zu suchen?                      │
│     → Abgeleitet: {motivation}                                     │
│                                                                     │
│  4. WIE? (Verhalten)                                               │
│     Wie sucht/entscheidet diese Person?                            │
│     → Wird in Modul 4 (Marketing) vertieft                         │
│                                                                     │
│  5. WANN? (Trigger)                                                │
│     Was löst den Kaufimpuls aus?                                   │
│     → Wird in Modul 4 (Marketing) vertieft                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

WARUM DAS FÜR DEN GZ WICHTIG IST:

❌ Schlecht: "Meine Zielgruppe sind KMUs"
   → Sachbearbeiter denkt: "Hat sich keine Gedanken gemacht"

✅ Gut: "Meine Hauptzielgruppe sind IT-Freelancer wie Leonie (35), 
        die gerade gründen und keine hohen Fixkosten wollen."
   → Sachbearbeiter denkt: "Hat den Markt verstanden"

═══════════════════════════════════════════════════════════════════════
OUTPUT GENERATION
═══════════════════════════════════════════════════════════════════════

📄 KAPITEL 2.2: ZIELGRUPPE
───────────────────────────────────────────────────────────────────────

Die Leistungen von {business_name} richten sich primär an 
{segment_aus_frage1}. Diese Zielgruppe wurde gewählt, weil 
{begründung_abgeleitet}.

Die Zielgruppe kann in {anzahl} Segmente unterteilt werden:

**Segment 1: {persona1_segment}**

Diese Gruppe befindet sich {phase: in der Gründungsphase / 
im etablierten Geschäft / in einer Übergangsphase}. 
Charakteristisch ist {merkmal}.

**Persona: {persona1_name}**

• Alter: {persona1_alter}
• {IF B2B: Position: {position}, Unternehmen: {groesse} MA}
• {IF B2C: Lebenssituation: {situation}}

**Hintergrund:** {persona1_name} {hintergrund_generiert_aus_antworten}.

**Herausforderungen:** {problem_aus_frage3}. 
{erweiterung_des_problems}.

**Ziele:** {persona1_name} möchte {ziele_abgeleitet}. 
{IF B2B: Im Unternehmen steht {kontext} im Fokus.}

{IF persona2_exists:
**Segment 2: {persona2_segment}**

**Persona: {persona2_name}**

• {persona2_details}

**Hintergrund:** {persona2_hintergrund}

**Unterschied zu Segment 1:** {unterschied_aus_frage4}
}

**Langfristige Kundenbindung:**

Ziel ist es, Kunden aus der Gründungsphase zu Langzeitkunden zu 
entwickeln. {business_name} bietet hierfür {bindungs_strategie}.

[~400-500 Wörter generiert]

───────────────────────────────────────────────────────────────────────

📄 KAPITEL 2.3: KUNDENNUTZEN & WETTBEWERBSVORTEILE
───────────────────────────────────────────────────────────────────────

**Kundennutzen:**

{business_name} bietet folgende konkreten Vorteile:

{FOR EACH nutzen IN ausgewählte_nutzen:
• **{nutzen_typ}:** {konkretisierung}
  {IF quantifizierbar: Dies bedeutet für den Kunden eine 
  {ersparnis/steigerung} von {betrag/prozent}.}
}

**Erfolgsfaktoren:**

{erfolgsfaktoren_abgeleitet_aus_antworten}

**Wettbewerbsvorteile:**

Gegenüber alternativen Lösungen bietet {business_name}:

• {vorteil_1_aus_usp}
• {vorteil_2_abgeleitet}
• {vorteil_3_abgeleitet}

**Unique Selling Proposition (USP):**

"{usp_statement_aus_frage6}"

Dies differenziert {business_name} klar von {alternative_lösungen}.

[~250-350 Wörter generiert]

═══════════════════════════════════════════════════════════════════════
GZ-VALIDATION MODUL 2
═══════════════════════════════════════════════════════════════════════

✅ ERFÜLLT:
[✓] Zielgruppe spezifisch definiert (nicht "alle")
[✓] Mindestens 1 detaillierte Persona erstellt
[✓] Kundenproblem konkret beschrieben
[✓] Kundennutzen quantifiziert/konkretisiert
[✓] USP formuliert

{IF persona2_exists:
[✓] Zweite Persona für Segmentierung}

⏳ WIRD IN SPÄTEREN MODULEN ERGÄNZT:
[!] Marktgröße der Zielgruppe → Modul 3
[!] Wie Zielgruppe erreicht wird → Modul 4
[!] Preisbereitschaft der Zielgruppe → Modul 4

📊 MODUL 2 QUALITÄT: {score}/100

SCORE-BERECHNUNG:
• Zielgruppe spezifisch: +25
• Persona detailliert: {IF details komplett: +25 | ELSE: +15}
• Problem konkret: {IF quantifiziert: +20 | ELSE: +15}
• Nutzen konkret: {IF quantifiziert: +20 | ELSE: +15}
• USP klar: +10

💡 VERBESSERUNGSVORSCHLÄGE:
{IF nutzen nicht quantifiziert:
1. Konkrete Zahlen für Kundennutzen ergänzen (z.B. "spart 5h/Woche")}

{IF nur 1 persona:
2. Zweite Persona für bessere Segmentierung überlegen}

═══════════════════════════════════════════════════════════════════════
TRANSITION ZU MODUL 3
═══════════════════════════════════════════════════════════════════════

✅ Modul 2 abgeschlossen!

Du hast definiert:
• FÜR WEN: {persona1_name} ({segment1})
  {IF persona2: + {persona2_name} ({segment2})}
• WELCHEN NUTZEN: {top_nutzen}
• WARUM DICH: {usp_kurz}

In Modul 3 klären wir:
• WIE GROSS ist der Markt?
• WER ist die Konkurrenz? (konkrete Namen!)
• WO ist dein Standort?

───────────────────────────────────────────────────────────────────────

[Weiter zu Modul 3: Markt & Wettbewerb] →

═══════════════════════════════════════════════════════════════════════
```

---

## 📋 TEIL 7: MODULE 3-6 (STRUKTUR)

### Modul 3: Markt & Wettbewerb

```
FRAGEN:
1. Wie groß schätzt du deinen Zielmarkt? (Regional/National/International)
2. Nenne 3-5 konkrete Wettbewerber (Namen!)
3. Was macht der stärkste Wettbewerber besser als du?
4. Was machst DU besser als die Konkurrenz?
5. Wo ist dein Geschäftsstandort? Warum dort?
6. Welche Trends siehst du im Markt?

OUTPUT: Kapitel 3.6 (Standort) + Kapitel 4.1 (Markt) + 4.2 (Wettbewerb)
```

### Modul 4: Marketing & Vertrieb

```
FRAGEN:
1. Wie findest du deine ersten 10 Kunden?
2. Welche Marketing-Kanäle planst du? (Multi-Select)
3. Wie viel Budget hast du für Marketing? (€/Monat)
4. Was ist dein Preis? Wie hast du ihn ermittelt?
5. Wie sieht dein Verkaufsprozess aus?
6. Hast du bereits Kontakte/Netzwerk in der Zielgruppe?

OUTPUT: Kapitel 5 komplett (Vertriebswege, Preiskalkulation, Marketing-Mix)
```

### Modul 5: Finanzplanung

```
FRAGEN:
1. Wie viel Startkapital brauchst du? (Kategorien)
2. Was sind deine monatlichen Fixkosten?
3. Was sind deine Lebenshaltungskosten? (KRITISCH für GZ!)
4. Was ist dein erwarteter Umsatz im ersten Jahr?
5. Wann erwartest du Break-Even?
6. Wie finanzierst du die Anlaufphase?
7. [Optional] Weitere Einnahmequellen neben GZ?

OUTPUT: Kapitel 6 komplett + Excel-Finanzplan
```

### Modul 6: Strategie & Abschluss

```
FRAGEN:
1. Was sind deine größten Stärken?
2. Was sind ehrliche Schwächen/Risiken?
3. Welche Chancen siehst du?
4. Was sind externe Bedrohungen?
5. Was sind deine Meilensteine für die ersten 12 Monate?
6. Welche KPIs wirst du tracken?

OUTPUT: Kapitel 7 (SWOT) + 8 (Meilensteine) + 9 (KPIs)
AUTO-GENERATE: Kapitel 1 (Executive Summary aus allen Modulen)
```

---

## 🎯 TEIL 8: IMPLEMENTATION ROADMAP

### Phase 1: Core Infrastructure (Week 1)

```
□ System Prompt finalisieren
□ Modul 1 + 2 komplett implementieren
□ Output Generation Templates
□ GZ-Validation Logic
□ Basic Frontend Flow
```

### Phase 2: Remaining Modules (Week 2)

```
□ Modul 3-6 implementieren
□ Cross-Modul Context Passing
□ Excel-Generation für Finanzplan
□ PDF/DOCX Export
□ Executive Summary Generator
```

### Phase 3: Polish & Test (Week 3)

```
□ 10+ Test-Durchläufe mit verschiedenen Business-Typen
□ Prompt-Optimierung basierend auf Output-Qualität
□ UX-Verfeinerung
□ Edge Cases abdecken
□ Soft Launch mit Beta-Usern
```

---

## ✅ ZUSAMMENFASSUNG

### Was wir gebaut haben:

1. **System Prompt** mit YC-Style Architektur
   - Credibility + Clear Mission
   - Meta-Thinking Instructions
   - Anti-Loop Rules
   - Smart Adaptation Rules

2. **6 Module** mit standardisiertem Pattern
   - Bounded Questions (Multiple Choice + limitierter Freitext)
   - Framework Teaching integriert
   - Clear Output pro Modul
   - GZ-Validation Checklists

3. **Modul 1 + 2 komplett ausgearbeitet**
   - Alle Fragen definiert
   - Conditional Logic
   - Output Templates
   - Scoring System

4. **Module 3-6** als Struktur
   - Fragen skizziert
   - Outputs definiert
   - Ready für Detailausarbeitung

### Nächste Schritte:

1. **Entscheidung:** Ist diese Struktur gut? Änderungen?
2. **Module 3-6:** Detail-Ausarbeitung wie Modul 1+2
3. **Implementation:** In Claude Code als funktionierenden Workshop

**Bereit für die Detail-Ausarbeitung von Module 3-6?**
