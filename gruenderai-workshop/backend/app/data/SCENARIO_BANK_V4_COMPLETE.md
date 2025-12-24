# GründerAI Scenario Bank V4 - Complete Specification

## Overview

| Aspect | Value |
|--------|-------|
| **Version** | 4.0.0 |
| **Total Questions** | 16 |
| **Format** | All scenario-based (A/B/C/D) |
| **Duration** | 8-10 minutes |
| **Personalization** | Business type, target customer, stage |

## Question Distribution

| Block | Theme | GZ-Readiness | Personality | Total |
|-------|-------|--------------|-------------|-------|
| A | Markt & Kunden | 2 | 3 | 5 |
| B | Finanzen & Risiko | 2 | 3 | 5 |
| C | Umsetzung & Du | 2 | 4 | 6 |
| **Total** | | **6** | **10** | **16** |

## Personality Dimensions Covered

| Dimension | Questions | IDs |
|-----------|-----------|-----|
| Proactiveness | 2 | A3, A5 |
| Risk-Taking | 2 | B3, B5 |
| Achievement Orientation | 2 | A4, C4 |
| Locus of Control | 2 | B4, C5 |
| Self-Efficacy | 2 | C3, C6 |

---

# BLOCK A: MARKT & KUNDEN

## A1: Zielkunden-Definition (GZ-Readiness)

```json
{
  "id": "A1",
  "block": "A",
  "type": "gz_readiness",
  "topic": "zielkunden",
  "weight": 20,
  "context": "ihk",
  
  "scenario": {
    "setting": "🏛️ IHK-GESPRÄCH",
    "theme": "Deine Zielkunden",
    
    "situation": "Die IHK-Beraterin schaut auf deinen Businessplan und fragt:",
    
    "question": "\"Sie wollen {{business_type_de}} für {{target_customer}} anbieten. Beschreiben Sie mir Ihre Zielkunden - mit Alter, Einkommen und typischem Kaufverhalten.\"",
    
    "prompt": "Wie antwortest du?",
    
    "options": [
      {
        "id": "A",
        "text": "\"Eigentlich alle, die das brauchen könnten...\"",
        "score": 0,
        "gap": true,
        "severity": "critical"
      },
      {
        "id": "B",
        "text": "\"Menschen zwischen 30-50, die sich dafür interessieren. Genauer müsste ich noch ausarbeiten.\"",
        "score": 35,
        "gap": true,
        "severity": "high"
      },
      {
        "id": "C",
        "text": "\"Ich habe das dokumentiert: {{target_customer}}, Alter 35-55, Haushaltseinkommen über 60.000€, kaufen bevorzugt online nach Empfehlungen.\"",
        "score": 75,
        "gap": false,
        "severity": null
      },
      {
        "id": "D",
        "text": "\"Hier sind meine 3 Kunden-Personas, basierend auf 12 Interviews. Mit konkreten Zitaten und Kaufmotiven.\"",
        "score": 100,
        "gap": false,
        "severity": null
      }
    ]
  },
  
  "gz_insight": {
    "trigger": ["A", "B"],
    "title": "💡 GUT ZU WISSEN",
    "content": "30% aller GZ-Anträge scheitern an fehlender Marktanalyse.\n\nDie IHK will konkrete Zahlen sehen:\n• Wer genau sind deine Kunden?\n• Wie viele gibt es davon?\n• Wie erreichst du sie?",
    "cta": "Im Workshop erstellst du deine Zielgruppen-Persona in 30 Minuten."
  },
  
  "gap_trigger": {
    "gap_id": "marktanalyse",
    "gap_title": "Zielgruppen-Definition",
    "gap_description": "Keine konkrete Beschreibung deiner Zielkunden",
    "covered_in_module": 2,
    "approval_impact": "30% der Ablehnungen"
  }
}
```

---

## A2: Wettbewerbsanalyse (GZ-Readiness)

```json
{
  "id": "A2",
  "block": "A",
  "type": "gz_readiness",
  "topic": "wettbewerb",
  "weight": 15,
  "context": "ihk",
  
  "scenario": {
    "setting": "🏛️ IHK-GESPRÄCH",
    "theme": "Dein Wettbewerb",
    
    "situation": "Die IHK-Beraterin fragt weiter:",
    
    "question": "\"Wer sind Ihre drei größten Wettbewerber und wodurch unterscheiden Sie sich von denen?\"",
    
    "prompt": "Wie antwortest du?",
    
    "options": [
      {
        "id": "A",
        "text": "\"Ich habe eigentlich keine direkten Konkurrenten - mein Angebot ist ziemlich einzigartig.\"",
        "score": 0,
        "gap": true,
        "severity": "critical"
      },
      {
        "id": "B",
        "text": "\"Es gibt ein paar ähnliche Anbieter, aber ich kenne die Details noch nicht so genau.\"",
        "score": 35,
        "gap": true,
        "severity": "high"
      },
      {
        "id": "C",
        "text": "\"Meine Top 3 sind [X], [Y] und [Z]. Ich bin schneller als X und persönlicher als Y. Mein Preis liegt dazwischen.\"",
        "score": 75,
        "gap": false,
        "severity": null
      },
      {
        "id": "D",
        "text": "\"Ich habe 8 Wettbewerber in einer Matrix analysiert. Hier ist meine Positionierung mit klarem USP und Preisvergleich.\"",
        "score": 100,
        "gap": false,
        "severity": null
      }
    ]
  },
  
  "gz_insight": {
    "trigger": ["A"],
    "title": "⚠️ ACHTUNG",
    "content": "\"Keine Konkurrenz\" ist ein RED FLAG für die IHK!\n\nDie Logik dahinter:\nKeine Konkurrenz = Kein Markt\n\nBesser: Zeige, dass du den Markt kennst UND erklärst, warum du trotzdem erfolgreich sein wirst.",
    "cta": null
  },
  
  "gz_insight_b": {
    "trigger": ["B"],
    "title": "💡 GUT ZU WISSEN",
    "content": "Ohne Wettbewerbsanalyse keine Tragfähigkeitsbescheinigung.\n\nDie IHK will sehen:\n• Mindestens 3 konkrete Konkurrenten\n• Deine Differenzierung\n• Deine Preisstrategie im Vergleich",
    "cta": "Im Workshop erstellen wir deine Wettbewerbs-Matrix."
  },
  
  "gap_trigger": {
    "gap_id": "wettbewerb",
    "gap_title": "Wettbewerbsanalyse",
    "gap_description": "Keine systematische Analyse der Konkurrenz",
    "covered_in_module": 2,
    "approval_impact": "IHK-Bescheinigung gefährdet"
  }
}
```

---

## A3: Kundengewinnung (Proactiveness #1)

```json
{
  "id": "A3",
  "block": "A",
  "type": "personality",
  "dimension": "proactiveness",
  "dimension_de": "Proaktivität",
  
  "scenario": {
    "setting": "💼 ALLTAGS-SITUATION",
    "theme": "Erste Kunden",
    
    "situation": "Du hast dein Angebot für {{target_customer}} fertig entwickelt. Jetzt brauchst du Kunden.",
    
    "question": "Wie gehst du vor?",
    
    "prompt": "Was machst du?",
    
    "options": [
      {
        "id": "A",
        "text": "Ich warte erstmal ab - gute Arbeit spricht sich rum. Die richtigen Kunden werden mich finden.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Ich erstelle Social Media Profile und poste regelmäßig. Mal schauen, wer sich meldet.",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Ich kontaktiere diese Woche 10 potenzielle Kunden direkt und biete ein Kennenlerngespräch an.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "Ich habe schon vor dem offiziellen Launch mit 20 potenziellen Kunden gesprochen und erste Zusagen.",
        "theta": 1.5
      }
    ]
  }
}
```

---

## A4: Ziele setzen (Achievement Orientation #1)

```json
{
  "id": "A4",
  "block": "A",
  "type": "personality",
  "dimension": "achievement_orientation",
  "dimension_de": "Leistungsorientierung",
  
  "scenario": {
    "setting": "💼 PLANUNGS-SITUATION",
    "theme": "Dein erstes Jahr",
    
    "situation": "Du planst dein erstes Geschäftsjahr als {{business_type_de}}.",
    
    "question": "Welches Umsatzziel setzt du dir?",
    
    "prompt": "Wie planst du?",
    
    "options": [
      {
        "id": "A",
        "text": "Ich setze mir lieber kein konkretes Ziel - das erzeugt nur unnötigen Druck.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Ein Ziel, das ich sicher erreichen kann. Lieber positiv überrascht werden als enttäuscht.",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Ein ambitioniertes aber realistisches Ziel, mit klaren Quartals-Meilensteinen zur Kontrolle.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "Das Maximum, was theoretisch möglich wäre. Ich will sehen, wie weit ich kommen kann.",
        "theta": 1.5
      }
    ]
  }
}
```

---

## A5: Marktchance (Proactiveness #2)

```json
{
  "id": "A5",
  "block": "A",
  "type": "personality",
  "dimension": "proactiveness",
  "dimension_de": "Proaktivität",
  
  "scenario": {
    "setting": "💼 CHANCEN-SITUATION",
    "theme": "Neuer Trend",
    
    "situation": "Du hörst von einem neuen Trend, der perfekt zu deinem {{business_type_de}} passen könnte. Andere haben ihn noch nicht aufgegriffen.",
    
    "question": "Wie reagierst du?",
    
    "prompt": "Was machst du?",
    
    "options": [
      {
        "id": "A",
        "text": "Interessant - ich beobachte erstmal ein paar Monate, wie sich das entwickelt.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Ich recherchiere gründlich und erstelle einen detaillierten Plan, bevor ich handle.",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Ich starte diese Woche ein kleines Experiment, um die Nachfrage zu testen.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "First Mover Advantage! Ich setze sofort alles auf diese Chance.",
        "theta": 1.5
      }
    ]
  }
}
```

---

# BLOCK B: FINANZEN & RISIKO

## B1: Umsatzprognose (GZ-Readiness)

```json
{
  "id": "B1",
  "block": "B",
  "type": "gz_readiness",
  "topic": "umsatzprognose",
  "weight": 20,
  "context": "bank",
  
  "scenario": {
    "setting": "🏦 BANK-GESPRÄCH",
    "theme": "Deine Zahlen",
    
    "situation": "Der Bankberater schaut auf deinen Finanzplan und zeigt auf die Umsatzzeile:",
    
    "question": "\"Sie planen 80.000€ Umsatz im ersten Jahr. Wie kommen Sie auf diese Zahl?\"",
    
    "prompt": "Wie antwortest du?",
    
    "options": [
      {
        "id": "A",
        "text": "\"Das erschien mir realistisch für den Anfang. Nicht zu hoch, nicht zu niedrig.\"",
        "score": 0,
        "gap": true,
        "severity": "critical"
      },
      {
        "id": "B",
        "text": "\"Ich habe recherchiert, was andere in der Branche so machen. Das ist ein üblicher Wert.\"",
        "score": 35,
        "gap": true,
        "severity": "high"
      },
      {
        "id": "C",
        "text": "\"Bei 15 Kunden à 450€ pro Monat = 81.000€. Ich brauche also etwa 1,5 Neukunden pro Monat.\"",
        "score": 75,
        "gap": false,
        "severity": null
      },
      {
        "id": "D",
        "text": "\"Bottom-Up-Rechnung: Marktgröße × realistische Conversion × mein Preis. Validiert durch 3 Vorbestellungen über insgesamt 1.500€.\"",
        "score": 100,
        "gap": false,
        "severity": null
      }
    ]
  },
  
  "gz_insight": {
    "trigger": ["A", "B"],
    "title": "💡 GUT ZU WISSEN",
    "content": "\"Unrealistische Umsatzprognosen\" ist Ablehnungsgrund #1.\n\nDie Bank und IHK wollen eine nachvollziehbare Rechnung:\n\nKunden × Preis × Frequenz = Umsatz\n\nJede Zahl muss begründbar sein!",
    "cta": "Im Workshop erstellst du einen wasserdichten Finanzplan."
  },
  
  "gap_trigger": {
    "gap_id": "finanzplan",
    "gap_title": "Umsatzprognose",
    "gap_description": "Keine nachvollziehbare Umsatzberechnung",
    "covered_in_module": 6,
    "approval_impact": "Häufigster Ablehnungsgrund"
  }
}
```

---

## B2: Break-Even (GZ-Readiness)

```json
{
  "id": "B2",
  "block": "B",
  "type": "gz_readiness",
  "topic": "break_even",
  "weight": 20,
  "context": "bank",
  
  "scenario": {
    "setting": "🏦 BANK-GESPRÄCH",
    "theme": "Profitabilität",
    
    "situation": "Der Bankberater fragt weiter:",
    
    "question": "\"Ab welchem Monat decken Ihre Einnahmen alle Kosten - inklusive eines angemessenen Gehalts für Sie selbst?\"",
    
    "prompt": "Wie antwortest du?",
    
    "options": [
      {
        "id": "A",
        "text": "\"Das habe ich ehrlich gesagt noch nicht konkret berechnet.\"",
        "score": 0,
        "gap": true,
        "severity": "critical"
      },
      {
        "id": "B",
        "text": "\"Ich schätze, so nach etwa einem Jahr ungefähr.\"",
        "score": 35,
        "gap": true,
        "severity": "high"
      },
      {
        "id": "C",
        "text": "\"Monat 14 laut meiner Kalkulation: dann 8.500€ Umsatz bei 7.200€ Gesamtkosten inklusive meiner Privatentnahme.\"",
        "score": 75,
        "gap": false,
        "severity": null
      },
      {
        "id": "D",
        "text": "\"Monat 11 im Best Case, Monat 16 im Worst Case. Hier sind beide Szenarien mit den jeweiligen Annahmen.\"",
        "score": 100,
        "gap": false,
        "severity": null
      }
    ]
  },
  
  "gz_insight": {
    "trigger": ["A", "B"],
    "title": "💡 GUT ZU WISSEN",
    "content": "Die Arbeitsagentur zahlt Gründungszuschuss für maximal 15 Monate.\n\nSie erwarten, dass du danach eigenständig tragfähig bist.\n\n→ Dein Break-Even sollte zwischen Monat 12-18 liegen.",
    "cta": "Im Workshop berechnen wir deinen Break-Even."
  },
  
  "gap_trigger": {
    "gap_id": "break_even",
    "gap_title": "Break-Even-Berechnung",
    "gap_description": "Kein konkreter Zeitpunkt für Profitabilität berechnet",
    "covered_in_module": 6,
    "approval_impact": "Tragfähigkeit nicht nachweisbar"
  }
}
```

---

## B3: Investitionsentscheidung (Risk-Taking #1)

```json
{
  "id": "B3",
  "block": "B",
  "type": "personality",
  "dimension": "risk_taking",
  "dimension_de": "Risikobereitschaft",
  
  "scenario": {
    "setting": "💼 ENTSCHEIDUNGS-SITUATION",
    "theme": "Investition",
    
    "situation": "Du hast 10.000€ Startkapital für dein {{business_type_de}}. Ein Marketing-Experte sagt: \"Mit 8.000€ Investment kann ich dir in 3 Monaten die ersten 10 Kunden bringen. Garantie gibt es keine.\"",
    
    "question": "Du hast auch die Option, mit 2.000€ langsam zu starten und den Rest als Sicherheit zu behalten.",
    
    "prompt": "Wie entscheidest du?",
    
    "options": [
      {
        "id": "A",
        "text": "Definitiv die 2.000€-Variante. Ich brauche die Sicherheit der Reserve.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Eher die 2.000€-Variante. Lieber langsam aber sicher wachsen.",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Ich investiere 5.000€ - ein Mittelweg aus Chance und Sicherheit.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "Die vollen 8.000€. Wer nicht investiert, kann nicht wachsen.",
        "theta": 1.5
      }
    ]
  }
}
```

---

## B4: Auftrag geplatzt (Locus of Control #1)

```json
{
  "id": "B4",
  "block": "B",
  "type": "personality",
  "dimension": "locus_of_control",
  "dimension_de": "Kontrollüberzeugung",
  
  "scenario": {
    "setting": "💼 RÜCKSCHLAG-SITUATION",
    "theme": "Verlorener Auftrag",
    
    "situation": "Ein Auftrag über 5.000€, den du schon als sicher eingeplant hattest, platzt im letzten Moment. Der Kunde sagt ab - ohne wirkliche Begründung.",
    
    "question": "Was denkst du?",
    
    "prompt": "Deine erste Reaktion:",
    
    "options": [
      {
        "id": "A",
        "text": "\"Typisch. Mir passiert sowas ständig. Ich habe einfach kein Glück im Business.\"",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "\"Pech gehabt. Falscher Zeitpunkt, falscher Kunde. Manchmal läuft es halt nicht.\"",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "\"Ärgerlich. Was hätte ich anders machen können? Das analysiere ich für nächstes Mal.\"",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "\"Gut, dass ich mehrere Optionen parallel aufgebaut habe. Auf zum nächsten!\"",
        "theta": 1.5
      }
    ]
  }
}
```

---

## B5: Großkunde (Risk-Taking #2)

```json
{
  "id": "B5",
  "block": "B",
  "type": "personality",
  "dimension": "risk_taking",
  "dimension_de": "Risikobereitschaft",
  
  "scenario": {
    "setting": "💼 CHANCEN-SITUATION",
    "theme": "Großkunde",
    
    "situation": "Ein großer Kunde will 60% deiner Kapazität für 12 Monate buchen. Sehr gut bezahlt, aber danach wärst du von diesem einen Kunden abhängig.",
    
    "question": "Wie entscheidest du?",
    
    "prompt": "Was machst du?",
    
    "options": [
      {
        "id": "A",
        "text": "Zu riskant. Ich lehne ab und suche lieber viele kleine Kunden.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Ich nehme an, aber mit Bauchschmerzen. Die Abhängigkeit macht mir Sorgen.",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Ich nehme an und nutze die Stabilität, um parallel weitere Kunden aufzubauen.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "Perfekt! Ich baue mein ganzes Business um diesen Kunden und gehe All-in.",
        "theta": 1.5
      }
    ]
  }
}
```

---

# BLOCK C: UMSETZUNG & DU

## C1: Kundenakquise-Plan (GZ-Readiness)

```json
{
  "id": "C1",
  "block": "C",
  "type": "gz_readiness",
  "topic": "marketing",
  "weight": 15,
  "context": "ihk",
  
  "scenario": {
    "setting": "🏛️ IHK-GESPRÄCH",
    "theme": "Marketing",
    
    "situation": "Die IHK-Beraterin stellt eine wichtige Frage:",
    
    "question": "\"Wie gewinnen Sie Ihre ersten 10 zahlenden Kunden?\"",
    
    "prompt": "Wie antwortest du?",
    
    "options": [
      {
        "id": "A",
        "text": "\"Ich hoffe auf Empfehlungen und Mundpropaganda. Wenn das Angebot gut ist, spricht sich das rum.\"",
        "score": 0,
        "gap": true,
        "severity": "critical"
      },
      {
        "id": "B",
        "text": "\"Ich werde eine Website bauen und dann Social Media und vielleicht etwas Werbung schalten.\"",
        "score": 35,
        "gap": true,
        "severity": "high"
      },
      {
        "id": "C",
        "text": "\"LinkedIn-Outreach: 20 Kontakte pro Tag, bei 5% Conversion habe ich in 4 Wochen 10 Kunden. Budget: 500€ für Ads.\"",
        "score": 75,
        "gap": false,
        "severity": null
      },
      {
        "id": "D",
        "text": "\"Ich habe bereits 3 Absichtserklärungen und eine Warteliste mit 47 Interessenten aus meiner Pilotphase.\"",
        "score": 100,
        "gap": false,
        "severity": null
      }
    ]
  },
  
  "gz_insight": {
    "trigger": ["A"],
    "title": "⚠️ ACHTUNG",
    "content": "\"Hoffen\" ist keine Strategie!\n\nDie IHK will einen konkreten Plan sehen:\n• Welche Kanäle?\n• Welches Budget?\n• Welche Conversion-Rate?\n\nOhne das ist deine Umsatzprognose nicht glaubwürdig.",
    "cta": "Im Workshop entwickeln wir deinen Marketing-Funnel."
  },
  
  "gz_insight_b": {
    "trigger": ["B"],
    "title": "💡 GUT ZU WISSEN",
    "content": "\"Website und Social Media\" ist ein Anfang, aber zu vage.\n\nDie IHK will Zahlen:\n• Wie viele Besucher → Leads → Kunden?\n• Welches Budget pro Kanal?\n• Welcher Zeitplan?",
    "cta": null
  },
  
  "gap_trigger": {
    "gap_id": "marketing",
    "gap_title": "Marketing-Strategie",
    "gap_description": "Kein konkreter Plan zur Kundengewinnung",
    "covered_in_module": 4,
    "approval_impact": "Umsatzprognose nicht glaubwürdig"
  }
}
```

---

## C2: Qualifikation (GZ-Readiness)

```json
{
  "id": "C2",
  "block": "C",
  "type": "gz_readiness",
  "topic": "qualifikation",
  "weight": 10,
  "context": "ihk",
  
  "scenario": {
    "setting": "🏛️ IHK-GESPRÄCH",
    "theme": "Deine Eignung",
    
    "situation": "Die IHK-Beraterin lehnt sich zurück und stellt die entscheidende Frage:",
    
    "question": "\"Warum sind ausgerechnet SIE die richtige Person, um {{business_type_de}} erfolgreich anzubieten?\"",
    
    "prompt": "Wie antwortest du?",
    
    "options": [
      {
        "id": "A",
        "text": "\"Ich bin hochmotiviert und lerne schnell. Den Rest werde ich mir aneignen.\"",
        "score": 0,
        "gap": true,
        "severity": "high"
      },
      {
        "id": "B",
        "text": "\"Ich habe mich intensiv eingelesen und mehrere Online-Kurse absolviert. Ich kenne die Theorie.\"",
        "score": 35,
        "gap": true,
        "severity": "medium"
      },
      {
        "id": "C",
        "text": "\"10 Jahre Berufserfahrung in der Branche, davon 3 Jahre in Führungsposition. Hier sind meine Zertifikate und Referenzen.\"",
        "score": 75,
        "gap": false,
        "severity": null
      },
      {
        "id": "D",
        "text": "\"Branchenexperte plus BWL-Hintergrund. Außerdem bin ich schon 2 Jahre nebenberuflich selbstständig mit ersten zahlenden Kunden.\"",
        "score": 100,
        "gap": false,
        "severity": null
      }
    ]
  },
  
  "gz_insight": {
    "trigger": ["A", "B"],
    "title": "💡 GUT ZU WISSEN",
    "content": "Die IHK prüft deine Eignung sehr genau.\n\nSie wollen sehen:\n• Fachliche Qualifikation (Ausbildung, Erfahrung)\n• Kaufmännische Grundkenntnisse\n• Erste praktische Erfahrungen\n\nMotivation allein reicht nicht.",
    "cta": null
  },
  
  "gap_trigger": {
    "gap_id": "qualifikation",
    "gap_title": "Qualifikationsnachweis",
    "gap_description": "Keine nachweisbare Fachkompetenz oder Erfahrung",
    "covered_in_module": 1,
    "approval_impact": "Diskretionäre Ablehnung möglich"
  }
}
```

---

## C3: IHK-Präsentation (Self-Efficacy #1)

```json
{
  "id": "C3",
  "block": "C",
  "type": "personality",
  "dimension": "self_efficacy",
  "dimension_de": "Selbstwirksamkeit",
  
  "scenario": {
    "setting": "💼 VORBEREITUNGS-SITUATION",
    "theme": "IHK-Termin",
    
    "situation": "In 2 Wochen hast du deinen Termin bei der IHK. Du musst deinen Businessplan präsentieren und kritische Fragen beantworten.",
    
    "question": "Wie fühlst du dich?",
    
    "prompt": "Dein Gefühl:",
    
    "options": [
      {
        "id": "A",
        "text": "Panik. Ich bin kein guter Präsentator. Hoffentlich stellen die keine schwierigen Fragen.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Nervös. Ich bereite mich gut vor, aber sicher bin ich mir nicht.",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Aufgeregt, aber zuversichtlich. Ich kenne meinen Plan und übe meine Antworten.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "Selbstsicher. Niemand kennt mein Business besser als ich. Die Fragen werden kein Problem.",
        "theta": 1.5
      }
    ]
  }
}
```

---

## C4: Halbjahres-Review (Achievement Orientation #2)

```json
{
  "id": "C4",
  "block": "C",
  "type": "personality",
  "dimension": "achievement_orientation",
  "dimension_de": "Leistungsorientierung",
  
  "scenario": {
    "setting": "💼 REVIEW-SITUATION",
    "theme": "Halbzeit-Bilanz",
    
    "situation": "Nach 6 Monaten ziehst du Bilanz: Du hast 80% deines Halbjahresziels erreicht. Nicht schlecht, aber eben nicht 100%.",
    
    "question": "Wie bewertest du das?",
    
    "prompt": "Dein Fazit:",
    
    "options": [
      {
        "id": "A",
        "text": "Enttäuschend. Ich habe mein Ziel nicht erreicht. Vielleicht habe ich mich überschätzt.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Okay, 80% ist akzeptabel. Immerhin bin ich nicht gescheitert.",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Solide Basis. Jetzt analysiere ich, was gefehlt hat, und passe meine Strategie für Q3/Q4 an.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "Motivierend! 80% nach 6 Monaten heißt, ich kann mein Jahresziel noch übertreffen. Ich erhöhe.",
        "theta": 1.5
      }
    ]
  }
}
```

---

## C5: Erfolg erklären (Locus of Control #2)

```json
{
  "id": "C5",
  "block": "C",
  "type": "personality",
  "dimension": "locus_of_control",
  "dimension_de": "Kontrollüberzeugung",
  
  "scenario": {
    "setting": "💼 ERFOLGS-SITUATION",
    "theme": "Großer Kunde gewonnen",
    
    "situation": "Du hast gerade deinen bisher größten Kunden gewonnen - ein Auftrag über 15.000€. Ein Freund fragt: \"Wie hast du das geschafft?\"",
    
    "question": "Wie erklärst du deinen Erfolg?",
    
    "prompt": "Deine Antwort:",
    
    "options": [
      {
        "id": "A",
        "text": "\"Ehrlich? Glück gehabt. Zur richtigen Zeit am richtigen Ort. Das hätte auch anders laufen können.\"",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "\"Der Kunde hatte gerade Bedarf und mein Angebot passte. Gutes Timing.\"",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "\"Mein Angebot hat überzeugt. Die gründliche Vorbereitung und das maßgeschneiderte Angebot haben sich ausgezahlt.\"",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "\"Das ist das Ergebnis meiner systematischen Akquise-Strategie. Ich habe 50 Kontakte bearbeitet, bis dieser dabei war.\"",
        "theta": 1.5
      }
    ]
  }
}
```

---

## C6: Neue Fähigkeit (Self-Efficacy #2)

```json
{
  "id": "C6",
  "block": "C",
  "type": "personality",
  "dimension": "self_efficacy",
  "dimension_de": "Selbstwirksamkeit",
  
  "scenario": {
    "setting": "💼 LERN-SITUATION",
    "theme": "Neue Skills",
    
    "situation": "Für dein {{business_type_de}} brauchst du eine Fähigkeit, die du noch nicht hast - zum Beispiel Buchhaltung, Verkaufen oder eine bestimmte Software.",
    
    "question": "Was denkst du?",
    
    "prompt": "Deine Einschätzung:",
    
    "options": [
      {
        "id": "A",
        "text": "Das kann ich nicht. Ich muss jemanden finden, der das für mich macht.",
        "theta": -1.5
      },
      {
        "id": "B",
        "text": "Wird schwierig. Vielleicht finde ich einen Online-Kurs, aber ob das reicht...",
        "theta": -0.5
      },
      {
        "id": "C",
        "text": "Herausforderung angenommen. Mit dem richtigen Kurs und etwas Übung habe ich das in 4 Wochen drauf.",
        "theta": 0.5
      },
      {
        "id": "D",
        "text": "Kein Problem. Ich habe mir schon viel schwierigere Dinge selbst beigebracht.",
        "theta": 1.5
      }
    ]
  }
}
```

---

# TIPS SCREEN (nach Block C)

```json
{
  "id": "TIPS",
  "type": "info_screen",
  
  "content": {
    "title": "⏰ BEVOR DU STARTEST",
    "subtitle": "3 Dinge, die du wissen musst",
    
    "tips": [
      {
        "icon": "1️⃣",
        "title": "ALG-RESTANSPRUCH",
        "text": "Du brauchst mindestens 150 Tage Restanspruch auf Arbeitslosengeld bei Antragstellung. Prüfe das in deinem Bescheid!"
      },
      {
        "icon": "2️⃣",
        "title": "REIHENFOLGE BEACHTEN",
        "text": "Erst GZ-Antrag stellen, DANN Gewerbe anmelden. Andersrum = automatische Ablehnung!"
      },
      {
        "icon": "3️⃣",
        "title": "FRÜH PLANEN",
        "text": "IHK-Termine dauern oft 4-6 Wochen. Fachkundige Stelle früh kontaktieren!"
      }
    ],
    
    "cta": "Verstanden"
  }
}
```

---

# SCORING & ARCHETYPE LOGIC

## GZ-Readiness Scoring

```python
GZ_WEIGHTS = {
    "A1_zielkunden": 20,
    "A2_wettbewerb": 15,
    "B1_umsatzprognose": 20,
    "B2_break_even": 20,
    "C1_marketing": 15,
    "C2_qualifikation": 10
}

ANSWER_SCORES = {
    "A": 0,
    "B": 35,
    "C": 75,
    "D": 100
}

def calculate_gz_score(gz_answers: dict) -> dict:
    """
    Calculate GZ-Readiness Score from 6 GZ questions.
    
    Returns:
        {
            "score": 0-100,
            "approval_chance": "20-95%",
            "gaps": [...],
            "critical_gaps": [...]
        }
    """
    total_weighted = 0
    max_weighted = 0
    gaps = []
    
    for question_id, weight in GZ_WEIGHTS.items():
        answer = gz_answers.get(question_id, "A")
        score = ANSWER_SCORES[answer]
        total_weighted += score * weight
        max_weighted += 100 * weight
        
        if answer in ["A", "B"]:
            gaps.append({
                "question_id": question_id,
                "severity": "critical" if answer == "A" else "high",
                "answer": answer
            })
    
    final_score = int(total_weighted / max_weighted * 100)
    
    # Map to approval chance
    if final_score >= 85:
        approval_chance = "80-95%"
    elif final_score >= 70:
        approval_chance = "65-80%"
    elif final_score >= 50:
        approval_chance = "50-65%"
    elif final_score >= 25:
        approval_chance = "35-50%"
    else:
        approval_chance = "20-35%"
    
    return {
        "score": final_score,
        "approval_chance": approval_chance,
        "gaps": gaps,
        "critical_gaps": [g for g in gaps if g["severity"] == "critical"]
    }
```

---

## Personality Scoring (IRT-based)

```python
DIMENSION_WEIGHTS = {
    "proactiveness": 1.0,      # A3, A5
    "risk_taking": 1.0,        # B3, B5
    "achievement_orientation": 1.0,  # A4, C4
    "locus_of_control": 1.0,   # B4, C5
    "self_efficacy": 1.0       # C3, C6
}

THETA_MAP = {
    "A": -1.5,
    "B": -0.5,
    "C": 0.5,
    "D": 1.5
}

def calculate_dimension_score(answers: list[str]) -> dict:
    """
    Calculate dimension score from 2 questions using simple averaging.
    
    Returns:
        {
            "theta": -1.5 to 1.5,
            "percentile": 0-100,
            "level": "low" | "medium" | "high"
        }
    """
    thetas = [THETA_MAP[a] for a in answers]
    avg_theta = sum(thetas) / len(thetas)
    
    # Convert theta to percentile (assuming normal distribution)
    # theta -1.5 ≈ 7th percentile
    # theta 0 ≈ 50th percentile
    # theta 1.5 ≈ 93rd percentile
    percentile = int(50 + avg_theta * 28)  # Simplified linear mapping
    percentile = max(5, min(95, percentile))
    
    if avg_theta < -0.5:
        level = "low"
    elif avg_theta > 0.5:
        level = "high"
    else:
        level = "medium"
    
    return {
        "theta": avg_theta,
        "percentile": percentile,
        "level": level
    }
```

---

## Archetype Determination

```python
ARCHETYPES = {
    "macher": {
        "name": "Der Macher",
        "emoji": "⚡",
        "dominant": ["proactiveness", "risk_taking"],
        "description": "Du packst an und lernst durch Tun. Deine Stärke: Schnelle Umsetzung. Achte darauf, auch mal innezuhalten und zu planen.",
        "strengths": ["Schnelle Umsetzung", "Hohe Energie", "Entscheidungsfreude"],
        "watch_outs": ["Gründliche Planung", "Risiko-Analyse", "Geduld"]
    },
    "stratege": {
        "name": "Der Stratege",
        "emoji": "🎯",
        "dominant": ["achievement_orientation", "locus_of_control"],
        "description": "Du planst gründlich und behältst die Kontrolle. Deine Stärke: Durchdachte Entscheidungen. Achte darauf, auch mal zu handeln, bevor alles perfekt ist.",
        "strengths": ["Gründliche Planung", "Systematisches Vorgehen", "Zielorientierung"],
        "watch_outs": ["Perfektionismus", "Analysis Paralysis", "Schnellere Umsetzung"]
    },
    "ueberzeuger": {
        "name": "Der Überzeuger",
        "emoji": "💪",
        "dominant": ["self_efficacy", "proactiveness"],
        "description": "Du glaubst an dich und gehst aktiv auf Menschen zu. Deine Stärke: Kunden gewinnen und überzeugen. Achte darauf, auch die Zahlen im Blick zu behalten.",
        "strengths": ["Überzeugungskraft", "Selbstvertrauen", "Netzwerken"],
        "watch_outs": ["Detailarbeit", "Finanzplanung", "Kritisches Hinterfragen"]
    },
    "analytiker": {
        "name": "Der Analytiker",
        "emoji": "📊",
        "dominant": ["locus_of_control", "achievement_orientation"],
        "description": "Du verstehst Zusammenhänge und triffst datenbasierte Entscheidungen. Deine Stärke: Fundierte Analyse. Achte darauf, nicht zu lange zu analysieren.",
        "strengths": ["Datengetrieben", "Systematisch", "Lösungsorientiert"],
        "watch_outs": ["Bauchentscheidungen", "Schnelles Testen", "Umgang mit Unsicherheit"]
    },
    "vorsichtiger": {
        "name": "Der Vorsichtige",
        "emoji": "🛡️",
        "dominant": ["low_risk_taking", "high_locus_of_control"],
        "description": "Du gehst kalkuliert vor und minimierst Risiken. Deine Stärke: Nachhaltiger Aufbau. Achte darauf, auch Chancen zu ergreifen.",
        "strengths": ["Risikobewusstsein", "Sorgfältige Vorbereitung", "Nachhaltigkeit"],
        "watch_outs": ["Chancen ergreifen", "Größer denken", "Schnellere Entscheidungen"]
    }
}

def determine_archetype(dimension_scores: dict) -> dict:
    """
    Determine archetype based on Top 5 dimension scores.
    
    Returns archetype dict with name, emoji, description, strengths, watch_outs
    """
    # Find dominant dimensions (highest scores)
    sorted_dims = sorted(
        dimension_scores.items(),
        key=lambda x: x[1]["theta"],
        reverse=True
    )
    
    top_2 = [d[0] for d in sorted_dims[:2]]
    
    # Special case: low risk-taking + high control = Vorsichtiger
    if (dimension_scores["risk_taking"]["theta"] < -0.3 and
        dimension_scores["locus_of_control"]["theta"] > 0.3):
        return ARCHETYPES["vorsichtiger"]
    
    # Match archetypes based on dominant dimensions
    if "proactiveness" in top_2 and "risk_taking" in top_2:
        return ARCHETYPES["macher"]
    elif "self_efficacy" in top_2 and "proactiveness" in top_2:
        return ARCHETYPES["ueberzeuger"]
    elif "achievement_orientation" in top_2 and "locus_of_control" in top_2:
        if dimension_scores["proactiveness"]["theta"] > 0:
            return ARCHETYPES["stratege"]
        else:
            return ARCHETYPES["analytiker"]
    elif "locus_of_control" in top_2:
        return ARCHETYPES["analytiker"]
    elif "achievement_orientation" in top_2:
        return ARCHETYPES["stratege"]
    else:
        # Default fallback
        return ARCHETYPES["stratege"]
```

---

# RESULT PAGE STRUCTURE

```json
{
  "result_page": {
    "sections": [
      {
        "id": "archetype",
        "title": "DEIN GRÜNDER-TYP",
        "content": {
          "name": "{{archetype.name}}",
          "emoji": "{{archetype.emoji}}",
          "description": "{{archetype.description}}"
        }
      },
      {
        "id": "strengths",
        "title": "DEINE STÄRKEN",
        "content": {
          "items": "{{archetype.strengths}}"
        }
      },
      {
        "id": "gz_readiness",
        "title": "DEIN GZ-READINESS CHECK",
        "content": {
          "current_score": "{{gz_score}}%",
          "approval_chance": "{{approval_chance}}",
          "gaps": "{{gaps_list}}",
          "with_workshop": "85%+"
        }
      },
      {
        "id": "cta",
        "title": "NÄCHSTER SCHRITT",
        "content": {
          "primary": {
            "text": "Zum Workshop →",
            "subtext": "In 6 Modulen zum bewilligungsfertigen Antrag"
          },
          "secondary": {
            "text": "Volles Persönlichkeitsprofil freischalten",
            "subtext": "7 Dimensionen + PDF-Report"
          }
        }
      }
    ]
  }
}
```

---

# GAP MAPPING

```python
GAP_DATABASE = {
    "marktanalyse": {
        "id": "marktanalyse",
        "title": "Zielgruppen-Definition",
        "icon": "👥",
        "module": 2,
        "module_name": "Markt & Wettbewerb",
        "impact": "30% der Ablehnungen",
        "description": "Keine konkrete Beschreibung deiner Zielkunden mit demographischen Daten.",
        "what_you_learn": "Du erstellst eine detaillierte Kunden-Persona mit Alter, Einkommen, Kaufverhalten und konkreten Zitaten."
    },
    "wettbewerb": {
        "id": "wettbewerb",
        "title": "Wettbewerbsanalyse",
        "icon": "⚔️",
        "module": 2,
        "module_name": "Markt & Wettbewerb",
        "impact": "IHK-Bescheinigung gefährdet",
        "description": "Keine systematische Analyse deiner Konkurrenten.",
        "what_you_learn": "Du erstellst eine Wettbewerbs-Matrix mit mindestens 5 Konkurrenten und deiner klaren Positionierung."
    },
    "finanzplan": {
        "id": "finanzplan",
        "title": "Umsatzprognose",
        "icon": "💰",
        "module": 6,
        "module_name": "Finanzplan",
        "impact": "Häufigster Ablehnungsgrund",
        "description": "Keine nachvollziehbare Bottom-Up-Umsatzberechnung.",
        "what_you_learn": "Du erstellst einen 36-Monats-Finanzplan mit Kunden × Preis × Frequenz Logik."
    },
    "break_even": {
        "id": "break_even",
        "title": "Break-Even-Berechnung",
        "icon": "📈",
        "module": 6,
        "module_name": "Finanzplan",
        "impact": "Tragfähigkeit nicht nachweisbar",
        "description": "Kein konkreter Zeitpunkt für Profitabilität berechnet.",
        "what_you_learn": "Du berechnest deinen Break-Even mit Best/Worst Case Szenarien."
    },
    "marketing": {
        "id": "marketing",
        "title": "Marketing-Strategie",
        "icon": "📣",
        "module": 4,
        "module_name": "Marketing & Vertrieb",
        "impact": "Umsatzprognose nicht glaubwürdig",
        "description": "Kein konkreter Plan zur Kundengewinnung mit Kanälen und Budget.",
        "what_you_learn": "Du entwickelst deinen Marketing-Funnel mit konkreten Conversion-Raten und Kosten pro Kunde."
    },
    "qualifikation": {
        "id": "qualifikation",
        "title": "Qualifikationsnachweis",
        "icon": "🎓",
        "module": 1,
        "module_name": "Vision & Positionierung",
        "impact": "Diskretionäre Ablehnung möglich",
        "description": "Keine nachweisbare Fachkompetenz oder relevante Erfahrung.",
        "what_you_learn": "Du lernst, wie du deine Qualifikation überzeugend für die IHK darstellst - auch ohne klassischen Berufsabschluss."
    }
}
```

---

# PERSONALIZATION TOKENS

## Available Tokens

| Token | Source | Example |
|-------|--------|---------|
| `{{business_type_de}}` | Onboarding | "Restaurant", "IT-Beratung" |
| `{{target_customer}}` | Onboarding | "Familien mit Kindern" |
| `{{stage}}` | Onboarding | "Konzeptphase" |
| `{{user_name}}` | Onboarding | "Anna" |

## Business Type Mapping

```python
BUSINESS_TYPES = {
    "gastro": {
        "de": "Gastronomie",
        "example": "Restaurant / Café",
        "context_scenarios": {
            "investment": "Küchenausstattung",
            "customer": "Gäste",
            "location": "Standort"
        }
    },
    "tech": {
        "de": "Software / Tech",
        "example": "SaaS / App",
        "context_scenarios": {
            "investment": "Entwicklung",
            "customer": "Nutzer",
            "location": "Remote"
        }
    },
    "consulting": {
        "de": "Beratung",
        "example": "Unternehmensberatung",
        "context_scenarios": {
            "investment": "Marketing",
            "customer": "Klienten",
            "location": "Büro / Remote"
        }
    },
    "ecommerce": {
        "de": "E-Commerce",
        "example": "Online-Shop",
        "context_scenarios": {
            "investment": "Lager & Marketing",
            "customer": "Online-Käufer",
            "location": "Lager / Dropshipping"
        }
    },
    "service": {
        "de": "Dienstleistung",
        "example": "Handwerk / Personal Service",
        "context_scenarios": {
            "investment": "Ausrüstung",
            "customer": "Kunden",
            "location": "Vor Ort"
        }
    },
    "creative": {
        "de": "Kreativ / Agentur",
        "example": "Design / Marketing",
        "context_scenarios": {
            "investment": "Software & Portfolio",
            "customer": "Auftraggeber",
            "location": "Studio / Remote"
        }
    },
    "health": {
        "de": "Gesundheit / Wellness",
        "example": "Praxis / Coaching",
        "context_scenarios": {
            "investment": "Praxisausstattung",
            "customer": "Patienten / Klienten",
            "location": "Praxis"
        }
    },
    "education": {
        "de": "Bildung / Coaching",
        "example": "Kurse / Training",
        "context_scenarios": {
            "investment": "Content-Erstellung",
            "customer": "Teilnehmer",
            "location": "Online / Präsenz"
        }
    }
}
```

---

# IMPLEMENTATION NOTES

## Question Sequence

```
1. A1 (GZ: Zielkunden)
2. A2 (GZ: Wettbewerb)
3. A3 (P: Proactiveness #1)
4. A4 (P: Achievement #1)
5. A5 (P: Proactiveness #2)
6. B1 (GZ: Umsatzprognose)
7. B2 (GZ: Break-Even)
8. B3 (P: Risk-Taking #1)
9. B4 (P: Locus of Control #1)
10. B5 (P: Risk-Taking #2)
11. C1 (GZ: Marketing)
12. C2 (GZ: Qualifikation)
13. C3 (P: Self-Efficacy #1)
14. C4 (P: Achievement #2)
15. C5 (P: Locus of Control #2)
16. C6 (P: Self-Efficacy #2)
17. TIPS Screen
18. RESULT
```

## GZ-Insight Display Logic

```python
def should_show_insight(question_id: str, answer: str) -> bool:
    """
    Determine if GZ-Insight should be shown after this answer.
    Only for GZ-Readiness questions with A or B answers.
    """
    gz_questions = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    if question_id not in gz_questions:
        return False
    
    return answer in ["A", "B"]
```

## Progress Calculation

```python
def calculate_progress(current_question: int) -> int:
    """Progress percentage for progress bar."""
    total = 17  # 16 questions + tips screen
    return int((current_question / total) * 100)
```

---

# VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2024-12 | Initial V4 with Top 5 dimensions, scenario-based GZ-Readiness |
| 3.0.0 | 2024-12 | Pre-generated bank (replaced AI on-demand) |
| 2.0.0 | 2024-11 | AI-generated scenarios |
| 1.0.0 | 2024-10 | Original Howard 7-dimension assessment |
