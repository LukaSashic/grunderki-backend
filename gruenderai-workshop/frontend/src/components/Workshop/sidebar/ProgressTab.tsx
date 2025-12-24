/**
 * ProgressTab Component
 *
 * Displays visual progress and collected data preview.
 * Features:
 * - Overall progress bar with percentage
 * - Section-by-section progress
 * - Collected data preview cards
 * - Missing fields indicator
 * - Next steps guidance
 * - GZ-Score preview
 */

import { useMemo } from 'react';
import { motion } from 'framer-motion';
import {
  Check,
  Clock,
  AlertCircle,
  ChevronRight,
  FileText,
  Target,
  TrendingUp,
  Sparkles,
  Lock,
  Star,
} from 'lucide-react';
import { clsx } from 'clsx';
import { useSidebar } from '@/contexts/SidebarContext';

// =============================================================================
// TYPES
// =============================================================================

interface SectionProgress {
  id: string;
  label: string;
  status: 'locked' | 'available' | 'in_progress' | 'completed';
  completedFields: number;
  totalFields: number;
  gzScore?: number;
}

interface CollectedField {
  id: string;
  label: string;
  value: string;
  status: 'complete' | 'partial' | 'missing';
}

// =============================================================================
// MOCK DATA (will be replaced with real data from store)
// =============================================================================

const MOCK_SECTIONS: SectionProgress[] = [
  { id: 'sektion_1', label: 'Geschaeftsmodell', status: 'in_progress', completedFields: 4, totalFields: 8, gzScore: 75 },
  { id: 'sektion_2', label: 'Zielgruppe', status: 'available', completedFields: 0, totalFields: 6 },
  { id: 'sektion_3', label: 'Markt & Wettbewerb', status: 'locked', completedFields: 0, totalFields: 6 },
  { id: 'sektion_4', label: 'Marketing', status: 'locked', completedFields: 0, totalFields: 6 },
  { id: 'sektion_5', label: 'Finanzplanung', status: 'locked', completedFields: 0, totalFields: 8 },
  { id: 'sektion_6', label: 'Strategie', status: 'locked', completedFields: 0, totalFields: 5 },
];

const MOCK_FIELDS: CollectedField[] = [
  { id: 'geschaeftsidee', label: 'Geschaeftsidee', value: 'Online-Coaching fuer Gruender', status: 'complete' },
  { id: 'business_type', label: 'Geschaeftstyp', value: 'Dienstleistung Online', status: 'complete' },
  { id: 'zielgruppe', label: 'Zielgruppe', value: 'Arbeitslose Gruender 30-50', status: 'partial' },
  { id: 'usp', label: 'USP', value: '', status: 'missing' },
];

// =============================================================================
// COMPONENTS
// =============================================================================

interface SectionCardProps {
  section: SectionProgress;
  isActive?: boolean;
}

function SectionCard({ section, isActive }: SectionCardProps) {
  const progress = section.totalFields > 0
    ? Math.round((section.completedFields / section.totalFields) * 100)
    : 0;

  const statusConfig = {
    locked: { icon: Lock, color: 'text-gray-400', bg: 'bg-gray-100' },
    available: { icon: ChevronRight, color: 'text-primary-500', bg: 'bg-primary-50' },
    in_progress: { icon: Clock, color: 'text-amber-500', bg: 'bg-amber-50' },
    completed: { icon: Check, color: 'text-emerald-500', bg: 'bg-emerald-50' },
  };

  const config = statusConfig[section.status];
  const Icon = config.icon;

  return (
    <motion.div
      whileHover={section.status !== 'locked' ? { scale: 1.02 } : undefined}
      className={clsx(
        'relative p-3 rounded-xl border-2 transition-all',
        section.status === 'locked'
          ? 'bg-gray-50 border-gray-100 opacity-60'
          : isActive
          ? 'bg-primary-50 border-primary-200 shadow-md'
          : 'bg-white border-gray-100 hover:border-primary-200 cursor-pointer'
      )}
    >
      <div className="flex items-center gap-3">
        {/* Status Icon */}
        <div className={clsx('w-8 h-8 rounded-lg flex items-center justify-center', config.bg)}>
          <Icon className={clsx('w-4 h-4', config.color)} />
        </div>

        {/* Section Info */}
        <div className="flex-1 min-w-0">
          <p className={clsx(
            'text-sm font-medium truncate',
            section.status === 'locked' ? 'text-gray-400' : 'text-gray-900'
          )}>
            {section.label}
          </p>
          <div className="flex items-center gap-2 mt-1">
            {/* Progress Bar */}
            <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                className={clsx(
                  'h-full rounded-full',
                  section.status === 'completed' ? 'bg-emerald-500' : 'bg-primary-500'
                )}
              />
            </div>
            <span className="text-xs text-gray-500">{progress}%</span>
          </div>
        </div>

        {/* GZ Score Badge */}
        {section.gzScore !== undefined && section.status !== 'locked' && (
          <div className={clsx(
            'px-2 py-1 rounded-lg text-xs font-bold',
            section.gzScore >= 80 ? 'bg-emerald-100 text-emerald-700' :
            section.gzScore >= 60 ? 'bg-amber-100 text-amber-700' :
            'bg-red-100 text-red-700'
          )}>
            {section.gzScore}%
          </div>
        )}
      </div>
    </motion.div>
  );
}

interface FieldPreviewCardProps {
  field: CollectedField;
}

function FieldPreviewCard({ field }: FieldPreviewCardProps) {
  const statusConfig = {
    complete: { icon: Check, color: 'text-emerald-500', bg: 'bg-emerald-50', border: 'border-emerald-200' },
    partial: { icon: Clock, color: 'text-amber-500', bg: 'bg-amber-50', border: 'border-amber-200' },
    missing: { icon: AlertCircle, color: 'text-red-500', bg: 'bg-red-50', border: 'border-red-200' },
  };

  const config = statusConfig[field.status];
  const Icon = config.icon;

  return (
    <div className={clsx(
      'p-3 rounded-lg border',
      config.bg,
      config.border
    )}>
      <div className="flex items-start gap-2">
        <Icon className={clsx('w-4 h-4 mt-0.5 flex-shrink-0', config.color)} />
        <div className="flex-1 min-w-0">
          <p className="text-xs text-gray-500">{field.label}</p>
          {field.value ? (
            <p className="text-sm font-medium text-gray-900 truncate">{field.value}</p>
          ) : (
            <p className="text-sm text-gray-400 italic">Noch nicht ausgefuellt</p>
          )}
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function ProgressTab() {
  const { state, getChecklistStats } = useSidebar();
  const stats = getChecklistStats();

  // Calculate overall progress
  const overallProgress = useMemo(() => {
    const totalFields = MOCK_SECTIONS.reduce((sum, s) => sum + s.totalFields, 0);
    const completedFields = MOCK_SECTIONS.reduce((sum, s) => sum + s.completedFields, 0);
    return totalFields > 0 ? Math.round((completedFields / totalFields) * 100) : 0;
  }, []);

  // Calculate estimated GZ Score
  const estimatedGzScore = useMemo(() => {
    const sectionsWithScore = MOCK_SECTIONS.filter(s => s.gzScore !== undefined);
    if (sectionsWithScore.length === 0) return null;
    const avg = sectionsWithScore.reduce((sum, s) => sum + (s.gzScore || 0), 0) / sectionsWithScore.length;
    return Math.round(avg);
  }, []);

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Overall Progress Header */}
      <div className="p-4 bg-gradient-to-r from-primary-50 to-blue-50 border-b border-primary-100">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="font-semibold text-gray-900">Gesamtfortschritt</h3>
            <p className="text-sm text-gray-600">Dein Businessplan</p>
          </div>
          <div className="relative w-16 h-16">
            <svg className="w-16 h-16 transform -rotate-90">
              <circle
                cx="32"
                cy="32"
                r="28"
                stroke="#E5E7EB"
                strokeWidth="6"
                fill="none"
              />
              <motion.circle
                cx="32"
                cy="32"
                r="28"
                stroke="url(#progressGradient2)"
                strokeWidth="6"
                fill="none"
                initial={{ strokeDasharray: '0 176' }}
                animate={{ strokeDasharray: `${(overallProgress / 100) * 176} 176` }}
                strokeLinecap="round"
              />
              <defs>
                <linearGradient id="progressGradient2" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#10B981" />
                  <stop offset="100%" stopColor="#059669" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-lg font-bold text-gray-900">{overallProgress}%</span>
            </div>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-2">
          <div className="bg-white/60 rounded-lg p-2 text-center">
            <p className="text-lg font-bold text-primary-600">
              {MOCK_SECTIONS.filter(s => s.status === 'completed').length}/{MOCK_SECTIONS.length}
            </p>
            <p className="text-xs text-gray-500">Module</p>
          </div>
          <div className="bg-white/60 rounded-lg p-2 text-center">
            <p className="text-lg font-bold text-emerald-600">{stats.completed}/{stats.total}</p>
            <p className="text-xs text-gray-500">Checkliste</p>
          </div>
          <div className="bg-white/60 rounded-lg p-2 text-center">
            <p className={clsx(
              'text-lg font-bold',
              estimatedGzScore && estimatedGzScore >= 80 ? 'text-emerald-600' :
              estimatedGzScore && estimatedGzScore >= 60 ? 'text-amber-600' :
              'text-gray-400'
            )}>
              {estimatedGzScore ? `${estimatedGzScore}%` : '—'}
            </p>
            <p className="text-xs text-gray-500">GZ-Score</p>
          </div>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto">
        {/* Sections Progress */}
        <div className="p-4">
          <div className="flex items-center gap-2 mb-3">
            <Target className="w-4 h-4 text-primary-500" />
            <h4 className="font-medium text-gray-900">Module</h4>
          </div>
          <div className="space-y-2">
            {MOCK_SECTIONS.map((section, idx) => (
              <SectionCard
                key={section.id}
                section={section}
                isActive={section.status === 'in_progress'}
              />
            ))}
          </div>
        </div>

        {/* Collected Data Preview */}
        <div className="p-4 border-t border-gray-100">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-primary-500" />
              <h4 className="font-medium text-gray-900">Gesammelte Daten</h4>
            </div>
            <span className="text-xs text-gray-500">
              {MOCK_FIELDS.filter(f => f.status === 'complete').length}/{MOCK_FIELDS.length} komplett
            </span>
          </div>
          <div className="space-y-2">
            {MOCK_FIELDS.slice(0, 4).map(field => (
              <FieldPreviewCard key={field.id} field={field} />
            ))}
            {MOCK_FIELDS.length > 4 && (
              <button className="w-full py-2 text-sm text-primary-600 hover:text-primary-700 font-medium">
                + {MOCK_FIELDS.length - 4} weitere anzeigen
              </button>
            )}
          </div>
        </div>

        {/* Next Steps */}
        <div className="p-4 border-t border-gray-100">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <h4 className="font-medium text-gray-900">Naechste Schritte</h4>
          </div>
          <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-4 border border-amber-100">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center flex-shrink-0">
                <TrendingUp className="w-4 h-4 text-amber-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900 mb-1">USP definieren</p>
                <p className="text-sm text-gray-600">
                  Dein Alleinstellungsmerkmal ist entscheidend fuer den GZ-Antrag.
                </p>
                <button className="mt-2 text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1">
                  Jetzt beantworten
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProgressTab;
