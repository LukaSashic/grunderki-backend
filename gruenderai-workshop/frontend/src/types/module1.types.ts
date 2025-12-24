/**
 * GründerAI Workshop - Module 1 Types
 * AI-Coached Workshop for Geschäftsidee & Gründerprofil
 */

// =============================================================================
// PERSONALITY PROFILE (from Assessment)
// =============================================================================

export interface PersonalityProfile {
  innovativeness: number;          // 0-100: Innovationsfreude
  riskTaking: number;              // 0-100: Risikobereitschaft
  achievementOrientation: number;  // 0-100: Leistungsorientierung
  autonomy: number;                // 0-100: Autonomieorientierung
  proactiveness: number;           // 0-100: Proaktivität
  locusOfControl: number;          // 0-100: Kontrollüberzeugung
  selfEfficacy: number;            // 0-100: Selbstwirksamkeit
}

// =============================================================================
// GZ DOORS (7 Critical Questions Tracker)
// =============================================================================

export type GZDoorStatus = 'locked' | 'checking' | 'passed' | 'failed';

export interface GZDoor {
  id: string;
  baQuestion: number;              // BA GZ 04 Frage Nummer
  title: string;
  fullQuestion: string;            // Original Wortlaut
  status: GZDoorStatus;
  tips: string[];
  moduleId: number;
}

export const INITIAL_GZ_DOORS: GZDoor[] = [
  {
    id: 'fachlich',
    baQuestion: 8,
    title: 'Fachliche Eignung',
    fullQuestion: 'Sind die Voraussetzungen für das Existenzgründungsvorhaben in fachlicher und branchenspezifischer Hinsicht gegeben?',
    status: 'locked',
    tips: [
      'Ausbildung/Studium im Bereich nachweisen',
      'Berufserfahrung dokumentieren',
      'Als Quereinsteiger: Übertragbare Skills betonen'
    ],
    moduleId: 1
  },
  {
    id: 'kaufmaennisch',
    baQuestion: 9,
    title: 'Kaufmännische Eignung',
    fullQuestion: 'Sind die Voraussetzungen für das Existenzgründungsvorhaben in kaufmännischer und unternehmerischer Hinsicht gegeben?',
    status: 'locked',
    tips: [
      'Kaufmännische Grundkenntnisse nachweisen',
      'Existenzgründerseminar absolvieren',
      'Coaching durch AVGS beantragen'
    ],
    moduleId: 1
  },
  {
    id: 'tragfaehigkeit',
    baQuestion: 10,
    title: 'Tragfähigkeit',
    fullQuestion: 'Kann davon ausgegangen werden, dass aus dem Existenzgründungsvorhaben auf absehbare Zeit der Lebensunterhalt bestritten werden kann?',
    status: 'locked',
    tips: [
      'Realistische Umsatzplanung erstellen',
      'Marktpotenzial belegen',
      'Konkrete Kundenakquise-Strategie zeigen'
    ],
    moduleId: 5
  },
  {
    id: 'konkurrenz',
    baQuestion: 11,
    title: 'Konkurrenzfähigkeit',
    fullQuestion: 'Scheint das Existenzgründungsvorhaben – auch in absehbarer Zeit – konkurrenzfähig?',
    status: 'locked',
    tips: [
      'USP klar definieren',
      'Wettbewerbsanalyse durchführen',
      'Differenzierung zeigen'
    ],
    moduleId: 3
  },
  {
    id: 'marketing',
    baQuestion: 12,
    title: 'Vermarktung',
    fullQuestion: 'Sind die Voraussetzungen für die Vermarktung des Existenzgründungsvorhabens gegeben?',
    status: 'locked',
    tips: [
      'Marketing-Kanäle definieren',
      'Kundengewinnungsstrategie erklären',
      'Budget für Marketing einplanen'
    ],
    moduleId: 4
  },
  {
    id: 'kapitalbedarf',
    baQuestion: 14,
    title: 'Kapitalbedarf',
    fullQuestion: 'Ist der für das Existenzgründungsvorhaben notwendige Kapitalbedarf gedeckt?',
    status: 'locked',
    tips: [
      'Startkapital realistisch berechnen',
      'Finanzierungsquellen benennen',
      'Liquiditätsreserve einplanen'
    ],
    moduleId: 5
  },
  {
    id: 'lebensunterhalt',
    baQuestion: 15,
    title: 'Lebensunterhalt',
    fullQuestion: 'Ist während der Anlaufphase der Lebensunterhalt des Existenzgründers gesichert?',
    status: 'locked',
    tips: [
      'Private Fixkosten kennen',
      'GZ + Privatentnahme = Lebensunterhalt',
      'Puffer für schwache Monate'
    ],
    moduleId: 5
  }
];

// =============================================================================
// BA FORM CONTEXT (Transparency)
// =============================================================================

export interface BAFormContext {
  formular: 'BA_GZ_02' | 'BA_GZ_04';
  frageNummer: number;
  originalWortlaut: string;
  warumWichtig: string;
  wieWirHelfen: string;
}

// =============================================================================
// MODULE 1 QUESTIONS
// =============================================================================

export type Module1QuestionType = 'textarea' | 'multiple_choice';

export interface Module1Option {
  value: string;
  label: string;
  score?: number;
  icon?: string;
  example?: string;
  pros?: string[];
  cons?: string[];
  triggersFollowUp?: string;
}

export interface PersonalityAdaptation {
  highInnovativeness?: { emphasis: string };
  lowInnovativeness?: { emphasis: string };
  highRiskTaking?: { emphasis: string };
  lowRiskTaking?: { emphasis: string };
  lowSelfEfficacy?: { emphasis: string };
}

export interface CoachingConfig {
  maxIterations: number;
  requireSpecificity?: boolean;
  checkForGeneric?: boolean;
  frameworkToTeach?: string;
  coachingTone?: 'standard' | 'empowering' | 'challenging';
  suggestResources?: boolean;
  resources?: Array<{ name: string; url?: string; note: string }>;
}

export interface Module1Question {
  id: string;
  type: Module1QuestionType;
  phase: 'geschaeftsidee' | 'gruenderprofil' | 'geschaeftsmodell' | 'formales';

  // Question content
  question: string;
  subtext?: string;
  placeholder?: string;

  // Options for multiple choice
  options?: Module1Option[];

  // Validation
  minLength?: number;
  maxLength?: number;
  required: boolean;

  // Conditional display
  showIf?: (answers: Module1Answers) => boolean;

  // GZ Relevance
  gzRelevant?: boolean;
  gzDoorId?: string;
  baFormContext?: BAFormContext;

  // AI Coaching
  coachingConfig?: CoachingConfig;

  // Personality adaptation
  personalityAdaptation?: PersonalityAdaptation;

  // Framework teaching
  frameworkToTeach?: string;

  // Module impact
  impactsModules?: number[];
}

// =============================================================================
// MODULE 1 ANSWERS
// =============================================================================

export interface Module1Answers {
  q1_angebot?: string;
  q2_hintergrund?: 'A' | 'B' | 'C' | 'D' | 'E';
  q2b_quereinsteiger?: string;
  q3_kaufmaennisch?: 'A' | 'B' | 'C' | 'D' | 'E';
  q3b_wie_erworben?: string;
  q4_business_typ?: 'dienstleistung' | 'produkt' | 'software' | 'handel';
  q5_zielgruppe?: 'B2C' | 'B2B' | 'hybrid' | 'oeffentlich';
  q6_rechtsform?: 'einzelunternehmen' | 'gbr' | 'ug' | 'gmbh' | 'freiberuf';
}

// =============================================================================
// COACHING TYPES
// =============================================================================

export interface CoachingExchange {
  questionId: string;
  userAnswer: string;
  aiResponse: CoachingResponse;
  iteration: number;
  timestamp: Date;
}

export interface CoachingResponse {
  insight: string;          // Was gut ist
  challenge: string;        // Was fehlt/verbessert werden kann
  suggestion: string;       // Konkreter Denkanstoß
  example?: string;         // Real-world Beispiel
  encouragement: string;    // Ermutigung
  shouldIterate: boolean;   // Soll User nochmal nachdenken?
  improvedVersion?: string; // Vorschlag für bessere Formulierung
  gzDoorUpdate?: {
    doorId: string;
    newStatus: GZDoorStatus;
  };
}

export interface CoachingRequest {
  questionId: string;
  userAnswer: string;
  questionContext: Module1Question;
  personalityProfile: PersonalityProfile;
  previousAnswers: Module1Answers;
  iterationCount: number;
  sessionId: string;
}

// =============================================================================
// MODULE 1 STATE
// =============================================================================

export interface Module1State {
  // Phase
  currentPhase: 'intro' | 'questions' | 'coaching' | 'summary';
  currentQuestionIndex: number;

  // Answers
  answers: Module1Answers;

  // AI Coaching
  coachingHistory: CoachingExchange[];
  iterationCount: Record<string, number>;

  // Personality Context
  personalityProfile: PersonalityProfile;

  // GZ Context
  gzDoorsStatus: GZDoor[];

  // Generated Output
  generatedChapter: {
    kapitel_2_1_angebot?: string;
    kapitel_3_1_gruenderprofil?: string;
    kapitel_3_4_rechtsform?: string;
  };

  // Time tracking
  startTime: number | null;
  questionStartTimes: Record<string, number>;
}

// =============================================================================
// FRAMEWORK TYPES
// =============================================================================

export interface Framework {
  id: string;
  name: string;
  author?: string;
  summary: string;
  example?: string;
  howToApply?: string[];
  dimensions?: Array<{ name: string; question: string }>;
  categories?: Array<{ name: string; examples: string[] }>;
}

export const FRAMEWORKS: Record<string, Framework> = {
  'jobs_to_be_done': {
    id: 'jobs_to_be_done',
    name: 'Jobs-to-be-Done',
    author: 'Clayton Christensen',
    summary: 'Menschen kaufen keine Produkte – sie "heuern" sie an, um einen "Job" zu erledigen.',
    example: 'Niemand will einen 6mm Bohrer. Menschen wollen ein 6mm Loch in der Wand.',
    howToApply: [
      'Frage: Welchen "Job" erledigt dein Produkt für den Kunden?',
      'Frage: Was ist die Alternative, wenn dein Produkt nicht existiert?',
      'Frage: Welches Ergebnis will der Kunde wirklich?'
    ]
  },
  'gruender_business_fit': {
    id: 'gruender_business_fit',
    name: 'Gründer-Business Fit',
    author: 'GründerAI Framework',
    summary: 'Die beste Geschäftsidee ist wertlos, wenn sie nicht zu DIR passt.',
    dimensions: [
      { name: 'Fachliche Passung', question: 'Hast du die nötigen Skills?' },
      { name: 'Motivations-Passung', question: 'Brennst du wirklich dafür?' },
      { name: 'Lebensumstände-Passung', question: 'Passt es zu deiner Situation?' },
      { name: 'Risiko-Passung', question: 'Passt das Risiko zu deiner Persönlichkeit?' }
    ]
  },
  'transferable_skills': {
    id: 'transferable_skills',
    name: 'Übertragbare Fähigkeiten',
    summary: 'Als Quereinsteiger hast du Skills, die du vielleicht unterschätzt.',
    categories: [
      { name: 'Meta-Skills', examples: ['Problemlösung', 'Kommunikation', 'Organisation'] },
      { name: 'Branchen-Skills', examples: ['Kundenumgang', 'Projektmanagement', 'Verhandlung'] },
      { name: 'Technische Skills', examples: ['Software', 'Sprachen', 'Zertifikate'] }
    ]
  },
  'rechtsformwahl': {
    id: 'rechtsformwahl',
    name: 'Rechtsform-Entscheidung',
    summary: 'Die richtige Rechtsform hängt von Haftung, Kapital und Aufwand ab.',
    dimensions: [
      { name: 'Haftung', question: 'Wie viel Risiko willst du persönlich tragen?' },
      { name: 'Kapital', question: 'Wie viel Startkapital kannst du aufbringen?' },
      { name: 'Aufwand', question: 'Wie viel Bürokratie bist du bereit zu akzeptieren?' },
      { name: 'Außenwirkung', question: 'Wie wichtig ist ein "seriöser" Auftritt für deine Kunden?' }
    ]
  }
};

// =============================================================================
// DEFAULT PERSONALITY (if not from assessment)
// =============================================================================

export const DEFAULT_PERSONALITY_PROFILE: PersonalityProfile = {
  innovativeness: 60,
  riskTaking: 50,
  achievementOrientation: 70,
  autonomy: 65,
  proactiveness: 60,
  locusOfControl: 55,
  selfEfficacy: 60
};
