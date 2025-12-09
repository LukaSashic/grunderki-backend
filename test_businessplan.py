# test_businessplan.py
"""
Test script for Businessplan Generator

Tests all TAG 4 features:
1. Citation Management
2. Geographic Intelligence
3. Living Cost Calculation
4. SWOT Analysis
5. Financial Planning
6. Content Generation
"""

import asyncio
import json
from businessplan_generator import BusinessplanGenerator


async def test_complete_generation():
    """
    Test complete businessplan generation
    """
    
    print("=" * 80)
    print("🧪 TESTING BUSINESSPLAN GENERATOR - TAG 4")
    print("=" * 80)
    
    # Initialize generator
    generator = BusinessplanGenerator()
    
    # === TEST DATA ===
    
    vision_data = {
        'magic_wand_answer': 'KMUs bei der Digitalisierung ihrer Prozesse unterstützen',
        'deep_why': 'Habe selbst in Unternehmen erlebt wie frustrierend manuelle Prozesse sind',
        'desired_outcome': 'Dass jedes KMU Zugang zu moderner Automatisierung hat',
        'personal_vision': 'Digitalisierung demokratisieren und für alle zugänglich machen'
    }
    
    jtbd_data = {
        'functional_job': 'Manuelle Geschäftsprozesse automatisieren',
        'emotional_job': 'Sich modern und zukunftsfähig fühlen',
        'social_job': 'Als innovatives Unternehmen wahrgenommen werden',
        'current_alternatives': 'Excel-Tabellen, manuelle Prozesse, teure externe Berater',
        'why_alternatives_fail': 'Zu zeitaufwendig, fehleranfällig, nicht skalierbar, zu teuer',
        'job_story': 'Wenn KMUs ihre Effizienz steigern wollen, wollen sie manuelle Prozesse automatisieren, damit sie sich zukunftsfähig fühlen',
        'opportunity_score': 75
    }
    
    gz_data = {
        'what': 'AI-Automatisierungs-Beratung für deutsche KMUs mit Fokus auf RPA und Process Mining',
        'who': 'Deutsche kleine und mittelständische Unternehmen mit 10-50 Mitarbeitern im Dienstleistungssektor',
        'problem': 'Manuelle, repetitive Prozesse die Zeit und Ressourcen verschwenden',
        'why_you': '8 Jahre IT-Beratungserfahrung, davon 5 Jahre spezialisiert auf RPA bei Roboyo, Zertifikate in UiPath und Blue Prism, Projekte bei Bayer und BMW',
        'revenue_source': 'Beratungsstunden à 120€, monatliche Workshops à 2.500€, Implementierungsprojekte à 15.000€',
        'how': 'Hauptberuflich 30 Stunden pro Woche, Kombination aus vor Ort Beratung und remote Support',
        'capital_needs': '8.000€ für Equipment (Laptop, Software-Lizenzen), Website und initiales Marketing'
    }
    
    user_info = {
        'location': {
            'city': 'Berlin',
            'district': 'Prenzlauer Berg',
            'bundesland': 'Berlin',
            'plz': '10405'
        },
        'family_status': 'familie_2_kinder'
    }
    
    # === GENERATE ===
    
    print("\n🚀 Starting generation...")
    print("-" * 80)
    
    businessplan = await generator.generate(
        vision_data=vision_data,
        jtbd_data=jtbd_data,
        gz_data=gz_data,
        user_info=user_info
    )
    
    # === DISPLAY RESULTS ===
    
    print("\n" + "=" * 80)
    print("✅ GENERATION COMPLETE!")
    print("=" * 80)
    
    # Meta info
    print("\n📊 META INFORMATION:")
    print(f"  Generated: {businessplan['meta']['generated_at']}")
    print(f"  Location: {businessplan['meta']['location']}")
    print(f"  Scope: {businessplan['meta']['scope']}")
    print(f"  Family: {businessplan['meta']['family_status']}")
    
    # Executive Summary
    print("\n" + "=" * 80)
    print("📄 EXECUTIVE SUMMARY:")
    print("=" * 80)
    print(businessplan['executive_summary'][:500] + "...")
    
    # Living Costs
    print("\n" + "=" * 80)
    print("💰 LEBENSHALTUNGSKOSTEN:")
    print("=" * 80)
    living = businessplan['lebenshaltungskosten']
    print(f"  Monatlich: {living['monatlich']['gesamt']:,.2f}€")
    print(f"  Mit Puffer: {living['monatlich']['mit_puffer']:,.2f}€")
    print(f"  Jährlich: {living['jaehrlich']:,.2f}€")
    print(f"\n  Details:")
    for key, value in living['monatlich']['kosten_detail'].items():
        print(f"    - {key}: {value:,.2f}€")
    
    # Financial Plan
    print("\n" + "=" * 80)
    print("💵 FINANZPLAN - JAHR 1 (Auszug):")
    print("=" * 80)
    jahr_1 = businessplan['finanzplan']['jahr_1']
    print(f"  Startkapital: {businessplan['finanzplan']['startkapital']:,.2f}€")
    print(f"\n  Erste 3 Monate:")
    for monat in jahr_1['monate'][:3]:
        print(f"\n  {monat['monat_name']}:")
        print(f"    Umsatz: {monat['umsatz']:,.2f}€ ({monat['auslastung_prozent']}% Auslastung)")
        print(f"    Kosten: {monat['kosten_gesamt']:,.2f}€")
        print(f"    Saldo: {monat['saldo']:,.2f}€")
        print(f"    Kontostand: {monat['kontostand']:,.2f}€")
    
    print(f"\n  JAHR 1 GESAMT:")
    print(f"    Umsatz: {jahr_1['gesamt_umsatz']:,.2f}€")
    print(f"    Kosten: {jahr_1['gesamt_kosten']:,.2f}€")
    print(f"    Ergebnis: {jahr_1['jahresergebnis']:,.2f}€")
    
    # 3-Year Summary
    print("\n" + "=" * 80)
    print("📈 3-JAHRES ÜBERSICHT:")
    print("=" * 80)
    summary = businessplan['finanzplan']['zusammenfassung']
    print(f"  Jahr 1 Umsatz: {summary['umsatz_jahr_1']:,.2f}€")
    print(f"  Jahr 2 Umsatz: {summary['umsatz_jahr_2']:,.2f}€")
    print(f"  Jahr 3 Umsatz: {summary['umsatz_jahr_3']:,.2f}€")
    print(f"\n  Gesamt 3 Jahre:")
    print(f"    Umsatz: {summary['gesamt_umsatz_3_jahre']:,.2f}€")
    print(f"    Gewinn: {summary['gesamt_gewinn_3_jahre']:,.2f}€")
    print(f"    ROI: {summary['roi_3_jahre_prozent']}%")
    print(f"\n  Break-Even: Monat {summary['break_even_monat']}")
    
    # Living Validation
    print("\n" + "=" * 80)
    print("🔍 LEBENSHALTUNGS-VALIDATION:")
    print("=" * 80)
    validation = businessplan['living_validation']
    print(f"  Lebensfähig: {'✅ JA' if validation['lebensfaehig'] else '❌ NEIN'}")
    print(f"  Severity: {validation['severity']}")
    print(f"\n  {validation['message']}")
    
    # SWOT
    print("\n" + "=" * 80)
    print("🎯 SWOT ANALYSE:")
    print("=" * 80)
    swot = businessplan['swot_data']
    print(f"\n  STÄRKEN ({len(swot['staerken'])}):")
    for s in swot['staerken']:
        print(f"    ✓ {s}")
    
    print(f"\n  SCHWÄCHEN ({len(swot['schwaechen'])}):")
    for s in swot['schwaechen']:
        print(f"    ✗ {s}")
    
    print(f"\n  CHANCEN ({len(swot['chancen'])}):")
    for c in swot['chancen']:
        print(f"    ↗ {c}")
    
    print(f"\n  RISIKEN ({len(swot['risiken'])}):")
    for r in swot['risiken']:
        print(f"    ⚠ {r}")
    
    # Citations
    print("\n" + "=" * 80)
    print("📚 QUELLENVERZEICHNIS:")
    print("=" * 80)
    if businessplan['quellenverzeichnis']:
        print(businessplan['quellenverzeichnis'][:500] + "...")
    else:
        print("  (Noch keine Quellen - Web Research Feature kommt in TAG 5)")
    
    # Save to file
    print("\n" + "=" * 80)
    print("💾 SAVING TO FILE...")
    print("=" * 80)
    
    with open('test_businessplan_output.json', 'w', encoding='utf-8') as f:
        json.dump(businessplan, f, ensure_ascii=False, indent=2)
    
    print("  ✅ Saved to: test_businessplan_output.json")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE!")
    print("=" * 80)
    
    return businessplan


if __name__ == "__main__":
    # Run test
    asyncio.run(test_complete_generation())
