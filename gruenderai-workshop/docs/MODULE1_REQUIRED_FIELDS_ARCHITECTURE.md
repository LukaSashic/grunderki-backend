# Module 1 Required Fields Architecture

**Version:** 2.0.0
**Date:** December 2024
**Status:** Production

---

## Overview

This document describes the new architecture for Module 1 (Geschäftsmodell) required fields. The system implements a **single source of truth** approach with business-type specific field requirements.

### Key Changes from v1.0

| Aspect | v1.0 (Old) | v2.0 (New) |
|--------|------------|------------|
| Required Fields | 9 static fields | 11-22 dynamic fields based on business type |
| Completion Threshold | 75% | 90% |
| Field Definition | 3 conflicting files | Single source: `required_fields.py` |
| Validation | Simple percentage | Category-based with detailed feedback |

---

## Architecture

### File Structure

```
backend/app/workshop/modules/
├── __init__.py
└── module1/
    ├── __init__.py
    ├── required_fields.py    # Single source of truth
    └── validation_ui.py      # UI helper functions
```

### Single Source of Truth

All required field definitions live in `required_fields.py`. Other modules import from here:

```python
from .modules.module1.required_fields import (
    get_required_fields,
    validate_completion,
    COMPLETION_CRITERIA,
)
```

---

## Field Categories

Fields are organized into three tiers:

### 1. Universal Required Fields (6 fields)

Required for ALL business types - these capture the core business model:

| Field | Description | Example |
|-------|-------------|---------|
| `geschaeftsidee` | Business idea | "Third Wave Coffee Café" |
| `angebot_detail` | Detailed offering | "Premium-Kaffee, Kuchen, Brunch" |
| `zielgruppe_primaer` | Primary target group | "Kreative Berufstätige, 28-45" |
| `usp` | Unique Selling Proposition | "Einziges Café mit Co-Working" |
| `preis_hauptprodukt` | Main product price | "4.50 EUR (Kaffee)" |
| `preismodell` | Pricing model | "A la carte + Membership" |

### 2. Persona Required Fields (5 fields)

Required for ALL business types - create customer profile:

| Field | Description | Example |
|-------|-------------|---------|
| `persona_alter_bereich` | Age range | "28-45 Jahre" |
| `persona_beruf_einkommen` | Occupation & income | "Kreative, 4000+ EUR" |
| `persona_beduerfnis` | Core need/pain point | "Flexibler Arbeitsplatz" |
| `persona_kaufverhalten` | Buying behavior | "2-3x pro Woche" |
| `persona_zahlungsbereitschaft` | Willingness to pay | "15-20 EUR pro Besuch" |

### 3. Business-Type Specific Fields (varies)

Additional fields based on business type:

| Business Type | Additional Fields | Total Fields |
|---------------|-------------------|--------------|
| Gastronomie | 11 | 22 |
| Einzelhandel | 8 | 19 |
| Dienstleistung Lokal | 6 | 17 |
| Dienstleistung Online | 6 | 17 |
| Dienstleistung Mobil | 8 | 19 |
| Handel Online | 7 | 18 |
| Produktion | 7 | 18 |
| Default (unknown) | 0 | 11 |

---

## Completion Criteria

```python
COMPLETION_CRITERIA = {
    "minimum_fill_percentage": 90,   # Can complete at 90%
    "optimal_fill_percentage": 100,  # Ideal completion
    "show_button_at": 90,            # Show "Fertig" button
    "min_questions_percentage": 80,  # Must answer 80% of questions
    "allow_user_completion": True,   # User can trigger manually
}
```

### Why 90% Threshold?

- **75% was too lenient**: Users skipped critical fields
- **100% too strict**: Some fields are genuinely optional
- **90% balanced**: Ensures critical data while allowing flexibility

---

## Usage Examples

### Getting Required Fields

```python
from app.workshop.modules.module1 import get_required_fields

# For gastronomie business
fields = get_required_fields("gastronomie")
print(len(fields))  # 22

# For unknown business type
fields = get_required_fields("default")
print(len(fields))  # 11 (universal + persona only)
```

### Validating Completion

```python
from app.workshop.modules.module1 import validate_completion

filled_fields = {
    "geschaeftsidee": "Café mit Co-Working",
    "angebot_detail": "Kaffee, Kuchen, Arbeitsplätze",
    # ... more fields
}

result = validate_completion(filled_fields, "gastronomie")
print(result["can_complete"])           # True/False
print(result["completion_percentage"])  # e.g., 85.5
print(result["missing_required"])       # ["field1", "field2"]
```

### Generating UI Feedback

```python
from app.workshop.modules.module1 import generate_completion_feedback

feedback = generate_completion_feedback(filled_fields, "gastronomie")

# Returns structured data for frontend:
# {
#     "overall_progress": 85.5,
#     "can_complete": False,
#     "categories": [...],
#     "next_required_field": {"field": "usp", "label": "Alleinstellungsmerkmal"},
#     "message": "Noch 3 wichtige Felder für deinen Businessplan"
# }
```

---

## Adding New Business Types

### Step 1: Define Fields

In `required_fields.py`, add entry to `BUSINESS_TYPE_REQUIRED_FIELDS`:

```python
BUSINESS_TYPE_REQUIRED_FIELDS = {
    # ... existing types ...

    "new_business_type": {
        "specific_field_1",
        "specific_field_2",
        # ...
    },
}
```

### Step 2: Add Field Labels

In `required_fields.py`, add to `FIELD_LABELS`:

```python
FIELD_LABELS = {
    # ... existing labels ...
    "specific_field_1": "Human Readable Name",
    "specific_field_2": "Another Field Name",
}
```

### Step 3: Add Validation Rules (Optional)

In `required_fields.py`, add to `VALIDATION_RULES`:

```python
VALIDATION_RULES = {
    # ... existing rules ...
    "specific_field_1": FieldValidation(
        min_length=10,
        max_length=200,
        examples=["Example value"],
        hint="Help text for user"
    ),
}
```

### Step 4: Create Question Templates

In `dynamic_question_generator.py`, add questions for new fields:

```python
NEW_TYPE_QUESTIONS = [
    Question(
        id="specific_field_1",
        text="Question text?",
        typ="open_text",
        block="relevant_block"
    ),
    # ...
]
```

### Step 5: Update Classifier

In `business_type_classifier.py`, register the new type.

---

## Migration from Old System

### What Changed

1. **state_machine.py**: Now imports from `modules.module1.required_fields`
2. **constants.py**: Removed duplicate field definitions
3. **business_type_classifier.py**: Uses shared field definitions
4. **Completion threshold**: Changed from 75% to 90%

### Backward Compatibility

- Old API responses still work
- New fields are additive (don't break existing data)
- Sessions started with old system continue normally

### Data Migration

No database migration needed. The new system:
- Reads existing `collected_fields` from sessions
- Validates against new requirements
- Existing "complete" sessions may now show as incomplete if missing fields

---

## API Response Changes

### Completion Status Endpoint

The `/completion-status/{session_id}` endpoint now returns additional fields:

```json
{
    "fill_percentage": 85.5,
    "filled_fields": 19,
    "total_fields": 22,
    "can_complete": false,
    "show_completion_button": false,
    "minimum_fill_percentage": 90,

    // NEW FIELDS:
    "missing_required": ["usp", "durchschnittlicher_bon", "preispositionierung"],
    "missing_by_category": {
        "universal": ["usp"],
        "business_type": ["durchschnittlicher_bon", "preispositionierung"]
    },
    "validation_errors": {},
    "business_type": "gastronomie"
}
```

---

## Troubleshooting

### Field Not Recognized

If a field isn't being counted:

1. Check if it's in `UNIVERSAL_REQUIRED_FIELDS`, `PERSONA_REQUIRED_FIELDS`, or `BUSINESS_TYPE_REQUIRED_FIELDS`
2. Check `FIELD_NAME_MAPPING` in `conversation_service.py` for aliases
3. Verify the field name matches exactly (case-sensitive)

### Completion Button Not Showing

The button appears when:
- `completion_percentage >= 90`
- `question_count >= min_questions`
- `allow_user_completion == True`

Check `get_completion_status()` in `state_machine.py`.

### Wrong Field Count

Clear the `lru_cache` if field definitions were changed:
```python
from app.workshop.modules.module1.required_fields import get_required_fields
get_required_fields.cache_clear()
```

---

## Performance Considerations

- `get_required_fields()` is cached with `@lru_cache(maxsize=32)`
- Validation is O(n) where n = number of required fields
- No database queries in field validation (only in data collection)

---

## Testing

Run unit tests:
```bash
pytest tests/test_module1_required_fields.py -v
```

Run with coverage:
```bash
pytest tests/test_module1_required_fields.py --cov=app.workshop.modules.module1
```

---

## Decision Rationale

### Why 3 Tiers?

1. **Universal**: Every business needs these basics
2. **Persona**: Customer understanding is critical for BA GZ approval
3. **Business-specific**: Different industries have different requirements

### Why 90% Threshold?

- Analysis showed 75% allowed critical gaps
- 90% ensures quality while accommodating edge cases
- Matches BA GZ 04 requirements for thorough plans

### Why Single Source of Truth?

- 3 conflicting definitions caused bugs
- Field counts were inconsistent
- Maintenance was difficult

---

## Contact

For questions about this architecture, contact the GründerAI development team.
