/**
 * TipsTab Component
 *
 * Displays contextual tips with starring functionality.
 * Features:
 * - Categorized tips (fact, warning, motivation, expert, success)
 * - Star/unstar functionality
 * - Search filter
 * - Export starred tips
 * - Category filter
 */

import { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Star,
  Search,
  Download,
  Lightbulb,
  AlertTriangle,
  Sparkles,
  GraduationCap,
  Trophy,
  TrendingUp,
  Copy,
  Check,
  Filter,
} from 'lucide-react';
import { clsx } from 'clsx';
import { useSidebar, type StarredTip } from '@/contexts/SidebarContext';
import { microTipsApi } from '@/services/api';

// =============================================================================
// TYPES
// =============================================================================

interface Tip {
  id: string;
  text: string;
  type: 'fact' | 'warning' | 'motivation' | 'expert' | 'success';
  category?: string;
}

// =============================================================================
// HELPERS
// =============================================================================

const CATEGORY_CONFIG = {
  fact: {
    icon: TrendingUp,
    label: 'Fakt',
    color: 'text-blue-600',
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    emoji: '📊',
  },
  warning: {
    icon: AlertTriangle,
    label: 'Achtung',
    color: 'text-amber-600',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    emoji: '⚠️',
  },
  motivation: {
    icon: Sparkles,
    label: 'Motivation',
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
    emoji: '💪',
  },
  expert: {
    icon: GraduationCap,
    label: 'Experten-Tipp',
    color: 'text-purple-600',
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    emoji: '🎓',
  },
  success: {
    icon: Trophy,
    label: 'Erfolg',
    color: 'text-green-600',
    bg: 'bg-green-50',
    border: 'border-green-200',
    emoji: '✨',
  },
};

// =============================================================================
// COMPONENTS
// =============================================================================

interface TipCardProps {
  tip: Tip;
  isStarred: boolean;
  onStar: () => void;
  onUnstar: () => void;
}

function TipCard({ tip, isStarred, onStar, onUnstar }: TipCardProps) {
  const [copied, setCopied] = useState(false);
  const config = CATEGORY_CONFIG[tip.type];
  const Icon = config.icon;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(tip.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className={clsx(
        'group relative p-4 rounded-xl border-2 transition-all',
        config.bg,
        config.border,
        isStarred && 'ring-2 ring-amber-300'
      )}
    >
      {/* Category Badge */}
      <div className="flex items-center gap-2 mb-2">
        <span className="text-lg">{config.emoji}</span>
        <span className={clsx('text-xs font-medium', config.color)}>
          {config.label}
        </span>
      </div>

      {/* Tip Text */}
      <p className="text-sm text-gray-800 leading-relaxed pr-8">{tip.text}</p>

      {/* Actions */}
      <div className="absolute top-3 right-3 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
        {/* Copy Button */}
        <button
          onClick={handleCopy}
          className="p-1.5 rounded-lg hover:bg-white/50 text-gray-500 hover:text-gray-700"
          title="Kopieren"
        >
          {copied ? (
            <Check className="w-4 h-4 text-emerald-500" />
          ) : (
            <Copy className="w-4 h-4" />
          )}
        </button>

        {/* Star Button */}
        <button
          onClick={isStarred ? onUnstar : onStar}
          className={clsx(
            'p-1.5 rounded-lg transition-colors',
            isStarred
              ? 'text-amber-500 hover:bg-amber-100'
              : 'text-gray-400 hover:text-amber-500 hover:bg-white/50'
          )}
          title={isStarred ? 'Stern entfernen' : 'Merken'}
        >
          <Star className={clsx('w-4 h-4', isStarred && 'fill-current')} />
        </button>
      </div>
    </motion.div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function TipsTab() {
  const { state, starTip, unstarTip, isStarred } = useSidebar();
  const [tips, setTips] = useState<Tip[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [showStarredOnly, setShowStarredOnly] = useState(false);

  // Fetch tips from API
  useEffect(() => {
    const fetchTips = async () => {
      setIsLoading(true);
      try {
        const response = await microTipsApi.getTips('sektion_1_geschaeftsmodell', undefined, true);
        if (response.tips) {
          setTips(
            response.tips.map((t, idx) => ({
              id: `tip-${idx}-${Date.now()}`,
              text: t.text,
              type: t.type as Tip['type'],
            }))
          );
        }
      } catch (error) {
        console.warn('[TipsTab] Failed to fetch tips:', error);
        // Use fallback tips
        setTips([
          { id: '1', text: 'Der Gruendungszuschuss betraegt ALG I + 300 EUR/Monat fuer 6 Monate.', type: 'fact' },
          { id: '2', text: '65% der GZ-Ablehnungen scheitern an mangelnden Fachkenntnissen.', type: 'warning' },
          { id: '3', text: 'Du investierst in deine Zukunft - das zahlt sich aus!', type: 'motivation' },
          { id: '4', text: 'Fachkundige Stelle: IHK, Steuerberatung oder Gruendungszentrum.', type: 'expert' },
          { id: '5', text: 'Jeder Schritt bringt dich deinem Ziel naeher!', type: 'success' },
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTips();
  }, []);

  // Filter tips
  const filteredTips = useMemo(() => {
    let result = tips;

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(tip => tip.text.toLowerCase().includes(query));
    }

    // Category filter
    if (selectedCategory) {
      result = result.filter(tip => tip.type === selectedCategory);
    }

    // Starred only filter
    if (showStarredOnly) {
      const starredIds = new Set(state.starredTips.map(t => t.id));
      result = result.filter(tip => starredIds.has(tip.id));
    }

    return result;
  }, [tips, searchQuery, selectedCategory, showStarredOnly, state.starredTips]);

  // Export starred tips
  const handleExport = () => {
    const content = state.starredTips
      .map(tip => `${tip.icon} ${tip.text}`)
      .join('\n\n');

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'gruenderai-tipps.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header with Search & Filters */}
      <div className="p-4 border-b border-gray-100 space-y-3">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Tipps durchsuchen..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        {/* Filter Row */}
        <div className="flex items-center justify-between">
          {/* Category Pills */}
          <div className="flex gap-1 overflow-x-auto pb-1">
            <button
              onClick={() => setSelectedCategory(null)}
              className={clsx(
                'px-2.5 py-1 text-xs font-medium rounded-full whitespace-nowrap transition-colors',
                !selectedCategory
                  ? 'bg-primary-100 text-primary-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              )}
            >
              Alle
            </button>
            {Object.entries(CATEGORY_CONFIG).map(([key, config]) => (
              <button
                key={key}
                onClick={() => setSelectedCategory(key)}
                className={clsx(
                  'px-2.5 py-1 text-xs font-medium rounded-full whitespace-nowrap transition-colors flex items-center gap-1',
                  selectedCategory === key
                    ? `${config.bg} ${config.color}`
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                )}
              >
                <span>{config.emoji}</span>
              </button>
            ))}
          </div>

          {/* Starred Only Toggle */}
          <button
            onClick={() => setShowStarredOnly(!showStarredOnly)}
            className={clsx(
              'flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium transition-colors',
              showStarredOnly
                ? 'bg-amber-100 text-amber-700'
                : 'text-gray-500 hover:bg-gray-100'
            )}
          >
            <Star className={clsx('w-3.5 h-3.5', showStarredOnly && 'fill-current')} />
            {state.starredTips.length}
          </button>
        </div>
      </div>

      {/* Tips List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : filteredTips.length === 0 ? (
          <div className="text-center py-12">
            <Lightbulb className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-sm text-gray-500">
              {showStarredOnly
                ? 'Keine gemerkten Tipps vorhanden.'
                : 'Keine Tipps gefunden.'}
            </p>
          </div>
        ) : (
          <AnimatePresence mode="popLayout">
            {filteredTips.map(tip => (
              <TipCard
                key={tip.id}
                tip={tip}
                isStarred={isStarred(tip.id)}
                onStar={() =>
                  starTip({
                    id: tip.id,
                    text: tip.text,
                    category: tip.type,
                    icon: CATEGORY_CONFIG[tip.type].emoji,
                  })
                }
                onUnstar={() => unstarTip(tip.id)}
              />
            ))}
          </AnimatePresence>
        )}
      </div>

      {/* Export Footer */}
      {state.starredTips.length > 0 && (
        <div className="p-4 border-t border-gray-100">
          <button
            onClick={handleExport}
            className="w-full flex items-center justify-center gap-2 py-2.5 bg-primary-50 hover:bg-primary-100 text-primary-700 font-medium rounded-lg transition-colors"
          >
            <Download className="w-4 h-4" />
            {state.starredTips.length} Tipps exportieren
          </button>
        </div>
      )}
    </div>
  );
}

export default TipsTab;
