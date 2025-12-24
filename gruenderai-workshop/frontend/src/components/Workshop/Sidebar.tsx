/**
 * Sidebar Component - Intelligent Workshop Sidebar
 *
 * Premium sidebar with 3 tabs:
 * - Checklist: GZ-relevant checklist items
 * - Tips: Contextual tips with starring
 * - Progress: Visual progress and collected data
 *
 * Features:
 * - Responsive (desktop/tablet/mobile)
 * - Collapsible
 * - LocalStorage persistence
 * - Smooth animations
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  ChevronLeft,
  ChevronRight,
  CheckSquare,
  Lightbulb,
  BarChart3,
  Menu,
  Star,
} from 'lucide-react';
import { clsx } from 'clsx';
import { useSidebar } from '@/contexts/SidebarContext';
import { ChecklistTab } from './sidebar/ChecklistTab';
import { TipsTab } from './sidebar/TipsTab';
import { ProgressTab } from './sidebar/ProgressTab';

// =============================================================================
// TYPES
// =============================================================================

interface Tab {
  id: 'checklist' | 'tips' | 'progress';
  label: string;
  icon: React.ReactNode;
  badge?: number;
}

// =============================================================================
// COMPONENT
// =============================================================================

export function Sidebar() {
  const { state, toggleSidebar, setActiveTab, getChecklistStats } = useSidebar();
  const [isMobile, setIsMobile] = useState(false);

  // Detect mobile
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 1024);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const stats = getChecklistStats();

  const tabs: Tab[] = [
    {
      id: 'checklist',
      label: 'Checkliste',
      icon: <CheckSquare className="w-5 h-5" />,
      badge: stats.total - stats.completed,
    },
    {
      id: 'tips',
      label: 'Tipps',
      icon: <Lightbulb className="w-5 h-5" />,
      badge: state.starredTips.length > 0 ? state.starredTips.length : undefined,
    },
    {
      id: 'progress',
      label: 'Fortschritt',
      icon: <BarChart3 className="w-5 h-5" />,
    },
  ];

  // Mobile: Floating button when closed
  if (isMobile && !state.isOpen) {
    return (
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0, opacity: 0 }}
        onClick={toggleSidebar}
        className="fixed bottom-20 right-4 z-50 w-14 h-14 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg flex items-center justify-center"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Menu className="w-6 h-6" />
        {stats.total - stats.completed > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
            {stats.total - stats.completed}
          </span>
        )}
      </motion.button>
    );
  }

  // Desktop: Collapsed state
  if (!isMobile && !state.isOpen) {
    return (
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: 56 }}
        className="h-full bg-white border-l border-gray-200 flex flex-col items-center py-4 gap-2"
      >
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-lg hover:bg-gray-100 text-gray-600"
          title="Sidebar oeffnen"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>

        <div className="w-full h-px bg-gray-200 my-2" />

        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => {
              setActiveTab(tab.id);
              toggleSidebar();
            }}
            className={clsx(
              'relative p-2 rounded-lg transition-colors',
              state.activeTab === tab.id
                ? 'bg-primary-100 text-primary-600'
                : 'text-gray-500 hover:bg-gray-100'
            )}
            title={tab.label}
          >
            {tab.icon}
            {tab.badge && tab.badge > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[10px] rounded-full flex items-center justify-center">
                {tab.badge > 9 ? '9+' : tab.badge}
              </span>
            )}
          </button>
        ))}
      </motion.div>
    );
  }

  // Full sidebar content
  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <h2 className="font-semibold text-gray-900">Workshop-Assistent</h2>
        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500"
        >
          {isMobile ? <X className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={clsx(
              'flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors relative',
              state.activeTab === tab.id
                ? 'text-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            )}
          >
            {tab.icon}
            <span className="hidden sm:inline">{tab.label}</span>
            {tab.badge && tab.badge > 0 && (
              <span className={clsx(
                'w-5 h-5 text-xs rounded-full flex items-center justify-center',
                state.activeTab === tab.id
                  ? 'bg-primary-100 text-primary-600'
                  : 'bg-gray-100 text-gray-600'
              )}>
                {tab.badge > 9 ? '9+' : tab.badge}
              </span>
            )}
            {state.activeTab === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-500"
              />
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-hidden">
        <AnimatePresence mode="wait">
          {state.activeTab === 'checklist' && (
            <motion.div
              key="checklist"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="h-full"
            >
              <ChecklistTab />
            </motion.div>
          )}
          {state.activeTab === 'tips' && (
            <motion.div
              key="tips"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="h-full"
            >
              <TipsTab />
            </motion.div>
          )}
          {state.activeTab === 'progress' && (
            <motion.div
              key="progress"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="h-full"
            >
              <ProgressTab />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer with Progress Ring */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center gap-3">
          {/* Progress Ring */}
          <div className="relative w-12 h-12">
            <svg className="w-12 h-12 transform -rotate-90">
              <circle
                cx="24"
                cy="24"
                r="20"
                stroke="#E5E7EB"
                strokeWidth="4"
                fill="none"
              />
              <circle
                cx="24"
                cy="24"
                r="20"
                stroke="url(#progressGradient)"
                strokeWidth="4"
                fill="none"
                strokeDasharray={`${(stats.percentage / 100) * 125.6} 125.6`}
                strokeLinecap="round"
              />
              <defs>
                <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#10B981" />
                  <stop offset="100%" stopColor="#059669" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-sm font-bold text-gray-900">{stats.percentage}%</span>
            </div>
          </div>

          <div className="flex-1">
            <p className="text-sm font-medium text-gray-900">
              {stats.completed} von {stats.total} erledigt
            </p>
            <p className="text-xs text-gray-500">
              {stats.total - stats.completed > 0
                ? `Noch ${stats.total - stats.completed} Punkte offen`
                : 'Alle Punkte erledigt!'}
            </p>
          </div>

          {state.starredTips.length > 0 && (
            <div className="flex items-center gap-1 text-amber-500">
              <Star className="w-4 h-4 fill-current" />
              <span className="text-sm font-medium">{state.starredTips.length}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  // Mobile: Full screen overlay
  if (isMobile) {
    return (
      <AnimatePresence>
        {state.isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={toggleSidebar}
              className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40"
            />

            {/* Sidebar Panel */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="fixed right-0 top-0 bottom-0 w-full max-w-sm bg-white shadow-2xl z-50"
            >
              {sidebarContent}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    );
  }

  // Desktop: Side panel
  return (
    <motion.aside
      initial={{ width: 0, opacity: 0 }}
      animate={{ width: 360, opacity: 1 }}
      exit={{ width: 0, opacity: 0 }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="h-full bg-white border-l border-gray-200 overflow-hidden"
    >
      {sidebarContent}
    </motion.aside>
  );
}

export default Sidebar;
