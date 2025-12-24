/**
 * GründerAI Workshop - TypeScript Types
 */

// =============================================================================
// MODULE TYPES
// =============================================================================

export type ModuleNumber = 1 | 2 | 3 | 4 | 5 | 6;

export interface Module {
  id: ModuleNumber;
  title: string;
  titleDe: string;
  duration: number; // minutes
  questionCount: number;
  outputChapters: string[];
  bagz04Questions: number[];
}

export const MODULES: Module[] = [
  {
    id: 1,
    title: "Business Idea & Founder Profile",
    titleDe: "Geschäftsidee & Gründerprofil",
    duration: 25,
    questionCount: 6,
    outputChapters: ["2.1", "3.1", "3.2", "3.3", "3.4", "3.5"],
    bagz04Questions: [7, 8, 9]
  },
  {
    id: 2,
    title: "Target Audience & Personas",
    titleDe: "Zielgruppe & Personas",
    duration: 25,
    questionCount: 6,
    outputChapters: ["2.2", "2.3"],
    bagz04Questions: [10]
  },
  {
    id: 3,
    title: "Market & Competition",
    titleDe: "Markt & Wettbewerb",
    duration: 25,
    questionCount: 6,
    outputChapters: ["3.6", "4.1", "4.2"],
    bagz04Questions: [11]
  },
  {
    id: 4,
    title: "Marketing & Sales",
    titleDe: "Marketing & Vertrieb",
    duration: 25,
    questionCount: 6,
    outputChapters: ["5.1", "5.2", "5.3"],
    bagz04Questions: [12]
  },
  {
    id: 5,
    title: "Financial Planning",
    titleDe: "Finanzplanung",
    duration: 35,
    questionCount: 7,
    outputChapters: ["6.1", "6.2", "6.3", "6.4"],
    bagz04Questions: [13, 14, 15]
  },
  {
    id: 6,
    title: "Strategy & Completion",
    titleDe: "Strategie & Abschluss",
    duration: 25,
    questionCount: 6,
    outputChapters: ["7", "8", "9", "1"],
    bagz04Questions: []
  }
];

// =============================================================================
// QUESTION TYPES
// =============================================================================

export type QuestionType = 
  | "text"
  | "textarea"
  | "multiple_choice"
  | "multiple_select"
  | "number"
  | "currency"
  | "dropdown";

export interface QuestionOption {
  id: string;
  label: string;
  description?: string;
}

export interface Question {
  id: string;
  questionNumber: number;
  question: string;
  type: QuestionType;
  options?: QuestionOption[];
  maxLength?: number;
  required: boolean;
  helpText?: string;
  gzHint?: string;
  conditionalOn?: {
    questionId: string;
    values: string[];
  };
}

export interface QuestionAnswer {
  questionId: string;
  value: string | string[] | number;
  timestamp: Date;
}

// =============================================================================
// SESSION TYPES
// =============================================================================

export type SessionStatus = 
  | "assessment"
  | "assessment_complete"
  | "payment_pending"
  | "workshop_active"
  | "workshop_complete";

export interface WorkshopSession {
  id: string;
  status: SessionStatus;
  currentModule: ModuleNumber;
  currentQuestion: number;
  answers: Record<string, QuestionAnswer>;
  outputs: Record<ModuleNumber, ModuleOutput>;
  assessmentScore?: number;
  paymentId?: string;
  createdAt: Date;
  updatedAt: Date;
}

// =============================================================================
// OUTPUT TYPES
// =============================================================================

export interface ValidationItem {
  item: string;
  status: "ok" | "warning" | "missing";
  bagz04Question?: number;
}

export interface ModuleOutput {
  moduleId: ModuleNumber;
  chapters: Record<string, string>;
  qualityScore: number;
  validationChecklist: ValidationItem[];
  improvementSuggestions: string[];
  generatedAt: Date;
}

export interface FinalOutput {
  businessPlanPdf: string; // URL or base64
  businessPlanDocx: string;
  financialPlanXlsx: string;
  executiveSummary: string;
  totalQualityScore: number;
  gzReadinessScore: number;
}

// =============================================================================
// ASSESSMENT TYPES
// =============================================================================

export interface AssessmentResult {
  score: number; // 0-100
  strengths: string[];
  gaps: string[];
  riskLevel: "low" | "medium" | "high";
  recommendation: string;
}

// =============================================================================
// PAYMENT TYPES
// =============================================================================

export interface PaymentIntent {
  id: string;
  amount: number;
  currency: "EUR";
  status: "pending" | "completed" | "failed";
  paypalOrderId?: string;
}

// =============================================================================
// API TYPES
// =============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface StartAssessmentResponse {
  sessionId: string;
  questions: Question[];
}

export interface SubmitAssessmentResponse {
  result: AssessmentResult;
  sessionId: string;
}

export interface StartWorkshopResponse {
  sessionId: string;
  currentModule: ModuleNumber;
  questions: Question[];
}

export interface SubmitModuleResponse {
  output: ModuleOutput;
  nextModule?: ModuleNumber;
  isComplete: boolean;
}

export interface CompleteWorkshopResponse {
  finalOutput: FinalOutput;
  downloadLinks: {
    pdf: string;
    docx: string;
    xlsx: string;
  };
}

// =============================================================================
// PREMIUM UI TYPES
// =============================================================================

// Disclosure Levels for Progressive Disclosure
export interface DisclosureLevel {
  level: 1 | 2 | 3;
  visibleBy: 'default' | 'hover' | 'click';
}

export interface LegalCitation {
  reference: string;      // "Paragraph 93 SGB III"
  fullText: string;
  sourceUrl: string;
}

export interface QuestionWithDisclosure {
  id: string;
  moduleNumber: number;
  order: number;
  totalInModule: number;

  // Level 1: Sofort sichtbar
  question: string;
  options: AnswerOption[];

  // Level 2: Expandable
  whyThisQuestion: string;
  businessRelevance: string;

  // Level 3: Deep Dive
  legalReference: LegalCitation;
  scientificBackground?: string;
}

export interface AnswerOption {
  id: string;
  text: string;
  score?: number;
}

// Adaptive Difficulty
export type DifficultyMode = 'guided' | 'standard' | 'advanced';
export type HelpLevel = 'high' | 'medium' | 'low';

export interface ResponsePattern {
  avgResponseTime: number;
  correctnessRate: number;
  helpRequestCount: number;
  skipCount: number;
  editCount: number;
}

export interface AdaptiveSettings {
  mode: DifficultyMode;
  helpLevel: HelpLevel;
  showExamples: boolean;
  showTemplates: boolean;
  questionComplexity: 'simple' | 'standard' | 'complex';
  feedbackDetail: 'minimal' | 'standard' | 'detailed';
  message?: string;
}

// Scaffolding
export interface ScaffoldingConfig {
  hints: 'always_visible' | 'on_hover' | 'on_request' | 'hidden';
  exampleCount: number;
  showTemplates: boolean;
  guidanceLevel: 'full' | 'partial' | 'minimal' | 'none';
  showStepByStep: boolean;
  autoSuggestions: boolean;
}

// Feedback
export interface FeedbackItem {
  type: 'strength' | 'improvement';
  message: string;
}

export interface ModuleFeedback {
  overallScore: number;
  completeness: number;
  strengths: string[];
  areasForImprovement: string[];
  ihkExpectations: string[];
  nextModulePreview: string;
}

// Gaps (Loss Aversion)
export interface Gap {
  id: string;
  title: string;
  description: string;
  rejectionImpact: string;
  severity: 'critical' | 'high' | 'medium';
  coveredInModule: number;
}

// Investment (Endowment)
export interface Investment {
  timeSpent: number;
  questionsAnswered: number;
  insightsUnlocked: number;
  strengthsIdentified: number;
  gzReadinessScore: number;
  personalityProfile: boolean;
}

// Progress
export interface ModuleInfo {
  number: number;
  name: string;
  progress: number;
  status: 'complete' | 'current' | 'locked';
  qualityScore?: number;
}

export interface ChapterInfo {
  id: string;
  name: string;
  status: 'complete' | 'current' | 'upcoming';
}

// User Context (Story)
export interface UserContext {
  name: string;
  profession: string;
  city: string;
  businessIdea: string;
  targetCustomer: string;
}

// Spaced Repetition
export interface ConceptProgression {
  conceptId: string;
  conceptName: string;
  modules: {
    moduleNumber: number;
    stage: 'introduce' | 'reinforce' | 'apply' | 'validate';
    questionId: string;
    depth: 'surface' | 'understanding' | 'application';
  }[];
}
