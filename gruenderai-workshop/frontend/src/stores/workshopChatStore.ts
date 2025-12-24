/**
 * GründerAI Workshop - Chat Store
 * Zustand store for managing chat-based workshop state
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  ChatMessage,
  SectionInfo,
  WorkshopStatusResponse,
  SendMessageResponse,
  StartWorkshopResponse,
  CoachingFeedback,
  GZReadinessInfo,
  UIHint,
} from '@/services/workshopChatApi';

// =============================================================================
// TYPES
// =============================================================================

export interface LocalMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sectionId?: string;
  stepId?: string;
  isLoading?: boolean;
  /** UI hint for card-based questions */
  uiHint?: UIHint;
}

export type CollectedItemStatus = 'complete' | 'partial' | 'missing';

export interface CollectedItem {
  label: string;
  value?: string;
  status: CollectedItemStatus;
  note?: string;
}

export interface SectionTransition {
  isActive: boolean;
  completedSectionId: string | null;
  completedSectionTitle: string | null;
  nextSectionId: string | null;
  nextSectionTitle: string | null;
  generatedText: string | null;
  gzScore: number | null;
  /** Explicitly collected data - NO INFERENCE */
  collectedData: CollectedItem[];
}

/** NEU: Completion Status für "Fertig" Button */
export interface CompletionStatus {
  fillPercentage: number;
  filledFields: number;
  totalFields: number;
  questionCount: number;
  minQuestions: number;
  canComplete: boolean;
  showCompletionButton: boolean;
  isOptimal: boolean;
  remainingForOptimal: number;
}

export interface WorkshopChatState {
  // Session
  sessionId: string | null;
  status: string;

  // Messages
  messages: LocalMessage[];
  isLoading: boolean;

  // Progress
  progress: number;
  currentSection: string;
  currentStep: string;
  sections: SectionInfo[];
  /** Index of first message in current section - for progress reset */
  sectionStartMessageIndex: number;

  // Export
  canExport: boolean;
  estimatedRemainingTime: string;

  // User Info
  userName: string;
  userEmail: string;

  // UI State
  isSidebarOpen: boolean;
  isTyping: boolean;

  // Section Transition State
  sectionTransition: SectionTransition;

  // Coaching & GZ
  lastCoachingFeedback: CoachingFeedback | null;
  lastGzReadiness: GZReadinessInfo | null;

  // NEU: Completion Status für "Fertig" Button
  completionStatus: CompletionStatus | null;

  // Actions
  setSession: (sessionId: string) => void;
  clearSession: () => void;

  // Message Actions
  addUserMessage: (content: string) => string;
  addAssistantMessage: (content: string, sectionId?: string, stepId?: string) => void;
  setAssistantLoading: (messageId: string, isLoading: boolean) => void;
  updateAssistantMessage: (messageId: string, content: string) => void;
  loadMessages: (messages: ChatMessage[]) => void;

  // Progress Actions
  updateProgress: (progress: number) => void;
  updateSection: (sectionId: string, step: string) => void;
  updateSections: (sections: SectionInfo[]) => void;
  updateStatus: (response: WorkshopStatusResponse) => void;

  // Workshop Actions
  handleStartResponse: (response: StartWorkshopResponse) => void;
  handleMessageResponse: (response: SendMessageResponse) => void;

  // User Actions
  setUserInfo: (name: string, email: string) => void;

  // UI Actions
  toggleSidebar: () => void;
  setTyping: (isTyping: boolean) => void;

  // Section Transition Actions
  dismissTransition: () => void;
  continueToNextSection: () => void;

  // Reset
  reset: () => void;
}

// =============================================================================
// HELPERS
// =============================================================================

const generateMessageId = () => `msg_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;

// =============================================================================
// STORE
// =============================================================================

const initialSectionTransition: SectionTransition = {
  isActive: false,
  completedSectionId: null,
  completedSectionTitle: null,
  nextSectionId: null,
  nextSectionTitle: null,
  generatedText: null,
  gzScore: null,
  collectedData: [],
};

export const useWorkshopChatStore = create<WorkshopChatState>()(
  persist(
    (set, get) => ({
      // Initial State
      sessionId: null,
      status: 'idle',
      messages: [],
      isLoading: false,
      progress: 0,
      currentSection: '',
      currentStep: '',
      sections: [],
      canExport: false,
      estimatedRemainingTime: '',
      userName: '',
      userEmail: '',
      isSidebarOpen: true,
      isTyping: false,
      sectionTransition: initialSectionTransition,
      lastCoachingFeedback: null,
      lastGzReadiness: null,
      completionStatus: null,
      sectionStartMessageIndex: 0,

      // Session Actions
      setSession: (sessionId) => set({ sessionId, status: 'active' }),

      clearSession: () => set({
        sessionId: null,
        status: 'idle',
        messages: [],
        progress: 0,
        currentSection: '',
        currentStep: '',
        sections: [],
        canExport: false,
      }),

      // Message Actions
      addUserMessage: (content) => {
        const id = generateMessageId();
        set((state) => ({
          messages: [
            ...state.messages,
            {
              id,
              role: 'user' as const,
              content,
              timestamp: new Date(),
            },
          ],
          isLoading: true,
        }));
        return id;
      },

      addAssistantMessage: (content, sectionId, stepId) => {
        set((state) => ({
          messages: [
            ...state.messages,
            {
              id: generateMessageId(),
              role: 'assistant' as const,
              content,
              timestamp: new Date(),
              sectionId,
              stepId,
            },
          ],
          isLoading: false,
          isTyping: false,
        }));
      },

      setAssistantLoading: (messageId, isLoading) => {
        set((state) => ({
          messages: state.messages.map((msg) =>
            msg.id === messageId ? { ...msg, isLoading } : msg
          ),
        }));
      },

      updateAssistantMessage: (messageId, content) => {
        set((state) => ({
          messages: state.messages.map((msg) =>
            msg.id === messageId ? { ...msg, content, isLoading: false } : msg
          ),
        }));
      },

      loadMessages: (messages) => {
        set({
          messages: messages.map((msg) => ({
            id: msg.id,
            role: msg.role,
            content: msg.content,
            timestamp: new Date(msg.created_at),
            sectionId: msg.section_id || undefined,
            stepId: msg.step_id || undefined,
          })),
        });
      },

      // Progress Actions
      updateProgress: (progress) => set({ progress }),

      updateSection: (sectionId, step) => set({
        currentSection: sectionId,
        currentStep: step,
      }),

      updateSections: (sections) => set({ sections }),

      updateStatus: (response) => set({
        status: response.status,
        progress: response.progress,
        currentSection: response.current_section,
        currentStep: response.current_step,
        sections: response.sections,
        canExport: response.can_export,
        estimatedRemainingTime: response.estimated_remaining_time,
      }),

      // Workshop Response Handlers
      handleStartResponse: (response) => {
        set({
          sessionId: response.session_id,
          status: 'active',
          progress: response.progress,
          currentSection: response.current_section.id,
          messages: [
            {
              id: generateMessageId(),
              role: 'assistant' as const,
              content: response.welcome_message,
              timestamp: new Date(),
              sectionId: response.current_section.id,
              uiHint: response.ui_hint,
            },
          ],
        });
      },

      handleMessageResponse: (response) => {
        const state = get();

        // Check if a section was completed
        const sectionCompleted = response.section_completed === true;

        // Debug logging
        console.log('[Store] handleMessageResponse:', {
          section_completed: response.section_completed,
          completed_section_id: response.completed_section_id,
          next_section_id: response.next_section_id,
          generated_text_length: response.generated_text?.length || 0,
          sectionCompleted,
        });

        // Find section titles for transition screen
        let completedSectionTitle: string | null = null;
        let nextSectionTitle: string | null = null;

        if (sectionCompleted && response.completed_section_id) {
          const completedSection = state.sections.find(s => s.id === response.completed_section_id);
          completedSectionTitle = completedSection?.titel || null;

          if (response.next_section_id) {
            const nextSection = state.sections.find(s => s.id === response.next_section_id);
            nextSectionTitle = nextSection?.titel || null;
          }
        }

        // Add assistant message
        set({
          messages: [
            ...state.messages,
            {
              id: generateMessageId(),
              role: 'assistant' as const,
              content: response.assistant_message,
              timestamp: new Date(),
              sectionId: response.current_section,
              stepId: response.current_step,
              uiHint: response.ui_hint,
            },
          ],
          progress: response.progress,
          currentSection: response.current_section,
          currentStep: response.current_step,
          isLoading: false,
          isTyping: false,
          // Update transition state if section completed
          sectionTransition: sectionCompleted ? (() => {
            // Parse collected data from response (backend should send this)
            const collectedData: CollectedItem[] = response.collected_data?.map((item: any) => ({
              label: item.label || item.field,
              value: item.value,
              status: item.status || (item.value ? 'complete' : 'missing'),
              note: item.note,
            })) || [];

            const newTransition: SectionTransition = {
              isActive: true,
              completedSectionId: response.completed_section_id || null,
              completedSectionTitle,
              nextSectionId: response.next_section_id || null,
              nextSectionTitle,
              generatedText: response.generated_text || null,
              gzScore: response.gz_readiness?.gz_score || null,
              collectedData,
            };
            console.log('[Store] Setting transition state:', newTransition);
            return newTransition;
          })() : state.sectionTransition,
          // Update coaching & GZ readiness
          lastCoachingFeedback: response.coaching_feedback || state.lastCoachingFeedback,
          lastGzReadiness: response.gz_readiness || state.lastGzReadiness,
          // NEU: Completion Status für "Fertig" Button
          completionStatus: response.completion_status ? {
            fillPercentage: response.completion_status.fill_percentage,
            filledFields: response.completion_status.filled_fields,
            totalFields: response.completion_status.total_fields,
            questionCount: response.completion_status.question_count,
            minQuestions: response.completion_status.min_questions,
            canComplete: response.completion_status.can_complete,
            showCompletionButton: response.completion_status.show_completion_button,
            isOptimal: response.completion_status.is_optimal,
            remainingForOptimal: response.completion_status.remaining_for_optimal,
          } : state.completionStatus,
        });
      },

      // User Actions
      setUserInfo: (name, email) => set({ userName: name, userEmail: email }),

      // UI Actions
      toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
      setTyping: (isTyping) => set({ isTyping }),

      // Section Transition Actions
      dismissTransition: () => set({
        sectionTransition: initialSectionTransition,
      }),

      continueToNextSection: () => {
        const state = get();
        const nextSectionId = state.sectionTransition.nextSectionId;

        set({
          sectionTransition: initialSectionTransition,
          currentSection: nextSectionId || state.currentSection,
          // Reset section start index for progress calculation
          sectionStartMessageIndex: state.messages.length,
        });
      },

      // Reset
      reset: () => set({
        sessionId: null,
        status: 'idle',
        messages: [],
        isLoading: false,
        progress: 0,
        currentSection: '',
        currentStep: '',
        sections: [],
        canExport: false,
        estimatedRemainingTime: '',
        userName: '',
        userEmail: '',
        isSidebarOpen: true,
        isTyping: false,
        sectionTransition: initialSectionTransition,
        lastCoachingFeedback: null,
        lastGzReadiness: null,
        completionStatus: null,
        sectionStartMessageIndex: 0,
      }),
    }),
    {
      name: 'gruenderai-workshop-chat',
      partialize: (state) => ({
        sessionId: state.sessionId,
        userName: state.userName,
        userEmail: state.userEmail,
        progress: state.progress,
        currentSection: state.currentSection,
      }),
    }
  )
);

// =============================================================================
// SELECTORS
// =============================================================================

export const selectCurrentSectionInfo = (state: WorkshopChatState) =>
  state.sections.find((s) => s.id === state.currentSection);

export const selectCompletedSections = (state: WorkshopChatState) =>
  state.sections.filter((s) => s.status === 'completed');

export const selectIsWorkshopComplete = (state: WorkshopChatState) =>
  state.progress >= 100 || state.sections.every((s) => s.status === 'completed');

export const selectMessageCount = (state: WorkshopChatState) =>
  state.messages.length;

export default useWorkshopChatStore;
