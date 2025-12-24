/**
 * ChecklistTab Component
 *
 * Displays GZ-relevant checklist items organized by section.
 * Features:
 * - Grouped by section
 * - Status indicators (pending, in_progress, completed, skipped)
 * - Priority badges (required, recommended, optional)
 * - Jump to question functionality
 * - Filter by status
 */

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Check,
  Circle,
  Clock,
  SkipForward,
  ChevronDown,
  ChevronRight,
  AlertCircle,
  ArrowRight,
  Search,
  Filter,
} from 'lucide-react';
import { clsx } from 'clsx';
import { useSidebar, type ChecklistItem } from '@/contexts/SidebarContext';

// =============================================================================
// HELPERS
// =============================================================================

const STATUS_CONFIG = {
  pending: {
    icon: Circle,
    color: 'text-gray-400',
    bg: 'bg-gray-100',
    label: 'Offen',
  },
  in_progress: {
    icon: Clock,
    color: 'text-amber-500',
    bg: 'bg-amber-50',
    label: 'In Bearbeitung',
  },
  completed: {
    icon: Check,
    color: 'text-emerald-500',
    bg: 'bg-emerald-50',
    label: 'Erledigt',
  },
  skipped: {
    icon: SkipForward,
    color: 'text-gray-400',
    bg: 'bg-gray-50',
    label: 'Uebersprungen',
  },
};

const PRIORITY_CONFIG = {
  required: {
    label: 'Pflicht',
    color: 'text-red-600',
    bg: 'bg-red-50',
    border: 'border-red-200',
  },
  recommended: {
    label: 'Empfohlen',
    color: 'text-amber-600',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
  },
  optional: {
    label: 'Optional',
    color: 'text-gray-500',
    bg: 'bg-gray-50',
    border: 'border-gray-200',
  },
};

const SECTION_LABELS: Record<string, string> = {
  sektion_1_geschaeftsmodell: 'Modul 1: Geschaeftsmodell',
  sektion_2_zielgruppe: 'Modul 2: Zielgruppe',
  sektion_3_markt: 'Modul 3: Markt & Wettbewerb',
  sektion_4_marketing: 'Modul 4: Marketing',
  sektion_5_finanzen: 'Modul 5: Finanzplanung',
  sektion_6_strategie: 'Modul 6: Strategie',
};

// =============================================================================
// COMPONENTS
// =============================================================================

interface ChecklistItemRowProps {
  item: ChecklistItem;
  onStatusChange: (status: ChecklistItem['status']) => void;
  onJumpTo: () => void;
}

function ChecklistItemRow({ item, onStatusChange, onJumpTo }: ChecklistItemRowProps) {
  const statusConfig = STATUS_CONFIG[item.status];
  const priorityConfig = PRIORITY_CONFIG[item.priority];
  const StatusIcon = statusConfig.icon;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={clsx(
        'group flex items-start gap-3 p-3 rounded-lg border transition-all',
        item.status === 'completed'
          ? 'bg-emerald-50/50 border-emerald-100'
          : 'bg-white border-gray-100 hover:border-primary-200 hover:shadow-sm'
      )}
    >
      {/* Status Toggle */}
      <button
        onClick={() => {
          if (item.status === 'completed') {
            onStatusChange('pending');
          } else {
            onStatusChange('completed');
          }
        }}
        className={clsx(
          'flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-colors',
          statusConfig.bg,
          statusConfig.color,
          'hover:ring-2 hover:ring-primary-200'
        )}
      >
        <StatusIcon className="w-4 h-4" />
      </button>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-start gap-2">
          <p
            className={clsx(
              'text-sm font-medium',
              item.status === 'completed' ? 'text-gray-500 line-through' : 'text-gray-900'
            )}
          >
            {item.label}
          </p>
          {item.gzRelevant && (
            <span className="flex-shrink-0 px-1.5 py-0.5 text-[10px] font-medium bg-blue-100 text-blue-700 rounded">
              GZ
            </span>
          )}
        </div>

        {item.description && (
          <p className="mt-0.5 text-xs text-gray-500 line-clamp-2">{item.description}</p>
        )}

        <div className="mt-2 flex items-center gap-2">
          <span
            className={clsx(
              'px-1.5 py-0.5 text-[10px] font-medium rounded border',
              priorityConfig.bg,
              priorityConfig.color,
              priorityConfig.border
            )}
          >
            {priorityConfig.label}
          </span>
          <span className="text-[10px] text-gray-400">{statusConfig.label}</span>
        </div>
      </div>

      {/* Jump to Question */}
      {item.fieldId && item.status !== 'completed' && (
        <button
          onClick={onJumpTo}
          className="flex-shrink-0 p-1.5 rounded-lg text-gray-400 hover:text-primary-600 hover:bg-primary-50 opacity-0 group-hover:opacity-100 transition-all"
          title="Zur Frage springen"
        >
          <ArrowRight className="w-4 h-4" />
        </button>
      )}
    </motion.div>
  );
}

interface SectionGroupProps {
  sectionId: string;
  items: ChecklistItem[];
  isExpanded: boolean;
  onToggle: () => void;
  onUpdateItem: (id: string, status: ChecklistItem['status']) => void;
  onJumpTo: (fieldId: string) => void;
}

function SectionGroup({
  sectionId,
  items,
  isExpanded,
  onToggle,
  onUpdateItem,
  onJumpTo,
}: SectionGroupProps) {
  const completedCount = items.filter(i => i.status === 'completed').length;
  const hasRequired = items.some(i => i.priority === 'required' && i.status !== 'completed');

  return (
    <div className="border-b border-gray-100 last:border-0">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <motion.div
            animate={{ rotate: isExpanded ? 90 : 0 }}
            transition={{ duration: 0.2 }}
          >
            <ChevronRight className="w-4 h-4 text-gray-400" />
          </motion.div>
          <div className="text-left">
            <p className="text-sm font-medium text-gray-900">
              {SECTION_LABELS[sectionId] || sectionId}
            </p>
            <p className="text-xs text-gray-500">
              {completedCount} von {items.length} erledigt
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {hasRequired && (
            <AlertCircle className="w-4 h-4 text-red-500" />
          )}
          <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-emerald-500 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${(completedCount / items.length) * 100}%` }}
            />
          </div>
        </div>
      </button>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 space-y-2">
              {items.map(item => (
                <ChecklistItemRow
                  key={item.id}
                  item={item}
                  onStatusChange={(status) => onUpdateItem(item.id, status)}
                  onJumpTo={() => item.fieldId && onJumpTo(item.fieldId)}
                />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function ChecklistTab() {
  const { state, dispatch, updateChecklistItem, jumpToQuestion } = useSidebar();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'pending' | 'completed'>('all');

  // Group items by section
  const groupedItems = useMemo(() => {
    let items = state.checklistItems;

    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      items = items.filter(
        item =>
          item.label.toLowerCase().includes(query) ||
          item.description?.toLowerCase().includes(query)
      );
    }

    // Apply status filter
    if (filterStatus !== 'all') {
      items = items.filter(item =>
        filterStatus === 'completed'
          ? item.status === 'completed'
          : item.status !== 'completed'
      );
    }

    // Group by section
    const groups: Record<string, ChecklistItem[]> = {};
    items.forEach(item => {
      if (!groups[item.sectionId]) {
        groups[item.sectionId] = [];
      }
      groups[item.sectionId].push(item);
    });

    return groups;
  }, [state.checklistItems, searchQuery, filterStatus]);

  const toggleSection = (sectionId: string) => {
    dispatch({ type: 'TOGGLE_SECTION', payload: sectionId });
  };

  // Empty state
  if (state.checklistItems.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-6 text-center">
        <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
          <Check className="w-8 h-8 text-gray-400" />
        </div>
        <h3 className="font-medium text-gray-900 mb-1">Keine Checkliste</h3>
        <p className="text-sm text-gray-500">
          Starte den Workshop, um deine Checkliste zu sehen.
        </p>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Search & Filter */}
      <div className="p-4 border-b border-gray-100 space-y-3">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Suchen..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        {/* Filter Pills */}
        <div className="flex gap-2">
          {(['all', 'pending', 'completed'] as const).map(status => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={clsx(
                'px-3 py-1.5 text-xs font-medium rounded-full transition-colors',
                filterStatus === status
                  ? 'bg-primary-100 text-primary-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              )}
            >
              {status === 'all' && 'Alle'}
              {status === 'pending' && 'Offen'}
              {status === 'completed' && 'Erledigt'}
            </button>
          ))}
        </div>
      </div>

      {/* Checklist Sections */}
      <div className="flex-1 overflow-y-auto">
        {Object.keys(groupedItems).length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <p className="text-sm">Keine Eintraege gefunden.</p>
          </div>
        ) : (
          Object.entries(groupedItems).map(([sectionId, items]) => (
            <SectionGroup
              key={sectionId}
              sectionId={sectionId}
              items={items}
              isExpanded={state.expandedSections.includes(sectionId)}
              onToggle={() => toggleSection(sectionId)}
              onUpdateItem={updateChecklistItem}
              onJumpTo={jumpToQuestion}
            />
          ))
        )}
      </div>
    </div>
  );
}

export default ChecklistTab;
