# Workshop Module 1 - Code Audit Root Causes

**Date:** 2024-12-19
**Auditor:** Claude Code
**Status:** CRITICAL BUGS IDENTIFIED

---

## Executive Summary

The comprehensive code audit has identified **3 CRITICAL ROOT CAUSES** that explain why Module 1 completes at 37-50% instead of the required 75%, why critical fields are missing, and why the system enters infinite question loops.

The core problem is **FIELD NAME FRAGMENTATION** across 4 different configuration systems that don't synchronize with each other.

---

## ROOT CAUSE 1: FIELD NAME MISMATCH (CRITICAL)

### Problem Description
There are **4 different systems** defining field names, and they use DIFFERENT naming conventions:

### 1. `state_machine.py` SECTION_CONFIG (Line 63-67)
Uses these 9 required fields for Module 1:
```python
"required_fields": [
    "geschaeftsidee", "angebot_detail", "zielgruppe_primaer", "usp",
    "preis_hauptprodukt", "preismodell",
    "persona_alter_bereich", "persona_beruf_einkommen", "persona_beduerfnis"
]
```

### 2. `business_type_classifier.py` pflichtfelder (Line 55-86)
Uses 25+ fields per business type with DIFFERENT names:
```python
pflichtfelder=[
    "geschaeftsidee_kurz",  # NOT "geschaeftsidee"!
    "gastro_subtyp",
    "konzept_typ",
    "standort_konkret",     # NOT in state_machine required_fields
    "usp_formulierung",     # NOT "usp"!
    "hauptprodukt_preise",  # NOT "preis_hauptprodukt"!
    ...
]
```

### 3. `dynamic_question_generator.py` Question IDs (Line 32)
Questions have IDs that match business_type_classifier:
```python
Question(
    id="geschaeftsidee_kurz",  # NOT "geschaeftsidee"!
    text="Beschreibe deine Geschaeftsidee in 1-2 Saetzen",
    ...
)
```

### 4. `system_prompt_builder.py` Instructed Field Names (Line 189-205)
Instructs Claude to use yet another set of names:
```python
- "geschaeftsidee": ...     # Different from "geschaeftsidee_kurz"
- "raeumlichkeiten": ...    # NOT in state_machine required_fields!
- "persona_alter": ...      # NOT "persona_alter_bereich"!
```

### Impact
When a user answers a question:
1. Question has ID `geschaeftsidee_kurz` (from dynamic_question_generator)
2. Field is stored as `geschaeftsidee_kurz`
3. State machine looks for `geschaeftsidee` in `get_collected_fields_count()`
4. **MISMATCH** - Field not found!
5. Fill percentage calculated as 0% for that field

---

## ROOT CAUSE 2: INCOMPLETE FIELD_NAME_MAPPING (CRITICAL)

### Problem Description
`conversation_service.py` has a `FIELD_NAME_MAPPING` (lines 99-223) meant to normalize field names, but it's **MISSING CRITICAL MAPPINGS**.

### Missing Mappings
The following field names from questions/classifiers are NOT in the mapping:
```python
# MISSING - these should map to canonical names:
"geschaeftsidee_kurz"     -> should map to "geschaeftsidee"
"usp_formulierung"        -> should map to "usp"
"hauptprodukt_preise"     -> should map to "preis_hauptprodukt"
"standort_konkret"        -> should map to "standort" or "raeumlichkeiten"
"gastro_subtyp"           -> unclear target
"konzept_typ"             -> unclear target
"groesse_qm"              -> should map to "raeumlichkeiten"
"sitzplaetze_innen"       -> should map to "raeumlichkeiten"
"speisekarte_umfang"      -> unclear target
"produktionsweise"        -> unclear target
"alkohol_geplant"         -> unclear target
"zielgruppen_hauptgruppen" -> should map to "zielgruppe_primaer"
"persona_kaufverhalten"   -> NOT in state_machine required_fields
"zielgruppe_groesse_schaetzung" -> NOT in state_machine required_fields
```

### Impact
Fields are collected and stored correctly, but the normalization step doesn't convert them to canonical names, so `get_collected_fields_count()` doesn't recognize them.

---

## ROOT CAUSE 3: DUAL FIELD DEFINITION SYSTEMS (ARCHITECTURAL)

### Problem Description
The system uses TWO parallel systems for defining required fields:

1. **Static System:** `state_machine.py` SECTION_CONFIG
   - 9 fixed fields for Module 1
   - Used for completion percentage calculation
   - Used for determining when to show "Fertig" button

2. **Dynamic System:** `business_type_classifier.py` pflichtfelder
   - 25+ fields per business type
   - Used by system_prompt_builder for AI instructions
   - Used by question_generator for question sequencing

### The Disconnect
- `state_machine.py` says Module 1 needs 9 fields
- `business_type_classifier.py` says gastronomie needs 25+ fields
- `system_prompt_builder.py` tells Claude to collect ~13 fields
- **Result:** Fill percentage is calculated against 9 fields while system collects for 25+ fields

### Impact
1. User answers many questions (25+ for gastronomie)
2. Many fields get stored with non-canonical names
3. State machine only recognizes 3-4 of the 9 required fields
4. Fill percentage shows 33-44% despite answering many questions
5. Module completes prematurely because auto-transition triggers

---

## ROOT CAUSE 4: QUESTION ID vs FIELD ID CONFUSION

### Problem Description
The `dynamic_question_generator.py` questions have:
- `id`: The question identifier (e.g., `"geschaeftsidee_kurz"`)
- `block`: The conceptual block (e.g., `"geschaeftsidee"`)

But the system stores answers using the **question ID**, not the block!

### Example Flow
```
Question: id="geschaeftsidee_kurz", block="geschaeftsidee"
User answers: "Third Wave Cafe in Neukoelln"
Field stored as: "geschaeftsidee_kurz" (question ID)
State machine looks for: "geschaeftsidee" (required_field name)
Result: NOT FOUND
```

### Impact
Even questions with correct `block` values don't map to the right field names.

---

## EVIDENCE: Data Flow Trace

### Full Request Flow
```
1. User sends message
2. conversation_service.send_message() receives it (line 538)
3. Claude API called with system prompt from system_prompt_builder
4. Claude responds with <structured_data> containing extracted_fields
5. _extract_structured_data() parses response (line 1905)
6. _normalize_field_names() attempts normalization (line 235)
   -> FAILS for missing mappings!
7. _accumulate_collected_fields() stores fields (line 2178)
   -> Fields stored with wrong names
8. state_machine.get_collected_fields_count() (line 240)
   -> Looks for canonical names, doesn't find them
9. Fill percentage calculated incorrectly
10. Completion logic triggers too early or too late
```

---

## FIX SPECIFICATIONS

### FIX 1: Synchronize Field Name Systems (HIGH PRIORITY)

**Option A: Single Source of Truth (Recommended)**
Create a single `FIELD_DEFINITIONS` configuration that all systems use:

```python
# New file: field_definitions.py
CANONICAL_FIELDS = {
    "sektion_1_geschaeftsmodell": {
        "geschaeftsidee": {
            "aliases": ["geschaeftsidee_kurz", "business_idea", "konzept", "idee"],
            "label": "Geschaeftsidee",
            "required": True
        },
        "preis_hauptprodukt": {
            "aliases": ["hauptprodukt_preise", "preise", "pricing"],
            "label": "Preis Hauptprodukt",
            "required": True
        },
        # ... all other fields
    }
}
```

**Option B: Comprehensive FIELD_NAME_MAPPING (Quick Fix)**
Add ALL missing mappings to conversation_service.py:

```python
FIELD_NAME_MAPPING = {
    # ... existing mappings ...

    # ADD THESE MISSING MAPPINGS:
    "geschaeftsidee_kurz": "geschaeftsidee",
    "usp_formulierung": "usp",
    "hauptprodukt_preise": "preis_hauptprodukt",
    "standort_konkret": "raeumlichkeiten",
    "groesse_qm": "raeumlichkeiten",
    "sitzplaetze_innen": "raeumlichkeiten",
    "zielgruppen_hauptgruppen": "zielgruppe_primaer",
    # ... etc
}
```

### FIX 2: Update State Machine Required Fields (HIGH PRIORITY)

Align `state_machine.py` SECTION_CONFIG with what the system actually collects:

```python
SECTION_CONFIG = {
    "sektion_1_geschaeftsmodell": {
        "max_questions": 15,
        "required_fields": [
            # Core fields (universal)
            "geschaeftsidee", "angebot_detail", "zielgruppe_primaer", "usp",
            "preis_hauptprodukt", "preismodell",
            # Persona fields
            "persona_alter_bereich", "persona_beruf_einkommen", "persona_beduerfnis"
        ],
        # ... rest stays same
    }
}
```

### FIX 3: Add Field Normalization to Question Generator

When storing answers, use the question's `block` attribute or normalize the ID:

```python
# In _accumulate_collected_fields or extraction logic
def normalize_question_id_to_field(question_id: str) -> str:
    """Convert question ID to canonical field name."""
    # Check if it's a known question ID
    question = get_question_by_id(question_id)
    if question and question.block:
        return question.block
    # Fall back to FIELD_NAME_MAPPING
    return FIELD_NAME_MAPPING.get(question_id, question_id)
```

### FIX 4: Add Debug Logging (DIAGNOSTIC)

Add comprehensive logging to track field flow:

```python
# In _accumulate_collected_fields
print(f"[FIELD TRACE] Input: {key}")
print(f"[FIELD TRACE] Normalized to: {canonical_name}")
print(f"[FIELD TRACE] Required fields expect: {required_fields}")
print(f"[FIELD TRACE] Match: {canonical_name in required_fields}")
```

---

## IMMEDIATE ACTION ITEMS

1. **URGENT:** Add missing mappings to FIELD_NAME_MAPPING:
   - `geschaeftsidee_kurz` -> `geschaeftsidee`
   - `usp_formulierung` -> `usp`
   - `hauptprodukt_preise` -> `preis_hauptprodukt`
   - All other identified missing mappings

2. **HIGH:** Verify state_machine required_fields match what questions collect

3. **MEDIUM:** Consider using question `block` attribute for field storage

4. **LOW:** Create unified field definition system (long-term architectural fix)

---

## Files Requiring Changes

| File | Change Type | Priority |
|------|-------------|----------|
| `conversation_service.py` lines 99-223 | Add missing field mappings | URGENT |
| `state_machine.py` lines 63-67 | Review required_fields alignment | HIGH |
| `business_type_classifier.py` | Align pflichtfelder with canonical names | HIGH |
| `dynamic_question_generator.py` | Consider using block for storage | MEDIUM |
| `system_prompt_builder.py` | Align instructed field names | HIGH |

---

## Test Cases to Verify Fix

After implementing fixes, test these scenarios:

1. **Test Field Accumulation:**
   - Answer question `geschaeftsidee_kurz`
   - Verify `collected_fields` contains `geschaeftsidee`

2. **Test Fill Percentage:**
   - Answer 6 out of 9 required fields
   - Verify fill_percentage shows ~66%

3. **Test Completion Logic:**
   - Reach 75% fill
   - Verify "Fertig" button appears

4. **Test No Infinite Loops:**
   - Answer a field once
   - Verify same question not repeated

---

## Conclusion

The Module 1 bugs are caused by a **fragmented field naming system** across 4 different configuration files. The fix requires synchronizing these systems, primarily by:

1. Completing the FIELD_NAME_MAPPING with all missing aliases
2. Ensuring state_machine required_fields match what questions actually collect
3. Potentially using question `block` attribute for field storage

Estimated fix time: 2-4 hours for comprehensive solution.
