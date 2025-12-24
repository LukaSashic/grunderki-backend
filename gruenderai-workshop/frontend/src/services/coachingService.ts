/**
 * GründerAI Workshop - Coaching Service
 * Frontend service for AI coaching interactions
 */

import axios from 'axios';
import type {
  CoachingRequest,
  CoachingResponse,
  PersonalityProfile,
  Module1Question,
  Module1Answers
} from '@/types/module1.types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds for AI responses
});

// =============================================================================
// COACHING API
// =============================================================================

export const coachingService = {
  /**
   * Get AI coaching response for a user's answer
   */
  getCoachingResponse: async (request: CoachingRequest): Promise<CoachingResponse> => {
    try {
      const response = await api.post('/api/workshop/coaching', {
        session_id: request.sessionId,
        question_id: request.questionId,
        user_answer: request.userAnswer,
        question_context: {
          question: request.questionContext.question,
          phase: request.questionContext.phase,
          ba_form_context: request.questionContext.baFormContext,
          gz_relevant: request.questionContext.gzRelevant,
          gz_door_id: request.questionContext.gzDoorId,
          framework_to_teach: request.questionContext.frameworkToTeach,
          coaching_config: request.questionContext.coachingConfig,
          personality_adaptation: request.questionContext.personalityAdaptation
        },
        personality_profile: request.personalityProfile,
        previous_answers: request.previousAnswers,
        iteration_count: request.iterationCount
      });

      return response.data;
    } catch (error) {
      console.error('Coaching API error:', error);
      // Return a fallback response if API fails
      return getFallbackCoachingResponse(request);
    }
  },

  /**
   * Get coaching response with retry logic
   */
  getCoachingResponseWithRetry: async (
    request: CoachingRequest,
    maxRetries: number = 2
  ): Promise<CoachingResponse> => {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        return await coachingService.getCoachingResponse(request);
      } catch (error) {
        lastError = error as Error;
        console.warn(`Coaching attempt ${attempt + 1} failed, retrying...`);
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)));
      }
    }

    console.error('All coaching attempts failed:', lastError);
    return getFallbackCoachingResponse(request);
  }
};

// =============================================================================
// FALLBACK RESPONSES (when API is unavailable)
// =============================================================================

function getFallbackCoachingResponse(request: CoachingRequest): CoachingResponse {
  const { questionId, userAnswer, iterationCount } = request;

  // Check answer length
  const isShort = userAnswer.length < 100;
  const isGeneric = containsGenericPhrases(userAnswer);

  if (isShort) {
    return {
      insight: 'Danke für deine Antwort!',
      challenge: 'Deine Antwort ist noch etwas kurz. Die IHK möchte konkrete Details sehen.',
      suggestion: 'Kannst du mehr ins Detail gehen? Was genau macht dein Angebot einzigartig?',
      encouragement: 'Du bist auf dem richtigen Weg!',
      shouldIterate: iterationCount < 2
    };
  }

  if (isGeneric) {
    return {
      insight: 'Du hast einen guten Anfang gemacht.',
      challenge: 'Einige Formulierungen könnten spezifischer sein.',
      suggestion: 'Versuche, allgemeine Aussagen wie "qualitativ hochwertig" durch konkrete Beispiele zu ersetzen.',
      encouragement: 'Mit etwas mehr Spezifität wird deine Antwort die IHK überzeugen!',
      shouldIterate: iterationCount < 2
    };
  }

  // Good answer
  return {
    insight: 'Sehr gut! Deine Antwort ist detailliert und zeigt, dass du dein Vorhaben gut durchdacht hast.',
    challenge: '',
    suggestion: '',
    encouragement: 'Weiter so! Du bist auf dem besten Weg zu einem überzeugenden Businessplan.',
    shouldIterate: false
  };
}

function containsGenericPhrases(text: string): boolean {
  const genericPhrases = [
    'qualitativ hochwertig',
    'beste qualität',
    'kundenorientiert',
    'professionell',
    'zuverlässig',
    'erfahren',
    'kompetent',
    'individuelle beratung',
    'maßgeschneidert',
    'ganzheitlich'
  ];

  const lowerText = text.toLowerCase();
  return genericPhrases.some(phrase => lowerText.includes(phrase));
}

// =============================================================================
// PERSONALITY-BASED PROMPT HELPERS
// =============================================================================

export function getPersonalityBasedEmphasis(
  profile: PersonalityProfile,
  question: Module1Question
): string | null {
  const { personalityAdaptation } = question;
  if (!personalityAdaptation) return null;

  // Check for high innovativeness
  if (profile.innovativeness > 70 && personalityAdaptation.highInnovativeness) {
    return personalityAdaptation.highInnovativeness.emphasis;
  }

  // Check for low risk taking
  if (profile.riskTaking < 40 && personalityAdaptation.lowRiskTaking) {
    return personalityAdaptation.lowRiskTaking.emphasis;
  }

  // Check for low self-efficacy (needs extra encouragement)
  if (profile.selfEfficacy < 50 && personalityAdaptation.lowSelfEfficacy) {
    return personalityAdaptation.lowSelfEfficacy.emphasis;
  }

  return null;
}

export function getCoachingToneForProfile(profile: PersonalityProfile): string {
  // Low self-efficacy needs extra encouragement
  if (profile.selfEfficacy < 50) {
    return 'empowering';
  }

  // High achievement orientation can handle challenges
  if (profile.achievementOrientation > 70) {
    return 'challenging';
  }

  return 'standard';
}

// =============================================================================
// ANSWER VALIDATION HELPERS
// =============================================================================

export interface AnswerValidation {
  isValid: boolean;
  score: number;
  issues: string[];
  suggestions: string[];
}

export function validateAnswer(
  answer: string,
  question: Module1Question
): AnswerValidation {
  const issues: string[] = [];
  const suggestions: string[] = [];
  let score = 100;

  // Check minimum length
  if (question.minLength && answer.length < question.minLength) {
    issues.push(`Mindestens ${question.minLength} Zeichen erforderlich`);
    suggestions.push('Füge mehr Details hinzu');
    score -= 30;
  }

  // Check maximum length
  if (question.maxLength && answer.length > question.maxLength) {
    issues.push(`Maximal ${question.maxLength} Zeichen erlaubt`);
    suggestions.push('Kürze deine Antwort');
    score -= 10;
  }

  // Check for generic phrases
  if (containsGenericPhrases(answer)) {
    issues.push('Enthält zu allgemeine Formulierungen');
    suggestions.push('Ersetze allgemeine Aussagen durch konkrete Beispiele');
    score -= 20;
  }

  // Check for specificity (should contain numbers or concrete examples)
  if (!containsSpecificDetails(answer) && question.coachingConfig?.requireSpecificity) {
    issues.push('Könnte spezifischer sein');
    suggestions.push('Füge konkrete Zahlen, Beispiele oder Details hinzu');
    score -= 15;
  }

  return {
    isValid: issues.length === 0,
    score: Math.max(0, score),
    issues,
    suggestions
  };
}

function containsSpecificDetails(text: string): boolean {
  // Check for numbers
  if (/\d+/.test(text)) return true;

  // Check for specific examples (indicated by certain patterns)
  const specificPatterns = [
    /zum beispiel/i,
    /beispielsweise/i,
    /konkret/i,
    /genauer gesagt/i,
    /€|euro/i,
    /prozent|%/i,
    /stunden?|tage?|wochen?|monate?|jahre?/i
  ];

  return specificPatterns.some(pattern => pattern.test(text));
}

// =============================================================================
// GZ DOOR STATUS HELPERS
// =============================================================================

export function evaluateGZDoorStatus(
  doorId: string,
  answers: Module1Answers,
  coachingHistory: Array<{ questionId: string; aiResponse: CoachingResponse }>
): 'locked' | 'checking' | 'passed' | 'failed' {
  const relevantQuestions = getQuestionsForDoor(doorId);

  // Check if any relevant question has been answered
  const hasAnswers = relevantQuestions.some(qId => {
    const answer = answers[qId as keyof Module1Answers];
    return answer !== undefined && answer !== '';
  });

  if (!hasAnswers) return 'locked';

  // Check coaching history for this door
  const relevantCoaching = coachingHistory.filter(
    c => relevantQuestions.includes(c.questionId)
  );

  // If still iterating, status is 'checking'
  const hasUnresolvedIteration = relevantCoaching.some(
    c => c.aiResponse.shouldIterate
  );

  if (hasUnresolvedIteration) return 'checking';

  // Check answer quality based on question type
  const score = calculateDoorScore(doorId, answers);

  if (score >= 70) return 'passed';
  if (score >= 40) return 'checking';
  return 'failed';
}

function getQuestionsForDoor(doorId: string): string[] {
  const doorQuestions: Record<string, string[]> = {
    'fachlich': ['q2_hintergrund', 'q2b_quereinsteiger'],
    'kaufmaennisch': ['q3_kaufmaennisch', 'q3b_wie_erworben'],
    'konkurrenz': ['q1_angebot']
  };

  return doorQuestions[doorId] || [];
}

function calculateDoorScore(doorId: string, answers: Module1Answers): number {
  switch (doorId) {
    case 'fachlich': {
      const baseScores: Record<string, number> = {
        'A': 100, 'B': 90, 'C': 70, 'D': 50, 'E': 20
      };
      let score = baseScores[answers.q2_hintergrund || ''] || 0;

      // Bonus for Quereinsteiger explanation
      if (answers.q2b_quereinsteiger && answers.q2b_quereinsteiger.length > 150) {
        score = Math.min(score + 25, 100);
      }
      return score;
    }

    case 'kaufmaennisch': {
      const baseScores: Record<string, number> = {
        'A': 100, 'B': 85, 'C': 60, 'D': 40, 'E': 20
      };
      let score = baseScores[answers.q3_kaufmaennisch || ''] || 0;

      // Bonus for learning plan
      if (answers.q3b_wie_erworben && answers.q3b_wie_erworben.length > 100) {
        score = Math.min(score + 25, 100);
      }
      return score;
    }

    case 'konkurrenz': {
      if (!answers.q1_angebot) return 0;
      // Score based on length and specificity
      let score = 50;
      if (answers.q1_angebot.length > 200) score += 25;
      if (containsSpecificDetails(answers.q1_angebot)) score += 25;
      return Math.min(score, 100);
    }

    default:
      return 0;
  }
}

export default coachingService;
