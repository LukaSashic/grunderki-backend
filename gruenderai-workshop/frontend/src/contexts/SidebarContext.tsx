/**
 * SidebarContext - State Management for Intelligent Sidebar
 *
 * Manages:
 * - Active tab (tips, checklist, progress)
 * - Checklist items and their status
 * - Starred tips
 * - Sidebar visibility (mobile)
 * - LocalStorage persistence
 */

import React, { createContext, useContext, useReducer, useEffect, useCallback } from 'react';

// =============================================================================
// TYPES
// =============================================================================

export interface ChecklistItem {
  id: string;
  label: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'skipped';
  fieldId?: string;
  sectionId: string;
  priority: 'required' | 'recommended' | 'optional';
  gzRelevant?: boolean;
  completedAt?: string;
}

export interface StarredTip {
  id: string;
  text: string;
  category: string;
  icon: string;
  starredAt: string;
}

export interface SidebarTab {
  id: 'tips' | 'checklist' | 'progress';
  label: string;
  icon: string;
  badge?: number;
}

interface SidebarState {
  isOpen: boolean;
  activeTab: SidebarTab['id'];
  checklistItems: ChecklistItem[];
  starredTips: StarredTip[];
  expandedSections: string[];
  searchQuery: string;
  filterStatus: 'all' | 'pending' | 'completed';
}

type SidebarAction =
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_SIDEBAR_OPEN'; payload: boolean }
  | { type: 'SET_ACTIVE_TAB'; payload: SidebarTab['id'] }
  | { type: 'SET_CHECKLIST_ITEMS'; payload: ChecklistItem[] }
  | { type: 'UPDATE_CHECKLIST_ITEM'; payload: { id: string; status: ChecklistItem['status'] } }
  | { type: 'ADD_STARRED_TIP'; payload: StarredTip }
  | { type: 'REMOVE_STARRED_TIP'; payload: string }
  | { type: 'TOGGLE_SECTION'; payload: string }
  | { type: 'SET_SEARCH_QUERY'; payload: string }
  | { type: 'SET_FILTER_STATUS'; payload: SidebarState['filterStatus'] }
  | { type: 'LOAD_FROM_STORAGE'; payload: Partial<SidebarState> };

// =============================================================================
// INITIAL STATE
// =============================================================================

const initialState: SidebarState = {
  isOpen: true,
  activeTab: 'checklist',
  checklistItems: [],
  starredTips: [],
  expandedSections: [],
  searchQuery: '',
  filterStatus: 'all',
};

// =============================================================================
// REDUCER
// =============================================================================

function sidebarReducer(state: SidebarState, action: SidebarAction): SidebarState {
  switch (action.type) {
    case 'TOGGLE_SIDEBAR':
      return { ...state, isOpen: !state.isOpen };

    case 'SET_SIDEBAR_OPEN':
      return { ...state, isOpen: action.payload };

    case 'SET_ACTIVE_TAB':
      return { ...state, activeTab: action.payload };

    case 'SET_CHECKLIST_ITEMS':
      return { ...state, checklistItems: action.payload };

    case 'UPDATE_CHECKLIST_ITEM':
      return {
        ...state,
        checklistItems: state.checklistItems.map(item =>
          item.id === action.payload.id
            ? {
                ...item,
                status: action.payload.status,
                completedAt: action.payload.status === 'completed' ? new Date().toISOString() : undefined,
              }
            : item
        ),
      };

    case 'ADD_STARRED_TIP':
      if (state.starredTips.some(t => t.id === action.payload.id)) {
        return state;
      }
      return { ...state, starredTips: [...state.starredTips, action.payload] };

    case 'REMOVE_STARRED_TIP':
      return {
        ...state,
        starredTips: state.starredTips.filter(t => t.id !== action.payload),
      };

    case 'TOGGLE_SECTION':
      return {
        ...state,
        expandedSections: state.expandedSections.includes(action.payload)
          ? state.expandedSections.filter(s => s !== action.payload)
          : [...state.expandedSections, action.payload],
      };

    case 'SET_SEARCH_QUERY':
      return { ...state, searchQuery: action.payload };

    case 'SET_FILTER_STATUS':
      return { ...state, filterStatus: action.payload };

    case 'LOAD_FROM_STORAGE':
      return { ...state, ...action.payload };

    default:
      return state;
  }
}

// =============================================================================
// CONTEXT
// =============================================================================

interface SidebarContextValue {
  state: SidebarState;
  dispatch: React.Dispatch<SidebarAction>;
  // Convenience methods
  toggleSidebar: () => void;
  setActiveTab: (tab: SidebarTab['id']) => void;
  updateChecklistItem: (id: string, status: ChecklistItem['status']) => void;
  starTip: (tip: Omit<StarredTip, 'starredAt'>) => void;
  unstarTip: (id: string) => void;
  isStarred: (id: string) => boolean;
  getChecklistStats: () => { total: number; completed: number; percentage: number };
  jumpToQuestion: (fieldId: string) => void;
}

const SidebarContext = createContext<SidebarContextValue | null>(null);

// =============================================================================
// STORAGE KEY
// =============================================================================

const STORAGE_KEY = 'gruenderai_sidebar_state';

// =============================================================================
// PROVIDER
// =============================================================================

interface SidebarProviderProps {
  children: React.ReactNode;
  sessionId?: string;
}

export function SidebarProvider({ children, sessionId }: SidebarProviderProps) {
  const [state, dispatch] = useReducer(sidebarReducer, initialState);

  // Load from localStorage on mount
  useEffect(() => {
    const storageKey = sessionId ? `${STORAGE_KEY}_${sessionId}` : STORAGE_KEY;
    try {
      const stored = localStorage.getItem(storageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        dispatch({ type: 'LOAD_FROM_STORAGE', payload: parsed });
      }
    } catch (e) {
      console.warn('[SidebarContext] Failed to load from storage:', e);
    }
  }, [sessionId]);

  // Save to localStorage on state change
  useEffect(() => {
    const storageKey = sessionId ? `${STORAGE_KEY}_${sessionId}` : STORAGE_KEY;
    try {
      const toStore = {
        starredTips: state.starredTips,
        expandedSections: state.expandedSections,
        activeTab: state.activeTab,
      };
      localStorage.setItem(storageKey, JSON.stringify(toStore));
    } catch (e) {
      console.warn('[SidebarContext] Failed to save to storage:', e);
    }
  }, [state.starredTips, state.expandedSections, state.activeTab, sessionId]);

  // Convenience methods
  const toggleSidebar = useCallback(() => {
    dispatch({ type: 'TOGGLE_SIDEBAR' });
  }, []);

  const setActiveTab = useCallback((tab: SidebarTab['id']) => {
    dispatch({ type: 'SET_ACTIVE_TAB', payload: tab });
  }, []);

  const updateChecklistItem = useCallback((id: string, status: ChecklistItem['status']) => {
    dispatch({ type: 'UPDATE_CHECKLIST_ITEM', payload: { id, status } });
  }, []);

  const starTip = useCallback((tip: Omit<StarredTip, 'starredAt'>) => {
    dispatch({
      type: 'ADD_STARRED_TIP',
      payload: { ...tip, starredAt: new Date().toISOString() },
    });
  }, []);

  const unstarTip = useCallback((id: string) => {
    dispatch({ type: 'REMOVE_STARRED_TIP', payload: id });
  }, []);

  const isStarred = useCallback((id: string) => {
    return state.starredTips.some(t => t.id === id);
  }, [state.starredTips]);

  const getChecklistStats = useCallback(() => {
    const total = state.checklistItems.length;
    const completed = state.checklistItems.filter(i => i.status === 'completed').length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    return { total, completed, percentage };
  }, [state.checklistItems]);

  const jumpToQuestion = useCallback((fieldId: string) => {
    // Emit custom event that the chat component can listen to
    const event = new CustomEvent('sidebar:jumpToQuestion', { detail: { fieldId } });
    window.dispatchEvent(event);
  }, []);

  const value: SidebarContextValue = {
    state,
    dispatch,
    toggleSidebar,
    setActiveTab,
    updateChecklistItem,
    starTip,
    unstarTip,
    isStarred,
    getChecklistStats,
    jumpToQuestion,
  };

  return (
    <SidebarContext.Provider value={value}>
      {children}
    </SidebarContext.Provider>
  );
}

// =============================================================================
// HOOK
// =============================================================================

export function useSidebar() {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error('useSidebar must be used within a SidebarProvider');
  }
  return context;
}

export default SidebarContext;
