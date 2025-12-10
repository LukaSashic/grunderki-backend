# adaptive_financial_calculator_full.py
"""
Adaptive Financial Calculator - WITH LEGAL CITATION VALIDATIONS

Berechnet realistische Finanzpläne basierend auf Gründer-Profil
+ Validiert alle Inputs gegen GZ-Anforderungen mit Rechtsgrundlagen

NEW IN THIS VERSION:
- validate_hauptberuflich_hours() - Min. 15h/Woche Validation
- validate_part_time_job() - Nebentätigkeit Validation
- validate_startup_capital() - Kapital Validation
- All validations include legal citations (SGB III § 93, Fachliche Weisungen BA)
- Validation results returned in generate_adaptive_financials()
"""

from typing import Dict, List, Tuple, Optional
import logging

try:
    from grounder_profile import (
        GrounderProfile,
        IndustryType,
        ExperienceLevel,
        NetworkStrength
    )
except ImportError:
    # Fallback for testing
    class IndustryType:
        CONSULTING = "consulting"
        COACHING = "coaching"
        HANDWERK = "handwerk"
    
    class ExperienceLevel:
        EXPERT = "expert"
        SENIOR = "senior"
        JUNIOR = "junior"
        EINSTEIGER = "einsteiger"
    
    class NetworkStrength:
        STRONG = "strong"
        MEDIUM = "medium"
        WEAK = "weak"
        NONE = "none"

logger = logging.getLogger(__name__)


# ====================================================================================
# LEGAL CITATIONS - SUBSET FOR VALIDATIONS
# ====================================================================================

LEGAL_CITATIONS_SUBSET = {
    'gz_hauptberuflich': {
        'format': 'SGB III § 93 Abs. 2',
        'short_text': 'Mind. 15 Stunden/Woche erforderlich für Hauptberuflichkeit',
        'official_source': 'https://www.gesetze-im-internet.de/sgb_3/__93.html'
    },
    'gz_nebentaetigkeit_allowed': {
        'format': 'SGB III § 421 i.V.m. § 155',
        'short_text': 'Nebentätigkeit < 15h/Woche ist erlaubt, aber meldepflichtig',
        'official_source': 'https://www.gesetze-im-internet.de/sgb_3/__155.html'
    },
    'gz_teilzeit_warning': {
        'format': 'Fachliche Weisungen BA zu § 93 SGB III',
        'short_text': 'Bei > 15h/Woche oder > 50% Einkommen droht Rückforderung!',
        'official_source': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-93_ba014875.pdf'
    },
    'gz_teilzeit_minijob': {
        'format': 'Fachliche Weisungen BA zu § 93 SGB III',
        'short_text': 'Minijob (bis 538 EUR) ist möglich, wenn < 15h/Woche',
        'official_source': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-93_ba014875.pdf'
    },
    'gz_tragfaehigkeit': {
        'format': 'Fachliche Weisungen BA zu § 93 SGB III',
        'short_text': 'Tragfähige Existenzgrundlage, Lebenshaltungskosten müssen gedeckt werden',
        'official_source': 'https://www.arbeitsagentur.de/datei/fw-sgb-iii-93_ba014875.pdf'
    }
}


# ====================================================================================
# VALIDATION FUNCTIONS WITH LEGAL CITATIONS
# ====================================================================================

def validate_hauptberuflich_hours(hours_per_week: int) -> Dict:
    """
    Validate if hours meet Hauptberuflichkeit requirement
    
    Args:
        hours_per_week: Hours per week dedicated to business
    
    Returns:
        {
            'valid': bool,
            'error': Optional[str],
            'warning': Optional[str],
            'legal_citation': str,
            'official_source': str,
            'requirement': str,
            'recommendation': Optional[str]
        }
    
    Examples:
        >>> validate_hauptberuflich_hours(30)
        {'valid': True, 'legal_citation': 'SGB III § 93 Abs. 2', ...}
        
        >>> validate_hauptberuflich_hours(12)
        {'valid': False, 'error': '⚠️ Mind. 15 Stunden/Woche erforderlich...', ...}
    """
    citation = LEGAL_CITATIONS_SUBSET['gz_hauptberuflich']
    
    result = {
        'legal_citation': citation['format'],
        'official_source': citation['official_source'],
        'requirement': citation['short_text']
    }
    
    if hours_per_week < 15:
        result.update({
            'valid': False,
            'error': f"""⚠️ GZ-ANFORDERUNG NICHT ERFÜLLT!

Sie haben {hours_per_week} Stunden pro Woche angegeben.

Rechtsgrundlage: {citation['format']}
Anforderung: {citation['short_text']}

Für den Gründungszuschuss ist eine hauptberufliche selbständige Tätigkeit erforderlich.
Dies ist in der Regel bei mindestens 15 Stunden wöchentlich der Fall.

WICHTIG: Bei weniger als 15 Stunden droht:
• Ablehnung des Gründungszuschuss-Antrags
• Rückforderung bereits gezahlter Beträge

Quelle: {citation['official_source']}""",
            'severity': 'CRITICAL',
            'recommendation': 'Erhöhen Sie Ihre wöchentlichen Stunden auf mindestens 15 (besser 20-30 Stunden).'
        })
        return result
    
    if hours_per_week < 20:
        result.update({
            'valid': True,
            'warning': f"""💡 HINWEIS: Niedrige Stundenzahl

Sie haben {hours_per_week} Stunden pro Woche angegeben.

Dies erfüllt zwar das Minimum von 15 Stunden ({citation['format']}), 
aber die Agentur für Arbeit könnte kritisch prüfen ob die Hauptberuflichkeit 
tatsächlich gegeben ist.

EMPFEHLUNG: 
• 20-30 Stunden pro Woche sind sicherer
• Dokumentieren Sie Ihre Arbeitszeiten
• Zeigen Sie intensive Geschäftstätigkeit""",
            'severity': 'INFO',
            'recommendation': '20-30 Stunden pro Woche empfohlen für sichere GZ-Bewilligung.'
        })
        return result
    
    # All good
    result.update({
        'valid': True,
        'note': f"""✅ GZ-KONFORM

{hours_per_week} Stunden pro Woche erfüllen die Hauptberuflichkeits-Anforderung.

Rechtsgrundlage: {citation['format']}"""
    })
    
    return result


def validate_part_time_job(
    part_time_hours: int,
    part_time_income: float,
    main_income_expected: float
) -> Dict:
    """
    Validate if part-time activity meets GZ rules
    
    Args:
        part_time_hours: Hours per week for part-time job
        part_time_income: Monthly income from part-time job
        main_income_expected: Expected monthly income from main business
    
    Returns:
        {
            'valid': bool,
            'error': Optional[str],
            'warning': Optional[str],
            'legal_citations': List[str],
            'requirements': List[str],
            'recommendation': str
        }
    
    Examples:
        >>> validate_part_time_job(10, 500, 2000)
        {'valid': True, 'note': 'Nebentätigkeit ist GZ-konform...'}
        
        >>> validate_part_time_job(20, 1500, 1000)
        {'valid': False, 'error': '🚨 KRITISCH: Nebentätigkeit gefährdet...'}
    """
    
    allowed = LEGAL_CITATIONS_SUBSET['gz_nebentaetigkeit_allowed']
    warning = LEGAL_CITATIONS_SUBSET['gz_teilzeit_warning']
    
    result = {
        'legal_citations': [allowed['format'], warning['format']],
        'official_sources': [allowed['official_source'], warning['official_source']],
        'requirements': [
            'Nebentätigkeit < 15 Stunden wöchentlich',
            'Nebeneinkommen < 50% des Gesamteinkommens',
            'Unverzüglich bei Agentur für Arbeit melden (§ 60 SGB III)'
        ]
    }
    
    # Check hours
    hours_violation = part_time_hours >= 15
    
    # Check income ratio
    total_income = part_time_income + main_income_expected
    if total_income > 0:
        part_time_ratio = (part_time_income / total_income) * 100
    else:
        part_time_ratio = 0
    
    income_violation = part_time_ratio > 50
    
    # CRITICAL: Both violations
    if hours_violation and income_violation:
        result.update({
            'valid': False,
            'error': f"""🚨 KRITISCH: Nebentätigkeit gefährdet Hauptberuflichkeit!

DOPPELTE VERLETZUNG der GZ-Anforderungen:

1. STUNDEN: {part_time_hours}h/Woche (Limit: < 15h)
   Rechtsgrundlage: {allowed['format']}
   
2. EINKOMMEN: {part_time_ratio:.0f}% des Gesamteinkommens (Limit: < 50%)
   Rechtsgrundlage: {warning['format']}

{warning['short_text']}

⚠️ RISIKO:
• Rückforderung des gesamten Gründungszuschusses
• Ablehnung der Phase 2 (weitere 9 Monate)
• Rechtliche Konsequenzen

Quellen: 
{allowed['official_source']}
{warning['official_source']}""",
            'severity': 'CRITICAL',
            'recommendation': 'Reduzieren Sie ENTWEDER Stunden auf max. 14h/Woche ODER Einkommen auf max. 40% des Gesamteinkommens.'
        })
        return result
    
    # CRITICAL: Hours violation only
    if hours_violation:
        result.update({
            'valid': False,
            'error': f"""🚨 KRITISCH: Zu viele Stunden Nebentätigkeit!

Sie haben {part_time_hours} Stunden pro Woche angegeben.

Rechtsgrundlage: {allowed['format']}
Anforderung: Nebentätigkeit < 15 Stunden wöchentlich

{warning['short_text']}

Bei mehr als 15 Stunden wöchentlich ist die Hauptberuflichkeit der selbständigen 
Tätigkeit gefährdet. Dies kann zur Rückforderung des Gründungszuschusses führen.

Quelle: {allowed['official_source']}""",
            'severity': 'CRITICAL',
            'recommendation': 'MAXIMUM: 14 Stunden pro Woche (besser 10-12 Stunden)'
        })
        return result
    
    # CRITICAL: Income violation only
    if income_violation:
        result.update({
            'valid': False,
            'error': f"""🚨 KRITISCH: Nebeneinkommen zu hoch!

Nebeneinkommen: {part_time_ratio:.0f}% des Gesamteinkommens
(Nebenjob: {part_time_income:.0f} EUR, Hauptgeschäft: {main_income_expected:.0f} EUR)

Rechtsgrundlage: {warning['format']}
Anforderung: Nebeneinkommen < 50% des Gesamteinkommens

{warning['short_text']}

Wenn die Nebentätigkeit mehr als 50% des Gesamteinkommens generiert, gefährdet 
dies die Hauptberuflichkeit der selbständigen Tätigkeit.

Quelle: {warning['official_source']}""",
            'severity': 'CRITICAL',
            'recommendation': f'Reduzieren Sie Nebeneinkommen auf max. {main_income_expected * 0.8:.0f} EUR/Monat (40% des Gesamteinkommens)'
        })
        return result
    
    # WARNING: Close to limits
    if part_time_hours >= 12 or part_time_ratio > 40:
        result.update({
            'valid': True,
            'warning': f"""⚠️ VORSICHT: Nahe an GZ-Grenzen!

Aktuelle Situation:
• Stunden: {part_time_hours}h/Woche (Limit: < 15h)
• Einkommen: {part_time_ratio:.0f}% (Limit: < 50%)

Sie sind noch GZ-konform, aber nahe an den Grenzen.

Rechtsgrundlagen:
{allowed['format']}: {allowed['short_text']}
{warning['format']}: {warning['short_text']}

WICHTIG:
• Melden Sie die Nebentätigkeit unverzüglich bei der Agentur für Arbeit (§ 60 SGB III)
• Dokumentieren Sie Ihre Arbeitszeiten
• Beobachten Sie das Einkommensverhältnis""",
            'severity': 'WARNING',
            'recommendation': 'Halten Sie Abstand zu den Grenzen (max. 12h/Woche, max. 40% Einkommen).'
        })
        return result
    
    # All good
    result.update({
        'valid': True,
        'note': f"""✅ NEBENTÄTIGKEIT GZ-KONFORM

Ihre Nebentätigkeit erfüllt die GZ-Anforderungen:
• {part_time_hours}h/Woche (< 15h) ✓
• {part_time_ratio:.0f}% des Einkommens (< 50%) ✓

Rechtsgrundlagen:
{allowed['format']}: {allowed['short_text']}

⚠️ WICHTIG: Unverzüglich bei Agentur für Arbeit melden!

Meldepflicht nach § 60 SGB III:
Alle Änderungen der persönlichen und wirtschaftlichen Verhältnisse müssen 
der Agentur für Arbeit unverzüglich gemeldet werden.

Quelle: {allowed['official_source']}""",
        'reminder': 'Meldung bei Agentur für Arbeit nicht vergessen!',
        'recommendation': 'Dokumentieren Sie Arbeitszeiten und Einnahmen fortlaufend.'
    })
    
    return result


def validate_startup_capital(capital: float, living_costs_monthly: float) -> Dict:
    """
    Validate if startup capital is sufficient
    
    According to Fachliche Weisungen BA: 
    "Sufficient capital to cover living costs and business expenses for several months"
    
    Args:
        capital: Available startup capital (EUR)
        living_costs_monthly: Monthly living costs (EUR)
    
    Returns:
        Validation result with recommendations
    """
    
    citation = LEGAL_CITATIONS_SUBSET['gz_tragfaehigkeit']
    
    months_covered = capital / living_costs_monthly if living_costs_monthly > 0 else 0
    
    result = {
        'legal_citation': citation['format'],
        'official_source': citation['official_source'],
        'requirement': citation['short_text']
    }
    
    if capital < 5000:
        result.update({
            'valid': False,
            'error': f"""⚠️ STARTKAPITAL ZU NIEDRIG

Verfügbar: {capital:.0f} EUR
Monatliche Lebenshaltungskosten: {living_costs_monthly:.0f} EUR
Reichweite: {months_covered:.1f} Monate

Rechtsgrundlage: {citation['format']}
Anforderung: {citation['short_text']}

EMPFEHLUNG: Mindestens 10.000 EUR Startkapital
→ Deckt ca. 3 Monate Lebenshaltungskosten + Geschäftskosten

Quelle: {citation['official_source']}""",
            'severity': 'HIGH',
            'recommendation': 'Erhöhen Sie Startkapital auf mind. 10.000 EUR'
        })
        return result
    
    if months_covered < 2:
        result.update({
            'valid': True,
            'warning': f"""💡 HINWEIS: Geringe Kapitalreserve

Startkapital: {capital:.0f} EUR
Reichweite: {months_covered:.1f} Monate Lebenshaltungskosten

Die fachkundige Stelle könnte dies als zu knapp bewerten.

Rechtsgrundlage: {citation['format']}
Anforderung: {citation['short_text']}

EMPFEHLUNG: 3-6 Monate Lebenshaltungskosten als Puffer
→ Mindestens {living_costs_monthly * 3:.0f} EUR

Quelle: {citation['official_source']}""",
            'severity': 'INFO',
            'recommendation': f'Puffer von {living_costs_monthly * 3:.0f} EUR empfohlen'
        })
        return result
    
    result.update({
        'valid': True,
        'note': f"""✅ STARTKAPITAL AUSREICHEND

{capital:.0f} EUR = {months_covered:.1f} Monate Lebenshaltungskosten

Dies bietet eine solide Grundlage für die Gründung.

Rechtsgrundlage: {citation['format']}"""
    })
    
    return result


# ====================================================================================
# INDUSTRY-SPECIFIC RAMP-UP PROFILES
# ====================================================================================

INDUSTRY_RAMP_PROFILES = {
    "consulting": {
        'base': 0.15,          # 15% Monat 1
        'growth': 0.08,        # 8% growth per month
        'max': 0.65,           # 65% max
        'months_to_max': 10
    },
    "coaching": {
        'base': 0.20,
        'growth': 0.10,
        'max': 0.70,
        'months_to_max': 8
    },
    "handwerk": {
        'base': 0.30,          # Schneller Start (lokal)
        'growth': 0.12,
        'max': 0.80,
        'months_to_max': 6
    },
    "freiberufler": {
        'base': 0.25,
        'growth': 0.10,
        'max': 0.75,
        'months_to_max': 7
    },
    "online": {
        'base': 0.05,          # Langsamer (Traffic-Aufbau)
        'growth': 0.06,
        'max': 0.60,
        'months_to_max': 12
    },
    "dienstleistung": {
        'base': 0.20,
        'growth': 0.09,
        'max': 0.70,
        'months_to_max': 9
    },
    "software": {
        'base': 0.10,
        'growth': 0.07,
        'max': 0.60,
        'months_to_max': 12
    },
    "gastronomie": {
        'base': 0.40,
        'growth': 0.08,
        'max': 0.85,
        'months_to_max': 6
    },
    "einzelhandel": {
        'base': 0.35,
        'growth': 0.10,
        'max': 0.80,
        'months_to_max': 6
    },
    "ecommerce": {
        'base': 0.08,
        'growth': 0.07,
        'max': 0.65,
        'months_to_max': 10
    }
}


# ====================================================================================
# ADAPTIVE FINANCIAL CALCULATOR - WITH VALIDATIONS
# ====================================================================================

class AdaptiveFinancialCalculator:
    """
    Berechnet intelligente Finanzpläne basierend auf Gründer-Profil
    WITH LEGAL CITATION VALIDATIONS
    
    Features:
    - Adaptive utilization curves (Erfahrung, Netzwerk, etc.)
    - Flexible living costs (Partner, Reduzierung)
    - Multiple scenarios (Base, Best, Worst, Optimal mit Teilzeit)
    - Automatic recommendation
    - INPUT VALIDATION with legal citations
    - Validation results included in output
    """
    
    def __init__(self):
        logger.info("✅ Adaptive Financial Calculator initialized WITH VALIDATIONS")
    
    def calculate_utilization_curve(
        self,
        profile: GrounderProfile,
        months: int = 12
    ) -> List[float]:
        """
        Berechne realistische Auslastungs-Kurve
        
        Faktoren:
        - Branche (base ramp-up)
        - Erfahrung (+bonus)
        - Netzwerk (+bonus)
        - First customers (+bonus)
        - Previous self-employment (+bonus)
        
        Returns:
            List of utilization rates (0.0 - 1.0) for each month
        """
        
        # Get industry profile
        industry_key = getattr(profile.industry, 'value', profile.industry) if hasattr(profile, 'industry') else 'consulting'
        industry_profile = INDUSTRY_RAMP_PROFILES.get(
            industry_key,
            INDUSTRY_RAMP_PROFILES['dienstleistung']  # Default
        )
        
        base_rate = industry_profile['base']
        growth_rate = industry_profile['growth']
        max_util = industry_profile['max']
        
        # === MODIFIERS ===
        
        # 1. Experience bonus
        exp_level = getattr(profile.experience_level, 'value', profile.experience_level) if hasattr(profile, 'experience_level') else 'junior'
        
        experience_bonus = 0
        if exp_level == 'expert':
            experience_bonus = 0.10
        elif exp_level == 'senior':
            experience_bonus = 0.07
        elif exp_level == 'junior':
            experience_bonus = 0.03
        
        # 2. Network bonus
        net_strength = getattr(profile.network_strength, 'value', profile.network_strength) if hasattr(profile, 'network_strength') else 'medium'
        
        network_bonus = 0
        if net_strength == 'strong':
            network_bonus = 0.08
        elif net_strength == 'medium':
            network_bonus = 0.05
        elif net_strength == 'weak':
            network_bonus = 0.02
        
        # 3. First customers bonus
        first_customers = getattr(profile, 'first_customers_pipeline', 0)
        first_customer_bonus = min(0.10, first_customers * 0.03)
        
        # 4. Previous self-employment
        prev_self = getattr(profile, 'previous_self_employment', False)
        self_emp_bonus = 0.05 if prev_self else 0
        
        # Total starting bonus
        total_start_bonus = (
            experience_bonus +
            network_bonus +
            first_customer_bonus +
            self_emp_bonus
        )
        
        # Adjusted max
        adjusted_max = min(0.90, max_util + (total_start_bonus * 0.5))
        
        # Generate curve
        curve = []
        for month in range(1, months + 1):
            # Base calculation
            util = base_rate + (growth_rate * (month - 1))
            
            # Add bonuses (diminishing over time)
            bonus_factor = max(0, 1 - (month / 12))
            util += total_start_bonus * bonus_factor
            
            # Cap at max
            util = min(adjusted_max, util)
            
            curve.append(round(util, 3))
        
        logger.info(f"📈 Utilization: {curve[0]:.1%} → {curve[-1]:.1%}")
        
        return curve
    
    def calculate_flexible_living_costs(
        self,
        profile: GrounderProfile,
        base_living_monthly: float,
        months: int = 12
    ) -> Tuple[List[float], Dict]:
        """
        Berechne flexible Living Costs
        
        Faktoren:
        - Partner-Einkommen
        - Temporäre Reduzierung
        - Teilzeit-Job (als zusätzliches Einkommen)
        
        Returns:
            (monthly_costs, metadata)
        """
        
        costs = []
        metadata = {
            'base_monthly': base_living_monthly,
            'effective_base': base_living_monthly,
            'partner_contribution': 0,
            'reduction_applied': False,
            'part_time_income': 0
        }
        
        # 1. Partner income
        partner_income = getattr(profile, 'partner_income_monthly', None)
        if partner_income:
            effective_need = max(0, base_living_monthly - partner_income)
            metadata['effective_base'] = effective_need
            metadata['partner_contribution'] = partner_income
        else:
            effective_need = base_living_monthly
        
        # 2. Calculate monthly
        can_reduce = getattr(profile, 'can_reduce_living_costs', False)
        reduction_months = getattr(profile, 'living_reduction_months', 0)
        reduction_percent = getattr(profile, 'living_reduction_percent', 0)
        
        for month in range(1, months + 1):
            monthly_cost = effective_need
            
            # Apply temporary reduction
            if can_reduce and month <= reduction_months:
                reduction = effective_need * (reduction_percent / 100)
                monthly_cost -= reduction
                metadata['reduction_applied'] = True
            
            costs.append(round(monthly_cost, 2))
        
        # 3. Part-time info (separate from costs)
        part_time_possible = getattr(profile, 'part_time_job_possible', False)
        if part_time_possible:
            pt_income = getattr(profile, 'part_time_income_monthly', 0)
            pt_months = getattr(profile, 'part_time_duration_months', 0)
            
            if pt_income > 0:
                metadata['part_time_income'] = pt_income
                metadata['part_time_months'] = pt_months
        
        logger.info(f"💰 Living costs: {costs[0]:,.0f} EUR/Monat (effective)")
        
        return costs, metadata
    
    def generate_adaptive_financials(
        self,
        profile: GrounderProfile,
        revenue_sources: List[Dict],
        base_living_costs: float,
        business_costs_monthly: float,
        startup_capital: float
    ) -> Dict:
        """
        Generate complete adaptive financial plan WITH VALIDATIONS
        
        Args:
            profile: GrounderProfile
            revenue_sources: [{'type': 'hourly', 'price': 120}, ...]
            base_living_costs: Base living costs
            business_costs_monthly: Avg monthly business costs
            startup_capital: Available startup capital
        
        Returns:
            Complete financial plan with scenarios, recommendation & VALIDATIONS
        """
        
        logger.info("🚀 Generating adaptive financial plan WITH VALIDATIONS...")
        
        # ========================================
        # NEW: VALIDATE INPUTS WITH LEGAL CITATIONS
        # ========================================
        
        validations = {}
        warnings = []
        critical_errors = []
        
        # 1. Validate hours
        hours_per_week = getattr(profile, 'hours_per_week_available', 0)
        hours_validation = validate_hauptberuflich_hours(hours_per_week)
        validations['hours'] = hours_validation
        
        if not hours_validation['valid']:
            critical_errors.append(hours_validation['error'])
            logger.error(f"❌ CRITICAL: Hours validation failed: {hours_validation['error'][:100]}...")
        elif 'warning' in hours_validation:
            warnings.append(hours_validation['warning'])
            logger.warning(f"⚠️ Hours validation warning")
        
        # 2. Validate part-time (if applicable)
        part_time_possible = getattr(profile, 'part_time_job_possible', False)
        if part_time_possible:
            pt_hours = getattr(profile, 'part_time_hours_per_week', 0)
            pt_income = getattr(profile, 'part_time_income_monthly', 0)
            
            # Estimate main income for validation
            # Use average monthly revenue from base scenario
            avg_hourly_rate = revenue_sources[0]['price'] if revenue_sources else 120
            estimated_main_income = avg_hourly_rate * 80 * 0.4  # Conservative estimate
            
            pt_validation = validate_part_time_job(
                pt_hours,
                pt_income,
                estimated_main_income
            )
            validations['part_time'] = pt_validation
            
            if not pt_validation['valid']:
                critical_errors.append(pt_validation['error'])
                logger.error(f"❌ CRITICAL: Part-time validation failed")
            elif 'warning' in pt_validation:
                warnings.append(pt_validation['warning'])
                logger.warning(f"⚠️ Part-time validation warning")
        else:
            validations['part_time'] = None
        
        # 3. Validate capital
        capital_validation = validate_startup_capital(
            startup_capital,
            base_living_costs
        )
        validations['capital'] = capital_validation
        
        if not capital_validation['valid']:
            warnings.append(capital_validation['error'])
            logger.warning(f"⚠️ Capital validation: Not sufficient")
        elif 'warning' in capital_validation:
            warnings.append(capital_validation['warning'])
        
        # ========================================
        # IF CRITICAL ERRORS: RETURN ERROR RESPONSE
        # ========================================
        
        if critical_errors:
            logger.error(f"🚨 Cannot generate financials: {len(critical_errors)} critical validation errors")
            return {
                'error': 'VALIDATION_FAILED',
                'critical_errors': critical_errors,
                'validations': validations,
                'message': 'Finanzplan kann nicht generiert werden - kritische GZ-Anforderungen nicht erfüllt'
            }
        
        # ========================================
        # CONTINUE WITH FINANCIAL PLANNING
        # ========================================
        
        # 1. Utilization curve
        utilization_curve = self.calculate_utilization_curve(profile)
        
        # 2. Flexible living costs
        living_costs_monthly, living_meta = self.calculate_flexible_living_costs(
            profile,
            base_living_costs
        )
        
        # 3. Base Scenario
        base_scenario = self._generate_scenario(
            "Base (Adaptive)",
            utilization_curve,
            revenue_sources,
            business_costs_monthly,
            living_costs_monthly,
            startup_capital,
            part_time_income=0
        )
        
        # 4. Best Case (+20%)
        best_util = [min(0.90, u * 1.2) for u in utilization_curve]
        best_scenario = self._generate_scenario(
            "Best Case (+20%)",
            best_util,
            revenue_sources,
            business_costs_monthly,
            living_costs_monthly,
            startup_capital,
            part_time_income=0
        )
        
        # 5. Worst Case (-30%)
        worst_util = [u * 0.7 for u in utilization_curve]
        worst_scenario = self._generate_scenario(
            "Worst Case (-30%)",
            worst_util,
            revenue_sources,
            business_costs_monthly * 1.05,
            living_costs_monthly,
            startup_capital,
            part_time_income=0
        )
        
        # 6. Optimal (mit Teilzeit)
        pt_income = living_meta.get('part_time_income', 0)
        pt_months = living_meta.get('part_time_months', 0)
        
        if pt_income > 0:
            optimal_scenario = self._generate_scenario(
                "Optimal (mit Teilzeit)",
                utilization_curve,
                revenue_sources,
                business_costs_monthly,
                living_costs_monthly,
                startup_capital,
                part_time_income=pt_income,
                part_time_months=pt_months
            )
        else:
            optimal_scenario = base_scenario
        
        # 7. Recommendation
        recommended = self._determine_best_scenario(
            base_scenario,
            optimal_scenario,
            profile
        )
        
        # 8. Confidence
        confidence = self._calculate_confidence(recommended, profile)
        
        # 9. Include warnings in recommendation
        recommendation_text = self._explain_recommendation(recommended, profile)
        if warnings:
            recommendation_text += "\n\n⚠️ HINWEISE:\n" + "\n".join(warnings)
        
        return {
            'recommended_scenario': recommended,
            'alternative_scenarios': {
                'base': base_scenario,
                'best': best_scenario,
                'worst': worst_scenario,
                'optimal': optimal_scenario if pt_income > 0 else None
            },
            'utilization_curve': utilization_curve,
            'living_costs_strategy': living_meta,
            'confidence_score': confidence,
            'profile_summary': {
                'experience': getattr(profile.experience_level, 'value', 'unknown'),
                'network': getattr(profile.network_strength, 'value', 'unknown'),
                'first_customers': getattr(profile, 'first_customers_pipeline', 0),
                'partner_support': getattr(profile, 'partner_income_monthly', None) is not None
            },
            'recommendation_reasoning': recommendation_text,
            'validations': validations,  # NEW! Include validation results
            'warnings': warnings,  # NEW! Separate warnings list
            'gz_compliant': len(critical_errors) == 0  # NEW! Quick check
        }
    
    def _generate_scenario(
        self,
        name: str,
        utilization_curve: List[float],
        revenue_sources: List[Dict],
        business_costs: float,
        living_costs: List[float],
        startup_capital: float,
        part_time_income: float = 0,
        part_time_months: int = 0
    ) -> Dict:
        """Generate single financial scenario"""
        
        monate = []
        kontostand = startup_capital
        
        for month in range(1, 13):
            util = utilization_curve[month - 1]
            
            # Revenue
            umsatz = self._calculate_revenue(revenue_sources, util, month)
            
            # Business costs
            kosten_geschaeft = business_costs
            if month == 1:
                kosten_geschaeft += 530  # Setup
            
            # Business profit
            gewinn_geschaeft = umsatz - kosten_geschaeft
            
            # Living costs
            privatentnahme = living_costs[month - 1]
            
            # Part-time income
            zusatz_einkommen = 0
            if part_time_income > 0 and month <= part_time_months:
                zusatz_einkommen = part_time_income
            
            # Net cashflow
            saldo = gewinn_geschaeft - privatentnahme + zusatz_einkommen
            kontostand += saldo
            
            monate.append({
                'monat': month,
                'umsatz': round(umsatz, 2),
                'kosten_geschaeft': round(kosten_geschaeft, 2),
                'gewinn_geschaeft': round(gewinn_geschaeft, 2),
                'privatentnahme': round(privatentnahme, 2),
                'zusatz_einkommen': round(zusatz_einkommen, 2),
                'saldo': round(saldo, 2),
                'kontostand': round(kontostand, 2),
                'auslastung': round(util * 100, 1)
            })
        
        # Break-even
        break_even = self._find_break_even(monate)
        
        return {
            'name': name,
            'monate': monate,
            'gesamt_umsatz': round(sum(m['umsatz'] for m in monate), 2),
            'gesamt_kosten_geschaeft': round(sum(m['kosten_geschaeft'] for m in monate), 2),
            'gesamt_gewinn_geschaeft': round(sum(m['gewinn_geschaeft'] for m in monate), 2),
            'gesamt_privatentnahme': round(sum(m['privatentnahme'] for m in monate), 2),
            'gesamt_zusatz_einkommen': round(sum(m['zusatz_einkommen'] for m in monate), 2),
            'jahresergebnis': round(sum(m['saldo'] for m in monate), 2),
            'endkontostand': round(monate[-1]['kontostand'], 2),
            'break_even_monat': break_even
        }
    
    def _calculate_revenue(
        self,
        revenue_sources: List[Dict],
        utilization: float,
        month: int
    ) -> float:
        """Calculate monthly revenue"""
        
        total = 0
        for source in revenue_sources:
            if source['type'] == 'hourly':
                hours = 80 * utilization
                total += hours * source['price']
            
            elif source['type'] == 'monthly':
                if month >= 4:
                    total += source['price'] * min(utilization * 1.5, 1.0)
            
            elif source['type'] == 'project':
                if month >= 7:
                    projects = utilization * 0.3
                    total += projects * source['price']
        
        return total
    
    def _find_break_even(self, monate: List[Dict]) -> str:
        """Find break-even month"""
        kumuliert = 0
        for m in monate:
            kumuliert += m['gewinn_geschaeft']
            if kumuliert > 0:
                return f"Monat {m['monat']}"
        return "Nicht in Jahr 1"
    
    def _determine_best_scenario(
        self,
        base: Dict,
        optimal: Dict,
        profile: GrounderProfile
    ) -> Dict:
        """Determine recommended scenario"""
        
        if optimal['endkontostand'] > base['endkontostand']:
            if optimal['endkontostand'] > 0:
                return optimal
        
        return base
    
    def _calculate_confidence(
        self,
        scenario: Dict,
        profile: GrounderProfile
    ) -> int:
        """Calculate confidence score (0-100)"""
        
        score = 0
        
        # End balance
        if scenario['endkontostand'] > 10000:
            score += 30
        elif scenario['endkontostand'] > 5000:
            score += 25
        elif scenario['endkontostand'] > 0:
            score += 15
        elif scenario['endkontostand'] > -5000:
            score += 5
        
        # Break-even speed
        if "Monat" in scenario['break_even_monat']:
            try:
                month_num = int(scenario['break_even_monat'].split()[1])
                if month_num <= 3:
                    score += 25
                elif month_num <= 6:
                    score += 20
                elif month_num <= 9:
                    score += 15
                else:
                    score += 10
            except:
                pass
        
        # Profile strength
        profile_confidence = getattr(profile, 'get_confidence_score', lambda: 50)()
        score += int(profile_confidence * 0.25)
        
        # Business profit
        gewinn = scenario['gesamt_gewinn_geschaeft']
        if gewinn > 30000:
            score += 20
        elif gewinn > 20000:
            score += 15
        elif gewinn > 10000:
            score += 10
        elif gewinn > 0:
            score += 5
        
        return min(100, int(score))
    
    def _explain_recommendation(
        self,
        scenario: Dict,
        profile: GrounderProfile
    ) -> str:
        """Explain recommendation"""
        
        reasons = []
        
        if scenario['endkontostand'] > 0:
            reasons.append(f"✅ Positiver Kontostand ({scenario['endkontostand']:,.0f} EUR)")
        else:
            reasons.append(f"⚠️ Negativer Kontostand ({scenario['endkontostand']:,.0f} EUR), mit Kapital + Emergency Fund überbrückbar")
        
        if scenario['gesamt_gewinn_geschaeft'] > 0:
            reasons.append(f"✅ Business profitabel ({scenario['gesamt_gewinn_geschaeft']:,.0f} EUR)")
        
        if "Monat" in scenario['break_even_monat']:
            reasons.append(f"✅ Break-Even: {scenario['break_even_monat']}")
        
        net_strength = getattr(profile.network_strength, 'value', 'unknown') if hasattr(profile, 'network_strength') else 'unknown'
        if net_strength == 'strong':
            reasons.append("✅ Starkes Netzwerk ermöglicht schnelleren Ramp-up")
        
        first_customers = getattr(profile, 'first_customers_pipeline', 0)
        if first_customers > 0:
            reasons.append(f"✅ {first_customers} Kunden bereits im Pipeline")
        
        if scenario.get('gesamt_zusatz_einkommen', 0) > 0:
            reasons.append(f"✅ Teilzeit-Job trägt {scenario['gesamt_zusatz_einkommen']:,.0f} EUR bei")
        
        return "\n".join(reasons)


# ====================================================================================
# EXPORT
# ====================================================================================

__all__ = [
    'AdaptiveFinancialCalculator',
    'validate_hauptberuflich_hours',
    'validate_part_time_job',
    'validate_startup_capital',
    'LEGAL_CITATIONS_SUBSET'
]


if __name__ == "__main__":
    print("✅ Adaptive Financial Calculator WITH VALIDATIONS loaded successfully!")
    print("📦 Main class: AdaptiveFinancialCalculator")
    print("🏛️ Legal Citations: validate_hauptberuflich_hours, validate_part_time_job, validate_startup_capital")
    print("🔧 Ready for integration!")
    print("")
    print("NEW FEATURES:")
    print("  - All inputs validated against GZ requirements")
    print("  - Legal citations (SGB III § 93, Fachliche Weisungen BA)")
    print("  - Validation results included in generate_adaptive_financials() output")
    print("  - Critical errors prevent financial plan generation")
    print("  - Warnings included in recommendation")
