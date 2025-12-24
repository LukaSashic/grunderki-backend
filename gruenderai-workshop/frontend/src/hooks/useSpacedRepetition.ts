import { useMemo, useCallback } from 'react';
import { CONCEPT_PROGRESSIONS } from '@/data/conceptProgressions';

interface ConceptContext {
  concept: typeof CONCEPT_PROGRESSIONS[0];
  previousAnswers: {
    module: number;
    answer: string;
    stage: string;
  }[];
  currentStage: string | undefined;
}

export const useSpacedRepetition = (
  moduleNumber: number,
  previousAnswers: Record<string, string>
) => {
  /**
   * Get all concepts that are relevant to the current module
   */
  const relevantConcepts = useMemo(() => {
    return CONCEPT_PROGRESSIONS.filter(concept =>
      concept.modules.some(m => m.moduleNumber === moduleNumber)
    );
  }, [moduleNumber]);

  /**
   * Get context for a specific concept including previous answers
   */
  const getConceptContext = useCallback((conceptId: string): ConceptContext | null => {
    const concept = CONCEPT_PROGRESSIONS.find(c => c.conceptId === conceptId);
    if (!concept) return null;

    // Get all modules before current one
    const previousModules = concept.modules.filter(m => m.moduleNumber < moduleNumber);

    // Map to previous answers
    const previousAnswersForConcept = previousModules
      .map(m => ({
        module: m.moduleNumber,
        answer: previousAnswers[m.questionId] || '',
        stage: m.stage
      }))
      .filter(a => a.answer);

    return {
      concept,
      previousAnswers: previousAnswersForConcept,
      currentStage: concept.modules.find(m => m.moduleNumber === moduleNumber)?.stage
    };
  }, [moduleNumber, previousAnswers]);

  /**
   * Get a recap message for a concept based on previous answers
   */
  const getRecapMessage = useCallback((conceptId: string): string | null => {
    const context = getConceptContext(conceptId);
    if (!context || context.previousAnswers.length === 0) return null;

    const lastAnswer = context.previousAnswers[context.previousAnswers.length - 1];
    const truncatedAnswer = lastAnswer.answer.length > 100
      ? `${lastAnswer.answer.substring(0, 100)}...`
      : lastAnswer.answer;

    return `In Modul ${lastAnswer.module} hast du definiert: "${truncatedAnswer}"`;
  }, [getConceptContext]);

  /**
   * Get the stage progression for a concept
   */
  const getStageProgression = useCallback((conceptId: string): string[] => {
    const concept = CONCEPT_PROGRESSIONS.find(c => c.conceptId === conceptId);
    if (!concept) return [];

    return concept.modules
      .sort((a, b) => a.moduleNumber - b.moduleNumber)
      .map(m => m.stage);
  }, []);

  /**
   * Check if a concept should show a recap
   */
  const shouldShowRecap = useCallback((conceptId: string): boolean => {
    const context = getConceptContext(conceptId);
    if (!context) return false;

    // Show recap if there are previous answers and we're in reinforce/apply/validate stage
    return (
      context.previousAnswers.length > 0 &&
      ['reinforce', 'apply', 'validate'].includes(context.currentStage || '')
    );
  }, [getConceptContext]);

  /**
   * Get all concepts that need recap in current module
   */
  const conceptsNeedingRecap = useMemo(() => {
    return relevantConcepts
      .filter(c => shouldShowRecap(c.conceptId))
      .map(c => ({
        ...c,
        recapMessage: getRecapMessage(c.conceptId)
      }));
  }, [relevantConcepts, shouldShowRecap, getRecapMessage]);

  return {
    relevantConcepts,
    getConceptContext,
    getRecapMessage,
    getStageProgression,
    shouldShowRecap,
    conceptsNeedingRecap
  };
};

export default useSpacedRepetition;
