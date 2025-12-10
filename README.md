# GründerKI Backend

Backend für GründerKI - AI-powered Businessplan Generator mit Gründungszuschuss-Compliance.

## Features

### 🏛️ Legal Citations System
- 18+ offizielle Rechtsgrundlagen integriert
- Automatische Validierung gegen GZ-Anforderungen
- Transparenz durch Paragraphen-Referenzen

### 📋 Businessplan Generator
- Enhanced mit Legal Citations in allen Prompts
- GZ-konforme Output-Generierung
- Automatischer Compliance-Check

### 💰 Adaptive Financial Calculator
- Input-Validierung mit Rechtsgrundlagen
- Hauptberuflichkeit-Check (min. 15h/Woche)
- Nebentätigkeits-Validierung

## Legal Citations

- **SGB III § 93 Abs. 1** - Ermessensleistung
- **SGB III § 93 Abs. 2** - Hauptberuflichkeit (min. 15h/Woche)
- **SGB III § 94** - Intensive Geschäftstätigkeit
- **Fachliche Weisungen BA zu § 93** - Qualifikation & Tragfähigkeit
- **Fachliche Weisungen BA zu § 94** - Intensive Geschäftstätigkeit

## Installation

\\\ash
pip install -r requirements.txt
\\\

## Usage

\\\python
from businessplan_generator_enhanced import EnhancedBusinessplanGenerator
from adaptive_financial_calculator_full import AdaptiveFinancialCalculator
from legal_citations import get_citation

# Generate GZ-compliant businessplan
generator = EnhancedBusinessplanGenerator()
result = generator.generate(profile)

# Validate inputs
calculator = AdaptiveFinancialCalculator()
validation = calculator.generate_adaptive_financials(profile, ...)
\\\

## API

See \usinessplan_api.py\ and \main.py\ for API endpoints.

## License

Proprietary
