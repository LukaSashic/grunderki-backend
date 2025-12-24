import { useMemo, useCallback } from 'react';
import type { ScaffoldingConfig } from '@/types/workshop.types';

/**
 * Scaffolding decreases as user progresses through modules
 * Module 1-2: Full support (examples, templates, step-by-step)
 * Module 3-4: Partial support (hints on hover)
 * Module 5-6: Minimal support (hints on request only)
 */
const SCAFFOLDING_BY_MODULE: Record<number, ScaffoldingConfig> = {
  1: {
    hints: 'always_visible',
    exampleCount: 3,
    showTemplates: true,
    guidanceLevel: 'full',
    showStepByStep: true,
    autoSuggestions: true
  },
  2: {
    hints: 'always_visible',
    exampleCount: 2,
    showTemplates: true,
    guidanceLevel: 'full',
    showStepByStep: true,
    autoSuggestions: true
  },
  3: {
    hints: 'on_hover',
    exampleCount: 1,
    showTemplates: false,
    guidanceLevel: 'partial',
    showStepByStep: false,
    autoSuggestions: true
  },
  4: {
    hints: 'on_hover',
    exampleCount: 1,
    showTemplates: false,
    guidanceLevel: 'partial',
    showStepByStep: false,
    autoSuggestions: false
  },
  5: {
    hints: 'on_request',
    exampleCount: 0,
    showTemplates: false,
    guidanceLevel: 'minimal',
    showStepByStep: false,
    autoSuggestions: false
  },
  6: {
    hints: 'on_request',
    exampleCount: 0,
    showTemplates: false,
    guidanceLevel: 'none',
    showStepByStep: false,
    autoSuggestions: false
  }
};

export const useScaffolding = (moduleNumber: number) => {
  const config = useMemo(() => {
    return SCAFFOLDING_BY_MODULE[moduleNumber] || SCAFFOLDING_BY_MODULE[6];
  }, [moduleNumber]);

  const shouldShowHints = useCallback((trigger: 'always' | 'hover' | 'request') => {
    if (config.hints === 'always_visible') return true;
    if (config.hints === 'on_hover' && (trigger === 'hover' || trigger === 'always')) return true;
    if (config.hints === 'on_request' && trigger === 'request') return true;
    return false;
  }, [config.hints]);

  const getGuidanceMessage = useCallback(() => {
    switch (config.guidanceLevel) {
      case 'full':
        return 'Wir führen dich Schritt für Schritt durch diese Frage.';
      case 'partial':
        return 'Nutze die Hinweise bei Bedarf.';
      case 'minimal':
        return 'Du hast das drauf! Klicke auf "Hilfe" wenn nötig.';
      case 'none':
        return '';
      default:
        return '';
    }
  }, [config.guidanceLevel]);

  const getProgressMessage = useCallback(() => {
    switch (moduleNumber) {
      case 1:
        return 'Keine Sorge - wir starten gemeinsam!';
      case 2:
        return 'Super Start! Jetzt zu deinen Kunden.';
      case 3:
        return 'Du machst Fortschritte! Weniger Hilfe nötig.';
      case 4:
        return 'Toll! Du wirst immer selbstständiger.';
      case 5:
        return 'Fast geschafft! Die Zahlen sind wichtig.';
      case 6:
        return 'Letzter Schliff! Du kannst das!';
      default:
        return '';
    }
  }, [moduleNumber]);

  return {
    config,
    shouldShowHints,
    getGuidanceMessage,
    getProgressMessage,
    scaffoldingLevel: 7 - moduleNumber // 6 for module 1, 1 for module 6
  };
};

export default useScaffolding;
