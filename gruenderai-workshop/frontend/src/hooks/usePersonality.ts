/**
 * GründerAI Workshop - usePersonality Hook
 * Manages personality profile from assessment for coaching personalization
 */

import { useState, useCallback, useEffect, useMemo } from 'react';
import type { PersonalityProfile } from '@/types/module1.types';
import { DEFAULT_PERSONALITY_PROFILE } from '@/types/module1.types';

interface UsePersonalityReturn {
  personalityProfile: PersonalityProfile;
  setPersonalityProfile: (profile: PersonalityProfile) => void;
  updateDimension: (dimension: keyof PersonalityProfile, value: number) => void;
  getCoachingTone: () => 'standard' | 'empowering' | 'challenging';
  needsExtraEncouragement: () => boolean;
  isRiskAverse: () => boolean;
  isHighAchiever: () => boolean;
  isInnovator: () => boolean;
  getPersonalityInsights: () => PersonalityInsight[];
  resetProfile: () => void;
}

interface PersonalityInsight {
  dimension: string;
  score: number;
  label: string;
  description: string;
  coachingImplication: string;
}

const STORAGE_KEY = 'gruenderai-personality-profile';

export const usePersonality = (): UsePersonalityReturn => {
  // Load initial state from localStorage or assessment
  const loadInitialState = (): PersonalityProfile => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        return JSON.parse(saved);
      }

      // Try to get from workshop store (from assessment)
      const workshopData = localStorage.getItem('gruenderai-workshop');
      if (workshopData) {
        const parsed = JSON.parse(workshopData);
        if (parsed.state?.personalityProfile) {
          return parsed.state.personalityProfile;
        }
      }
    } catch (e) {
      console.error('Failed to load personality profile:', e);
    }
    return DEFAULT_PERSONALITY_PROFILE;
  };

  const [personalityProfile, setPersonalityProfileState] = useState<PersonalityProfile>(loadInitialState);

  // Persist to localStorage on change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(personalityProfile));
  }, [personalityProfile]);

  // Set entire profile
  const setPersonalityProfile = useCallback((profile: PersonalityProfile) => {
    setPersonalityProfileState(profile);
  }, []);

  // Update a single dimension
  const updateDimension = useCallback((
    dimension: keyof PersonalityProfile,
    value: number
  ) => {
    setPersonalityProfileState(prev => ({
      ...prev,
      [dimension]: Math.max(0, Math.min(100, value))
    }));
  }, []);

  // Determine coaching tone based on profile
  const getCoachingTone = useCallback((): 'standard' | 'empowering' | 'challenging' => {
    if (personalityProfile.selfEfficacy < 50) {
      return 'empowering';
    }
    if (personalityProfile.achievementOrientation > 70) {
      return 'challenging';
    }
    return 'standard';
  }, [personalityProfile]);

  // Check if user needs extra encouragement
  const needsExtraEncouragement = useCallback(() => {
    return personalityProfile.selfEfficacy < 50;
  }, [personalityProfile]);

  // Check if user is risk averse
  const isRiskAverse = useCallback(() => {
    return personalityProfile.riskTaking < 40;
  }, [personalityProfile]);

  // Check if user is high achiever
  const isHighAchiever = useCallback(() => {
    return personalityProfile.achievementOrientation > 70;
  }, [personalityProfile]);

  // Check if user is innovative
  const isInnovator = useCallback(() => {
    return personalityProfile.innovativeness > 70;
  }, [personalityProfile]);

  // Get detailed personality insights
  const getPersonalityInsights = useCallback((): PersonalityInsight[] => {
    return [
      {
        dimension: 'Innovationsfreude',
        score: personalityProfile.innovativeness,
        label: personalityProfile.innovativeness > 70 ? 'Hoch' :
               personalityProfile.innovativeness > 40 ? 'Mittel' : 'Niedrig',
        description: personalityProfile.innovativeness > 70
          ? 'Du bist offen für neue Ideen und Ansätze.'
          : 'Du bevorzugst bewährte Methoden und Lösungen.',
        coachingImplication: personalityProfile.innovativeness > 70
          ? 'Wir betonen das Innovative an deinem Angebot.'
          : 'Wir zeigen, wie du bewährte Konzepte adaptierst.'
      },
      {
        dimension: 'Risikobereitschaft',
        score: personalityProfile.riskTaking,
        label: personalityProfile.riskTaking > 70 ? 'Hoch' :
               personalityProfile.riskTaking > 40 ? 'Mittel' : 'Niedrig',
        description: personalityProfile.riskTaking > 70
          ? 'Du gehst gerne kalkulierte Risiken ein.'
          : 'Du bevorzugst sichere und planbare Wege.',
        coachingImplication: personalityProfile.riskTaking < 40
          ? 'Wir betonen Sicherheitsnetze und schrittweises Vorgehen.'
          : 'Wir unterstützen dein mutiges Handeln.'
      },
      {
        dimension: 'Leistungsorientierung',
        score: personalityProfile.achievementOrientation,
        label: personalityProfile.achievementOrientation > 70 ? 'Hoch' :
               personalityProfile.achievementOrientation > 40 ? 'Mittel' : 'Niedrig',
        description: personalityProfile.achievementOrientation > 70
          ? 'Du setzt dir hohe Ziele und arbeitest hart dafür.'
          : 'Du legst Wert auf Work-Life-Balance.',
        coachingImplication: personalityProfile.achievementOrientation > 70
          ? 'Wir fordern dich heraus, dein Bestes zu geben.'
          : 'Wir achten auf realistische Ziele und Pausen.'
      },
      {
        dimension: 'Autonomie',
        score: personalityProfile.autonomy,
        label: personalityProfile.autonomy > 70 ? 'Hoch' :
               personalityProfile.autonomy > 40 ? 'Mittel' : 'Niedrig',
        description: personalityProfile.autonomy > 70
          ? 'Du möchtest unabhängig Entscheidungen treffen.'
          : 'Du schätzt Struktur und klare Vorgaben.',
        coachingImplication: personalityProfile.autonomy > 70
          ? 'Wir geben dir Raum für eigene Entscheidungen.'
          : 'Wir liefern klare Frameworks und Anleitungen.'
      },
      {
        dimension: 'Selbstwirksamkeit',
        score: personalityProfile.selfEfficacy,
        label: personalityProfile.selfEfficacy > 70 ? 'Hoch' :
               personalityProfile.selfEfficacy > 40 ? 'Mittel' : 'Niedrig',
        description: personalityProfile.selfEfficacy > 70
          ? 'Du glaubst an deine Fähigkeit, Ziele zu erreichen.'
          : 'Du zweifelst manchmal an deinen Fähigkeiten.',
        coachingImplication: personalityProfile.selfEfficacy < 50
          ? '⚠️ Wir geben dir extra Ermutigung und betonen deine Stärken.'
          : 'Wir unterstützen dein Selbstvertrauen.'
      }
    ];
  }, [personalityProfile]);

  // Reset to default
  const resetProfile = useCallback(() => {
    setPersonalityProfileState(DEFAULT_PERSONALITY_PROFILE);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return {
    personalityProfile,
    setPersonalityProfile,
    updateDimension,
    getCoachingTone,
    needsExtraEncouragement,
    isRiskAverse,
    isHighAchiever,
    isInnovator,
    getPersonalityInsights,
    resetProfile
  };
};

// =============================================================================
// PERSONALITY ADAPTERS FOR PROMPTS
// =============================================================================

export const getPersonalityAdaptedPrompt = (
  basePrompt: string,
  profile: PersonalityProfile
): string => {
  let adaptedPrompt = basePrompt;

  // Add encouragement for low self-efficacy
  if (profile.selfEfficacy < 50) {
    adaptedPrompt += '\n\n[WICHTIG: Diese Person braucht extra Ermutigung. Betone Stärken, gib positives Feedback, und zeige dass Herausforderungen lösbar sind.]';
  }

  // Add safety focus for risk-averse
  if (profile.riskTaking < 40) {
    adaptedPrompt += '\n\n[HINWEIS: Diese Person ist sicherheitsorientiert. Betone risikominimierende Strategien, Fallback-Optionen und schrittweises Vorgehen.]';
  }

  // Add challenge for high achievers
  if (profile.achievementOrientation > 70) {
    adaptedPrompt += '\n\n[HINWEIS: Diese Person ist leistungsorientiert. Du kannst sie herausfordern und hohe Standards setzen.]';
  }

  // Add innovation focus for innovators
  if (profile.innovativeness > 70) {
    adaptedPrompt += '\n\n[HINWEIS: Diese Person ist innovationsfreudig. Betone Differenzierung, Neuheit und kreative Ansätze.]';
  }

  return adaptedPrompt;
};

export default usePersonality;
