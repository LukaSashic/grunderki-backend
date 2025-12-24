import type { ConceptProgression } from '@/types/workshop.types';

/**
 * Concept Progressions for Spaced Repetition
 *
 * Key concepts are introduced early, then reinforced and applied in later modules.
 * This ensures better retention and deeper understanding.
 */
export const CONCEPT_PROGRESSIONS: ConceptProgression[] = [
  {
    conceptId: 'target_customer',
    conceptName: 'Zielgruppe',
    modules: [
      {
        moduleNumber: 1,
        stage: 'introduce',
        questionId: 'q1_target',
        depth: 'surface'
      },
      {
        moduleNumber: 2,
        stage: 'reinforce',
        questionId: 'q2_persona',
        depth: 'understanding'
      },
      {
        moduleNumber: 3,
        stage: 'apply',
        questionId: 'q3_target_vs_comp',
        depth: 'understanding'
      },
      {
        moduleNumber: 4,
        stage: 'apply',
        questionId: 'q4_reach_target',
        depth: 'application'
      },
      {
        moduleNumber: 6,
        stage: 'validate',
        questionId: 'q6_cac',
        depth: 'application'
      }
    ]
  },
  {
    conceptId: 'unique_value',
    conceptName: 'Alleinstellungsmerkmal (USP)',
    modules: [
      {
        moduleNumber: 1,
        stage: 'introduce',
        questionId: 'q1_usp',
        depth: 'surface'
      },
      {
        moduleNumber: 3,
        stage: 'reinforce',
        questionId: 'q3_advantage',
        depth: 'understanding'
      },
      {
        moduleNumber: 4,
        stage: 'apply',
        questionId: 'q4_message',
        depth: 'application'
      },
      {
        moduleNumber: 6,
        stage: 'validate',
        questionId: 'q6_swot_strengths',
        depth: 'application'
      }
    ]
  },
  {
    conceptId: 'revenue_model',
    conceptName: 'Einnahmemodell',
    modules: [
      {
        moduleNumber: 1,
        stage: 'introduce',
        questionId: 'q1_revenue',
        depth: 'surface'
      },
      {
        moduleNumber: 4,
        stage: 'reinforce',
        questionId: 'q4_pricing',
        depth: 'understanding'
      },
      {
        moduleNumber: 5,
        stage: 'apply',
        questionId: 'q5_projections',
        depth: 'application'
      },
      {
        moduleNumber: 6,
        stage: 'validate',
        questionId: 'q6_financial_risks',
        depth: 'application'
      }
    ]
  },
  {
    conceptId: 'market_size',
    conceptName: 'Marktgröße',
    modules: [
      {
        moduleNumber: 2,
        stage: 'introduce',
        questionId: 'q2_market_intro',
        depth: 'surface'
      },
      {
        moduleNumber: 3,
        stage: 'reinforce',
        questionId: 'q3_market_analysis',
        depth: 'understanding'
      },
      {
        moduleNumber: 5,
        stage: 'apply',
        questionId: 'q5_market_share',
        depth: 'application'
      }
    ]
  },
  {
    conceptId: 'founder_qualification',
    conceptName: 'Gründerqualifikation',
    modules: [
      {
        moduleNumber: 1,
        stage: 'introduce',
        questionId: 'q1_qualification',
        depth: 'surface'
      },
      {
        moduleNumber: 1,
        stage: 'reinforce',
        questionId: 'q1_experience',
        depth: 'understanding'
      },
      {
        moduleNumber: 6,
        stage: 'validate',
        questionId: 'q6_swot_competencies',
        depth: 'application'
      }
    ]
  },
  {
    conceptId: 'customer_need',
    conceptName: 'Kundenbeduerfnis',
    modules: [
      {
        moduleNumber: 2,
        stage: 'introduce',
        questionId: 'q2_pain_points',
        depth: 'surface'
      },
      {
        moduleNumber: 2,
        stage: 'reinforce',
        questionId: 'q2_solution',
        depth: 'understanding'
      },
      {
        moduleNumber: 4,
        stage: 'apply',
        questionId: 'q4_value_prop',
        depth: 'application'
      }
    ]
  }
];

export default CONCEPT_PROGRESSIONS;
