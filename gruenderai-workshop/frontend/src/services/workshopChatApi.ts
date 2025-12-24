/**
 * GründerAI Workshop - Chat API Service
 * API client for the interactive chat-based workshop
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// =============================================================================
// TYPES
// =============================================================================

export interface StartWorkshopRequest {
  user_name?: string;
  user_email?: string;
  personality_profile?: Record<string, unknown>;
}

export interface StartWorkshopResponse {
  session_id: string;
  welcome_message: string;
  current_section: {
    id: string;
    nummer: number;
    titel: string;
    untertitel: string;
  };
  progress: number;
  ui_hint?: UIHint;
}

export interface SendMessageRequest {
  message: string;
  session_id: string;
}

export interface CoachingFeedback {
  insight?: string;
  challenge?: string;
  suggestion?: string;
  example?: string;
  encouragement?: string;
  should_iterate: boolean;
  improved_version?: string;
}

export interface GZReadinessInfo {
  module_id: number;
  module_status: string;
  gz_score: number;
  gz_status: string;
  critical_missing: string[];
}

export interface CardOption {
  id: string;
  label: string;
  description?: string;
  icon?: string;
  example?: string;
}

export interface UIHint {
  type: 'cards' | 'text' | 'number' | 'date' | 'textarea';
  question?: string;
  options?: CardOption[];
  placeholder?: string;
  hint?: string;
  examples?: string[];
  multiSelect?: boolean;
  minLength?: number;
  maxLength?: number;
}

export interface CollectedDataItem {
  label: string;
  value?: string;
  status: 'complete' | 'partial' | 'missing';
  fieldId?: string;
  note?: string;
}

/** NEU: Completion Status für "Fertig" Button */
export interface CompletionStatus {
  fill_percentage: number;
  filled_fields: number;
  total_fields: number;
  question_count: number;
  min_questions: number;
  can_complete: boolean;
  show_completion_button: boolean;
  is_optimal: boolean;
  remaining_for_optimal: number;
}

export interface CompleteSectionResponse {
  success: boolean;
  message: string;
  section_id: string;
  section_title?: string;
  generated_text?: string;
  next_section_id?: string;
  collected_data?: CollectedDataItem[];
  fill_percentage?: number;
  section_completed: boolean;
}

export interface SendMessageResponse {
  session_id: string;
  assistant_message: string;
  progress: number;
  current_section: string;
  current_step: string;
  validation_status: string;
  structured_data?: Record<string, unknown>;
  // UI hint for card-based questions
  ui_hint?: UIHint;
  // Section completion fields
  section_completed?: boolean;
  completed_section_id?: string;
  next_section_id?: string;
  generated_text?: string;
  // Coaching and GZ compliance
  coaching_feedback?: CoachingFeedback;
  gz_readiness?: GZReadinessInfo;
  // Collected data for transition screen
  collected_data?: CollectedDataItem[];
  // NEU: Completion Status für "Fertig" Button
  completion_status?: CompletionStatus;
}

export interface WorkshopStatusResponse {
  session_id: string;
  status: string;
  progress: number;
  current_section: string;
  current_step: string;
  sections: SectionInfo[];
  can_export: boolean;
  estimated_remaining_time: string;
}

export interface SectionInfo {
  id: string;
  nummer: number;
  titel: string;
  untertitel: string;
  status: 'locked' | 'available' | 'in_progress' | 'completed';
  quality_score: number | null;
  completed_at: string | null;
  geschaetzte_dauer: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  section_id: string | null;
  step_id: string | null;
  created_at: string;
}

export interface MessagesResponse {
  session_id: string;
  messages: ChatMessage[];
  total: number;
  limit: number;
  offset: number;
}

export interface BusinessPlanData {
  session_id: string;
  data: Record<string, unknown>;
  updated_at: string | null;
  pdf_url: string | null;
  docx_url: string | null;
}

export interface ExportRequest {
  format: 'pdf' | 'docx';
}

export interface ExportResponse {
  download_url: string;
  format: string;
  generated_at: string;
}

export interface SectionPreview {
  section_id: string;
  section_titel: string;
  section_nummer: number;
  status: string;
  generated_text: string | null;
  quality_score: number | null;
  completed_at: string | null;
}

export interface PreviewResponse {
  session_id: string;
  progress: number;
  sections: SectionPreview[];
  total_sections: number;
  completed_sections: number;
}

export interface SectionPreviewDetail {
  session_id: string;
  section_id: string;
  section_titel: string;
  section_nummer: number;
  status: string;
  generated_text: string | null;
  quality_score: number | null;
  collected_data: Record<string, unknown> | null;
  completed_at: string | null;
}

export interface BATipp {
  id: string;
  type: 'info' | 'warning' | 'success';
  title: string;
  content: string;
  details?: string;
  example?: string;
  legal_ref?: string;
  trigger_field?: string;
  trigger_section?: string;
  priority: number;
}

export interface TippsResponse {
  tipps: BATipp[];
  count: number;
}

export interface SectionTippsResponse {
  section_id: string;
  tipps: BATipp[];
  count: number;
}

export interface CriticalTippsResponse {
  warning: string;
  tipps: BATipp[];
  count: number;
}

export interface WorkshopSection {
  id: string;
  nummer: number;
  titel: string;
  untertitel: string;
  beschreibung: string;
  geschaetzte_dauer: string;
  schritte: string[];
  pflichtfelder: string[];
  gz_fragen: number[];
}

// =============================================================================
// API FUNCTIONS
// =============================================================================

export const workshopChatApi = {
  /**
   * Startet einen neuen Workshop und gibt die Willkommensnachricht zurück
   */
  start: async (request: StartWorkshopRequest = {}): Promise<StartWorkshopResponse> => {
    const response = await api.post('/api/workshop-chat/start', request);
    return response.data;
  },

  /**
   * Sendet eine Nachricht im Workshop-Chat
   */
  sendMessage: async (request: SendMessageRequest): Promise<SendMessageResponse> => {
    const response = await api.post('/api/workshop-chat/message', request);
    return response.data;
  },

  /**
   * Holt den aktuellen Workshop-Status
   */
  getStatus: async (sessionId: string): Promise<WorkshopStatusResponse> => {
    const response = await api.get(`/api/workshop-chat/status/${sessionId}`);
    return response.data;
  },

  /**
   * Holt die Chat-Historie
   */
  getMessages: async (
    sessionId: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<MessagesResponse> => {
    const response = await api.get(`/api/workshop-chat/messages/${sessionId}`, {
      params: { limit, offset }
    });
    return response.data;
  },

  /**
   * Holt die Businessplan-Daten
   */
  getBusinessPlan: async (sessionId: string): Promise<BusinessPlanData> => {
    const response = await api.get(`/api/workshop-chat/business-plan/${sessionId}`);
    return response.data;
  },

  /**
   * Exportiert den Businessplan
   */
  export: async (sessionId: string, request: ExportRequest): Promise<ExportResponse> => {
    const response = await api.post(`/api/workshop-chat/export/${sessionId}`, request);
    return response.data;
  },

  /**
   * Holt alle Workshop-Sektionen
   */
  getSections: async (): Promise<{ sections: WorkshopSection[]; total: number }> => {
    const response = await api.get('/api/workshop-chat/sections');
    return response.data;
  },

  /**
   * Pausiert den Workshop
   */
  pause: async (sessionId: string): Promise<{ message: string; session_id: string; progress: number; can_resume: boolean }> => {
    const response = await api.post(`/api/workshop-chat/session/${sessionId}/pause`);
    return response.data;
  },

  /**
   * Setzt den Workshop fort
   */
  resume: async (sessionId: string): Promise<{
    message: string;
    session_id: string;
    progress: number;
    current_section: string;
    current_step: string;
    last_assistant_message: string | null;
  }> => {
    const response = await api.post(`/api/workshop-chat/session/${sessionId}/resume`);
    return response.data;
  },

  /**
   * Löscht eine Session
   */
  deleteSession: async (sessionId: string): Promise<{ message: string; session_id: string }> => {
    const response = await api.delete(`/api/workshop-chat/session/${sessionId}`);
    return response.data;
  },

  // =============================================================================
  // COMPLETION API (NEU: Flexible Module Completion)
  // =============================================================================

  /**
   * Holt den Completion-Status für die aktuelle Sektion
   */
  getCompletionStatus: async (sessionId: string): Promise<CompletionStatus> => {
    const response = await api.get(`/api/workshop-chat/completion-status/${sessionId}`);
    return response.data;
  },

  /**
   * User-initiated Section Completion (ab 75% möglich)
   */
  completeSection: async (sessionId: string): Promise<CompleteSectionResponse> => {
    const response = await api.post(`/api/workshop-chat/complete-section/${sessionId}`);
    return response.data;
  },

  // Download URLs
  getDownloadUrls: (sessionId: string) => ({
    pdf: `${API_BASE_URL}/api/workshop-chat/download/${sessionId}/pdf`,
    docx: `${API_BASE_URL}/api/workshop-chat/download/${sessionId}/docx`,
    xlsx: `${API_BASE_URL}/api/workshop-chat/download/${sessionId}/xlsx`,
    all: `${API_BASE_URL}/api/workshop-chat/download/${sessionId}/all`,
  }),

  // =============================================================================
  // PREVIEW API
  // =============================================================================

  /**
   * Holt alle generierten Texte fuer die Live-Vorschau
   */
  getPreview: async (sessionId: string): Promise<PreviewResponse> => {
    const response = await api.get(`/api/workshop-chat/preview/${sessionId}`);
    return response.data;
  },

  /**
   * Holt den generierten Text fuer eine spezifische Sektion
   */
  getSectionPreview: async (sessionId: string, sectionId: string): Promise<SectionPreviewDetail> => {
    const response = await api.get(`/api/workshop-chat/preview/${sessionId}/section/${sectionId}`);
    return response.data;
  },

  // =============================================================================
  // BA TIPPS API
  // =============================================================================

  /**
   * Holt alle BA-Tipps
   */
  getAllTipps: async (): Promise<TippsResponse> => {
    const response = await api.get('/api/workshop-chat/tipps');
    return response.data;
  },

  /**
   * Holt BA-Tipps fuer eine spezifische Sektion
   */
  getTippsForSection: async (sectionId: string): Promise<SectionTippsResponse> => {
    const response = await api.get(`/api/workshop-chat/tipps/section/${sectionId}`);
    return response.data;
  },

  /**
   * Holt die kritischsten BA-Tipps
   */
  getCriticalTipps: async (): Promise<CriticalTippsResponse> => {
    const response = await api.get('/api/workshop-chat/tipps/critical');
    return response.data;
  },

  // =============================================================================
  // MICROTIPS API (Loading State UX)
  // =============================================================================

  /**
   * Holt kontextuelle Microtips fuer Loading States
   * Macht Wartezeit zu Lernzeit!
   */
  getMicrotips: async (
    sessionId: string,
    questionId: string,
    nextQuestionId?: string
  ): Promise<{ tips: Array<{ icon: string; text: string; category: string }> }> => {
    const params = new URLSearchParams({
      session_id: sessionId,
      question_id: questionId,
    });
    if (nextQuestionId) {
      params.append('next_question_id', nextQuestionId);
    }
    const response = await api.post(`/api/workshop-chat/microtips?${params.toString()}`);
    return response.data;
  },

  // =============================================================================
  // CHECKLIST API
  // =============================================================================

  /**
   * Holt die Checkliste fuer die Sidebar
   */
  getChecklist: async (
    sessionId: string,
    includeAllSections: boolean = true
  ): Promise<{
    session_id: string;
    current_section: string;
    items: Array<{
      id: string;
      label: string;
      description?: string;
      status: 'pending' | 'in_progress' | 'completed' | 'skipped';
      sectionId: string;
      priority: 'required' | 'recommended' | 'optional';
      fieldId?: string;
      gzRelevant?: boolean;
      completedAt?: string;
    }>;
    stats: {
      total: number;
      completed: number;
      in_progress: number;
      required_completed: number;
      required_total: number;
      gz_completed: number;
      gz_total: number;
      percentage: number;
    };
  }> => {
    const response = await api.get(`/api/workshop-chat/checklist/${sessionId}`, {
      params: { include_all_sections: includeAllSections }
    });
    return response.data;
  },

  /**
   * Aktualisiert den Status eines Checklist-Items
   */
  updateChecklistItem: async (
    sessionId: string,
    itemId: string,
    status: 'pending' | 'in_progress' | 'completed' | 'skipped'
  ): Promise<{
    success: boolean;
    item_id: string;
    status: string;
  }> => {
    const response = await api.post(`/api/workshop-chat/checklist/${sessionId}/update`, null, {
      params: { item_id: itemId, status }
    });
    return response.data;
  },
};

export default workshopChatApi;
