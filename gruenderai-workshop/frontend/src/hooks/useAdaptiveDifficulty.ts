import { useState, useCallback, useMemo } from 'react';
import type { ResponsePattern, AdaptiveSettings } from '@/types/workshop.types';

export const useAdaptiveDifficulty = (moduleNumber: number) => {
  const [responseHistory, setResponseHistory] = useState<ResponsePattern[]>([]);

  const analyzePattern = useCallback((): ResponsePattern => {
    if (responseHistory.length === 0) {
      return {
        avgResponseTime: 0,
        correctnessRate: 0.5,
        helpRequestCount: 0,
        skipCount: 0,
        editCount: 0
      };
    }

    const recent = responseHistory.slice(-5);
    return {
      avgResponseTime: recent.reduce((sum, r) => sum + r.avgResponseTime, 0) / recent.length,
      correctnessRate: recent.reduce((sum, r) => sum + r.correctnessRate, 0) / recent.length,
      helpRequestCount: recent.reduce((sum, r) => sum + r.helpRequestCount, 0),
      skipCount: recent.reduce((sum, r) => sum + r.skipCount, 0),
      editCount: recent.reduce((sum, r) => sum + r.editCount, 0)
    };
  }, [responseHistory]);

  const settings = useMemo((): AdaptiveSettings => {
    const pattern = analyzePattern();

    // Struggling user - needs more guidance
    if (pattern.correctnessRate < 0.4 || pattern.helpRequestCount > 3 || pattern.skipCount > 2) {
      return {
        mode: 'guided',
        helpLevel: 'high',
        showExamples: true,
        showTemplates: true,
        questionComplexity: 'simple',
        feedbackDetail: 'detailed',
        message: 'Ich breche das in kleinere Schritte auf...'
      };
    }

    // Advanced user - can handle more complexity
    if (pattern.correctnessRate > 0.8 && pattern.avgResponseTime < 30000 && pattern.helpRequestCount === 0) {
      return {
        mode: 'advanced',
        helpLevel: 'low',
        showExamples: false,
        showTemplates: false,
        questionComplexity: 'complex',
        feedbackDetail: 'minimal',
        message: 'Du meisterst das schnell! Bereit für mehr Tiefe?'
      };
    }

    // Standard user - balanced approach
    return {
      mode: 'standard',
      helpLevel: 'medium',
      showExamples: moduleNumber <= 2,
      showTemplates: moduleNumber === 1,
      questionComplexity: 'standard',
      feedbackDetail: 'standard'
    };
  }, [analyzePattern, moduleNumber]);

  const recordResponse = useCallback((response: Partial<ResponsePattern>) => {
    setResponseHistory(prev => [...prev, {
      avgResponseTime: response.avgResponseTime || 0,
      correctnessRate: response.correctnessRate || 0.5,
      helpRequestCount: response.helpRequestCount || 0,
      skipCount: response.skipCount || 0,
      editCount: response.editCount || 0
    }]);
  }, []);

  const resetHistory = useCallback(() => {
    setResponseHistory([]);
  }, []);

  return {
    settings,
    recordResponse,
    resetHistory,
    pattern: analyzePattern(),
    historyLength: responseHistory.length
  };
};

export default useAdaptiveDifficulty;
