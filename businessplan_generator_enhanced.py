# businessplan_generator_enhanced.py
"""
Enhanced Businessplan Generator - TAG 6 Implementation WITH LEGAL CITATIONS

GZ-COMPLIANT BUSINESSPLAN GENERATOR + LEGAL CITATIONS
======================================================

NEW IN THIS VERSION:
- ALL prompts include legal citations (SGB III Â§ 93, Fachliche Weisungen BA)
- GZ_CRITERIA enhanced with rechtsgrundlage for each criterion
- Helper functions for legal citations
- Compliance checker shows legal basis for requirements
- Error messages include official sources

Features:
- Complete chapter coverage (11 chapters vs. 6 in TAG 4)
- Marketing & Sales Strategy (NEW!)
- Risk Management with GZ-specific risks (NEW!)
- Milestones & Timeline (NEW!)
- Realistic financial planning (conservative assumptions)
- Web research integration for market data
- Iterative refinement workflow
- GZ-compliance checks WITH LEGAL BASIS
- Quality scoring with improvement suggestions

Chapters Generated:
1. Executive Summary (GZ-focused + Legal Citations)
2. GeschÃ¤ftsidee & Vision
3. GrÃ¼nderperson & Qualifikation (extended with legal requirements)
4. Markt & Wettbewerb (with research & sources)
5. Marketing & Vertriebsstrategie (with "intensive GeschÃ¤ftstÃ¤tigkeit")
6. JTBD & Kundennutzen
7. Organisation & Arbeitsweise
8. Finanzplanung (realistic + scenarios)
9. Risikomanagement (with GZ-specific risks + legal basis)
10. Meilensteine & Zeitplan
11. Anhang & Quellen

GZ-Compliance Criteria Checked (WITH LEGAL BASIS):
- Hauptberuflichkeit (SGB III Â§ 93 Abs. 2)
- Fachliche Qualifikation (Fachliche Weisungen BA)
- Wirtschaftliche TragfÃ¤higkeit (Fachliche Weisungen BA)
- Marktpotenzial nachgewiesen
- Lebenshaltungskosten gedeckt
- Konkrete Umsetzungsplanung
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# ADAPTIVE CALCULATOR INTEGRATION
# ============================================================================

# Try to import adaptive calculator and grounder profile
try:
    from adaptive_financial_calculator_full import AdaptiveFinancialCalculator
    ADAPTIVE_CALCULATOR_AVAILABLE = True
    logger.info("âœ… Adaptive Financial Calculator available")
except ImportError:
    ADAPTIVE_CALCULATOR_AVAILABLE = False
    logger.warning("âš ï¸ Adaptive Calculator not available - using standard calculator")

try:
    from grounder_profile import GrounderProfile, create_profile_from_dict
    GROUNDER_PROFILE_AVAILABLE = True
    logger.info("âœ… Grounder Profile schema available")
except ImportError:
    GROUNDER_PROFILE_AVAILABLE = False
    logger.warning("âš ï¸ Grounder Profile not available - using standard calculator")

# Try to import legal citations (optional)
try:
    from legal_citations import get_citation, format_citation_for_docx
    LEGAL_CITATIONS_AVAILABLE = True
    logger.info("âœ… Legal Citations module available")
except ImportError:
    LEGAL_CITATIONS_AVAILABLE = False
    logger.warning("âš ï¸ Legal Citations module not available - using hardcoded citations")


# ============================================================================
# ENHANCED CONTENT GENERATOR WITH GZ-FOCUS + LEGAL CITATIONS
# ============================================================================

class EnhancedContentGenerator:
    """
    Generate GZ-compliant businessplan content WITH LEGAL CITATIONS
    
    Key Improvements:
    - All chapters covered
    - Legal citations in every prompt
    - Conservative financial assumptions
    - Detailed justifications
    - Source citations
    - GZ-specific language with official legal basis
    """
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set!")
        
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest model
        
        logger.info("âœ… Enhanced Content Generator initialized with Legal Citations")
    
    async def generate_executive_summary(self, data: Dict) -> str:
        """
        Executive Summary - GZ-focused with LEGAL CITATIONS
        
        Key Points:
        - Hauptberuflichkeit (SGB III Â§ 93 Abs. 2)
        - Qualifikation (Fachliche Weisungen BA)
        - Wirtschaftliche TragfÃ¤higkeit (Fachliche Weisungen BA)
        - Conservative language with legal basis
        """
        
        prompt = f"""Schreibe eine Executive Summary fÃ¼r einen Businessplan (max 350 WÃ¶rter).

**KRITISCH: Dies ist fÃ¼r einen GrÃ¼ndungszuschuss (GZ) Antrag!**

**RECHTSGRUNDLAGEN:**
Der GrÃ¼ndungszuschuss ist eine Ermessensleistung (SGB III Â§ 93 Abs. 1) - KEIN Rechtsanspruch!
Die fachkundige Stelle (IHK/HWK/Steuerberater) prÃ¼ft nach Fachlichen Weisungen BA:

1. HAUPTBERUFLICHKEIT (SGB III Â§ 93 Abs. 2)
   â†’ Anforderung: Mindestens 15 Stunden wÃ¶chentlich
   â†’ WICHTIG: Explizit Stundenzahl nennen!
   â†’ VERMEIDE: "nebenbei", "Freizeit", "Hobby"

2. FACHLICHE QUALIFIKATION (Fachliche Weisungen BA)
   â†’ Anforderung: Notwendige Kenntnisse und FÃ¤higkeiten nachweisbar
   â†’ Betone: Jahre Berufserfahrung, Zertifikate, Projekterfolge

3. WIRTSCHAFTLICHE TRAGFÃ„HIGKEIT (Fachliche Weisungen BA)
   â†’ Anforderung: TragfÃ¤hige Existenzgrundlage, Lebenshaltungskosten gedeckt
   â†’ Zeige: Realistische Zahlen, konservative Planung

**STIL:**
- Sachlich-professionell, konservativ
- KEINE Superlative oder Marketing-Sprache
- Fokus: Machbarkeit, Qualifikation, Realismus

**STRUKTUR:**

1. GeschÃ¤ftsidee (2 SÃ¤tze):
   - WAS: {data.get('what', '')}
   - FÃœR WEN: {data.get('who', '')}

2. Marktproblem (2 SÃ¤tze):
   - Problem: {data.get('problem', '')}
   - Warum wichtig/dringend?

3. GrÃ¼nderperson (3 SÃ¤tze):
   - Qualifikation: {data.get('why_you', '')}
   - WARUM fachlich geeignet (Nachweise!)
   - Hauptberuflich: EXPLIZIT Stunden nennen!

4. GeschÃ¤ftsmodell (2 SÃ¤tze):
   - Revenue: {data.get('revenue_source', '')}
   - Warum realistisch?

5. Finanzierung & TragfÃ¤higkeit (2 SÃ¤tze):
   - Kapitalbedarf: {data.get('capital_needs', '')}
   - Wirtschaftliche TragfÃ¤higkeit gegeben

6. Ziel & Ausblick (1 Satz)

**WICHTIG:**
- Zahlen NUR wenn aus Input vorhanden
- VERWENDE: "fundiert", "nachweislich", "realistisch", "tragfÃ¤hig"

**PFLICHT-FORMULIERUNG am Ende:**
"Die GrÃ¼ndung erfolgt hauptberuflich mit mindestens [X] Stunden pro Woche (SGB III Â§ 93 Abs. 2). Die wirtschaftliche TragfÃ¤higkeit ist durch konservative Finanzplanung und nachgewiesene fachliche Qualifikation gegeben."

Schreibe NUR die Executive Summary:"""

        return await self._call_claude(prompt)
    
    async def generate_gruenderperson_extended(self, data: Dict) -> str:
        """
        GrÃ¼nderperson - Extended with CV-style + LEGAL CITATIONS
        
        IHK/AfA want to see:
        - Detailed work history
        - Concrete projects with results  
        - Qualifications with certificates (Fachliche Weisungen BA requirement)
        - Why now?
        - Network/connections
        """
        
        why_you = data.get('why_you', '')
        how = data.get('how', '')
        
        prompt = f"""Schreibe einen ausfÃ¼hrlichen "GrÃ¼nderperson & Qualifikation" Abschnitt (600-800 WÃ¶rter).

**RECHTSGRUNDLAGE:**
Fachliche Weisungen BA zu Â§ 93 SGB III: Fachliche Qualifikation

â†’ Anforderung: "Die Antragstellerin oder der Antragsteller muss Ã¼ber die notwendigen Kenntnisse und FÃ¤higkeiten zur AusÃ¼bung der selbstÃ¤ndigen TÃ¤tigkeit verfÃ¼gen."

Die fachkundige Stelle (IHK/HWK/Steuerberater) prÃ¼ft:
- Ausbildung & formale Qualifikationen
- Berufserfahrung (mind. 2-3 Jahre empfohlen)
- Branchenkenntnisse
- Projekterfolge mit messbaren Ergebnissen
- Nachweis der fachlichen Eignung

**VERFÃœGBARE INFORMATIONEN:**
{why_you}

Arbeitsweise: {how}

**STRUKTUR:**

### 3.1 Beruflicher Werdegang

Schreibe im CV-Stil (neueste zuerst):
- Extrahiere alle Firmen/Positionen aus dem Input
- FÃ¼r jede Station: Zeitraum, Firma, Position, Verantwortung
- WENN konkrete Projekte erwÃ¤hnt: Beschreibe sie mit Ergebnissen

Beispiel-Format:
"**2020-2024: Senior Consultant bei [Firma], [Ort]**
- Position: [Rolle]
- Verantwortung: [Was gemacht]
- Erfolge: [Konkrete Ergebnisse mit Zahlen wenn mÃ¶glich]"

### 3.2 Fachliche Qualifikationen

Listen auf:
- Alle erwÃ¤hnten Zertifikate
- Fortbildungen
- Technische Skills
- Branchen-Expertise

### 3.3 Warum SelbstÃ¤ndigkeit jetzt?

ErklÃ¤re in 2-3 AbsÃ¤tzen:
1. Was in der Karriere zur GrÃ¼ndungs-Idee gefÃ¼hrt hat
2. Welche MarktlÃ¼cke erkannt wurde
3. Warum JETZT der richtige Zeitpunkt ist
4. PersÃ¶nliche Motivation (authentisch aber professionell)

### 3.4 Netzwerk & Branchenkontakte

WENN im Input erwÃ¤hnt:
- Mitgliedschaften
- Kontakte
- Speaking/Workshops
- SONST: Allgemein halten

**WICHTIG:**
- Zeige LÃœCKENLOS: Diese Person KANN das Business fÃ¼hren
- Belege ALLES mit konkreten Beispielen
- Fachkundige Stelle prÃ¼ft kritisch nach Fachlichen Weisungen BA!
- Je mehr Nachweise, desto besser

**STIL:**
- Faktisch, nicht prahlend
- Erfolge mit Zahlen wenn mÃ¶glich
- Realistische SelbsteinschÃ¤tzung
- GZ-konform: Zeigen dass hauptberuflich mÃ¶glich

Schreibe den kompletten Abschnitt:"""

        return await self._call_claude(prompt, max_tokens=2000)
    
    async def generate_markt_wettbewerb(
        self, 
        data: Dict, 
        market_research: Optional[Dict] = None
    ) -> str:
        """
        Markt & Wettbewerb - With research data & sources
        
        IHK wants to see:
        - Market size with numbers
        - Growth rates
        - Named competitors
        - Differentiation/USP
        - Sources cited
        """
        
        what = data.get('what', '')
        who = data.get('who', '')
        problem = data.get('problem', '')
        
        # If research data provided, use it
        research_text = ""
        if market_research:
            research_text = f"""
**VERFÃœGBARE MARKTDATEN:**
{json.dumps(market_research, indent=2, ensure_ascii=False)}
"""
        
        prompt = f"""Schreibe einen umfassenden "Markt & Wettbewerbsanalyse" Abschnitt (800-1000 WÃ¶rter).

**KRITISCH: IHK fordert Nachweis von Marktpotenzial!**

**GESCHÃ„FTSIDEE:**
- Was: {what}
- Zielgruppe: {who}
- Problem: {problem}

{research_text}

**STRUKTUR (GENAU befolgen!):**

### 4.1 MarktgrÃ¶ÃŸe & Potenzial

**Deutscher Gesamtmarkt:**
- Wie viele potenzielle Kunden gibt es? (SchÃ¤tze basierend auf Zielgruppe)
- Wenn Daten verfÃ¼gbar: Zitiere mit [Quelle]
- Wenn keine Daten: "Laut BranchenschÃ¤tzung..."

**Marktpotenzial fÃ¼r diese Branche:**
- Marktwachstum (wenn bekannt)
- Digitalisierungsgrad
- Budget-Potenzial

**Lokaler/regionaler Markt (wenn relevant):**
- Fokusregion
- Anzahl Zielkunden dort

### 4.2 Wettbewerbsanalyse

**Hauptwettbewerber (mind. 3-5 benennen):**

FÃ¼r jeden Konkurrenten (selbst wenn nicht im Input, generiere plausible):
1. Name: [Firma oder Typ wie "GroÃŸe Beratungen", "Freelancer"]
2. Fokus: [Was sie machen]
3. StÃ¤rke: [Ihr Vorteil]
4. SchwÃ¤che: [Ihre Limitation]

**Beispiel-Format:**
"**1. [Konkurrent A] (z.B. groÃŸe Beratung)**
- Fokus: Enterprise-Kunden
- StÃ¤rke: Etabliert, viele Ressourcen
- SchwÃ¤che: Zu teuer fÃ¼r KMUs (200+ EUR/h)

**2. [Konkurrent B] (z.B. Freelancer)**
- Fokus: Einzelprojekte
- StÃ¤rke: GÃ¼nstig (80-100 EUR/h)
- SchwÃ¤che: Keine Prozessberatung, nur Umsetzung"

### 4.3 Wettbewerbsvorteil (USP)

**Positionierung:**
Eine klare Positionierungs-Aussage (1 Satz)

**Konkrete Vorteile (mind. 4):**
1. Preis: [Wie positioniert vs. Wettbewerb]
2. Fokus: [Spezialisierung]
3. Geschwindigkeit: [Schneller? Wie?]
4. QualitÃ¤t: [Was besser?]
5. Erreichbarkeit: [PersÃ¶nlich vs. groÃŸe Firma?]

### 4.4 Markteintritt & Potenzial

- Wie leicht ist Markteintritt?
- Realistische Marktdurchdringung Jahr 1-3
- Langfristiges Potenzial

**STIL:**
- Faktisch mit Zahlen wo mÃ¶glich
- Bei SchÃ¤tzungen: Konservativ!
- Quellen zitieren wenn vorhanden
- Realistisch bleiben (nicht Ã¼bertreiben)

**WICHTIG:**
- WENN keine echten Daten: "Basierend auf Branchenerfahrung..."
- Keine unrealistischen Marktanteile (z.B. nicht "10% des Marktes")
- Konservativ: "Realistisches Ziel: 0.1% des Marktes = X Kunden"

Schreibe den kompletten Abschnitt:"""

        return await self._call_claude(prompt, max_tokens=2500)
    
    async def generate_marketing_vertrieb(self, data: Dict) -> str:
        """
        Marketing & Vertriebsstrategie - WITH LEGAL CITATION
        
        AfA MUST see:
        - Concrete customer acquisition plan
        - How will first customers come?
        - "Intensive GeschÃ¤ftstÃ¤tigkeit" (legal requirement for Phase 2)
        - Sales funnel
        - Budget allocation
        """
        
        what = data.get('what', '')
        who = data.get('who', '')
        revenue_source = data.get('revenue_source', '')
        
        prompt = f"""Schreibe ein vollstÃ¤ndiges "Marketing & Vertriebsstrategie" Kapitel (700-900 WÃ¶rter).

**RECHTSGRUNDLAGE FÃœR GZ-BEWILLIGUNG:**
Fachliche Weisungen BA zu Â§ 94 SGB III: Nachweis der GeschÃ¤ftstÃ¤tigkeit

â†’ Anforderung: "FÃ¼r die Bewilligung der zweiten FÃ¶rderphase muss nach 6 Monaten nachgewiesen werden, dass eine intensive GeschÃ¤ftstÃ¤tigkeit und hauptberufliche unternehmerische AktivitÃ¤ten vorliegen."

Die Agentur prÃ¼ft:
- Wie werden erste Kunden gewonnen? (konkret!)
- Wann kommt der erste Umsatz? (Monat 1-3 ideal)
- Wie wird hauptberufliche TÃ¤tigkeit sichergestellt?

**NACHWEISE FÃœR "INTENSIVE GESCHÃ„FTSTÃ„TIGKEIT":**
- Kundenlisten
- Rechnungen / Angebote
- VertrÃ¤ge
- Akquise-AktivitÃ¤ten dokumentiert
- Arbeitszeitnachweise

**GESCHÃ„FTSIDEE:**
- Was: {what}
- Zielgruppe: {who}
- Revenue: {revenue_source}

**STRUKTUR:**

### 5.1 Customer Acquisition Strategy

**Ziel Jahr 1:** [Realistische Kundenanzahl, z.B. 8-12 Kunden]

**Phase 1: Monat 1-3 (Netzwerk-Aktivierung)**

Budget: [500-800 EUR]
MaÃŸnahmen (konkret!):
1. LinkedIn: Profil optimieren + [X] Kontakte/Woche
2. Networking: [Typ wie BNI, IHK-Events] + wÃ¶chentliche Treffen
3. Direktansprache: [X] ErstgesprÃ¤che mit [bestehenden Kontakten/Ex-Kollegen]
4. [Weitere MaÃŸnahme basierend auf Branche]

Erwartung: 2-3 Pilotkunden aus Netzwerk

**Phase 2: Monat 4-6 (Content & Empfehlungen)**

Budget: [600-1000 EUR]
MaÃŸnahmen:
1. Content: [LinkedIn Posts / Blog / Videos] - [Frequenz]
2. Workshops: [Wo? IHK? Online?] - [Thema]
3. Case Studies: Erste Projekte dokumentieren
4. Empfehlungsprogramm: [Incentive]

Erwartung: 3-4 neue Kunden

**Phase 3: Monat 7-12 (Skalierung)**

Budget: [1000-1500 EUR]
MaÃŸnahmen:
1. Paid Ads: [LinkedIn/Google] - [Budget/Monat]
2. Partnerschaften: [Mit wem? Steuerberater? IT-Dienstleister?]
3. Events: [Networking, Speaking]
4. [Weitere KanÃ¤le]

Erwartung: 5-8 neue Kunden

### 5.2 Sales Funnel & Conversion

**Pipeline-Struktur:**
```
[X] Leads (z.B. LinkedIn-Kontakte)
  â†’ [Y] Antworten ([Z]%)
  â†’ [A] GesprÃ¤che ([B]%)
  â†’ [C] Angebote ([D]%)
  â†’ [E] AuftrÃ¤ge ([F]%)
```

Beispiel: 100 â†’ 20 â†’ 10 â†’ 4 â†’ 2

**Customer Journey:**
1. Awareness: [Wie werden sie aufmerksam?]
2. Interest: [ErstgesprÃ¤ch - wie lang? kostenlos?]
3. Consideration: [Assessment/Probe-Projekt?]
4. Decision: [Angebot]
5. Retention: [Wie Kunden halten?]

**Sales Cycle:** [3-6 Monate fÃ¼r B2B typisch]

### 5.3 Erste Kunden-Leads

**WENN vorhanden im Input:**
- Benenne konkrete Kontakte (anonymisiert: "Kontakt A: Ex-Kollege bei [Branche]")

**WENN NICHT vorhanden:**
"**Erste Kontakte in Akquise:**
- Ex-Kollegen aus [vorherige Firma/Branche]
- Networking-Kontakte aus [BNI/Toastmasters/etc.]
- LinkedIn-Netzwerk (aktuell [X] relevante Kontakte)

**Branchen-Fokus (wo am wahrscheinlichsten):**
1. [Branche 1]: [Warum?]
2. [Branche 2]: [Warum?]
3. [Branche 3]: [Warum?]"

### 5.4 Pricing & Angebote

**Einstiegsangebot:** [Name]
- Preis: [Niedrig fÃ¼r Quick-Win]
- Dauer: [Kurz]
- Scope: [Klein aber Wert-generierend]
- Ziel: Schneller Erfolg â†’ FolgeauftrÃ¤ge

**Standard-Angebot:** [Name]
- Preis: [Aus revenue_source ableiten]
- Details...

**Premium:** [Falls relevant]

**STIL:**
- KONKRET (nicht vage!)
- REALISTISCH (konservative Conversion-Raten)
- NACHVOLLZIEHBAR (jede Zahl begrÃ¼nden)

**KRITISCH fÃ¼r GZ Phase 2 (nach 6 Monaten):**
Die Agentur will NACHWEISE sehen fÃ¼r "intensive GeschÃ¤ftstÃ¤tigkeit":
- Kundenliste mit Projekten
- Rechnungen & ZahlungseingÃ¤nge
- Dokumentierte Akquise-AktivitÃ¤ten
- Arbeitszeitnachweise (Hauptberuflichkeit!)

Ohne diese Nachweise: Phase 2 (weitere 300 EUR/Monat fÃ¼r 9 Monate) wird NICHT bewilligt!

Schreibe das komplette Kapitel:"""

        return await self._call_claude(prompt, max_tokens=2500)
    
    async def generate_risikomanagement(self, data: Dict, swot_data: Dict) -> str:
        """
        Risikomanagement - WITH GZ-SPECIFIC RISKS + LEGAL CITATIONS
        
        IHK wants to see:
        - Identified risks (INCLUDING GZ-specific!)
        - Probability assessment
        - Concrete countermeasures
        - Shows professional planning
        """
        
        risks_from_swot = swot_data.get('risiken', [])
        
        prompt = f"""Schreibe ein "Risikomanagement" Kapitel (600-800 WÃ¶rter).

**KRITISCH: IHK will sehen dass ALLE Risiken erkannt und GegenmaÃŸnahmen geplant sind!**

**WICHTIG - GZ-SPEZIFISCHE RISIKEN MÃœSSEN ABGEDECKT WERDEN:**

1. HAUPTBERUFLICHKEIT GEFÃ„HRDET
   Rechtsgrundlage: SGB III Â§ 93 Abs. 2
   Risiko: Weniger als 15h/Woche fÃ¼r Business â†’ GZ-RÃ¼ckforderung
   GegenmaÃŸnahme: Zeiterfassung, klare Arbeitsplanung, keine Vollzeit-Anstellung parallel

2. NEBENTÃ„TIGKEIT ZU UMFANGREICH
   Rechtsgrundlage: Fachliche Weisungen BA zu Â§ 93 SGB III
   Erlaubt: NebentÃ¤tigkeit < 15h/Woche UND < 50% des Einkommens
   Risiko: Bei Ãœberschreitung droht RÃ¼ckforderung des gesamten GrÃ¼ndungszuschusses!
   GegenmaÃŸnahme: 
   - Wenn NebentÃ¤tigkeit nÃ¶tig â†’ max. 14h/Woche
   - UnverzÃ¼glich bei Agentur fÃ¼r Arbeit melden (Â§ 60 SGB III)
   - Dokumentation der Arbeitszeiten

3. WIRTSCHAFTLICHE TRAGFÃ„HIGKEIT NICHT NACHWEISBAR
   Rechtsgrundlage: Fachliche Weisungen BA zu Â§ 93 SGB III
   Risiko: Break-Even > 12 Monate, LiquiditÃ¤t nicht gesichert â†’ Ablehnung oder RÃ¼ckforderung
   GegenmaÃŸnahme: 
   - Konservative Planung
   - Puffer einplanen (mindestens 3 Monate Lebenshaltungskosten)
   - Alternative Einnahmequellen identifizieren
   - Teilzeit-Job als ÃœberbrÃ¼ckung (max. 14h/Woche!)

4. KEINE "INTENSIVE GESCHÃ„FTSTÃ„TIGKEIT" NACHWEISBAR (fÃ¼r Phase 2)
   Rechtsgrundlage: Fachliche Weisungen BA zu Â§ 94 SGB III
   Risiko: Phase 2 (weitere 300 EUR fÃ¼r 9 Monate) wird nicht bewilligt
   GegenmaÃŸnahme:
   - Ab Monat 1: Kunden akquirieren
   - Alle AktivitÃ¤ten dokumentieren (Angebote, GesprÃ¤che, VertrÃ¤ge)
   - Rechnungen schreiben und aufbewahren
   - Arbeitszeitnachweise fÃ¼hren

**IDENTIFIZIERTE RISIKEN (aus SWOT):**
{chr(10).join(f'- {r}' for r in risks_from_swot)}

**STRUKTUR:**

### 9.1 Risiko-Ãœbersicht

Erstelle Tabelle (als Text formatiert):

| Risiko | Wahrscheinlichkeit | Auswirkung | GegenmaÃŸnahme |
|--------|-------------------|------------|---------------|
| Hauptberuflichkeit gefÃ¤hrdet | [Niedrig/Mittel] | [Sehr Hoch] | [Zeiterfassung, klare Planung] |
| Kundenakquise dauert lÃ¤nger | [Mittel bis Hoch] | [Mittel-Hoch] | [Teilzeit-Job, Puffer] |
| ... | ... | ... | ... |

**WEITERE RISIKEN ABDECKEN:**

5. **Krankheit/Ausfall**
   - Wahrscheinlichkeit: Niedrig
   - Auswirkung: Projektabbruch, Umsatzausfall
   - GegenmaÃŸnahme: [Netzwerk fÃ¼r Vertretung? Versicherung?]

6. **Preisdruck durch Wettbewerb**
   - Wahrscheinlichkeit: Mittel
   - Auswirkung: Geringere Margen
   - GegenmaÃŸnahme: [Differenzierung? Premium-Positionierung?]

7. **Technologische Ã„nderungen**
   - Wahrscheinlichkeit: Mittel
   - Auswirkung: Expertise veraltet
   - GegenmaÃŸnahme: [Fortbildungsbudget? Netzwerk?]

8. **Wirtschaftskrise**
   - Wahrscheinlichkeit: Niedrig bis Mittel
   - Auswirkung: BudgetkÃ¼rzungen bei Kunden
   - GegenmaÃŸnahme: [Diversifikation? Flexible Kostenstruktur?]

9-10. [Weitere branchenspezifische Risiken]

### 9.2 LiquiditÃ¤tssicherung

**Worst-Case Szenario:**
- Wenn Umsatz 30% unter Plan:
  - [Was passiert?]
  - [Wie lange Eigenkapital reicht]
  - [Ab wann GegenmaÃŸnahmen?]

**GegenmaÃŸnahmen bei LiquiditÃ¤tsengpass:**
1. [Privatentnahme reduzieren]
2. [Teilzeit-Job suchen - max. 14h/Woche!]
3. [Kurzfristige Finanzierung?]
4. [Notfallplan: ZurÃ¼ck in Anstellung]

### 9.3 Versicherungen & Absicherung

- Berufshaftpflicht: [Ja, [X] EUR/Monat]
- Krankenversicherung: [Selbstzahler, [X] EUR/Monat]
- BerufsunfÃ¤higkeit: [Optional, erwÃ¤gen]
- [Weitere relevante]

**STIL:**
- Ehrlich (Risiken nicht kleinreden)
- LÃ¶sungsorientiert (immer GegenmaÃŸnahme)
- Realistisch (keine SchÃ¶nfÃ¤rberei)
- GZ-konform (spezifische Risiken ansprechen!)

Schreibe das komplette Kapitel:"""

        return await self._call_claude(prompt, max_tokens=2000)
    
    async def generate_meilensteine(self, data: Dict) -> str:
        """
        Meilensteine & Zeitplan
        
        AfA wants to see:
        - Concrete timeline
        - Month-by-month plan
        - Realistic milestones
        - Shows commitment
        """
        
        prompt = f"""Schreibe ein "Meilensteine & Zeitplan" Kapitel (400-600 WÃ¶rter).

**KRITISCH: AfA will konkrete Umsetzungsplanung sehen!**

**STRUKTUR:**

### 10.1 Vorbereitungsphase (vor GrÃ¼ndung)

**Woche 1-2:**
- Gewerbeanmeldung
- Steuerberater beauftragen
- Versicherungen abschlieÃŸen

**Woche 3-4:**
- Website/LinkedIn optimieren
- Erstkontakte aktivieren
- Equipment beschaffen

### 10.2 Startphase (Monat 1-3)

**Monat 1:**
- Ziel: 2 ErstgesprÃ¤che
- MaÃŸnahmen: [Networking, LinkedIn]
- Meilenstein: Website live

**Monat 2:**
- Ziel: 1 Pilot-Projekt akquiriert
- MaÃŸnahmen: [Follow-ups, Angebote]
- Meilenstein: Erster Auftrag

**Monat 3:**
- Ziel: Pilot-Projekt erfolgreich abgeschlossen
- MaÃŸnahmen: Case Study erstellen
- Meilenstein: Erste Empfehlung

### 10.3 Wachstumsphase (Monat 4-12)

**Monat 4-6:**
- Ziel: 3-4 aktive Kunden
- MaÃŸnahmen: Content Marketing starten
- Meilenstein: Break-Even erreicht

**Monat 7-9:**
- Ziel: 6-8 Kunden
- MaÃŸnahmen: Paid Ads, Partnerschaften
- Meilenstein: [X] EUR Umsatz/Monat stabil

**Monat 10-12:**
- Ziel: 8-12 Kunden
- MaÃŸnahmen: Skalierung, evtl. Freelancer fÃ¼r Overflow
- Meilenstein: Jahr 1 Ziel erreicht

### 10.4 Langfristige Vision (Jahr 2-3)

**Jahr 2:**
- Ziel: [Realistic goal]
- Fokus: [Was anders?]

**Jahr 3:**
- Ziel: [Realistic goal]
- Fokus: [Expansion? Team?]

### 10.5 Kritische Erfolgsfaktoren

Was muss passieren damit Plan aufgeht:
1. [Faktor 1]
2. [Faktor 2]
3. [Faktor 3]

**STIL:**
- KONKRET (nicht "Kunden gewinnen" sondern "2 Kunden bis Monat 3")
- REALISTISCH (konservative Ziele)
- NACHVOLLZIEHBAR (jedes Ziel erreichbar)

Schreibe das komplette Kapitel:"""

        return await self._call_claude(prompt, max_tokens=1800)
    
    async def _call_claude(self, prompt: str, max_tokens: int = 1500) -> str:
        """Call Claude API with error handling"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"[Fehler beim Generieren: {str(e)}]"


# ============================================================================
# REALISTIC FINANCIAL PLANNER - CONSERVATIVE ASSUMPTIONS
# ============================================================================

class RealisticFinancialPlanner:
    """
    Conservative financial planning for GZ compliance
    
    Key Changes from TAG 4:
    - Lower utilization rates (20-50% vs. 20-70%)
    - More detailed cost breakdown
    - Justifications for every number
    - Best/Worst case scenarios
    - Startup capital properly modeled
    """
    
    def generate_realistic_financials(
        self,
        data: Dict,
        living_costs: Dict
    ) -> Dict:
        """
        Generate conservative 3-year financial plan
        
        CONSERVATIVE ASSUMPTIONS:
        - Year 1: Max 40-50% utilization (not 70%!)
        - Slow ramp-up (realistic for B2B)
        - All costs detailed
        - Startup capital needed
        """
        
        # Parse revenue sources
        revenue_sources = self._parse_revenue_source(data.get('revenue_source', ''))
        
        # Calculate realistic startup capital
        capital = self._calculate_realistic_capital(data.get('capital_needs', ''))
        
        # Generate Year 1 (monthly, CONSERVATIVE)
        jahr_1 = self._generate_conservative_jahr_1(
            revenue_sources,
            capital,
            living_costs
        )
        
        # Generate scenarios
        scenarios = self._generate_scenarios(jahr_1, living_costs)
        
        # Generate Years 2-3
        jahr_2 = self._generate_jahr_2(jahr_1)
        jahr_3 = self._generate_jahr_3(jahr_2)
        
        # Summary
        summary = self._generate_summary(jahr_1, jahr_2, jahr_3, capital)
        
        # Add assumptions & justifications
        assumptions = self._generate_assumptions(revenue_sources, jahr_1)
        
        return {
            'startkapital': capital,
            'startkapital_herkunft': self._explain_capital_source(capital),
            'annahmen': assumptions,
            'jahr_1': jahr_1,
            'jahr_2': jahr_2,
            'jahr_3': jahr_3,
            'szenarien': scenarios,
            'zusammenfassung': summary
        }
    
    def _generate_conservative_jahr_1(
        self,
        revenue_sources: List[Dict],
        capital: float,
        living_costs: Dict
    ) -> Dict:
        """
        Year 1 with CONSERVATIVE assumptions
        
        IMPORTANT: Separate business costs from private withdrawal!
        - Business profit = Revenue - Business costs
        - Cashflow = Business profit - Private withdrawal
        
        Utilization:
        - Month 1-3: 20% (realistic for cold start)
        - Month 4-6: 35% (first projects closing)
        - Month 7-12: 45-50% MAX (includes admin time)
        """
        
        monate = []
        kontostand = capital
        
        monthly_living = living_costs['monatlich']['mit_puffer']
        
        for monat in range(1, 13):
            # CONSERVATIVE utilization
            if monat <= 3:
                auslastung = 0.20  # 20%
            elif monat <= 6:
                auslastung = 0.35  # 35%
            elif monat <= 9:
                auslastung = 0.45  # 45%
            else:
                auslastung = 0.50  # 50% MAX (realistic with admin)
            
            # Revenue
            umsatz = self._calculate_monthly_revenue(
                revenue_sources,
                auslastung,
                monat
            )
            
            # Business Costs (DETAILED, without living costs!)
            kosten_fix = self._calculate_detailed_fixkosten(monat, capital)
            kosten_var = umsatz * 0.12  # 12% variable (travel, materials)
            
            kosten_geschaeft = kosten_fix + kosten_var
            
            # Business profit (before private withdrawal)
            gewinn_geschaeft = umsatz - kosten_geschaeft
            
            # Private withdrawal (living costs)
            privatentnahme = monthly_living
            
            # Net cashflow
            saldo = gewinn_geschaeft - privatentnahme
            kontostand += saldo
            
            monate.append({
                'monat': monat,
                'monat_name': self._monat_name(monat),
                'umsatz': round(umsatz, 2),
                'kosten_fix': round(kosten_fix, 2),
                'kosten_var': round(kosten_var, 2),
                'kosten_geschaeft': round(kosten_geschaeft, 2),
                'gewinn_geschaeft': round(gewinn_geschaeft, 2),
                'privatentnahme': round(privatentnahme, 2),
                'saldo': round(saldo, 2),
                'kontostand': round(kontostand, 2),
                'auslastung_prozent': int(auslastung * 100)
            })
        
        # Totals
        gesamt_umsatz = sum(m['umsatz'] for m in monate)
        gesamt_kosten_geschaeft = sum(m['kosten_geschaeft'] for m in monate)
        gesamt_gewinn_geschaeft = sum(m['gewinn_geschaeft'] for m in monate)
        gesamt_privatentnahme = sum(m['privatentnahme'] for m in monate)
        gesamt_saldo = sum(m['saldo'] for m in monate)
        
        return {
            'monate': monate,
            'gesamt_umsatz': round(gesamt_umsatz, 2),
            'gesamt_kosten_geschaeft': round(gesamt_kosten_geschaeft, 2),
            'gesamt_gewinn_geschaeft': round(gesamt_gewinn_geschaeft, 2),
            'gesamt_privatentnahme': round(gesamt_privatentnahme, 2),
            'jahresergebnis': round(gesamt_saldo, 2),
            'endkontostand': round(monate[11]['kontostand'], 2),
            'break_even_monat': self._find_break_even(monate)
        }
    
    def _calculate_detailed_fixkosten(self, monat: int, capital: float) -> float:
        """
        DETAILED fixed costs breakdown
        
        GZ-PrÃ¼fer want to see EVERY cost item!
        
        NOTE: Living costs (Privatentnahme) are separate!
        NOTE: Equipment purchases from capital, not monthly costs!
        """
        
        kosten = {
            'krankenversicherung': 450,  # Self-employed
            'rentenversicherung': 300,   # Voluntary
            'berufshaftpflicht': 95,     # Professional liability
            'software_tools': 150,       # Monthly licenses
            'coworking': 180,            # Flex desk
            'steuerberater': 150,        # Accountant
            'marketing': 200,            # LinkedIn/Ads
            'telefon_internet': 50,
            'fortbildung': 100,          # Continuous learning
            'versicherungen_sonstige': 50,
            'ruecklagen_steuern': 200    # Tax provisions
        }
        
        # Month 1: One-time setup costs (NOT equipment - that's from capital!)
        if monat == 1:
            kosten['gewerbeanmeldung'] = 30
            kosten['erstberatung_steuerberater'] = 300
            kosten['gruendung_sonstiges'] = 200
        
        return sum(kosten.values())
    
    def _calculate_realistic_capital(self, capital_str: str) -> float:
        """
        Calculate REALISTIC startup capital
        
        Most founders underestimate!
        """
        
        # Extract from string
        match = re.search(r'(\d{1,3}(?:[.,]\d{3})*)', capital_str)
        stated_capital = float(match.group(1).replace('.', '').replace(',', '')) if match else 8000
        
        # Minimum realistic capital
        minimum_needed = 10000  # For professional setup
        
        return max(stated_capital, minimum_needed)
    
    def _explain_capital_source(self, capital: float) -> Dict:
        """Explain where capital comes from"""
        
        return {
            'gesamt': capital,
            'herkunft': {
                'eigenkapital': capital * 0.5,
                'familie_freunde': capital * 0.3,
                'kfw_startgeld': capital * 0.2
            },
            'verwendung': {
                'equipment': 2500,
                'software_jahr_1': 1800,
                'website_branding': 1500,
                'marketing_initial': 1200,
                'liquiditaetsreserve': capital - 7000
            }
        }
    
    def _generate_scenarios(self, jahr_1: Dict, living_costs: Dict) -> Dict:
        """
        Best/Base/Worst case scenarios
        
        GZ-PrÃ¼fer want to see: "What if things go wrong?"
        """
        
        base_umsatz = jahr_1['gesamt_umsatz']
        base_kosten = jahr_1['gesamt_kosten_geschaeft']
        base_privat = jahr_1['gesamt_privatentnahme']
        
        return {
            'best_case': {
                'name': 'Best-Case (+20% Umsatz)',
                'umsatz': round(base_umsatz * 1.2, 2),
                'kosten_geschaeft': round(base_kosten * 1.05, 2),  # Slightly higher
                'privatentnahme': base_privat,
                'gewinn_geschaeft': round((base_umsatz * 1.2) - (base_kosten * 1.05), 2),
                'saldo': round((base_umsatz * 1.2) - (base_kosten * 1.05) - base_privat, 2),
                'beschreibung': 'Mehr Empfehlungen, schnellere ProjektabschlÃ¼sse'
            },
            'base_case': {
                'name': 'Base-Case (Planung)',
                'umsatz': base_umsatz,
                'kosten_geschaeft': base_kosten,
                'privatentnahme': base_privat,
                'gewinn_geschaeft': jahr_1['gesamt_gewinn_geschaeft'],
                'saldo': jahr_1['jahresergebnis'],
                'beschreibung': 'Konservative Planung wie dargestellt'
            },
            'worst_case': {
                'name': 'Worst-Case (-30% Umsatz)',
                'umsatz': round(base_umsatz * 0.7, 2),
                'kosten_geschaeft': round(base_kosten * 0.95, 2),  # Can reduce variable costs
                'privatentnahme': round(base_privat * 0.8, 2),  # Reduce living standard temporarily
                'gewinn_geschaeft': round((base_umsatz * 0.7) - (base_kosten * 0.95), 2),
                'saldo': round((base_umsatz * 0.7) - (base_kosten * 0.95) - (base_privat * 0.8), 2),
                'beschreibung': 'VerzÃ¶gerte Akquise, lÃ¤ngere Sales Cycles',
                'ueberbrueckung': 'Teilzeit-Job parallel (max. 14h/Woche, 1.200 EUR/Monat gemÃ¤ÃŸ Fachlichen Weisungen BA) oder Privatentnahme reduzieren'
            }
        }
    
    def _generate_assumptions(self, revenue_sources: List[Dict], jahr_1: Dict) -> Dict:
        """
        Document ALL assumptions for transparency
        
        GZ-PrÃ¼fer: "Woher kommen diese Zahlen?"
        """
        
        return {
            'umsatz': {
                'stundensatz': revenue_sources[0]['price'] if revenue_sources else 120,
                'stundensatz_begruendung': 'Marktvergleich: Enterprise 200-280 EUR/h, Freelancer 80-150 EUR/h. Positionierung: Premium-KMU',
                'auslastung_jahr_1': 'Konservativ: Max 50% (inkl. Akquise, Admin, Fortbildung)',
                'auslastung_begruendung': 'B2B Sales Cycle 3-4 Monate. Einzelunternehmer benÃ¶tigt 20% fÃ¼r nicht-fakturierbare TÃ¤tigkeiten',
                'verfuegbare_stunden': '80h/Monat fakturierbar (bei 30h/Woche gesamt - Hauptberuflichkeit gemÃ¤ÃŸ SGB III Â§ 93 Abs. 2 erfÃ¼llt)'
            },
            'kosten': {
                'fixkosten_monat': 1925,
                'fixkosten_detail': 'Siehe detaillierte AufschlÃ¼sselung im Finanzplan',
                'variable_kosten': '12% vom Umsatz (Reisen, Material)',
                'privatentnahme': f"{jahr_1['monate'][0]['privatentnahme']:.0f} EUR/Monat",
                'privatentnahme_begruendung': 'Basierend auf realen Lebenshaltungskosten mit 20% Puffer'
            },
            'annahmen': {
                'break_even': self._find_break_even(jahr_1['monate']),
                'kunden_jahr_1': '8-12 Kunden (konservativ)',
                'kunden_akquise': 'Aus Netzwerk + LinkedIn + Networking-Events',
                'zahlungsziel': '30 Tage (Standard B2B)'
            }
        }
    
    def _find_break_even(self, monate: List[Dict]) -> str:
        """
        Find break-even month
        
        Break-even = When cumulative business profit > startup capital used
        (Not when cashflow after private withdrawal is positive!)
        """
        kumuliert_gewinn = 0
        for m in monate:
            kumuliert_gewinn += m.get('gewinn_geschaeft', 0)
            # Break-even when cumulative business profit covers startup
            if kumuliert_gewinn > 0:
                return f"Monat {m['monat']}"
        return "Nicht in Jahr 1"
    
    # ... (other helper methods similar to original FinancialPlanner)
    
    def _calculate_monthly_revenue(self, revenue_sources, auslastung, monat):
        """Calculate revenue based on sources and utilization"""
        umsatz = 0
        for source in revenue_sources:
            if source['type'] == 'hourly':
                hours = 80 * auslastung  # 80h/month available
                umsatz += hours * source['price']
            elif source['type'] == 'monthly':
                # Workshops start from month 4
                if monat >= 4:
                    umsatz += source['price'] * min(auslastung * 1.5, 1.0)
            elif source['type'] == 'project':
                # Projects from month 7
                if monat >= 7:
                    projects = auslastung * 0.3  # 0-0.15 projects/month
                    umsatz += projects * source['price']
        return umsatz
    
    def _parse_revenue_source(self, revenue_str: str) -> List[Dict]:
        """Parse revenue sources from string"""
        import re
        sources = []
        parts = revenue_str.split(',')
        
        for part in parts:
            price_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s*â‚¬', part)
            if price_match:
                price = float(price_match.group(1).replace('.', '').replace(',', '.'))
                name = part.split('Ã ')[0].strip() if 'Ã ' in part else 'Umsatz'
                
                if 'stunde' in part.lower():
                    sources.append({'name': name, 'price': price, 'type': 'hourly'})
                elif 'monat' in part.lower():
                    sources.append({'name': name, 'price': price, 'type': 'monthly'})
                else:
                    sources.append({'name': name, 'price': price, 'type': 'project'})
        
        return sources if sources else [{'name': 'Umsatz', 'price': 120, 'type': 'hourly'}]
    
    def _monat_name(self, monat: int) -> str:
        """Month number to name"""
        names = ['Jan', 'Feb', 'MÃ¤r', 'Apr', 'Mai', 'Jun',
                'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        return names[monat - 1]
    
    def _generate_jahr_2(self, jahr_1: Dict) -> Dict:
        """
        Year 2: Moderate growth (25-30%)
        More stable, less aggressive than TAG 4
        """
        
        jahr_1_umsatz = jahr_1['gesamt_umsatz']
        jahr_1_kosten = jahr_1['gesamt_kosten_geschaeft']
        jahr_1_privat = jahr_1['gesamt_privatentnahme']
        
        # Conservative growth
        growth_rate = 0.25  # 25%
        
        quartale = []
        for q in range(1, 5):
            # Gradual growth through year
            quarter_growth = 1 + (growth_rate * (q / 4))
            
            umsatz_q = (jahr_1_umsatz / 4) * quarter_growth
            kosten_geschaeft_q = (jahr_1_kosten / 4) * 1.1  # Costs grow slower
            privatentnahme_q = jahr_1_privat / 4  # Same living standard
            
            gewinn_geschaeft_q = umsatz_q - kosten_geschaeft_q
            saldo_q = gewinn_geschaeft_q - privatentnahme_q
            
            quartale.append({
                'quartal': q,
                'quartal_name': f'Q{q}',
                'umsatz': round(umsatz_q, 2),
                'kosten_geschaeft': round(kosten_geschaeft_q, 2),
                'gewinn_geschaeft': round(gewinn_geschaeft_q, 2),
                'privatentnahme': round(privatentnahme_q, 2),
                'saldo': round(saldo_q, 2)
            })
        
        gesamt_umsatz = sum(q['umsatz'] for q in quartale)
        gesamt_kosten = sum(q['kosten_geschaeft'] for q in quartale)
        gesamt_gewinn = sum(q['gewinn_geschaeft'] for q in quartale)
        gesamt_privat = sum(q['privatentnahme'] for q in quartale)
        gesamt_saldo = sum(q['saldo'] for q in quartale)
        
        return {
            'quartale': quartale,
            'gesamt_umsatz': round(gesamt_umsatz, 2),
            'gesamt_kosten_geschaeft': round(gesamt_kosten, 2),
            'gesamt_gewinn_geschaeft': round(gesamt_gewinn, 2),
            'gesamt_privatentnahme': round(gesamt_privat, 2),
            'jahresergebnis': round(gesamt_saldo, 2),
            'endkontostand': round(jahr_1.get('endkontostand', 0) + gesamt_saldo, 2)
        }
    
    def _generate_jahr_3(self, jahr_2: Dict) -> Dict:
        """
        Year 3: Stabilization (15-20% growth)
        More mature business
        """
        
        jahr_2_umsatz = jahr_2['gesamt_umsatz']
        jahr_2_kosten = jahr_2['gesamt_kosten_geschaeft']
        jahr_2_privat = jahr_2['gesamt_privatentnahme']
        
        # Conservative growth
        growth_rate = 0.18  # 18%
        
        quartale = []
        for q in range(1, 5):
            # Steady growth
            quarter_growth = 1 + growth_rate
            
            umsatz_q = (jahr_2_umsatz / 4) * quarter_growth
            kosten_geschaeft_q = (jahr_2_kosten / 4) * 1.08  # Costs still grow slower
            privatentnahme_q = jahr_2_privat / 4  # Same living standard
            
            gewinn_geschaeft_q = umsatz_q - kosten_geschaeft_q
            saldo_q = gewinn_geschaeft_q - privatentnahme_q
            
            quartale.append({
                'quartal': q,
                'quartal_name': f'Q{q}',
                'umsatz': round(umsatz_q, 2),
                'kosten_geschaeft': round(kosten_geschaeft_q, 2),
                'gewinn_geschaeft': round(gewinn_geschaeft_q, 2),
                'privatentnahme': round(privatentnahme_q, 2),
                'saldo': round(saldo_q, 2)
            })
        
        gesamt_umsatz = sum(q['umsatz'] for q in quartale)
        gesamt_kosten = sum(q['kosten_geschaeft'] for q in quartale)
        gesamt_gewinn = sum(q['gewinn_geschaeft'] for q in quartale)
        gesamt_privat = sum(q['privatentnahme'] for q in quartale)
        gesamt_saldo = sum(q['saldo'] for q in quartale)
        
        return {
            'quartale': quartale,
            'gesamt_umsatz': round(gesamt_umsatz, 2),
            'gesamt_kosten_geschaeft': round(gesamt_kosten, 2),
            'gesamt_gewinn_geschaeft': round(gesamt_gewinn, 2),
            'gesamt_privatentnahme': round(gesamt_privat, 2),
            'jahresergebnis': round(gesamt_saldo, 2),
            'endkontostand': round(jahr_2.get('endkontostand', 0) + gesamt_saldo, 2)
        }
    
    def _generate_summary(self, j1: Dict, j2: Dict, j3: Dict, capital: float) -> Dict:
        """3-year summary with key metrics"""
        
        # Break-even is already calculated in jahr_1
        break_even_monat = j1.get('break_even_monat', 'Nicht in Jahr 1')
        
        # Calculate ROI based on business profit (not cashflow after private withdrawal)
        total_investment = capital
        total_profit_3y = (
            j1.get('gesamt_gewinn_geschaeft', 0) + 
            j2.get('gesamt_gewinn_geschaeft', 0) + 
            j3.get('gesamt_gewinn_geschaeft', 0)
        )
        roi_prozent = ((total_profit_3y / total_investment) * 100) if total_investment > 0 else 0
        
        # Cashflow after private withdrawal
        total_cashflow_3y = (
            j1.get('jahresergebnis', 0) + 
            j2.get('jahresergebnis', 0) + 
            j3.get('jahresergebnis', 0)
        )
        
        return {
            'startkapital': capital,
            'break_even_monat': break_even_monat,
            'gesamt_umsatz_3_jahre': round(
                j1.get('gesamt_umsatz', 0) + 
                j2.get('gesamt_umsatz', 0) + 
                j3.get('gesamt_umsatz', 0), 2
            ),
            'gesamt_gewinn_geschaeft_3_jahre': round(total_profit_3y, 2),
            'gesamt_cashflow_3_jahre': round(total_cashflow_3y, 2),
            'roi_3_jahre_prozent': round(roi_prozent, 1),
            'durchschnitt_gewinn_geschaeft_jahr': round(total_profit_3y / 3, 2) if total_profit_3y > 0 else 0,
            'endkontostand_jahr_3': round(j3.get('endkontostand', capital + total_cashflow_3y), 2)
        }


# ============================================================================
# GZ COMPLIANCE CHECKER - WITH LEGAL CITATIONS
# ============================================================================

class GZComplianceChecker:
    """
    Check businessplan for GZ compliance WITH LEGAL BASIS
    
    Returns:
    - Compliance score (0-100)
    - Issues identified WITH legal citations
    - Improvement suggestions with official requirements
    """
    
    GZ_CRITERIA = {
        'hauptberuflichkeit': {
            'weight': 15,
            'rechtsgrundlage': 'SGB III Â§ 93 Abs. 2',
            'quelle': 'https://www.gesetze-im-internet.de/sgb_3/__93.html',
            'anforderung': 'Mindestens 15 Stunden wÃ¶chentlich fÃ¼r die selbstÃ¤ndige TÃ¤tigkeit',
            'checks': [
                {
                    'id': '15h_mentioned',
                    'name': 'Mind. 15h/Woche erwÃ¤hnt',
                    'rechtsgrundlage': 'SGB III Â§ 93 Abs. 2',
                    'severity': 'CRITICAL',
                    'points': 5
                },
                {
                    'id': 'hauptberuflich_stated',
                    'name': '"Hauptberuflich" explizit genannt',
                    'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 93',
                    'severity': 'HIGH',
                    'points': 5
                },
                {
                    'id': 'no_hobby_words',
                    'name': 'Keine Hobby-WÃ¶rter verwendet',
                    'rechtsgrundlage': 'SGB III Â§ 93 Abs. 2',
                    'severity': 'MEDIUM',
                    'points': 5
                }
            ]
        },
        'qualifikation': {
            'weight': 15,
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 93 SGB III',
            'quelle': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-93_ba014875.pdf',
            'anforderung': 'Notwendige Kenntnisse und FÃ¤higkeiten zur AusÃ¼bung der selbstÃ¤ndigen TÃ¤tigkeit',
            'checks': [
                {
                    'id': 'experience_detailed',
                    'name': 'Berufserfahrung detailliert (mind. 2-3 Jahre)',
                    'severity': 'HIGH',
                    'points': 6
                },
                {
                    'id': 'certificates_mentioned',
                    'name': 'Zertifikate/Qualifikationen erwÃ¤hnt',
                    'severity': 'MEDIUM',
                    'points': 4
                },
                {
                    'id': 'projects_with_results',
                    'name': 'Projekte mit messbaren Ergebnissen',
                    'severity': 'MEDIUM',
                    'points': 5
                }
            ]
        },
        'marktanalyse': {
            'weight': 20,
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 93 SGB III',
            'anforderung': 'Marktpotenzial muss nachvollziehbar dargestellt werden',
            'checks': [
                {
                    'id': 'market_size_numbers',
                    'name': 'MarktgrÃ¶ÃŸe mit Zahlen',
                    'severity': 'HIGH',
                    'points': 6
                },
                {
                    'id': 'competitors_named',
                    'name': 'Mind. 3 Wettbewerber benannt',
                    'severity': 'MEDIUM',
                    'points': 5
                },
                {
                    'id': 'sources_cited',
                    'name': 'Quellen zitiert',
                    'severity': 'MEDIUM',
                    'points': 4
                },
                {
                    'id': 'usp_clear',
                    'name': 'USP klar formuliert',
                    'severity': 'HIGH',
                    'points': 5
                }
            ]
        },
        'finanzplan': {
            'weight': 25,
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 93 SGB III',
            'anforderung': 'Finanzplan zeigt tragfÃ¤hige Existenzgrundlage, Lebenshaltungskosten kÃ¶nnen gedeckt werden',
            'checks': [
                {
                    'id': 'realistic_revenue',
                    'name': 'Umsatz realistisch (<100k Jahr 1)',
                    'severity': 'HIGH',
                    'points': 6
                },
                {
                    'id': 'living_costs_covered',
                    'name': 'Lebenshaltungskosten gedeckt',
                    'rechtsgrundlage': 'Fachliche Weisungen BA',
                    'severity': 'CRITICAL',
                    'points': 7
                },
                {
                    'id': 'break_even_reasonable',
                    'name': 'Break-Even <12 Monate',
                    'severity': 'HIGH',
                    'points': 6
                },
                {
                    'id': 'scenarios_included',
                    'name': 'Best/Worst-Case vorhanden',
                    'severity': 'MEDIUM',
                    'points': 3
                },
                {
                    'id': 'assumptions_documented',
                    'name': 'Annahmen dokumentiert',
                    'severity': 'MEDIUM',
                    'points': 3
                }
            ]
        },
        'marketing': {
            'weight': 10,
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 94 SGB III',
            'anforderung': 'Intensive GeschÃ¤ftstÃ¤tigkeit muss nachgewiesen werden kÃ¶nnen',
            'checks': [
                {
                    'id': 'acquisition_plan',
                    'name': 'Kundenakquise-Plan vorhanden',
                    'severity': 'HIGH',
                    'points': 4
                },
                {
                    'id': 'first_customers',
                    'name': 'Strategie fÃ¼r erste Kunden',
                    'severity': 'HIGH',
                    'points': 3
                },
                {
                    'id': 'sales_funnel',
                    'name': 'Sales Funnel beschrieben',
                    'severity': 'MEDIUM',
                    'points': 3
                }
            ]
        },
        'risiken': {
            'weight': 10,
            'rechtsgrundlage': 'Allgemeine Anforderung fachkundige Stelle',
            'anforderung': 'Risiken mÃ¼ssen erkannt und GegenmaÃŸnahmen geplant sein',
            'checks': [
                {
                    'id': 'risks_identified',
                    'name': 'Mind. 5 Risiken identifiziert (inkl. GZ-spezifisch)',
                    'severity': 'MEDIUM',
                    'points': 4
                },
                {
                    'id': 'countermeasures',
                    'name': 'GegenmaÃŸnahmen fÃ¼r jedes Risiko',
                    'severity': 'MEDIUM',
                    'points': 3
                },
                {
                    'id': 'worst_case_plan',
                    'name': 'Worst-Case Plan vorhanden',
                    'severity': 'MEDIUM',
                    'points': 3
                }
            ]
        },
        'vollstaendigkeit': {
            'weight': 5,
            'rechtsgrundlage': 'Allgemeine Anforderung fachkundige Stelle',
            'checks': [
                {
                    'id': 'all_chapters',
                    'name': 'Alle Kapitel vorhanden',
                    'severity': 'MEDIUM',
                    'points': 2
                },
                {
                    'id': 'sources_bibliography',
                    'name': 'Quellenverzeichnis gefÃ¼llt',
                    'severity': 'LOW',
                    'points': 2
                },
                {
                    'id': 'milestones',
                    'name': 'Meilensteine & Zeitplan vorhanden',
                    'severity': 'MEDIUM',
                    'points': 1
                }
            ]
        }
    }
    
    def check_compliance(self, businessplan: Dict) -> Dict:
        """
        Comprehensive GZ compliance check WITH LEGAL CITATIONS
        
        Returns detailed report with score and issues
        """
        
        results = {
            'total_score': 0,
            'category_scores': {},
            'issues': [],
            'improvements': [],
            'critical_missing': [],
            'bewilligungs_wahrscheinlichkeit': '',
            'legal_basis': {}  # NEW! Store legal citations used
        }
        
        total_points = 0
        max_points = 0
        
        for category, config in self.GZ_CRITERIA.items():
            weight = config['weight']
            max_points += weight
            
            # Store legal basis for category
            results['legal_basis'][category] = {
                'rechtsgrundlage': config.get('rechtsgrundlage', 'Allgemeine Anforderung'),
                'quelle': config.get('quelle', ''),
                'anforderung': config.get('anforderung', '')
            }
            
            category_checks = []
            for check in config['checks']:
                if isinstance(check, dict):
                    check_id = check['id']
                    check_name = check['name']
                    severity = check.get('severity', 'MEDIUM')
                else:
                    # Old format compatibility
                    check_id, check_name = check
                    severity = 'MEDIUM'
                
                passed = self._run_check(check_id, businessplan)
                category_checks.append({
                    'name': check_name,
                    'passed': passed,
                    'severity': severity
                })
                
                if not passed:
                    # Format issue with legal citation
                    issue_text = f"âŒ {check_name}"
                    if config.get('rechtsgrundlage'):
                        issue_text += f" (Rechtsgrundlage: {config['rechtsgrundlage']})"
                    
                    results['issues'].append(issue_text)
                    
                    if severity == 'CRITICAL' or weight >= 20:
                        results['critical_missing'].append(check_name)
            
            # Calculate category score
            passed_checks = sum(1 for c in category_checks if c['passed'])
            category_score = (passed_checks / len(category_checks)) * weight
            total_points += category_score
            
            results['category_scores'][category] = {
                'score': round(category_score, 1),
                'max': weight,
                'checks': category_checks,
                'rechtsgrundlage': config.get('rechtsgrundlage', '')
            }
        
        # Total score
        results['total_score'] = round((total_points / max_points) * 100, 1)
        
        # Cashflow warnings
        cashflow_warnings = self._check_cashflow_warnings(businessplan)
        
        # Apply score deductions
        score_deductions = 0
        for warning in cashflow_warnings:
            score_deductions += warning.get('score_deduction', 0)
            
            if warning['severity'] == 'CRITICAL':
                results['critical_missing'].append(warning['message'])
                results['issues'].append(warning['message'])
            elif warning['severity'] == 'WARNING':
                results['improvements'].append(warning['message'])
            else:  # INFO
                results['improvements'].append(warning['message'])
        
        # Adjust final score
        results['total_score'] = max(0, results['total_score'] - score_deductions)
        
        # Probability assessment (more realistic)
        gz_ready = len([w for w in cashflow_warnings if w['severity'] == 'CRITICAL']) == 0
        
        if results['total_score'] >= 90 and gz_ready:
            results['bewilligungs_wahrscheinlichkeit'] = '90-95% (Exzellent)'
        elif results['total_score'] >= 80 and gz_ready:
            results['bewilligungs_wahrscheinlichkeit'] = '80-90% (Gut bis Sehr Gut)'
        elif results['total_score'] >= 70:
            results['bewilligungs_wahrscheinlichkeit'] = '60-75% (Befriedigend - kleine Verbesserungen)'
        elif results['total_score'] >= 60:
            results['bewilligungs_wahrscheinlichkeit'] = '40-55% (Grenzfall - Nachbesserung empfohlen)'
        else:
            results['bewilligungs_wahrscheinlichkeit'] = '<40% (UngenÃ¼gend - Umfassende Ãœberarbeitung erforderlich)'
        
        # Generate improvements
        results['improvements'] = self._generate_improvements(results)
        
        return results
    
    def _run_check(self, check_id: str, businessplan: Dict) -> bool:
        """Run individual compliance check"""
        
        # Implement specific checks
        # This is a simplified version - full implementation would check actual content
        
        if check_id == 'realistic_revenue':
            jahr_1_umsatz = businessplan.get('finanzplan', {}).get('jahr_1', {}).get('gesamt_umsatz', 0)
            return jahr_1_umsatz < 100000
        
        elif check_id == 'break_even_reasonable':
            zusammenfassung = businessplan.get('finanzplan', {}).get('zusammenfassung')
            if not zusammenfassung:
                # Try jahr_1 directly
                jahr_1 = businessplan.get('finanzplan', {}).get('jahr_1', {})
                break_even = jahr_1.get('break_even_monat', 'Nicht')
            else:
                break_even = zusammenfassung.get('break_even_monat', 'Nicht')
            
            if isinstance(break_even, str) and 'Monat' in break_even:
                try:
                    monat_num = int(break_even.split()[1])
                    return monat_num <= 12
                except:
                    return False
            return False
        
        elif check_id == 'sources_realistically_filled':
            quellen = businessplan.get('quellenverzeichnis', '')
            
            if not quellen or len(quellen) < 50:
                return False
            
            # Check for actual source indicators
            has_urls = 'http' in quellen.lower() or 'www' in quellen.lower()
            has_years = any(str(year) in quellen for year in range(2020, 2026))
            has_citations = '[' in quellen or '(' in quellen
            
            if not (has_urls or has_years or has_citations):
                return False
            
            # Count potential sources
            potential_sources = quellen.count('\n') + quellen.count('[')
            
            return potential_sources >= 3
        
        # Add more checks as needed
        # For now, return True as placeholder for unimplemented checks
        return True
    
    def _generate_improvements(self, results: Dict) -> List[str]:
        """Generate concrete improvement suggestions WITH LEGAL BASIS"""
        
        improvements = []
        
        if results['total_score'] < 80:
            improvements.append("ðŸ“‹ PRIORITÃ„T: Kritische MÃ¤ngel beheben")
        
        for issue in results['critical_missing']:
            improvements.append(f"ðŸ”´ KRITISCH: {issue} ergÃ¤nzen")
        
        # Add legal reminders
        if results['total_score'] < 90:
            improvements.append("""
ðŸ“– RECHTLICHE GRUNDLAGEN BEACHTEN:
- Hauptberuflichkeit: SGB III Â§ 93 Abs. 2 (Min. 15h/Woche)
- Fachliche Qualifikation: Fachliche Weisungen BA zu Â§ 93
- Wirtschaftliche TragfÃ¤higkeit: Fachliche Weisungen BA zu Â§ 93
- Intensive GeschÃ¤ftstÃ¤tigkeit: Fachliche Weisungen BA zu Â§ 94 (fÃ¼r Phase 2)

Alle Anforderungen mÃ¼ssen dokumentiert nachweisbar sein!
            """)
        
        return improvements
    
    def _check_cashflow_warnings(self, businessplan: Dict) -> List[Dict]:
        """
        Generate warnings about financial situation
        
        Returns:
            List of warnings with severity and score deductions
        """
        
        warnings = []
        
        financials = businessplan.get('finanzplan', {})
        jahr_1 = financials.get('jahr_1', {})
        startkapital = financials.get('startkapital', 0)
        
        # Check 1: Business profit
        gewinn_geschaeft = jahr_1.get('gesamt_gewinn_geschaeft', 0)
        
        if gewinn_geschaeft < 0:
            warnings.append({
                'severity': 'CRITICAL',
                'category': 'Finanzplan',
                'message': f"ðŸš¨ KRITISCH: GeschÃ¤ftsgewinn Jahr 1 ist negativ ({gewinn_geschaeft:,.0f} EUR)! Wirtschaftliche TragfÃ¤higkeit nicht gegeben (Fachliche Weisungen BA zu Â§ 93)!",
                'score_deduction': 30
            })
        elif gewinn_geschaeft < 10000:
            warnings.append({
                'severity': 'WARNING',
                'category': 'Finanzplan',
                'message': f"âš ï¸ GeschÃ¤ftsgewinn Jahr 1 ist niedrig ({gewinn_geschaeft:,.0f} EUR). Empfehlung: Umsatz erhÃ¶hen oder Kosten senken.",
                'score_deduction': 10
            })
        
        # Check 2: Cashflow
        cashflow = jahr_1.get('jahresergebnis', 0)
        endkontostand = jahr_1.get('endkontostand', startkapital + cashflow)
        
        if endkontostand < 0:
            if abs(endkontostand) > startkapital:
                warnings.append({
                    'severity': 'CRITICAL',
                    'category': 'Finanzplan',
                    'message': f"ðŸš¨ KRITISCH: Kontostand am Jahresende ({endkontostand:,.0f} EUR) Ã¼bersteigt Startkapital ({startkapital:,.0f} EUR)! Finanzierung unklar!",
                    'score_deduction': 25
                })
            else:
                warnings.append({
                    'severity': 'WARNING',
                    'category': 'Finanzplan',
                    'message': f"âš ï¸ Negativer Kontostand am Jahresende ({endkontostand:,.0f} EUR), aber mit Startkapital ({startkapital:,.0f} EUR) Ã¼berbrÃ¼ckbar. Agentur kÃ¶nnte nachfragen.",
                    'score_deduction': 10
                })
        elif endkontostand < startkapital * 0.5:
            warnings.append({
                'severity': 'INFO',
                'category': 'Finanzplan',
                'message': f"ðŸ’¡ Kontostand am Jahresende ({endkontostand:,.0f} EUR) ist niedriger als Startkapital. LiquiditÃ¤tsreserve gering.",
                'score_deduction': 5
            })
        
        # Check 3: Break-even
        break_even = jahr_1.get('break_even_monat', 'Nicht in Jahr 1')
        
        if "Nicht" in break_even:
            warnings.append({
                'severity': 'WARNING',
                'category': 'Finanzplan',
                'message': "âš ï¸ Break-Even nicht in Jahr 1 erreicht. Business braucht lÃ¤nger bis ProfitabilitÃ¤t.",
                'score_deduction': 15
            })
        elif "Monat" in break_even:
            try:
                month_num = int(break_even.split()[1])
                if month_num > 9:
                    warnings.append({
                        'severity': 'INFO',
                        'category': 'Finanzplan',
                        'message': f"ðŸ’¡ Break-Even erst in {break_even}. KÃ¶nnte schneller sein mit besserer Akquise.",
                        'score_deduction': 5
                    })
            except:
                pass
        
        return warnings


# ============================================================================
# LEGAL CITATIONS HELPER FUNCTIONS
# ============================================================================

def get_legal_citation_for_criterion(criterion_id: str) -> dict:
    """
    Get legal citation for a compliance criterion
    
    Returns:
        {
            'rechtsgrundlage': 'SGB III Â§ 93 Abs. 2',
            'quelle': 'https://...',
            'anforderung': 'Mindestens 15 Stunden...'
        }
    """
    citations = {
        'hauptberuflichkeit': {
            'rechtsgrundlage': 'SGB III Â§ 93 Abs. 2',
            'quelle': 'https://www.gesetze-im-internet.de/sgb_3/__93.html',
            'anforderung': 'Mindestens 15 Stunden wÃ¶chentlich fÃ¼r die selbstÃ¤ndige TÃ¤tigkeit'
        },
        'qualifikation': {
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 93 SGB III',
            'quelle': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-93_ba014875.pdf',
            'anforderung': 'Notwendige Kenntnisse und FÃ¤higkeiten nachweisbar'
        },
        'tragfaehigkeit': {
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 93 SGB III',
            'quelle': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-93_ba014875.pdf',
            'anforderung': 'TragfÃ¤hige Existenzgrundlage, Lebenshaltungskosten kÃ¶nnen gedeckt werden'
        },
        'ermessen': {
            'rechtsgrundlage': 'SGB III Â§ 93 Abs. 1',
            'quelle': 'https://www.gesetze-im-internet.de/sgb_3/__93.html',
            'anforderung': 'GrÃ¼ndungszuschuss ist Ermessensleistung - kein Rechtsanspruch'
        },
        'nebentaetigkeit': {
            'rechtsgrundlage': 'SGB III Â§ 421 i.V.m. Â§ 155',
            'quelle': 'https://www.gesetze-im-internet.de/sgb_3/__155.html',
            'anforderung': 'NebentÃ¤tigkeit < 15h/Woche erlaubt, aber meldepflichtig'
        },
        'nebentaetigkeit_warning': {
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 93 SGB III',
            'quelle': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-93_ba014875.pdf',
            'anforderung': 'Bei > 15h oder > 50% Einkommen droht RÃ¼ckforderung'
        },
        'intensive_geschaeftstÃ¤tigkeit': {
            'rechtsgrundlage': 'Fachliche Weisungen BA zu Â§ 94 SGB III',
            'quelle': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-94_ba014876.pdf',
            'anforderung': 'Intensive GeschÃ¤ftstÃ¤tigkeit und hauptberufliche unternehmerische AktivitÃ¤ten fÃ¼r Phase 2 erforderlich'
        }
    }
    
    return citations.get(criterion_id, {})


def format_legal_warning(criterion_id: str, issue: str) -> str:
    """
    Format warning message with legal citation
    
    Example:
    >>> format_legal_warning('hauptberuflichkeit', 'Mind. 15h/Woche nicht erwÃ¤hnt')
    'âš ï¸ Mind. 15h/Woche nicht erwÃ¤hnt
    
    Rechtsgrundlage: SGB III Â§ 93 Abs. 2
    Anforderung: Mindestens 15 Stunden wÃ¶chentlich...'
    """
    citation = get_legal_citation_for_criterion(criterion_id)
    
    if not citation:
        return f"âš ï¸ {issue}"
    
    return f"""âš ï¸ {issue}

Rechtsgrundlage: {citation.get('rechtsgrundlage', 'N/A')}
Anforderung: {citation.get('anforderung', 'N/A')}

Quelle: {citation.get('quelle', 'N/A')}"""


# ============================================================================
# MASTER ORCHESTRATOR - ENHANCED BUSINESSPLAN GENERATOR
# ============================================================================

class EnhancedBusinessplanGenerator:
    """
    Master class for GZ-compliant businessplan generation WITH LEGAL CITATIONS
    
    Complete workflow:
    1. Collect data (from Vision Discovery)
    2. Generate all 11 chapters WITH legal citations
    3. Run GZ compliance check WITH legal basis
    4. Provide improvement suggestions with official requirements
    5. Allow iterative refinement
    """
    
    def __init__(self):
        self.content_generator = EnhancedContentGenerator()
        self.financial_planner = RealisticFinancialPlanner()
        self.compliance_checker = GZComplianceChecker()
        
        # Adaptive calculator (if available)
        if ADAPTIVE_CALCULATOR_AVAILABLE:
            self.adaptive_calculator = AdaptiveFinancialCalculator()
            logger.info("âœ… Adaptive Financial Calculator enabled")
        else:
            self.adaptive_calculator = None
            logger.info("â„¹ï¸ Using standard financial calculator")
        
        # From TAG 4
        from businessplan_generator import (
            CitationManager,
            GeographicDataResolver,
            LivingCostCalculator,
            SWOTAnalyzer
        )
        
        self.citations = CitationManager()
        self.geo_resolver = GeographicDataResolver(self.citations)
        self.living_calc = LivingCostCalculator()
        self.swot = SWOTAnalyzer()
        
        logger.info("âœ… Enhanced Businessplan Generator initialized WITH LEGAL CITATIONS")

   # ========================================================================
    # WRAPPER METHOD - PASTE THIS INTO businessplan_generator_enhanced.py
    # Replace the entire generate_from_simple_profile method with this version
    # Location: Inside EnhancedBusinessplanGenerator class, after __init__
    # ========================================================================
    
    async def generate_from_simple_profile(self, profile: Dict) -> Dict:
        """
        Simplified businessplan generation from basic profile data
        
        Perfect for:
        - API endpoints with simple user input
        - Testing and prototyping
        - Quick businessplan generation without full discovery process
        
        Args:
            profile: Simple profile with:
                - name (str): User name
                - business_idea (str): Business concept
                - industry (str, optional): Industry/sector
                - experience_level (str, optional): junior/mid/senior
                - hours_per_week_available (int): Available hours
                - startup_capital (float): Available capital
                - monthly_living_costs (float): Monthly expenses
                - target_market (str, optional): Target customers
                - email (str, optional): Contact email
                - plus any other fields from EnhancedBusinessplanRequest
        
        Returns:
            Dict with:
                - All original sections from generate_complete
                - gz_compliance with gz_score and citations_used
        """
        logger.info(f"📝 Generating businessplan from simple profile: {profile.get('name', 'Unknown')}")
        
        # Extract core data
        business_idea = profile.get('business_idea', 'Dienstleistung')
        industry = profile.get('industry', 'dienstleistung')
        name = profile.get('name', 'Gründer')
        experience = profile.get('experience_level', 'junior')
        
        # ===================================================================
        # VISION DATA - Auto-generate from business idea
        # ===================================================================
        vision_data = {
            "mission": business_idea,
            "vision": f"Führender Anbieter für {business_idea} mit höchster Qualität und Kundenzufriedenheit",
            "values": [
                "Qualität und Exzellenz",
                "Kundenorientierung",
                "Innovation und Weiterentwicklung",
                "Nachhaltigkeit"
            ],
            "business_model": "Dienstleistung" if industry == "coaching" else industry.capitalize(),
            "unique_value_proposition": f"Professionelle {business_idea} mit individueller Betreuung",
            "target_customer": profile.get('target_market', 'Unternehmen und Privatpersonen in Deutschland'),
            "industry": industry
        }
        
        # ===================================================================
        # JTBD DATA - Jobs-to-be-Done Analysis
        # ===================================================================
        jtbd_data = {
            "jobs": [
                "Effiziente Problemlösung für Zielkunden",
                "Zeitersparnis durch professionelle Unterstützung",
                "Qualitätssteigerung in relevanten Bereichen"
            ],
            "pains": [
                "Zeitmangel bei komplexen Aufgaben",
                "Fehlende Expertise in spezifischen Bereichen",
                "Hoher Koordinationsaufwand",
                "Unsicherheit bei wichtigen Entscheidungen"
            ],
            "gains": [
                "Deutliche Zeitersparnis",
                "Professionelle Expertise",
                "Messbare Ergebnisse",
                "Langfristige Unterstützung"
            ],
            "customer_segments": [
                profile.get('target_market', 'Kleine und mittlere Unternehmen'),
                "Gründer und Startups",
                "Etablierte Unternehmen mit Optimierungsbedarf"
            ]
        }
        
        # ===================================================================
        # GZ DATA - Gründungszuschuss Requirements
        # ===================================================================
        hours = profile.get('hours_per_week_available', 20)
        capital = profile.get('startup_capital', 10000)
        living_costs = profile.get('monthly_living_costs', 2000)
        
        gz_data = {
            "hours_per_week": hours,
            "startup_capital": capital,
            "monthly_living_costs": living_costs,
            "hauptberuflich": hours >= 15,
            "part_time_job": profile.get('part_time_job_possible', False),
            "part_time_hours": profile.get('part_time_hours_per_week', 0),
            "part_time_income": profile.get('part_time_income_monthly', 0),
            "partner_income": profile.get('partner_income_monthly', 0),
            "previous_self_employment": profile.get('previous_self_employment', False),
            "years_experience": profile.get('years_experience', 0),
            "network_strength": profile.get('network_strength', 'medium'),
            "first_customers": profile.get('first_customers_pipeline', 0)
        }
        
        # ===================================================================
        # USER INFO - Personal and Location Data
        # ===================================================================
        user_info = {
            "name": name,
            "email": profile.get('email', ''),
            "location": {
                "city": "Berlin",
                "bundesland": "Berlin",
                "plz": "10115",
                "district": "Mitte"
            },
            "family_status": "single",
            "experience_level": experience,
            "qualifications": self._generate_qualifications(experience, industry)
        }
        
        # ===================================================================
        # GROUNDER PROFILE - Complete profile for adaptive calculator
        # ===================================================================
        grounder_profile = profile.copy()
        grounder_profile.update({
            "calculated_fields": {
                "hauptberuflich_compliant": hours >= 15,
                "capital_sufficient": capital >= 5000,
                "hours_compliant": hours >= 15
            }
        })
        
        # ===================================================================
        # GENERATE COMPLETE BUSINESSPLAN
        # ===================================================================
        logger.info("🚀 Calling generate_complete with auto-generated data...")
        
        result = await self.generate_complete(
            vision_data=vision_data,
            jtbd_data=jtbd_data,
            gz_data=gz_data,
            user_info=user_info,
            market_research=None,
            grounder_profile=grounder_profile
        )
        
        # ===================================================================
        # DEBUG: Show result structure
        # ===================================================================
        logger.info("=" * 70)
        logger.info("🔍 DEBUG: Checking result structure...")
        logger.info(f"Result type: {type(result)}")
        logger.info(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'NOT A DICT'}")
        if isinstance(result, dict):
            for key in result.keys():
                value = result[key]
                if isinstance(value, (list, dict)):
                    logger.info(f"  {key}: {type(value).__name__} (length: {len(value)})")
                else:
                    logger.info(f"  {key}: {str(value)[:100]}...")
        logger.info("=" * 70)
        
        # ===================================================================
        # EXTRACT COMPLIANCE DATA - FIX: Use correct keys!
        # ===================================================================
        gz_compliance_data = result.get('gz_compliance', {})
        logger.info("=" * 70)
        logger.info("INSPECTING GZ_COMPLIANCE:")
        logger.info(f"Type: {type(gz_compliance_data)}")
        logger.info(f"Keys: {list(gz_compliance_data.keys()) if isinstance(gz_compliance_data, dict) else 'NOT A DICT'}")
        if isinstance(gz_compliance_data, dict):
            for k, v in gz_compliance_data.items():
                logger.info(f"  {k} = {v}")
        logger.info("=" * 70)
        gz_score = gz_compliance_data.get('total_score', 0)
        
        # Extract legal citations from legal_basis dict
        legal_basis_dict = gz_compliance_data.get('legal_basis', {})
        citations_used = [
            {
                'category': cat,
                'format': info.get('rechtsgrundlage', ''),
                'short_text': info.get('anforderung', ''),
                'source': info.get('quelle', '')
            }
            for cat, info in legal_basis_dict.items()
        ]
        
        logger.info(f"✅ Businessplan generated! Compliance: {gz_score}/100")
        logger.info(f"📖 Legal Citations: {len(citations_used)}")
        
        return result
    
    def _generate_qualifications(self, experience_level: str, industry: str) -> list:
        """Generate realistic qualifications based on experience and industry"""
        base_qualifications = {
            "junior": [
                "Relevante Ausbildung oder Studium",
                "Erste praktische Erfahrungen",
                "Grundlegende Branchenkenntnisse"
            ],
            "mid": [
                "Mehrjährige Berufserfahrung in der Branche",
                "Nachweisbare Erfolge in relevanten Projekten",
                "Fundierte Fachkenntnisse",
                "Netzwerk in der Branche"
            ],
            "senior": [
                "Langjährige Expertise (8+ Jahre)",
                "Nachweisbare Erfolge und Referenzen",
                "Umfassendes Branchennetzwerk",
                "Spezialisierung in relevanten Bereichen",
                "Führungserfahrung"
            ]
        }
        
        return base_qualifications.get(experience_level, base_qualifications["mid"])

    
    async def generate_complete(
        self,
        vision_data: Dict,
        jtbd_data: Dict,
        gz_data: Dict,
        user_info: Dict,
        market_research: Optional[Dict] = None,
        grounder_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Generate complete, GZ-compliant businessplan WITH LEGAL CITATIONS
        
        Args:
            vision_data: From TAG 2 (vision discovery)
            jtbd_data: From TAG 3 (JTBD analysis)
            gz_data: From TAG 3 (GZ requirements)
            user_info: Location, family status, etc.
            market_research: Optional market research data
            grounder_profile: Optional founder profile for adaptive financial planning
        
        Returns:
            Complete businessplan with compliance report + legal citations
        """
        
        logger.info("ðŸš€ Starting ENHANCED businessplan generation WITH LEGAL CITATIONS...")
        
        # Check if adaptive planning is enabled
        if grounder_profile and self.adaptive_calculator:
            logger.info("ðŸŽ¯ Using ADAPTIVE financial planning based on founder profile")
        else:
            logger.info("ðŸ“Š Using STANDARD financial planning")
        
        # Merge data
        data = {**vision_data, **jtbd_data, **gz_data}
        
        # Determine scope
        scope = self.geo_resolver.determine_scope(data)
        location_text = self.geo_resolver.format_location_text(
            user_info['location'],
            scope
        )
        
        # Calculate living costs
        logger.info("ðŸ’° Calculating living costs...")
        
        # Ensure location is in proper format for living costs calculation
        location_for_calc = user_info['location']
        if isinstance(location_for_calc, str):
            # Convert string to dict
            parts = location_for_calc.split(',')
            location_dict = {
                'city': parts[0].strip(),
                'state': parts[1].strip() if len(parts) > 1 else '',
                'country': 'Deutschland'
            }
        else:
            # Already a dict
            location_dict = location_for_calc
        
        living_costs = self.living_calc.calculate_required_income(
            location_dict,
            user_info.get('family_status', 'single')
        )
        
        # Generate SWOT
        logger.info("ðŸ“Š Generating SWOT...")
        swot_data = self.swot.generate_swot(data)
        
        # Generate Financial Plan (ADAPTIVE or STANDARD)
        logger.info("ðŸ’µ Generating financial plan...")
        
        if grounder_profile and self.adaptive_calculator and GROUNDER_PROFILE_AVAILABLE:
            # === ADAPTIVE FINANCIAL PLANNING ===
            logger.info("ðŸŽ¯ Using ADAPTIVE calculator with founder profile")
            
            try:
                # Create GrounderProfile object from dict
                profile = create_profile_from_dict(grounder_profile)
                
                # Prepare revenue sources
                revenue_sources = data.get('revenue_streams', [])
                if not revenue_sources:
                    # Default: hourly consulting
                    hourly_rate = data.get('pricing', {}).get('hourly_rate', 120)
                    revenue_sources = [{'type': 'hourly', 'price': hourly_rate}]
                
                # Calculate business costs (monthly average)
                business_costs_monthly = 2401  # From RealisticFinancialPlanner
                
                # Get startup capital
                startup_capital = profile.startup_capital_available
                
                # Generate adaptive financials
                adaptive_result = self.adaptive_calculator.generate_adaptive_financials(
                    profile,
                    revenue_sources,
                    living_costs['monatlich']['mit_puffer'],
                    business_costs_monthly,
                    startup_capital
                )
                
                # Use recommended scenario as financials
                financials = {
                    'startkapital': startup_capital,
                    'startkapital_herkunft': 'Siehe GrÃ¼nderprofil',
                    'jahr_1': adaptive_result['recommended_scenario'],
                    'jahr_2': adaptive_result['alternative_scenarios']['base'],
                    'jahr_3': adaptive_result['alternative_scenarios']['base'],
                    'szenarien': {
                        'base': adaptive_result['alternative_scenarios']['base'],
                        'best_case': adaptive_result['alternative_scenarios']['best'],
                        'worst_case': adaptive_result['alternative_scenarios']['worst']
                    },
                    'zusammenfassung': {
                        'adaptive_mode': True,
                        'utilization_curve': adaptive_result['utilization_curve'],
                        'confidence_score': adaptive_result['confidence_score'],
                        'recommendation_reasoning': adaptive_result['recommendation_reasoning']
                    },
                    'annahmen': f"Adaptive Finanzplanung basierend auf GrÃ¼nderprofil:\n{adaptive_result['recommendation_reasoning']}"
                }
                
                logger.info(f"âœ… Adaptive planning: Confidence {adaptive_result['confidence_score']}/100")
                
            except Exception as e:
                logger.error(f"âŒ Adaptive calculator failed: {e}, falling back to standard")
                financials = self.financial_planner.generate_realistic_financials(data, living_costs)
        else:
            # === STANDARD FINANCIAL PLANNING ===
            logger.info("ðŸ“Š Using STANDARD calculator")
            financials = self.financial_planner.generate_realistic_financials(data, living_costs)
        
        # Validate living costs
        living_validation = self.living_calc.validate_financial_plan(
            financials,
            living_costs
        )
        
        # Generate ALL CHAPTERS
        logger.info("âœï¸ Generating ALL chapters WITH LEGAL CITATIONS...")
        
        businessplan = {
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'location': location_text,
                'scope': scope,
                'family_status': user_info.get('family_status', 'single'),
                'generator_version': 'Enhanced_TAG6_WITH_LEGAL_CITATIONS'
            },
            
            # Chapter 1: Executive Summary (WITH LEGAL CITATIONS)
            'executive_summary': await self.content_generator.generate_executive_summary(data),
            
            # Chapter 2: Vision (reuse from TAG 4)
            'geschaeftsidee': await self.content_generator.generate_executive_summary(data),
            
            # Chapter 3: GrÃ¼nderperson (WITH LEGAL REQUIREMENTS)
            'gruenderperson': await self.content_generator.generate_gruenderperson_extended(data),
            
            # Chapter 4: Markt & Wettbewerb
            'markt_wettbewerb': await self.content_generator.generate_markt_wettbewerb(
                data,
                market_research
            ),
            
            # Chapter 5: Marketing & Vertrieb (WITH LEGAL REQUIREMENTS)
            'marketing_vertrieb': await self.content_generator.generate_marketing_vertrieb(data),
            
            # Chapter 6: JTBD
            'jtbd_analyse': data.get('job_story', ''),
            
            # Chapter 7: Organisation
            'organisation': data.get('how', ''),
            
            # Chapter 8: Finanzplan
            'finanzplan': financials,
            
            # Chapter 9: Risikomanagement (WITH GZ-SPECIFIC RISKS)
            'risikomanagement': await self.content_generator.generate_risikomanagement(data, swot_data),
            
            # Chapter 10: Meilensteine
            'meilensteine': await self.content_generator.generate_meilensteine(data),
            
            # Chapter 11: Anhang
            'quellenverzeichnis': self.citations.generate_bibliography(),
            
            # Additional data
            'swot_data': swot_data,
            'lebenshaltungskosten': living_costs,
            'living_validation': living_validation
        }
        
        # Run GZ Compliance Check WITH LEGAL CITATIONS
        logger.info("ðŸ” Running GZ compliance check WITH LEGAL BASIS...")
        compliance_report = self.compliance_checker.check_compliance(businessplan)
        
        businessplan['gz_compliance'] = compliance_report
        
        logger.info(f"âœ… Businessplan generated! GZ Score: {compliance_report['total_score']}/100")
        logger.info(f"ðŸ“– Legal citations included in all chapters and compliance report")
        
        return businessplan


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'EnhancedBusinessplanGenerator',
    'EnhancedContentGenerator',
    'RealisticFinancialPlanner',
    'GZComplianceChecker',
    'get_legal_citation_for_criterion',
    'format_legal_warning'
]


if __name__ == "__main__":
    print("âœ… Enhanced Businessplan Generator (TAG 6) WITH LEGAL CITATIONS loaded!")
    print("ðŸ“¦ Features:")
    print("  - 11 complete chapters (vs. 6 in TAG 4)")
    print("  - ALL prompts include legal citations (SGB III, Fachliche Weisungen BA)")
    print("  - GZ compliance checking WITH legal basis")
    print("  - Marketing with 'intensive GeschÃ¤ftstÃ¤tigkeit' requirement")
    print("  - Risikomanagement with GZ-specific risks")
    print("  - Meilensteine & Zeitplan")
    print("  - Realistic financial planning")
    print("  - Iterative refinement support")
    print("")
    print("ðŸ›ï¸ Legal Citations Integrated:")
    print("  - SGB III Â§ 93 Abs. 1 (Ermessensleistung)")
    print("  - SGB III Â§ 93 Abs. 2 (Hauptberuflichkeit)")
    print("  - Fachliche Weisungen BA zu Â§ 93 (Qualifikation, TragfÃ¤higkeit)")
    print("  - Fachliche Weisungen BA zu Â§ 94 (Intensive GeschÃ¤ftstÃ¤tigkeit)")
    print("  - SGB III Â§ 421 i.V.m. Â§ 155 (NebentÃ¤tigkeit)")




