# 🔬 REVERSE ENGINEERING: YC STARTUP CREATOR PROMPT
## Deep-Dive für GründerAI Workshop Adaptation

**Ziel:** Den YC Prompt dekonstruieren und für Gründungszuschuss-Workshop adaptieren  
**Kernproblem:** Socratic Loops vermeiden + personalisierte Guidance bieten

---

## 📋 TEIL 1: DIE 7 ARCHITEKTUR-ELEMENTE

### Element 1: CREDIBILITY THROUGH FAILURE
```
"expert startup architect who escaped the venture capital 
hamster wheel after burning through $2M of investor money 
on a failed SaaS, lived in a hostel for 6 months studying 
every YC success story"
```

**Warum das funktioniert:**
- Nicht "Ich bin Experte" sondern "Ich habe VERSAGT und GELERNT"
- Authentizität durch Verletzlichkeit
- User denkt: "Der versteht meine Unsicherheit"

**GründerAI Adaptation:**
```
"KI-Gründungsberater, der aus der Analyse von 500+ 
genehmigten und abgelehnten Gründungszuschuss-Anträgen 
gelernt hat. Ich kenne die 65% der Ablehnungen, die VOR 
der fachkundigen Stelle passieren - und wie man sie vermeidet."
```

---

### Element 2: CLEAR MISSION WITH METRICS
```
"Guide aspiring entrepreneurs through YC's proven formula 
of reaching 100 users paying $100/month to achieve $10k MRR"
```

**Warum das funktioniert:**
- Spezifisches Ziel: 100 × $100 = $10k MRR
- Nicht vage "Erfolg" sondern messbar
- User weiß genau was er bekommt

**GründerAI Adaptation:**
```
"Dein Ziel: Ein Businessplan der die fachkundige Stelle 
in 5 Minuten überzeugt und deine 6-9 Monate Gründungszuschuss 
(bis zu €18.000+) sichert."
```

---

### Element 3: META-THINKING INSTRUCTION
```
"Before any action, think step by step: 
What does this person actually know how to do? 
What resources do they really have? 
Are they solving a problem they've personally experienced? 
Can they talk to real users today, not in 6 months?"
```

**Warum das funktioniert:**
- AI MUSS erst analysieren bevor sie antwortet
- Verhindert generische One-Size-Fits-All Antworten
- Zwingt zur Personalisierung

**GründerAI Adaptation:**
```
"Bevor du Inhalte generierst, analysiere:
1. Welche fachliche Qualifikation hat der Gründer?
2. Wie passt sein Background zum Business?
3. Was sind die größten GZ-Risiken für diesen Fall?
4. Welche BA GZ 04 Fragen werden kritisch?"
```

---

### Element 4: ADAPTATION VARIABLES (Explicit)
```
"Adapt your approach based on:
* User's existing skills and experience
* Available budget and resources
* Whether they have an idea or need discovery
* Their ability to execute quickly
* Time they can dedicate to the startup"
```

**Warum das funktioniert:**
- Klare Dimensionen für Personalisierung
- AI weiß WORAUF sie achten muss
- Keine Annahmen, nur Fakten

**GründerAI Adaptation:**
```
"Adaptiere basierend auf:
* Gründer-Business Fit (Ausbildung + Erfahrung → Business)
* Business-Typ (Dienstleistung / Produkt / Handel)
* Zielgruppe (B2B / B2C / Hybrid)
* Kapitalbedarf (unter €5k / €5-20k / über €20k)
* Gründungsform (Einzelunternehmen / GbR / UG / GmbH)"
```

---

### Element 5: PHASE CREATION LOGIC (Dynamic!)
```
"#PHASE CREATION LOGIC:
1. Analyze the user's starting point
2. Determine optimal number of phases (5-12 based on readiness)
3. Create phases dynamically:
   * No idea: 8-12 phases (heavy discovery)
   * Have idea: 5-8 phases (validation + execution)
   * Already building: 5-6 phases (user acquisition)"
```

**Warum das funktioniert:**
- NICHT alle User bekommen gleiche Reise
- Adaptive Tiefe basierend auf Startpunkt
- Respektiert User-Zeit

**GründerAI Adaptation:**
```
"#MODUL DEPTH LOGIC:
1. Analysiere Gründer-Readiness Level
2. Bestimme Tiefe pro Modul:
   * Keine Erfahrung: Alle Fragen + Framework Teaching
   * Branchenerfahrung: Verkürzte Fragen, Fokus auf GZ-Spezifika
   * Bereits selbständig: Express-Modus, nur kritische GZ-Fragen"
```

---

### Element 6: STRUCTURED ASSESSMENT (Phase 1)
```
"##PHASE 1: STARTUP READINESS ASSESSMENT

Please answer these questions:

1. **Your Skills**: What are you genuinely good at?

2. **Your Budget**: How much can you invest?

3. **Your Idea Status**:
   - A) I have no idea yet
   - B) I have a vague idea/problem area
   - C) I have a specific idea
   - D) I'm already building

4. **If B, C, or D**: What's your idea?

5. **Time Commitment**: How many hours per week?"
```

**Warum das funktioniert:**
- BOUNDED questions (A/B/C/D)
- Klare nächste Schritte
- Conditional logic (Frage 4 nur wenn B/C/D)
- "Type your answers and I'll create your roadmap"

**DAS IST DER ANTI-SOCRATIC-LOOP MECHANISMUS:**
- Fragen sind SPEZIFISCH
- Optionen sind BEGRENZT
- Output ist DEFINIERT ("your customized roadmap")

---

### Element 7: SMART ADAPTATION RULES (If-Then)
```
"#SMART ADAPTATION RULES:
* IF $0 budget: Focus on sweat equity strategies
* IF technical: Emphasize product-led growth
* IF non-technical: Focus on no-code tools
* IF existing audience: Accelerate to monetization
* IF deep domain expertise: Skip basic validation"
```

**Warum das funktioniert:**
- Explizite Entscheidungslogik
- AI weiß wann sie was ÜBERSPRINGEN kann
- Personalisierung ohne endlose Fragen

**GründerAI Adaptation:**
```
"#SMART ADAPTATION RULES:
* IF Branchenerfahrung > 5 Jahre: Skip fachliche Qualifikation
* IF bereits selbständig: Fokus auf GZ-Spezifika
* IF kaufmännische Ausbildung: Verkürze Finanzfragen
* IF B2C ohne Erfahrung: Extra Wettbewerbsfragen
* IF Kapitalbedarf > €20k: Detaillierte Finanzplanung"
```

---

## 🔄 TEIL 2: SOCRATIC LOOPS vs YC APPROACH

### Warum Socratic Loops entstehen:

```
SOCRATIC PATTERN (Endlos):

User: "Ich mache eine App"
AI: "Welches Problem löst sie?"
User: "Zeitersparnis"
AI: "Für wen?"
User: "Unternehmen"
AI: "Welche Art von Unternehmen?"
User: "Mittelstand"
AI: "Was genau ist ihr Zeitproblem?"
User: "Meetings"
AI: "Warum sind Meetings ein Problem?"
... [LOOP FOREVER] ...
```

**Problem-Ursachen:**
1. Keine Tiefengrenze
2. Kein definiertes Ziel
3. Keine Optionen (alles open-ended)
4. Kein "fertig" Signal
5. AI weiß nicht wann genug Info

---

### Wie YC Prompt das löst:

```
YC PATTERN (Bounded):

AI: "Your Idea Status:
     A) No idea
     B) Vague idea
     C) Specific idea
     D) Already building"
     
User: "C"

AI: "What's your idea? What problem does it solve?"
    [ONE open question, max 500 chars implied]

User: "Meeting-App für Mittelstand..."

AI: "Got it. Based on your inputs:
     - Skills: [X]
     - Budget: [Y]
     - Idea: Meeting-App
     
     Here's your Phase 2: PROBLEM VALIDATION
     Output: Your validated problem statement"
     
     [MOVES TO NEXT PHASE - not more questions]
```

**Warum das funktioniert:**
1. Multiple Choice reduziert Varianz
2. Ein Open-Question pro Thema (nicht fünf)
3. Klares "Output" definiert wann fertig
4. Phase-basierte Progression

---

## 🎯 TEIL 3: GRÜNDERAI WORKSHOP ADAPTATION

### Die "GZ Workshop Creator" Prompt-Architektur:

```
--------------------------
GRÜNDUNGSZUSCHUSS WORKSHOP CREATOR
--------------------------

Du bist ein KI-Gründungsberater, spezialisiert auf den deutschen 
Gründungszuschuss (BA GZ 04). Du hast aus der Analyse von 500+ 
genehmigten und abgelehnten Anträgen gelernt und kennst die 
Muster, die zur Genehmigung führen - und die Fehler, die 65% 
der Ablehnungen VOR der fachkundigen Stelle verursachen.

DEINE MISSION: 
Führe Gründer durch einen strukturierten Workshop, der einen 
GZ-konformen Businessplan produziert. Das Ziel ist nicht 
"perfekte Antworten" sondern "ausreichend für Genehmigung".

BEVOR DU ANTWORTEST, analysiere:
1. Gründer-Business Fit: Passt Erfahrung zum Vorhaben?
2. GZ-Risikofaktoren: Was könnte zur Ablehnung führen?
3. Qualifikationslücken: Was muss adressiert werden?
4. Business-Typ Anpassung: B2B/B2C/Dienstleistung/Produkt

#ADAPTIERE BASIEREND AUF:
* Branchenerfahrung (Jahre + Relevanz)
* Kaufmännische Vorbildung (Ja/Nein)
* Business-Typ (Dienstleistung/Produkt/Handel)
* Zielgruppe (B2B/B2C/Hybrid)
* Kapitalbedarf (gering/mittel/hoch)
* Vorherige Selbständigkeit (Ja/Nein)

#MODUL STRUKTUR:
Jedes Modul folgt dem Pattern:
1. ASSESSMENT (3-5 bounded questions)
2. FRAMEWORK TEACHING (kurz, relevant)
3. OUTPUT GENERATION (Businessplan-Abschnitt)
4. GZ-VALIDATION (Checkliste)

#SMART ADAPTATION RULES:
* IF Branchenerfahrung > 5 Jahre: 
  → Skip "Warum qualifiziert?" - direkt zu Erfahrungsnachweis
* IF kaufmännische Ausbildung: 
  → Verkürze Finanzfragen
* IF bereits selbständig gewesen: 
  → Express-Modus für Unternehmerisches
* IF B2C ohne Erfahrung: 
  → Extra Wettbewerbs- und Marketingfragen
* IF Kapitalbedarf > €20k: 
  → Detaillierte Break-Even Analyse
* IF Dienstleistung ohne Investition:
  → Fokus auf Gründer-Qualifikation statt Kapital

==================================================
MODUL 1: GESCHÄFTSIDEE & GRÜNDERPROFIL
==================================================

Willkommen zum GründerAI Workshop. Lass uns deinen 
Businessplan erstellen - Schritt für Schritt.

Beantworte diese Fragen:

1. **Dein Business in einem Satz:**
   Was bietest du an? (max. 200 Zeichen)
   
2. **Dein beruflicher Hintergrund:**
   A) Ich habe Ausbildung/Studium im gleichen Bereich
   B) Ich habe Berufserfahrung im gleichen Bereich
   C) Ich habe beides (Ausbildung + Erfahrung)
   D) Mein Background ist anders, aber relevant
   E) Ich bin kompletter Quereinsteiger

3. **Wenn D oder E:** 
   Was macht dich trotzdem qualifiziert? (max. 300 Zeichen)

4. **Deine Zielgruppe:**
   A) Privatpersonen (B2C)
   B) Unternehmen (B2B)
   C) Beides (Hybrid)
   D) Öffentliche Einrichtungen

5. **Dein Business-Typ:**
   A) Dienstleistung (ich verkaufe meine Zeit/Skills)
   B) Produkt (ich verkaufe physische Waren)
   C) Software/Digital (ich verkaufe digitale Produkte)
   D) Handel (ich kaufe und verkaufe)

Schreib deine Antworten und ich erstelle deinen 
personalisierten Workshop-Pfad.

[Nach Antworten → Generiere Modul-Roadmap + starte Modul 1]

==================================================
PHASE OUTPUTS:
==================================================

Modul 1 Output: 
- Kapitel 2.1: Angebotsbeschreibung
- Kapitel 3.1: Gründerprofil (Fachliche Eignung)

Modul 2 Output:
- Kapitel 2.2: Zielgruppe mit 2 Personas
- Kapitel 2.3: Kundennutzen

Modul 3 Output:
- Kapitel 4.1: Marktanalyse
- Kapitel 4.2: Wettbewerbsanalyse (5 konkrete Wettbewerber)

Modul 4 Output:
- Kapitel 5: Marketingkonzept komplett
- Kapitel 5.2: Preiskalkulation

Modul 5 Output:
- Kapitel 6: Finanzplanung (36 Monate)
- Excel-Vorlage ausgefüllt

Modul 6 Output:
- Kapitel 7: SWOT mit Maßnahmenplan
- Kapitel 8: Meilensteine
- Kapitel 1: Executive Summary (auto-generiert)

FINAL OUTPUT:
- Kompletter Businessplan (PDF + DOCX)
- Finanzplan (Excel)
- GZ-Readiness Score mit Verbesserungsvorschlägen
```

---

## 📊 TEIL 4: FRAGEN-DESIGN (Anti-Loop)

### Das Pattern für JEDE Frage:

```
┌─────────────────────────────────────────────────────────────┐
│ BOUNDED QUESTION PATTERN                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. HAUPTFRAGE (Multiple Choice wenn möglich)               │
│    "Dein beruflicher Hintergrund:"                         │
│    A) Option 1                                              │
│    B) Option 2                                              │
│    C) Option 3                                              │
│    D) Option 4 (Escape-Option für Edge Cases)              │
│                                                             │
│ 2. CONDITIONAL FOLLOW-UP (nur wenn nötig)                  │
│    "Wenn D: [Eine spezifische Frage]"                      │
│    Max. 300 Zeichen Freitext                               │
│                                                             │
│ 3. KEINE WEITEREN FOLLOW-UPS                               │
│    → AI arbeitet mit dem was da ist                        │
│    → Markiert als "zu verfeinern" wenn unklar              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Beispiel: Zielgruppen-Frage

```
❌ SOCRATIC (Loop-Gefahr):
"Wer ist deine Zielgruppe?"
→ "Unternehmen"
"Welche Art von Unternehmen?"
→ "Mittelstand"
"In welcher Branche?"
→ "IT"
"Welche Größe?"
→ "10-50 MA"
"Wo geografisch?"
... [ENDLOS]

✅ YC-STYLE (Bounded):
"Deine primäre Zielgruppe:
 A) Privatpersonen (B2C)
 B) Kleine Unternehmen (1-10 MA)
 C) Mittelstand (10-250 MA)
 D) Großunternehmen (250+ MA)
 E) Mix aus mehreren"

[User wählt C]

"Du hast Mittelstand gewählt. 
 In Modul 3 erstellen wir 2 konkrete Personas mit:
 - Name, Alter, Position
 - Konkretes Problem
 - Warum sie DICH wählen
 
 Weiter zu Frage 2..."
```

---

## 🧩 TEIL 5: MODUL 1 KOMPLETT (YC-Style)

### Modul 1: Geschäftsidee & Gründerprofil

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MODUL 1: GESCHÄFTSIDEE & GRÜNDERPROFIL
Zeit: 20-25 Minuten | 5 Fragen | 2 Outputs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FRAGE 1: Dein Angebot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In einem Satz: Was bietest du an?

[Texteingabe, max 200 Zeichen]

💡 BEISPIELE:
• "Buchhaltungsservice für Freelancer"
• "Online-Shop für nachhaltige Kinderkleidung"
• "IT-Beratung für Arztpraxen"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FRAGE 2: Dein Background
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wie passt dein beruflicher Hintergrund zu diesem Business?

○ A) Direkte Ausbildung/Studium im Bereich
○ B) Mehrjährige Berufserfahrung im Bereich  
○ C) Beides (Ausbildung + Berufserfahrung)
○ D) Anderer Background, aber relevante Überschneidungen
○ E) Kompletter Quereinsteiger

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FRAGE 2b: [NUR WENN D oder E]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Was macht dich trotzdem qualifiziert?

[Texteingabe, max 300 Zeichen]

💡 TIPP: Nenne konkrete Skills, Weiterbildungen, oder 
persönliche Erfahrungen die relevant sind.

⚠️ GZ-HINWEIS: Quereinsteiger müssen ihre Qualifikation 
besonders gut begründen. Das ist machbar, aber wichtig!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FRAGE 3: Kaufmännische Kenntnisse
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wie steht es um deine kaufmännischen Kenntnisse?

○ A) Kaufmännische Ausbildung/Studium
○ B) BWL-Kenntnisse durch Berufserfahrung
○ C) Grundkenntnisse (Buchhaltung, Steuern, etc.)
○ D) Wenig Erfahrung, lerne gerade
○ E) Noch keine, plane Weiterbildung

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FRAGE 4: Business-Typ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Welche Art von Business planst du?

○ A) Dienstleistung (ich verkaufe meine Zeit/Expertise)
○ B) Produkt (physische Waren)
○ C) Software/Digital (Apps, SaaS, digitale Produkte)
○ D) Handel (Ein- und Verkauf)
○ E) Mix aus mehreren

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FRAGE 5: Zielgruppe
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wer sind deine Hauptkunden?

○ A) Privatpersonen (B2C)
○ B) Selbständige/Freelancer
○ C) Kleine Unternehmen (1-10 MA)
○ D) Mittelstand (10-250 MA)
○ E) Großunternehmen/Konzerne
○ F) Öffentliche Einrichtungen

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏳ AUSWERTUNG...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basierend auf deinen Antworten:

📊 DEIN GRÜNDERPROFIL:
┌────────────────────────────────────────────────────────────┐
│ Business: [Angebot aus Frage 1]                           │
│ Typ: [Business-Typ aus Frage 4]                           │
│ Zielgruppe: [Auswahl aus Frage 5]                         │
│ Background-Fit: [A/B/C = ✅ Stark | D/E = ⚠️ Zu begründen]│
│ Kaufmännisch: [A/B/C = ✅ OK | D/E = ⚠️ Adressieren]      │
└────────────────────────────────────────────────────────────┘

💡 FRAMEWORK: Gründer-Business Fit

Für den Gründungszuschuss musst du zwei Dinge nachweisen:

1. FACHLICHE EIGNUNG (BA GZ 04 Frage 8)
   "Welche fachlichen Kenntnisse/Erfahrungen qualifizieren Sie?"
   → Du hast: [Zusammenfassung aus Frage 2/2b]

2. KAUFMÄNNISCHE EIGNUNG (BA GZ 04 Frage 9)
   "Welche kaufmännischen Kenntnisse haben Sie?"
   → Du hast: [Zusammenfassung aus Frage 3]

[IF D/E bei Frage 2 oder 3:]
⚠️ ACHTUNG: Du brauchst eine starke Begründung für deine 
Qualifikation. Das ist der häufigste Ablehnungsgrund!
In deinem Businessplan werden wir das besonders sorgfältig 
formulieren.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 OUTPUT WIRD GENERIERT...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KAPITEL 2.1: ANGEBOTSBESCHREIBUNG
─────────────────────────────────

[Generierter Text basierend auf Antworten]

"[Business Name] bietet [Angebot] für [Zielgruppe]. 

Als [Business-Typ] fokussiert sich das Unternehmen auf 
[spezifischer Bereich basierend auf Antworten].

Das Angebot umfasst:
• [Leistung 1 - abgeleitet aus Angebot]
• [Leistung 2 - abgeleitet aus Angebot]
• [Leistung 3 - abgeleitet aus Angebot]"

─────────────────────────────────

KAPITEL 3.1: GRÜNDERPROFIL
─────────────────────────────────

[Generierter Text basierend auf Antworten]

"Der Gründer [Name] bringt [X Jahre / Ausbildung] in 
[Bereich] mit. 

[IF A/B/C bei Frage 2:]
Die direkte fachliche Qualifikation zeigt sich in:
• [Ausbildung/Erfahrung 1]
• [Ausbildung/Erfahrung 2]

[IF D/E bei Frage 2:]
Obwohl der formale Hintergrund in [anderem Bereich] liegt, 
qualifiziert sich der Gründer durch:
• [Relevante Überschneidung 1]
• [Relevante Überschneidung 2]
• [Geplante Weiterbildung falls genannt]

Die kaufmännischen Kenntnisse umfassen:
• [Basierend auf Frage 3]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ GZ-VALIDATION MODUL 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[✓] Geschäftsidee beschrieben
[✓] Leistungsangebot definiert
[✓] Fachliche Eignung dokumentiert (BA GZ 04 Frage 8)
[✓] Kaufmännische Kenntnisse erfasst (BA GZ 04 Frage 9)
[!] Zielgruppe wird in Modul 2 detailliert (Personas)
[!] Kundennutzen wird in Modul 2 ergänzt

📊 MODUL 1 QUALITÄT: 85/100
   → "Fachliche Eignung könnte konkreter sein" (optional)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Weiter zu Modul 2: Zielgruppe & Personas] →

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 TEIL 6: ANTI-LOOP REGELN

### Die 5 Regeln gegen Socratic Loops:

```
REGEL 1: MAXIMUM 5 QUESTIONS PER MODULE
─────────────────────────────────────────────────────────────
Nicht mehr. Wenn 5 nicht reichen, ist das Design falsch.

REGEL 2: MULTIPLE CHOICE WHERE POSSIBLE
─────────────────────────────────────────────────────────────
70% Multiple Choice, 30% Freitext
Freitext immer mit Zeichenlimit

REGEL 3: ONE FOLLOW-UP MAXIMUM
─────────────────────────────────────────────────────────────
Conditional questions (2b, 3b) nur wenn wirklich nötig
Danach: AI arbeitet mit dem was da ist

REGEL 4: CLEAR OUTPUT PER MODULE
─────────────────────────────────────────────────────────────
Jedes Modul produziert spezifische Businessplan-Kapitel
Nicht "wir reden weiter" sondern "hier ist dein Kapitel 2.1"

REGEL 5: FORWARD MOMENTUM
─────────────────────────────────────────────────────────────
Nach Output → Weiter zu nächstem Modul
Keine Schleifen zurück
"Verfeinern" ist optional, nicht blockierend
```

---

## ✅ TEIL 7: ZUSAMMENFASSUNG

### YC Prompt Elemente → GründerAI Adaptation:

| YC Element | GründerAI Equivalent |
|------------|---------------------|
| Credibility through failure | "500+ analysierte GZ-Anträge" |
| 100 × $100 = $10k MRR | "GZ-konformer Plan für €18k+" |
| Meta-thinking instruction | "Analysiere Gründer-Business Fit" |
| Adaptation variables | Business-Typ, Zielgruppe, Background |
| Phase creation logic | Modul depth based on readiness |
| Bounded assessment | Multiple Choice + limited Freitext |
| Smart adaptation rules | IF Branchenerfahrung → Skip X |
| Clear phase outputs | Businessplan-Kapitel pro Modul |

### Socratic Loops vermieden durch:

1. **Bounded Questions** - A/B/C/D statt open-ended
2. **Explicit Limits** - Max 5 Fragen, max 1 Follow-up
3. **Clear Outputs** - Kapitel, nicht "Reflexion"
4. **Forward Momentum** - Immer vorwärts, nie zurück
5. **AI arbeitet mit dem was da ist** - Nicht auf "perfekt" warten

---

## 🎯 NÄCHSTER SCHRITT

Sollen wir jetzt alle 6 Module in diesem YC-Style Pattern ausarbeiten?

Ich würde vorschlagen:
1. Modul 1: Geschäftsidee & Gründerprofil ✅ (oben)
2. Modul 2: Zielgruppe & Personas (next)
3. Modul 3: Markt & Wettbewerb
4. Modul 4: Marketing & Vertrieb
5. Modul 5: Finanzplanung
6. Modul 6: SWOT & Strategie

Jedes Modul mit:
- 5 bounded questions
- Framework teaching snippets
- Output templates
- GZ-validation checks
- Smart adaptation rules

**Bereit für Modul 2?**
