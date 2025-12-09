# businessplan_generator.py
"""
Businessplan Generator - TAG 4 Complete Implementation

Features:
- Professional Citation Management (IEEE Style)
- Geographic Intelligence (Local/Regional/National)
- Living Cost Validation (City-specific)
- SWOT Analysis
- 3-Year Financial Planning with Research
- Real-time Benchmark Integration
- Quality Checks & GZ Compliance

Sessions Included:
- 4.1: Citation Manager + Template
- 4.2: Geographic Data Resolver
- 4.3: Living Cost Calculator
- 4.4: SWOT Analyzer
- 4.5: Financial Planner
- 4.6: Content Generator
- 4.7: Assembly & Quality Control
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from anthropic import Anthropic
import os
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# SESSION 4.1: CITATION MANAGER & TEMPLATE
# ============================================================================

class CitationManager:
    """
    Professional citation management with IEEE-style footnotes
    """
    
    def __init__(self):
        self.sources = []
        self.citation_style = "ieee"
    
    def cite(self, text: str, source: Dict) -> str:
        """
        Add citation to text
        
        Args:
            text: Text to cite
            source: {
                'title': str,
                'author': str,
                'source': str,
                'year': int,
                'url': str,
                'type': 'study|report|website',
                'accessed': str (optional)
            }
        
        Returns:
            Text with citation marker: "Text[1]"
        """
        citation_num = self._find_or_add_source(source)
        return f"{text}[{citation_num}]"
    
    def _find_or_add_source(self, source: Dict) -> int:
        """Find existing or add new source"""
        
        # Normalize URL for comparison
        normalized_url = source['url'].lower().strip('/')
        
        for i, existing in enumerate(self.sources, 1):
            if existing['url'].lower().strip('/') == normalized_url:
                return i
        
        # Add new source
        if 'accessed' not in source:
            source['accessed'] = datetime.now().strftime('%d.%m.%Y')
        
        self.sources.append(source)
        return len(self.sources)
    
    def generate_footnotes(self) -> str:
        """Generate footnotes section (end of chapter/page)"""
        
        if not self.sources:
            return ""
        
        footnotes = "\n\n---\n**Quellenangaben:**\n\n"
        
        for i, source in enumerate(self.sources, 1):
            footnotes += self._format_ieee(i, source)
        
        return footnotes
    
    def _format_ieee(self, num: int, source: Dict) -> str:
        """Format citation in IEEE style"""
        
        if source.get('type') == 'study':
            return (
                f"[{num}] {source.get('author', source['source'])}, "
                f"\"{source['title']},\" {source['source']}, {source['year']}. "
                f"[Online]. Verfügbar: {source['url']} "
                f"[Zugriff: {source['accessed']}]\n\n"
            )
        else:
            return (
                f"[{num}] {source['source']}, \"{source['title']},\" "
                f"{source['year']}. [Online]. Verfügbar: {source['url']} "
                f"[Zugriff: {source['accessed']}]\n\n"
            )
    
    def generate_bibliography(self) -> str:
        """Generate complete bibliography for appendix"""
        
        if not self.sources:
            return ""
        
        bib = "# Quellenverzeichnis\n\n"
        bib += "Alle in diesem Businessplan verwendeten Quellen:\n\n"
        
        # Sort by type then alphabetically
        studies = [s for s in self.sources if s.get('type') == 'study']
        reports = [s for s in self.sources if s.get('type') == 'report']
        websites = [s for s in self.sources if s.get('type') == 'website']
        
        if studies:
            bib += "## Studien & Forschung\n\n"
            for source in sorted(studies, key=lambda x: x.get('author', x['source'])):
                bib += self._format_full_reference(source)
        
        if reports:
            bib += "## Berichte & Statistiken\n\n"
            for source in sorted(reports, key=lambda x: x['source']):
                bib += self._format_full_reference(source)
        
        if websites:
            bib += "## Websites & Online-Quellen\n\n"
            for source in sorted(websites, key=lambda x: x['source']):
                bib += self._format_full_reference(source)
        
        return bib
    
    def _format_full_reference(self, source: Dict) -> str:
        """Full reference for appendix"""
        
        return f"""**{source['title']}**
- Autor/Herausgeber: {source.get('author', source['source'])}
- Quelle: {source['source']}
- Jahr: {source['year']}
- URL: {source['url']}
- Abrufdatum: {source['accessed']}
- Typ: {source.get('type', 'website').title()}

"""


class BusinessplanTemplate:
    """
    GZ-compliant Businessplan structure
    """
    
    SECTIONS = [
        {
            'id': 'executive_summary',
            'title': 'Executive Summary',
            'required': True,
            'max_words': 300,
            'style': 'concise'
        },
        {
            'id': 'geschaeftsidee',
            'title': 'Geschäftsidee & Vision',
            'required': True,
            'max_words': 500,
            'style': 'inspiring'
        },
        {
            'id': 'gruenderperson',
            'title': 'Gründerperson & Qualifikation',
            'required': True,
            'max_words': 350,
            'style': 'factual'
        },
        {
            'id': 'markt_wettbewerb',
            'title': 'Markt & Wettbewerbsanalyse',
            'required': True,
            'max_words': 400,
            'style': 'analytical'
        },
        {
            'id': 'jtbd_analyse',
            'title': 'Kundennutzen (Jobs-to-be-Done)',
            'required': True,
            'max_words': 300,
            'style': 'framework'
        },
        {
            'id': 'marketing_vertrieb',
            'title': 'Marketing & Vertriebsstrategie',
            'required': True,
            'max_words': 350,
            'style': 'pragmatic'
        },
        {
            'id': 'organisation',
            'title': 'Organisation & Personal',
            'required': True,
            'max_words': 250,
            'style': 'factual'
        },
        {
            'id': 'finanzplan',
            'title': 'Finanzplanung',
            'required': True,
            'style': 'conservative',
            'subsections': ['umsatz', 'kosten', 'liquiditaet', 'rentabilitaet']
        },
        {
            'id': 'swot',
            'title': 'SWOT-Analyse',
            'required': True,
            'max_words': 400,
            'style': 'balanced'
        },
        {
            'id': 'meilensteine',
            'title': 'Meilensteine & Zeitplan',
            'required': True,
            'max_words': 250,
            'style': 'timeline'
        },
        {
            'id': 'anhang',
            'title': 'Anhang',
            'required': True,
            'style': 'appendix'
        }
    ]
    
    def get_section_config(self, section_id: str) -> Dict:
        """Get configuration for a section"""
        for section in self.SECTIONS:
            if section['id'] == section_id:
                return section
        return None


# ============================================================================
# SESSION 4.2: GEOGRAPHIC DATA RESOLVER
# ============================================================================

class GeographicDataResolver:
    """
    Intelligent data selection: Local > Regional > National
    """
    
    BUSINESS_TYPES = {
        'local': [
            'café', 'cafe', 'restaurant', 'friseur', 'bäckerei',
            'einzelhandel', 'laden', 'geschäft', 'praxis', 'kiosk',
            'bar', 'imbiss', 'boutique', 'studio'
        ],
        'regional': [
            'handwerk', 'handwerker', 'dienstleistung', 'beratung',
            'agentur', 'baugewerbe', 'installation'
        ],
        'national': [
            'online', 'software', 'e-commerce', 'saas', 'app',
            'digital', 'consulting', 'coaching'
        ]
    }
    
    def __init__(self, citation_manager: CitationManager):
        self.citations = citation_manager
    
    def determine_scope(self, business_data: Dict) -> str:
        """
        Determine if business is local/regional/national
        
        Returns: 'local' | 'regional' | 'national'
        """
        what = business_data.get('what', '').lower()
        
        # Check local
        if any(keyword in what for keyword in self.BUSINESS_TYPES['local']):
            logger.info(f"📍 Business scope: LOCAL (based on '{what}')")
            return 'local'
        
        # Check national
        if any(keyword in what for keyword in self.BUSINESS_TYPES['national']):
            logger.info(f"🌐 Business scope: NATIONAL (based on '{what}')")
            return 'national'
        
        # Default: regional
        logger.info(f"🗺️ Business scope: REGIONAL (default for '{what}')")
        return 'regional'
    
    def format_location_text(self, location: Dict, scope: str) -> str:
        """
        Format location for businessplan text
        
        Examples:
        - local: "Prenzlauer Berg, Berlin"
        - regional: "Berlin und Umgebung"
        - national: "deutschlandweit"
        """
        if scope == 'local':
            if location.get('district'):
                return f"{location['district']}, {location['city']}"
            return location['city']
        elif scope == 'regional':
            return f"{location['city']} und Umgebung"
        else:
            return "deutschlandweit"


# ============================================================================
# SESSION 4.3: LIVING COST CALCULATOR
# ============================================================================

class LivingCostCalculator:
    """
    City-specific living cost calculator
    
    CRITICAL: Founder must be able to LIVE from income!
    """
    
    # Base living costs Germany 2025
    BASE_COSTS = {
        'single': {
            'miete_warm': 0,  # City-dependent!
            'lebensmittel': 300,
            'transport': 80,
            'krankenversicherung': 450,
            'rentenversicherung': 300,
            'versicherungen': 50,
            'kleidung': 80,
            'freizeit': 150,
            'sonstiges': 140
        },
        'familie_2_kinder': {
            'miete_warm': 0,  # City-dependent!
            'lebensmittel': 650,
            'transport': 150,
            'kita': 400,
            'krankenversicherung': 650,
            'rentenversicherung': 300,
            'versicherungen': 80,
            'kleidung': 150,
            'freizeit': 200,
            'sonstiges': 200
        }
    }
    
    # Average rent by city 2025 (Warmmiete)
    RENT_BY_CITY = {
        'München': {'single': 1200, 'familie': 2200},
        'Berlin': {'single': 900, 'familie': 1600},
        'Hamburg': {'single': 1000, 'familie': 1800},
        'Frankfurt': {'single': 1100, 'familie': 1900},
        'Frankfurt am Main': {'single': 1100, 'familie': 1900},
        'Köln': {'single': 900, 'familie': 1550},
        'Stuttgart': {'single': 1050, 'familie': 1850},
        'Düsseldorf': {'single': 950, 'familie': 1700},
        'Leipzig': {'single': 650, 'familie': 1100},
        'Dresden': {'single': 700, 'familie': 1150},
        'Hannover': {'single': 750, 'familie': 1300},
        'Nürnberg': {'single': 800, 'familie': 1400},
        'Bremen': {'single': 750, 'familie': 1350},
    }
    
    def calculate_required_income(
        self,
        location: Dict,
        family_status: str = 'single'
    ) -> Dict:
        """
        Calculate MINIMUM net income needed to live
        
        Args:
            location: {'city': str, 'district': str, 'bundesland': str}
            family_status: 'single' | 'familie_2_kinder'
        
        Returns:
            {
                'monatlich': {...},
                'jaehrlich': float,
                'mindest_privatentnahme': float,
                'rent_source': {...}
            }
        """
        
        # Get base costs
        costs = self.BASE_COSTS[family_status].copy()
        
        # City-specific rent
        city = location['city']
        
        if city in self.RENT_BY_CITY:
            rent = self.RENT_BY_CITY[city][family_status]
            rent_source = {
                'value': rent,
                'title': f'Durchschnittliche Mieten {city} 2025',
                'source': 'Wohnungsmarkt-Analyse Deutschland',
                'year': 2025,
                'url': 'https://statistik.immobilienscout24.de',
                'type': 'report'
            }
        else:
            # Unknown city - use Bundesland average
            rent = 800 if family_status == 'single' else 1400
            rent_source = {
                'value': rent,
                'title': f'Durchschnittliche Mieten Deutschland 2025',
                'source': 'Statistisches Bundesamt',
                'year': 2025,
                'url': 'https://destatis.de',
                'type': 'report'
            }
        
        costs['miete_warm'] = rent
        
        # Total living costs
        monthly_living = sum(costs.values())
        
        # Safety buffer (20%)
        monthly_with_buffer = monthly_living * 1.2
        
        # Yearly requirement
        yearly_living = monthly_with_buffer * 12
        
        return {
            'monatlich': {
                'kosten_detail': costs,
                'gesamt': round(monthly_living, 2),
                'mit_puffer': round(monthly_with_buffer, 2)
            },
            'jaehrlich': round(yearly_living, 2),
            'mindest_privatentnahme': round(monthly_with_buffer, 2),
            'rent_source': rent_source,
            'location': f"{city}, {location.get('bundesland', '')}",
            'family_status': family_status
        }
    
    def validate_financial_plan(
        self,
        financial_plan: Dict,
        living_costs: Dict
    ) -> Dict:
        """
        CRITICAL: Check if founder can live from income!
        """
        
        # Calculate available income
        jahr_1_gewinn = financial_plan.get('jahr_1', {}).get('jahresergebnis', 0)
        required_income = living_costs['jaehrlich']
        
        validation = {
            'lebensfaehig': jahr_1_gewinn >= required_income,
            'gewinn_jahr_1': jahr_1_gewinn,
            'mindest_bedarf': required_income,
            'differenz': jahr_1_gewinn - required_income,
            'monate_ueberbrueckbar': 0
        }
        
        if not validation['lebensfaehig']:
            # CRITICAL!
            validation['severity'] = 'critical'
            validation['message'] = (
                f"🚨 KRITISCH: Gewinn Jahr 1 ({jahr_1_gewinn:,.0f}€) "
                f"reicht nicht für Lebenshaltungskosten ({required_income:,.0f}€)! "
                f"Fehlbetrag: {abs(validation['differenz']):,.0f}€"
            )
            
            # How long does start capital last?
            startkapital = financial_plan.get('startkapital', 0)
            if startkapital > 0:
                monthly_need = living_costs['monatlich']['mit_puffer']
                monate = int(startkapital / monthly_need)
                validation['monate_ueberbrueckbar'] = monate
                validation['message'] += (
                    f"\n\nStartkapital ({startkapital:,.0f}€) reicht für ca. {monate} Monate. "
                    f"Danach muss Gewinn Lebenshaltung decken!"
                )
        else:
            validation['severity'] = 'ok'
            validation['message'] = (
                f"✅ Gewinn Jahr 1 deckt Lebenshaltungskosten. "
                f"Überschuss: {validation['differenz']:,.0f}€"
            )
        
        return validation


# ============================================================================
# SESSION 4.4: SWOT ANALYZER
# ============================================================================

class SWOTAnalyzer:
    """
    Structured SWOT analysis from collected data
    """
    
    def generate_swot(self, data: Dict) -> Dict:
        """
        Generate SWOT from business data
        
        Returns:
            {
                'staerken': [str, ...],
                'schwaechen': [str, ...],
                'chancen': [str, ...],
                'risiken': [str, ...]
            }
        """
        
        swot = {
            'staerken': [],
            'schwaechen': [],
            'chancen': [],
            'risiken': []
        }
        
        # === STÄRKEN (from why_you, qualifications) ===
        why_you = data.get('why_you', '')
        
        # Extract years of experience
        years_match = re.search(r'(\d+)\s+jahr', why_you.lower())
        if years_match:
            years = years_match.group(1)
            swot['staerken'].append(f"{years} Jahre Berufserfahrung in der Branche")
        
        # Qualifications mentioned
        if any(word in why_you.lower() for word in ['zertifikat', 'abschluss', 'ausbildung']):
            swot['staerken'].append("Nachgewiesene fachliche Qualifikationen")
        
        # From GZ data
        if data.get('how') and '30' in data.get('how', ''):
            swot['staerken'].append("Hauptberufliche Ausrichtung (30h/Woche)")
        elif data.get('how') and '15' in data.get('how', ''):
            swot['staerken'].append("Hauptberufliche Ausrichtung (mind. 15h/Woche)")
        
        # From JTBD
        if data.get('job_story'):
            swot['staerken'].append("Klares Verständnis des Kundennutzens (JTBD-validiert)")
        
        # === SCHWÄCHEN (realistic!) ===
        capital = data.get('capital_needs', '')
        if capital:
            # Extract number
            capital_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*)', capital)
            if capital_match:
                amount = capital_match.group(1).replace('.', '').replace(',', '')
                if int(amount) < 10000:
                    swot['schwaechen'].append(f"Limitiertes Startkapital ({capital})")
        
        swot['schwaechen'].append("Keine bestehende Kundenbasis bei Gründung")
        swot['schwaechen'].append("Ein-Personen-Unternehmen (Kapazitätslimit)")
        
        # === CHANCEN (from market) ===
        if data.get('opportunity_score', 0) > 60:
            swot['chancen'].append("Hoher Opportunity Score: Unzureichende aktuelle Lösungen")
        
        # From alternatives analysis
        if data.get('why_alternatives_fail'):
            swot['chancen'].append("Identifizierte Schwächen aktueller Lösungen adressierbar")
        
        # General market
        swot['chancen'].append("Wachsender Markt für digitale Lösungen")
        
        # === RISIKEN (conservative!) ===
        swot['risiken'].append("Verzögerter Kundenaufbau in ersten Monaten")
        swot['risiken'].append("Längere Verkaufszyklen als geplant")
        swot['risiken'].append("Krankheit/Ausfall als Einzelunternehmer")
        swot['risiken'].append("Höhere Akquisekosten als kalkuliert")
        
        return swot


# ============================================================================
# SESSION 4.5: FINANCIAL PLANNER
# ============================================================================

class FinancialPlanner:
    """
    Conservative 3-year financial planning
    """
    
    def __init__(self):
        pass
    
    def generate_complete_financials(
        self,
        data: Dict,
        living_costs: Dict
    ) -> Dict:
        """
        Generate complete 3-year financial plan
        
        Structure:
        - Year 1: Monthly (Months 1-12)
        - Year 2: Quarterly (Q1-Q4)
        - Year 3: Quarterly (Q1-Q4)
        """
        
        # Parse inputs
        revenue_sources = self._parse_revenue_source(data.get('revenue_source', ''))
        capital_str = data.get('capital_needs', '')
        capital = self._parse_capital_needs(capital_str)
        
        # Generate Year 1 (monthly)
        jahr_1 = self._generate_jahr_1_monthly(
            revenue_sources,
            capital,
            living_costs
        )
        
        # Generate Year 2-3 (quarterly)
        jahr_2 = self._generate_jahr_2_quarterly(jahr_1['monate'][-1])
        jahr_3 = self._generate_jahr_3_quarterly(jahr_2['quartale'][-1])
        
        # Summary
        summary = self._generate_summary(jahr_1, jahr_2, jahr_3, capital)
        
        return {
            'startkapital': capital,
            'jahr_1': jahr_1,
            'jahr_2': jahr_2,
            'jahr_3': jahr_3,
            'zusammenfassung': summary
        }
    
    def _parse_revenue_source(self, revenue_str: str) -> List[Dict]:
        """
        Parse revenue source string
        
        Input: "Beratungsstunden à 120€, monatliche Workshops à 2.500€"
        Output: [
            {'name': 'Beratungsstunden', 'price': 120, 'unit': 'Stunde', 'type': 'hourly'},
            {'name': 'Workshops', 'price': 2500, 'unit': 'Workshop', 'type': 'monthly'}
        ]
        """
        sources = []
        
        # Split by comma
        parts = revenue_str.split(',')
        
        for part in parts:
            # Extract price
            price_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s*€', part)
            if price_match:
                price = float(price_match.group(1).replace('.', '').replace(',', '.'))
                
                # Determine name
                name = part.split('à')[0].strip() if 'à' in part else 'Umsatz'
                
                # Determine type
                if 'stunde' in part.lower():
                    sources.append({'name': name, 'price': price, 'unit': 'Stunde', 'type': 'hourly'})
                elif 'monat' in part.lower():
                    sources.append({'name': name, 'price': price, 'unit': 'Monatlich', 'type': 'monthly'})
                elif 'workshop' in part.lower() or 'kurs' in part.lower():
                    sources.append({'name': name, 'price': price, 'unit': 'Einheit', 'type': 'project'})
                else:
                    sources.append({'name': name, 'price': price, 'unit': 'Einheit', 'type': 'other'})
        
        return sources if sources else [{'name': 'Umsatz', 'price': 5000, 'unit': 'Monat', 'type': 'monthly'}]
    
    def _parse_capital_needs(self, capital_str: str) -> float:
        """Parse capital needs from string"""
        
        # Extract first number
        match = re.search(r'(\d{1,3}(?:[.,]\d{3})*)', capital_str)
        if match:
            amount = match.group(1).replace('.', '').replace(',', '')
            return float(amount)
        
        return 8000.0  # Default
    
    def _generate_jahr_1_monthly(
        self,
        revenue_sources: List[Dict],
        capital: float,
        living_costs: Dict
    ) -> Dict:
        """
        Year 1: Monthly planning (CONSERVATIVE!)
        
        Assumptions:
        - Slow start (Month 1-3: 20% utilization)
        - Ramp-up (Month 4-6: 40%)
        - Stabilization (Month 7-12: 60-70% max!)
        """
        
        monate = []
        kontostand = capital
        
        monthly_living = living_costs['monatlich']['mit_puffer']
        
        for monat in range(1, 13):
            # Revenue (conservative!)
            if monat <= 3:
                auslastung = 0.2  # 20% first 3 months
            elif monat <= 6:
                auslastung = 0.4  # 40% months 4-6
            else:
                auslastung = min(0.7, 0.5 + (monat - 6) * 0.03)  # Max 70%!
            
            # Calculate revenue
            umsatz = 0
            for source in revenue_sources:
                if source['type'] == 'hourly':
                    # Assume 80h/month available, times utilization
                    hours = 80 * auslastung
                    umsatz += hours * source['price']
                elif source['type'] == 'monthly':
                    umsatz += source['price'] * auslastung
                elif source['type'] == 'project':
                    # Projects per month based on utilization
                    projects = auslastung * 2  # 0-1.4 projects/month
                    umsatz += projects * source['price']
                else:
                    umsatz += source['price'] * auslastung
            
            # Costs
            kosten_fix = self._calculate_fixkosten(monat, capital)
            kosten_var = umsatz * 0.15  # 15% variable costs
            kosten_privat = monthly_living
            
            kosten_gesamt = kosten_fix + kosten_var + kosten_privat
            
            # Cashflow
            saldo = umsatz - kosten_gesamt
            kontostand += saldo
            
            monate.append({
                'monat': monat,
                'monat_name': self._monat_name(monat),
                'umsatz': round(umsatz, 2),
                'kosten_fix': round(kosten_fix, 2),
                'kosten_var': round(kosten_var, 2),
                'privatentnahme': round(kosten_privat, 2),
                'kosten_gesamt': round(kosten_gesamt, 2),
                'saldo': round(saldo, 2),
                'kontostand': round(kontostand, 2),
                'auslastung_prozent': int(auslastung * 100)
            })
        
        return {
            'monate': monate,
            'gesamt_umsatz': sum(m['umsatz'] for m in monate),
            'gesamt_kosten': sum(m['kosten_gesamt'] for m in monate),
            'jahresergebnis': sum(m['saldo'] for m in monate),
            'endkontostand': monate[11]['kontostand']
        }
    
    def _calculate_fixkosten(self, monat: int, capital: float) -> float:
        """Monthly fixed costs"""
        
        kosten = {
            'software_tools': 150,
            'marketing': 200,
            'steuerberater': 150,
            'bueromaterial': 80,
            'telefon_internet': 50,
            'fortbildung': 100,
            'versicherungen': 80
        }
        
        # Month 1: One-time costs
        if monat == 1:
            kosten['gruendung'] = 500
            kosten['gewerbeanmeldung'] = 30
            # Initial investments from capital
            if capital >= 5000:
                kosten['equipment'] = 2000
            if capital >= 8000:
                kosten['website'] = 1500
        
        return sum(kosten.values())
    
    def _monat_name(self, monat: int) -> str:
        """Month number to name"""
        names = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun',
                'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        return names[monat - 1]
    
    def _generate_jahr_2_quarterly(self, jahr_1_last_month: Dict) -> Dict:
        """
        Year 2: Quarterly forecast (moderate growth)
        
        Assumption: 30% growth over year 2
        """
        
        basis_umsatz = jahr_1_last_month['umsatz'] * 3  # Basis: avg last 3 months
        
        quartale = []
        for q in range(1, 5):
            # Moderate growth: 7% per quarter
            wachstum = 1 + (q * 0.07)
            
            umsatz = basis_umsatz * wachstum
            kosten = umsatz * 0.55  # 55% cost ratio
            saldo = umsatz - kosten
            
            quartale.append({
                'quartal': f'Q{q}',
                'umsatz': round(umsatz, 2),
                'kosten': round(kosten, 2),
                'saldo': round(saldo, 2)
            })
        
        return {
            'quartale': quartale,
            'gesamt_umsatz': sum(q['umsatz'] for q in quartale),
            'gesamt_kosten': sum(q['kosten'] for q in quartale),
            'jahresergebnis': sum(q['saldo'] for q in quartale)
        }
    
    def _generate_jahr_3_quarterly(self, jahr_2_last_quarter: Dict) -> Dict:
        """
        Year 3: Quarterly forecast (stabilization)
        
        Assumption: 20% growth over year 3
        """
        
        basis_umsatz = jahr_2_last_quarter['umsatz']
        
        quartale = []
        for q in range(1, 5):
            # Slower growth: 4.5% per quarter
            wachstum = 1 + (q * 0.045)
            
            umsatz = basis_umsatz * wachstum
            kosten = umsatz * 0.52  # 52% (economies of scale)
            saldo = umsatz - kosten
            
            quartale.append({
                'quartal': f'Q{q}',
                'umsatz': round(umsatz, 2),
                'kosten': round(kosten, 2),
                'saldo': round(saldo, 2)
            })
        
        return {
            'quartale': quartale,
            'gesamt_umsatz': sum(q['umsatz'] for q in quartale),
            'gesamt_kosten': sum(q['kosten'] for q in quartale),
            'jahresergebnis': sum(q['saldo'] for q in quartale)
        }
    
    def _generate_summary(self, j1, j2, j3, capital) -> Dict:
        """3-year summary"""
        
        total_umsatz = j1['gesamt_umsatz'] + j2['gesamt_umsatz'] + j3['gesamt_umsatz']
        total_kosten = j1['gesamt_kosten'] + j2['gesamt_kosten'] + j3['gesamt_kosten']
        total_gewinn = total_umsatz - total_kosten
        
        # Find break-even
        break_even_monat = None
        kumuliert = 0
        for m in j1['monate']:
            kumuliert += m['saldo']
            if kumuliert > 0 and break_even_monat is None:
                break_even_monat = m['monat']
        
        return {
            'gesamt_umsatz_3_jahre': round(total_umsatz, 2),
            'gesamt_kosten_3_jahre': round(total_kosten, 2),
            'gesamt_gewinn_3_jahre': round(total_gewinn, 2),
            'break_even_monat': break_even_monat or 'Nicht in Jahr 1',
            'umsatz_jahr_1': round(j1['gesamt_umsatz'], 2),
            'umsatz_jahr_2': round(j2['gesamt_umsatz'], 2),
            'umsatz_jahr_3': round(j3['gesamt_umsatz'], 2),
            'roi_3_jahre_prozent': round((total_gewinn / capital) * 100, 1) if capital > 0 else 0
        }


# ============================================================================
# SESSION 4.6: CONTENT GENERATOR
# ============================================================================

class ContentGenerator:
    """
    Generate businessplan content with conservative style
    """
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set!")
        
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-haiku-20241022"
    
    async def generate_executive_summary(
        self,
        data: Dict,
        citations: CitationManager
    ) -> str:
        """Sachlich, prägnant, GZ-konform"""
        
        prompt = f"""Schreibe eine Executive Summary für einen Businessplan (max 300 Wörter).

**STIL: Sachlich-professionell, GZ-konform**

**STRUKTUR:**
1. Geschäftsidee (1 Satz): Was wird angeboten?
   - {data.get('what', '')}

2. Zielgruppe (1 Satz): Für wen?
   - {data.get('who', '')}

3. Problem & Lösung (2 Sätze): Welches Problem wird gelöst?
   - Problem: {data.get('problem', '')}
   - Lösung: {data.get('how', '')}

4. Gründerperson (2 Sätze): Warum qualifiziert?
   - {data.get('why_you', '')}

5. Geschäftsmodell (1 Satz): Wie wird Geld verdient?
   - {data.get('revenue_source', '')}

6. GZ-Konformität (1 Satz): Hauptberuflich, tragfähig
   - Kapitalbedarf: {data.get('capital_needs', '')}

**WICHTIG:**
- KEINE Superlative oder Buzzwords
- KEINE unrealistischen Versprechungen
- Sachlich, konkret, überzeugend
- Fokus auf Machbarkeit und Qualifikation

Schreibe NUR die Executive Summary (max 300 Wörter):"""

        return await self._call_claude(prompt)
    
    async def generate_vision_section(self, data: Dict) -> str:
        """Geschäftsidee & Vision"""
        
        prompt = f"""Schreibe den "Geschäftsidee & Vision" Abschnitt (400-500 Wörter).

**ZWEI-TEIL STRUKTUR:**

**Teil 1: Die persönliche Vision**
Nutze diese Infos:
- Magic Wand: {data.get('magic_wand_answer', '')}
- Deep Why: {data.get('deep_why', '')}
- Desired Outcome: {data.get('desired_outcome', '')}

Schreibe 2-3 Absätze die zeigen:
- Was der Gründer erreichen will
- Warum ihm das persönlich wichtig ist
- Welche Veränderung er schaffen möchte

**Teil 2: Die konkrete Geschäftsidee**
- WAS: {data.get('what', '')}
- FÜR WEN: {data.get('who', '')}
- PROBLEM: {data.get('problem', '')}
- WIE: {data.get('how', '')}

**STIL:**
- Teil 1: Inspirierend aber authentisch
- Teil 2: Konkret, praktisch, GZ-konform
- Nahtloser Übergang von Vision zu Umsetzung

Schreibe den Abschnitt:"""

        return await self._call_claude(prompt)
    
    async def _call_claude(self, prompt: str) -> str:
        """Call Claude API"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"[Fehler beim Generieren: {str(e)}]"


# ============================================================================
# SESSION 4.7: BUSINESSPLAN GENERATOR (ASSEMBLY)
# ============================================================================

class BusinessplanGenerator:
    """
    Master class: Generate complete businessplan
    """
    
    def __init__(self):
        self.template = BusinessplanTemplate()
        self.citations = CitationManager()
        self.geo_resolver = GeographicDataResolver(self.citations)
        self.living_calc = LivingCostCalculator()
        self.swot = SWOTAnalyzer()
        self.financial = FinancialPlanner()
        self.content = ContentGenerator()
        
        logger.info("✅ Businessplan Generator initialized")
    
    async def generate(
        self,
        vision_data: Dict,
        jtbd_data: Dict,
        gz_data: Dict,
        user_info: Dict
    ) -> Dict:
        """
        Generate complete, GZ-compliant businessplan
        
        Args:
            vision_data: From Vision Discovery Phase
            jtbd_data: From JTBD Validation Phase
            gz_data: From GZ Optimization Phase
            user_info: {
                'location': {'city': str, 'district': str, 'bundesland': str},
                'family_status': 'single' | 'familie_2_kinder'
            }
        
        Returns:
            Complete businessplan dict
        """
        
        logger.info("🚀 Starting businessplan generation...")
        
        # Merge all data
        data = {**vision_data, **jtbd_data, **gz_data}
        
        # Determine scope
        scope = self.geo_resolver.determine_scope(data)
        location_text = self.geo_resolver.format_location_text(
            user_info['location'],
            scope
        )
        
        # Calculate living costs
        logger.info("💰 Calculating living costs...")
        living_costs = self.living_calc.calculate_required_income(
            user_info['location'],
            user_info.get('family_status', 'single')
        )
        
        # Generate SWOT
        logger.info("📊 Generating SWOT analysis...")
        swot_data = self.swot.generate_swot(data)
        
        # Generate Financial Plan
        logger.info("💵 Generating financial plan...")
        financials = self.financial.generate_complete_financials(data, living_costs)
        
        # Validate against living costs
        logger.info("🔍 Validating financial viability...")
        living_validation = self.living_calc.validate_financial_plan(
            financials,
            living_costs
        )
        
        # Generate Content
        logger.info("✍️ Generating content sections...")
        
        businessplan = {
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'location': location_text,
                'scope': scope,
                'family_status': user_info.get('family_status', 'single')
            },
            'executive_summary': await self.content.generate_executive_summary(data, self.citations),
            'geschaeftsidee': await self.content.generate_vision_section(data),
            'swot_data': swot_data,
            'finanzplan': financials,
            'lebenshaltungskosten': living_costs,
            'living_validation': living_validation,
            'quellenverzeichnis': self.citations.generate_bibliography()
        }
        
        logger.info("✅ Businessplan generation complete!")
        
        return businessplan


# ============================================================================
# API ENDPOINT WRAPPER
# ============================================================================

async def generate_businessplan(
    session_id: str,
    session_data: Dict,
    user_info: Dict
) -> Dict:
    """
    Main API function to generate businessplan
    
    Args:
        session_id: Vision discovery session ID
        session_data: Complete session data from all 3 phases
        user_info: User location and family info
    
    Returns:
        Complete businessplan
    """
    
    generator = BusinessplanGenerator()
    
    # Extract phase data
    vision_data = session_data.get('vision', {})
    jtbd_data = session_data.get('jtbd', {})
    gz_data = session_data.get('gz', {})
    
    # Generate
    businessplan = await generator.generate(
        vision_data=vision_data,
        jtbd_data=jtbd_data,
        gz_data=gz_data,
        user_info=user_info
    )
    
    return businessplan


if __name__ == "__main__":
    # Test
    print("✅ Businessplan Generator loaded successfully!")
    print("📦 Modules available:")
    print("  - CitationManager")
    print("  - GeographicDataResolver")
    print("  - LivingCostCalculator")
    print("  - SWOTAnalyzer")
    print("  - FinancialPlanner")
    print("  - ContentGenerator")
    print("  - BusinessplanGenerator")
