import axios from 'axios';
import type {
  StartAssessmentResponse,
  SubmitAssessmentResponse,
  StartWorkshopResponse,
  SubmitModuleResponse,
  CompleteWorkshopResponse,
  Question,
  ModuleNumber
} from '@/types/workshop.types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding session ID
api.interceptors.request.use((config) => {
  const sessionId = localStorage.getItem('gruenderai-session-id');
  if (sessionId) {
    config.headers['X-Session-ID'] = sessionId;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// =============================================================================
// ASSESSMENT API
// =============================================================================

export const assessmentApi = {
  start: async (): Promise<StartAssessmentResponse> => {
    const response = await api.post('/api/assessment/start');
    // Backend returns { sessionId, questions } directly
    const data = response.data;

    // Store session ID
    if (data.sessionId) {
      localStorage.setItem('gruenderai-session-id', data.sessionId);
    }

    return {
      session_id: data.sessionId,
      questions: data.questions || []
    };
  },

  submit: async (
    sessionId: string,
    answers: Record<string, string | string[] | number>
  ): Promise<SubmitAssessmentResponse> => {
    const response = await api.post('/api/assessment/submit', {
      sessionId: sessionId,
      answers: answers
    });

    const data = response.data;
    return {
      session_id: sessionId,
      gz_readiness_score: data.gzReadinessScore || data.gz_readiness_score || 45,
      dimension_scores: data.dimensionScores || data.dimension_scores || {},
      gaps: data.gaps || [],
      recommendations: data.recommendations || []
    };
  },

  getResult: async (sessionId: string): Promise<SubmitAssessmentResponse> => {
    const response = await api.get(`/api/assessment/result/${sessionId}`);
    const data = response.data;
    return {
      session_id: sessionId,
      gz_readiness_score: data.gzReadinessScore || data.gz_readiness_score || 45,
      dimension_scores: data.dimensionScores || data.dimension_scores || {},
      gaps: data.gaps || [],
      recommendations: data.recommendations || []
    };
  },
};

// =============================================================================
// WORKSHOP API
// =============================================================================

export const workshopApi = {
  start: async (sessionId: string): Promise<StartWorkshopResponse> => {
    const response = await api.post('/api/workshop/start', {
      sessionId: sessionId
    });
    const data = response.data;
    return {
      session_id: data.sessionId || sessionId,
      current_module: data.currentModule || data.current_module || 1,
      total_modules: data.totalModules || data.total_modules || 6
    };
  },

  getModule: async (
    sessionId: string,
    moduleNumber: ModuleNumber
  ): Promise<{ questions: Question[] }> => {
    const response = await api.get(`/api/workshop/module/${moduleNumber}`, {
      params: { session_id: sessionId }
    });
    const data = response.data;
    return {
      questions: data.questions || []
    };
  },

  submitModule: async (
    sessionId: string,
    moduleNumber: ModuleNumber,
    answers: Record<string, string | string[] | number>
  ): Promise<SubmitModuleResponse> => {
    const response = await api.post(`/api/workshop/module/${moduleNumber}/submit`, {
      sessionId: sessionId,
      answers: answers
    });
    const data = response.data;
    return {
      module_number: moduleNumber,
      score: data.score || 0,
      feedback: data.feedback || [],
      generated_chapters: data.generatedChapters || data.generated_chapters || [],
      next_module: data.nextModule || data.next_module || null
    };
  },

  getProgress: async (sessionId: string): Promise<{
    currentModule: ModuleNumber;
    moduleProgress: Record<number, number>;
    gzReadinessScore: number;
  }> => {
    const response = await api.get(`/api/workshop/progress/${sessionId}`);
    const data = response.data;
    return {
      currentModule: data.currentModule || data.current_module || 1,
      moduleProgress: data.moduleProgress || data.module_progress || {},
      gzReadinessScore: data.gzReadinessScore || data.gz_readiness_score || 35
    };
  },

  complete: async (sessionId: string): Promise<CompleteWorkshopResponse> => {
    const response = await api.post('/api/workshop/complete', {
      sessionId: sessionId
    });
    const data = response.data;
    return {
      session_id: sessionId,
      final_score: data.finalScore || data.final_score || 0,
      businessplan_url: data.businessplanUrl || data.businessplan_url || '',
      documents: data.documents || {}
    };
  },
};

// =============================================================================
// DOCUMENTS API
// =============================================================================

export const documentsApi = {
  getStatus: async (sessionId: string) => {
    const response = await api.get(`/api/documents/${sessionId}/status`);
    return response.data;
  },

  generate: async (sessionId: string) => {
    const response = await api.post(`/api/documents/${sessionId}/generate`);
    return response.data;
  },

  downloadPdf: (sessionId: string) =>
    `${API_BASE_URL}/api/documents/${sessionId}/pdf`,

  downloadDocx: (sessionId: string) =>
    `${API_BASE_URL}/api/documents/${sessionId}/docx`,

  downloadXlsx: (sessionId: string) =>
    `${API_BASE_URL}/api/documents/${sessionId}/xlsx`,

  downloadAll: (sessionId: string) =>
    `${API_BASE_URL}/api/documents/${sessionId}/all`,
};

// =============================================================================
// MICROTIPS API
// =============================================================================

export interface MicroTip {
  text: string;
  type: 'fact' | 'warning' | 'motivation' | 'expert' | 'success';
}

export interface MicroTipsResponse {
  section_id: string;
  business_category: string | null;
  tips: MicroTip[];
  count: number;
}

export interface MicroTipsCategoriesResponse {
  categories: string[];
  sections: string[];
}

export const microTipsApi = {
  /**
   * Holt typisierte Micro-Tips für die Loading-Animation
   * @param sectionId - Aktuelle Sektion (z.B. "sektion_1_geschaeftsmodell")
   * @param businessCategory - Business-Kategorie (optional, z.B. "gastronomie")
   * @param shuffle - Tips mischen für Abwechslung (default: true)
   */
  getTips: async (
    sectionId: string,
    businessCategory?: string,
    shuffle: boolean = true
  ): Promise<MicroTipsResponse> => {
    const params = new URLSearchParams({
      section_id: sectionId,
      shuffle: String(shuffle),
    });
    if (businessCategory) {
      params.append('business_category', businessCategory);
    }

    const response = await api.get(`/api/workshop-chat/microtips?${params}`);
    return response.data;
  },

  /**
   * Holt alle verfügbaren Kategorien und Sektionen
   */
  getCategories: async (): Promise<MicroTipsCategoriesResponse> => {
    const response = await api.get('/api/workshop-chat/microtips/categories');
    return response.data;
  },
};

export default api;
