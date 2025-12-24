import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { UserContext, ModuleInfo, ResponsePattern } from '@/types/workshop.types';

interface WorkshopState {
  // Session
  sessionId: string;

  // User Context
  userContext: UserContext;

  // Progress
  currentModule: number;
  currentChapter: string;
  currentQuestion: number;
  moduleProgress: Record<number, number>;

  // Scores
  qualityScores: Record<number, number>;
  gzReadinessScore: number;
  businessPlanProgress: number;

  // Answers & Feedback
  answers: Record<string, string | string[] | number>;
  feedback: Record<string, unknown>;

  // Adaptive
  responsePatterns: ResponsePattern[];
  adaptiveMode: 'guided' | 'standard' | 'advanced';

  // Story
  storyAchievements: string[];

  // Time tracking
  startTime: number | null;
  moduleStartTimes: Record<number, number>;

  // Actions
  setSessionId: (sessionId: string) => void;
  setUserContext: (context: Partial<UserContext>) => void;
  setAnswer: (questionId: string, answer: string | string[] | number) => void;
  setFeedback: (questionId: string, feedback: unknown) => void;
  updateProgress: (module: number, chapter: string, progress: number) => void;
  updateScores: (qualityScore: number, gzReadiness: number) => void;
  recordResponsePattern: (pattern: ResponsePattern) => void;
  addStoryAchievement: (achievement: string) => void;
  nextModule: () => void;
  nextQuestion: () => void;
  setCurrentQuestion: (questionNumber: number) => void;
  startWorkshop: () => void;
  startModule: (moduleNumber: number) => void;
  getTimeSpent: () => number;
  setGzReadinessScore: (score: number) => void;
  reset: () => void;
}

const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
};

export const useWorkshopStore = create<WorkshopState>()(
  persist(
    (set, get) => ({
      // Initial State
      sessionId: generateSessionId(),
      userContext: {
        name: '',
        profession: '',
        city: '',
        businessIdea: '',
        targetCustomer: ''
      },
      currentModule: 1,
      currentChapter: '',
      currentQuestion: 1,
      moduleProgress: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 },
      qualityScores: {},
      gzReadinessScore: 35,
      businessPlanProgress: 0,
      answers: {},
      feedback: {},
      responsePatterns: [],
      adaptiveMode: 'standard',
      storyAchievements: [],
      startTime: null,
      moduleStartTimes: {},

      // Actions
      setSessionId: (sessionId) => set({ sessionId }),

      setUserContext: (context) =>
        set((state) => ({
          userContext: { ...state.userContext, ...context }
        })),

      setAnswer: (questionId, answer) =>
        set((state) => ({
          answers: { ...state.answers, [questionId]: answer }
        })),

      setFeedback: (questionId, feedback) =>
        set((state) => ({
          feedback: { ...state.feedback, [questionId]: feedback }
        })),

      updateProgress: (module, chapter, progress) =>
        set((state) => ({
          moduleProgress: { ...state.moduleProgress, [module]: progress },
          currentChapter: chapter,
          businessPlanProgress: Math.round(
            Object.values({ ...state.moduleProgress, [module]: progress })
              .reduce((sum, p) => sum + p, 0) / 6
          )
        })),

      updateScores: (qualityScore, gzReadiness) =>
        set((state) => ({
          qualityScores: { ...state.qualityScores, [state.currentModule]: qualityScore },
          gzReadinessScore: gzReadiness
        })),

      recordResponsePattern: (pattern) =>
        set((state) => ({
          responsePatterns: [...state.responsePatterns.slice(-10), pattern]
        })),

      addStoryAchievement: (achievement) =>
        set((state) => ({
          storyAchievements: [...state.storyAchievements, achievement]
        })),

      nextModule: () =>
        set((state) => ({
          currentModule: Math.min(state.currentModule + 1, 6),
          currentQuestion: 1,
          moduleProgress: { ...state.moduleProgress, [state.currentModule]: 100 }
        })),

      nextQuestion: () =>
        set((state) => ({
          currentQuestion: state.currentQuestion + 1
        })),

      setCurrentQuestion: (questionNumber) =>
        set({ currentQuestion: questionNumber }),

      startWorkshop: () =>
        set({
          startTime: Date.now(),
          currentModule: 1,
          currentQuestion: 1
        }),

      startModule: (moduleNumber) =>
        set((state) => ({
          currentModule: moduleNumber,
          currentQuestion: 1,
          moduleStartTimes: {
            ...state.moduleStartTimes,
            [moduleNumber]: Date.now()
          }
        })),

      getTimeSpent: () => {
        const state = get();
        if (!state.startTime) return 0;
        return Math.round((Date.now() - state.startTime) / 60000); // minutes
      },

      setGzReadinessScore: (score) => set({ gzReadinessScore: score }),

      reset: () => set({
        sessionId: generateSessionId(),
        userContext: {
          name: '',
          profession: '',
          city: '',
          businessIdea: '',
          targetCustomer: ''
        },
        currentModule: 1,
        currentChapter: '',
        currentQuestion: 1,
        moduleProgress: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 },
        qualityScores: {},
        gzReadinessScore: 35,
        businessPlanProgress: 0,
        answers: {},
        feedback: {},
        responsePatterns: [],
        adaptiveMode: 'standard',
        storyAchievements: [],
        startTime: null,
        moduleStartTimes: {}
      })
    }),
    {
      name: 'gruenderai-workshop',
      partialize: (state) => ({
        sessionId: state.sessionId,
        userContext: state.userContext,
        currentModule: state.currentModule,
        currentQuestion: state.currentQuestion,
        moduleProgress: state.moduleProgress,
        qualityScores: state.qualityScores,
        gzReadinessScore: state.gzReadinessScore,
        businessPlanProgress: state.businessPlanProgress,
        answers: state.answers,
        storyAchievements: state.storyAchievements,
        startTime: state.startTime
      })
    }
  )
);

// Selectors
export const selectIsWorkshopComplete = (state: WorkshopState) =>
  state.currentModule === 6 && state.moduleProgress[6] === 100;

export const selectQuestionsAnswered = (state: WorkshopState) =>
  Object.keys(state.answers).length;

export const selectAverageQualityScore = (state: WorkshopState) => {
  const scores = Object.values(state.qualityScores);
  if (scores.length === 0) return 0;
  return Math.round(scores.reduce((sum, s) => sum + s, 0) / scores.length);
};
