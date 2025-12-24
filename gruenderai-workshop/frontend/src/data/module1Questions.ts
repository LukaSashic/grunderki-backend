/**
 * GründerAI Workshop - Module 1 Questions
 * Die 6-8 Fragen für "Geschäftsidee & Gründerprofil"
 * Mit Conditional Logic, BA GZ 04 Kontext und AI Coaching Config
 */

import type { Module1Question, Module1Answers } from '@/types/module1.types';

export const MODULE_1_QUESTIONS: Module1Question[] = [
  // ============================================================================
  // FRAGE 1: Was bietest du an? (GESCHÄFTSIDEE)
  // ============================================================================
  {
    id: 'q1_angebot',
    type: 'textarea',
    phase: 'geschaeftsidee',

    question: 'Was genau bietest du an?',
    subtext: 'Beschreibe dein Produkt oder deine Dienstleistung in 2-3 Sätzen. Was macht dein Angebot einzigartig?',
    placeholder: 'Ich biete... für... an, um das Problem... zu lösen. Das Besondere daran ist...',

    baFormContext: {
      formular: 'BA_GZ_04',
      frageNummer: 11,
      originalWortlaut: 'Scheint das Existenzgründungsvorhaben – auch in absehbarer Zeit – konkurrenzfähig?',
      warumWichtig: 'Die fachkundige Stelle (IHK) muss verstehen, was du anbietest, um Konkurrenzfähigkeit zu beurteilen. Eine unklare Beschreibung führt zu Rückfragen oder Ablehnung.',
      wieWirHelfen: 'Deine Antwort wird Teil des Businessplan-Kapitels 2.1 (Angebot). Wir helfen dir, es GZ-konform zu formulieren.'
    },

    gzRelevant: true,
    gzDoorId: 'konkurrenz',

    minLength: 100,
    maxLength: 500,
    required: true,

    coachingConfig: {
      maxIterations: 3,
      requireSpecificity: true,
      checkForGeneric: true,
      frameworkToTeach: 'jobs_to_be_done',
      coachingTone: 'standard'
    },

    personalityAdaptation: {
      highInnovativeness: {
        emphasis: 'Was ist das Innovative an deinem Angebot? Wie unterscheidest du dich von bestehenden Lösungen?'
      },
      lowRiskTaking: {
        emphasis: 'Welche bewährten Elemente greifst du auf? Warum funktioniert dieser Ansatz?'
      }
    },

    frameworkToTeach: 'jobs_to_be_done'
  },

  // ============================================================================
  // FRAGE 2: Fachlicher Hintergrund (GRÜNDERPROFIL - KRITISCH!)
  // ============================================================================
  {
    id: 'q2_hintergrund',
    type: 'multiple_choice',
    phase: 'gruenderprofil',

    question: 'Wie würdest du deinen fachlichen Hintergrund für diese Geschäftsidee beschreiben?',
    subtext: 'Die IHK prüft, ob du die fachlichen Voraussetzungen für dein Vorhaben mitbringst. Das ist eine der kritischsten Fragen!',

    options: [
      {
        value: 'A',
        label: 'Ich habe eine Ausbildung/Studium genau in diesem Bereich',
        score: 100,
        icon: '🎓'
      },
      {
        value: 'B',
        label: 'Ich habe 5+ Jahre Berufserfahrung in der Branche',
        score: 90,
        icon: '💼'
      },
      {
        value: 'C',
        label: 'Ich habe 2-5 Jahre Erfahrung in einem verwandten Bereich',
        score: 70,
        icon: '📊'
      },
      {
        value: 'D',
        label: 'Ich bin Quereinsteiger mit relevanten Skills',
        score: 50,
        icon: '🔄',
        triggersFollowUp: 'q2b_quereinsteiger'
      },
      {
        value: 'E',
        label: 'Ich bin kompletter Neuling in diesem Bereich',
        score: 20,
        icon: '🌱',
        triggersFollowUp: 'q2b_quereinsteiger'
      }
    ],

    baFormContext: {
      formular: 'BA_GZ_04',
      frageNummer: 8,
      originalWortlaut: 'Sind die Voraussetzungen für das Existenzgründungsvorhaben in fachlicher und branchenspezifischer Hinsicht gegeben?',
      warumWichtig: '⚠️ KRITISCH: 65% der Ablehnungen hängen mit mangelnder fachlicher Qualifikation zusammen! Diese Frage ist entscheidend.',
      wieWirHelfen: 'Wir zeigen dir, wie du auch als Quereinsteiger überzeugst und welche Nachweise du erbringen kannst.'
    },

    gzRelevant: true,
    gzDoorId: 'fachlich',
    required: true,

    frameworkToTeach: 'gruender_business_fit'
  },

  // ============================================================================
  // FRAGE 2b: Quereinsteiger Details (CONDITIONAL - nur wenn D oder E)
  // ============================================================================
  {
    id: 'q2b_quereinsteiger',
    type: 'textarea',
    phase: 'gruenderprofil',

    showIf: (answers: Module1Answers) =>
      answers.q2_hintergrund === 'D' || answers.q2_hintergrund === 'E',

    question: 'Welche Qualifikationen und Erfahrungen bringst du mit, die für deine Geschäftsidee relevant sind?',
    subtext: 'Denke an: Übertragbare Skills, Weiterbildungen, Praktika, Projekte, Selbststudium, ehrenamtliche Tätigkeiten...',
    placeholder: 'Obwohl ich nicht direkt aus der Branche komme, bringe ich folgende relevante Qualifikationen mit: ...',

    baFormContext: {
      formular: 'BA_GZ_04',
      frageNummer: 8,
      originalWortlaut: '(Fortsetzung) Sind die Voraussetzungen für das Existenzgründungsvorhaben in fachlicher und branchenspezifischer Hinsicht gegeben?',
      warumWichtig: 'Als Quereinsteiger musst du zeigen, dass du die nötigen Fähigkeiten erwerben KANNST oder bereits hast. Konkrete Beispiele sind wichtiger als allgemeine Aussagen.',
      wieWirHelfen: 'Wir helfen dir, deine übertragbaren Fähigkeiten überzeugend zu formulieren und zeigen dir, welche Weiterbildungen die IHK überzeugen.'
    },

    gzRelevant: true,
    gzDoorId: 'fachlich',

    minLength: 150,
    maxLength: 600,
    required: true,

    coachingConfig: {
      maxIterations: 3,
      frameworkToTeach: 'transferable_skills',
      coachingTone: 'empowering',
      suggestResources: true,
      resources: [
        { name: 'IHK Existenzgründerseminar', note: 'Kostenlos, 2-3 Tage – zeigt kaufmännische Initiative' },
        { name: 'Branchenspezifische Zertifikate', note: 'Online-Kurse (Coursera, Udemy) als Nachweis' },
        { name: 'AVGS Gründercoaching', note: 'Über Arbeitsagentur finanzierbar' }
      ]
    },

    personalityAdaptation: {
      lowSelfEfficacy: {
        emphasis: 'Du hast mehr relevante Erfahrung als du denkst! Lass uns gemeinsam herausfinden, welche deiner Fähigkeiten übertragbar sind.'
      }
    },

    frameworkToTeach: 'transferable_skills'
  },

  // ============================================================================
  // FRAGE 3: Kaufmännische Kenntnisse (KRITISCH!)
  // ============================================================================
  {
    id: 'q3_kaufmaennisch',
    type: 'multiple_choice',
    phase: 'gruenderprofil',

    question: 'Wie schätzt du deine kaufmännischen Kenntnisse ein?',
    subtext: 'Die IHK prüft, ob du ein Unternehmen FÜHREN kannst, nicht nur ob du fachlich gut bist.',

    options: [
      {
        value: 'A',
        label: 'Kaufmännische Ausbildung / BWL-Studium',
        score: 100,
        icon: '📈'
      },
      {
        value: 'B',
        label: 'Mehrjährige Erfahrung mit Buchhaltung/Finanzen im Job',
        score: 85,
        icon: '💹'
      },
      {
        value: 'C',
        label: 'Grundkenntnisse durch Selbststudium/Kurse',
        score: 60,
        icon: '📚'
      },
      {
        value: 'D',
        label: 'Wenig Erfahrung, aber lernwillig',
        score: 40,
        icon: '🎯',
        triggersFollowUp: 'q3b_wie_erworben'
      },
      {
        value: 'E',
        label: 'Keine kaufmännischen Kenntnisse',
        score: 20,
        icon: '🔰',
        triggersFollowUp: 'q3b_wie_erworben'
      }
    ],

    baFormContext: {
      formular: 'BA_GZ_04',
      frageNummer: 9,
      originalWortlaut: 'Sind die Voraussetzungen für das Existenzgründungsvorhaben in kaufmännischer und unternehmerischer Hinsicht gegeben?',
      warumWichtig: 'Die IHK will sehen, dass du Buchhaltung, Steuern, Kalkulation und Unternehmensführung verstehst. Ohne diese Grundlagen besteht Insolvenzrisiko.',
      wieWirHelfen: 'Wir zeigen dir, welche Weiterbildungen schnell helfen (z.B. kostenloses IHK Existenzgründerseminar).'
    },

    gzRelevant: true,
    gzDoorId: 'kaufmaennisch',
    required: true
  },

  // ============================================================================
  // FRAGE 3b: Wie Kenntnisse erwerben (CONDITIONAL - nur wenn D oder E)
  // ============================================================================
  {
    id: 'q3b_wie_erworben',
    type: 'textarea',
    phase: 'gruenderprofil',

    showIf: (answers: Module1Answers) =>
      answers.q3_kaufmaennisch === 'D' || answers.q3_kaufmaennisch === 'E',

    question: 'Wie planst du, dir die nötigen kaufmännischen Kenntnisse anzueignen?',
    subtext: 'Die IHK akzeptiert konkrete Pläne! Existenzgründerseminar? AVGS-Coaching? Online-Kurse? Steuerberater?',
    placeholder: 'Um meine kaufmännischen Kenntnisse zu erweitern, plane ich: ...',

    baFormContext: {
      formular: 'BA_GZ_04',
      frageNummer: 9,
      originalWortlaut: '(Fortsetzung) Sind die Voraussetzungen für das Existenzgründungsvorhaben in kaufmännischer und unternehmerischer Hinsicht gegeben?',
      warumWichtig: 'Ein konkreter Weiterbildungsplan kann fehlende Kenntnisse ausgleichen. Die IHK will sehen, dass du das Problem erkannt hast und aktiv angehst.',
      wieWirHelfen: 'Wir geben dir konkrete Empfehlungen für Weiterbildungen, die von der IHK anerkannt werden.'
    },

    gzRelevant: true,
    gzDoorId: 'kaufmaennisch',

    minLength: 100,
    maxLength: 400,
    required: true,

    coachingConfig: {
      maxIterations: 2,
      coachingTone: 'empowering',
      suggestResources: true,
      resources: [
        { name: 'IHK Existenzgründerseminar', url: 'https://ihk.de', note: 'Kostenlos, 2-3 Tage – wird von jeder IHK angeboten' },
        { name: 'AVGS Coaching', note: 'Über Arbeitsagentur finanzierbar – individuelle Betreuung' },
        { name: 'Lexware/DATEV Grundkurs', note: 'Online-Kurse für Buchhaltungs-Basics' },
        { name: 'Steuerberater', note: 'Für die Buchhaltung outsourcen – Kosten einplanen' }
      ]
    }
  },

  // ============================================================================
  // FRAGE 4: Business-Typ (GESCHÄFTSMODELL)
  // ============================================================================
  {
    id: 'q4_business_typ',
    type: 'multiple_choice',
    phase: 'geschaeftsmodell',

    question: 'Welche Art von Business planst du?',
    subtext: 'Diese Einordnung hilft uns, die richtigen Folgefragen zu stellen und deinen Businessplan anzupassen.',

    options: [
      {
        value: 'dienstleistung',
        label: 'Dienstleistung',
        icon: '🛠️',
        example: 'Beratung, Coaching, Service, Handwerk'
      },
      {
        value: 'produkt',
        label: 'Physisches Produkt',
        icon: '📦',
        example: 'Herstellung, Manufaktur, Handmade'
      },
      {
        value: 'software',
        label: 'Software / Digitales Produkt',
        icon: '💻',
        example: 'SaaS, App, Online-Kurse, Templates'
      },
      {
        value: 'handel',
        label: 'Handel',
        icon: '🏪',
        example: 'Einkauf & Verkauf, Import, E-Commerce'
      }
    ],

    baFormContext: {
      formular: 'BA_GZ_02',
      frageNummer: 36,
      originalWortlaut: 'Bitte beschreiben Sie hier in kurzer Form Ihre Geschäftsidee.',
      warumWichtig: 'Der Business-Typ bestimmt deine Kostenstruktur, Kapitalbedarf und Skalierbarkeit. Die IHK erwartet, dass du dein Geschäftsmodell verstehst.',
      wieWirHelfen: 'Basierend auf deinem Business-Typ passen wir die Fragen in den folgenden Modulen an (Markt, Finanzen, Marketing).'
    },

    required: true,
    impactsModules: [3, 4, 5]
  },

  // ============================================================================
  // FRAGE 5: Zielgruppe B2B/B2C (GESCHÄFTSMODELL)
  // ============================================================================
  {
    id: 'q5_zielgruppe',
    type: 'multiple_choice',
    phase: 'geschaeftsmodell',

    question: 'Wer sind deine Hauptkunden?',
    subtext: 'Diese Einordnung ist wichtig für Modul 2 (Zielgruppe & Personas) und beeinflusst deine Marketing-Strategie.',

    options: [
      {
        value: 'B2C',
        label: 'Privatkunden (B2C)',
        icon: '👥',
        example: 'Einzelpersonen, Familien, Konsumenten'
      },
      {
        value: 'B2B',
        label: 'Geschäftskunden (B2B)',
        icon: '🏢',
        example: 'Unternehmen, Selbständige, Freiberufler'
      },
      {
        value: 'hybrid',
        label: 'Beides (B2B + B2C)',
        icon: '🔀',
        example: 'Je nach Produkt/Service unterschiedlich'
      },
      {
        value: 'oeffentlich',
        label: 'Öffentlicher Sektor',
        icon: '🏛️',
        example: 'Behörden, Kommunen, Bildungseinrichtungen'
      }
    ],

    baFormContext: {
      formular: 'BA_GZ_04',
      frageNummer: 10,
      originalWortlaut: 'Kann davon ausgegangen werden, dass aus dem Existenzgründungsvorhaben auf absehbare Zeit der Lebensunterhalt bestritten werden kann?',
      warumWichtig: 'Die Zielgruppe bestimmt Verkaufszyklen, Zahlungsverhalten und Akquise-Aufwand. B2B-Kunden zahlen oft später, B2C braucht mehr Marketing.',
      wieWirHelfen: 'In Modul 2 erstellen wir detaillierte Personas für deine Zielgruppe.'
    },

    required: true,
    impactsModules: [2]
  },

  // ============================================================================
  // FRAGE 6: Rechtsform (FORMALES)
  // ============================================================================
  {
    id: 'q6_rechtsform',
    type: 'multiple_choice',
    phase: 'formales',

    question: 'Welche Rechtsform planst du?',
    subtext: 'Die Rechtsform hat Auswirkungen auf Haftung, Steuern und Außenwirkung. Du kannst später noch wechseln.',

    options: [
      {
        value: 'einzelunternehmen',
        label: 'Einzelunternehmen / Gewerbetreibend',
        icon: '👤',
        pros: ['Einfach zu gründen', 'Niedrige Kosten', 'Volle Kontrolle'],
        cons: ['Volle persönliche Haftung', 'Gewerbesteuer']
      },
      {
        value: 'freiberuf',
        label: 'Freiberufler (kein Gewerbe)',
        icon: '🎨',
        pros: ['Keine Gewerbesteuer', 'Einfache Buchführung', 'Kein Handelsregister'],
        cons: ['Nur für bestimmte Berufe (§18 EStG)', 'Volle Haftung']
      },
      {
        value: 'gbr',
        label: 'GbR (mit Partner)',
        icon: '🤝',
        pros: ['Flexibel', 'Einfache Gründung', 'Keine Mindesteinlage'],
        cons: ['Alle haften persönlich und solidarisch', 'Keine Rechtspersönlichkeit']
      },
      {
        value: 'ug',
        label: 'UG (haftungsbeschränkt)',
        icon: '🛡️',
        pros: ['Haftungsbeschränkung', 'Ab 1€ Kapital möglich', 'Seriöser Auftritt'],
        cons: ['Buchführungspflicht', 'Rücklagenpflicht (25%)', 'Notarkosten']
      },
      {
        value: 'gmbh',
        label: 'GmbH',
        icon: '🏛️',
        pros: ['Seriöser Auftritt', 'Haftungsbeschränkung', 'Steuervorteile bei hohem Gewinn'],
        cons: ['25.000€ Stammkapital', 'Aufwändige Gründung', 'Hohe laufende Kosten']
      }
    ],

    baFormContext: {
      formular: 'BA_GZ_02',
      frageNummer: 29,
      originalWortlaut: 'Üben Sie eine Tätigkeit als Geschäftsführer/in einer GmbH aus?',
      warumWichtig: 'Bei GmbH/UG muss geklärt werden, ob echte Selbständigkeit vorliegt (mindestens 50% Anteile). Die Rechtsform beeinflusst auch den Kapitalbedarf.',
      wieWirHelfen: 'Wir erklären die Vor- und Nachteile jeder Rechtsform und wie sie sich auf deinen GZ-Antrag auswirkt.'
    },

    required: true,
    frameworkToTeach: 'rechtsformwahl'
  }
];

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Get visible questions based on conditional logic
 */
export const getVisibleQuestions = (answers: Module1Answers): Module1Question[] => {
  return MODULE_1_QUESTIONS.filter(q => {
    if (!q.showIf) return true;
    return q.showIf(answers);
  });
};

/**
 * Get progress percentage
 */
export const getModule1Progress = (answers: Module1Answers): number => {
  const visibleQuestions = getVisibleQuestions(answers);
  const answeredCount = visibleQuestions.filter(q => {
    const answer = answers[q.id as keyof Module1Answers];
    return answer !== undefined && answer !== '';
  }).length;
  return Math.round((answeredCount / visibleQuestions.length) * 100);
};

/**
 * Get phase label in German
 */
export const getPhaseLabel = (phase: Module1Question['phase']): string => {
  const labels = {
    geschaeftsidee: 'Geschäftsidee',
    gruenderprofil: 'Gründerprofil',
    geschaeftsmodell: 'Geschäftsmodell',
    formales: 'Formales'
  };
  return labels[phase];
};

/**
 * Calculate GZ score impact based on answers
 */
export const calculateGZScoreImpact = (answers: Module1Answers): {
  fachlichScore: number;
  kaufmaennischScore: number;
  overallImpact: number;
} => {
  let fachlichScore = 0;
  let kaufmaennischScore = 0;

  // Fachliche Qualifikation
  const hintergrundScores: Record<string, number> = {
    'A': 100, 'B': 90, 'C': 70, 'D': 50, 'E': 20
  };
  if (answers.q2_hintergrund) {
    fachlichScore = hintergrundScores[answers.q2_hintergrund] || 0;
  }

  // Bonus für Quereinsteiger-Begründung
  if ((answers.q2_hintergrund === 'D' || answers.q2_hintergrund === 'E') &&
      answers.q2b_quereinsteiger && answers.q2b_quereinsteiger.length > 200) {
    fachlichScore += 20; // Bonus für gute Begründung
  }

  // Kaufmännische Kenntnisse
  const kaufmaennischScores: Record<string, number> = {
    'A': 100, 'B': 85, 'C': 60, 'D': 40, 'E': 20
  };
  if (answers.q3_kaufmaennisch) {
    kaufmaennischScore = kaufmaennischScores[answers.q3_kaufmaennisch] || 0;
  }

  // Bonus für Weiterbildungsplan
  if ((answers.q3_kaufmaennisch === 'D' || answers.q3_kaufmaennisch === 'E') &&
      answers.q3b_wie_erworben && answers.q3b_wie_erworben.length > 100) {
    kaufmaennischScore += 20;
  }

  // Overall impact on GZ score (weighted average)
  const overallImpact = Math.round(
    (fachlichScore * 0.4 + kaufmaennischScore * 0.3) / 0.7
  );

  return {
    fachlichScore: Math.min(fachlichScore, 100),
    kaufmaennischScore: Math.min(kaufmaennischScore, 100),
    overallImpact: Math.min(overallImpact, 100)
  };
};
