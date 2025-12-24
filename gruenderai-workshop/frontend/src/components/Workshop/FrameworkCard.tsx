/**
 * GründerAI Workshop - Framework Card Component
 * Educational component that teaches business frameworks
 * Examples: Jobs-to-be-Done, Gründer-Business Fit, Transferable Skills
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Lightbulb,
  ChevronDown,
  ExternalLink,
  BookOpen,
  Target,
  Users,
  Briefcase
} from 'lucide-react';
import type { Framework } from '@/types/module1.types';
import { FRAMEWORKS } from '@/types/module1.types';

interface FrameworkCardProps {
  frameworkId: string;
  variant?: 'default' | 'compact' | 'expanded';
  showTitle?: boolean;
}

export const FrameworkCard: React.FC<FrameworkCardProps> = ({
  frameworkId,
  variant = 'default',
  showTitle = true
}) => {
  const [isExpanded, setIsExpanded] = useState(variant === 'expanded');

  const framework = FRAMEWORKS[frameworkId];

  if (!framework) {
    console.warn(`Framework not found: ${frameworkId}`);
    return null;
  }

  const getFrameworkIcon = (id: string) => {
    switch (id) {
      case 'jobs_to_be_done':
        return Target;
      case 'gruender_business_fit':
        return Users;
      case 'transferable_skills':
        return Briefcase;
      case 'rechtsformwahl':
        return BookOpen;
      default:
        return Lightbulb;
    }
  };

  const Icon = getFrameworkIcon(frameworkId);

  // Compact variant - just a button to expand
  if (variant === 'compact') {
    return (
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="inline-flex items-center gap-1.5 text-sm text-accent-600 hover:text-accent-800 transition-colors"
      >
        <Lightbulb className="w-4 h-4" />
        <span>Was ist "{framework.name}"?</span>
        <ChevronDown className={`w-3 h-3 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
      </button>
    );
  }

  return (
    <motion.div
      className="framework-card bg-gradient-to-br from-accent-50 to-primary-50 rounded-xl border border-accent-200 overflow-hidden"
      layout
    >
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-5 flex items-start justify-between text-left"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-accent-500 flex items-center justify-center flex-shrink-0">
            <Icon className="w-5 h-5 text-white" />
          </div>
          <div>
            {showTitle && (
              <p className="text-xs text-accent-600 font-medium mb-0.5">Framework</p>
            )}
            <h4 className="font-display text-lg text-primary-900">{framework.name}</h4>
            {framework.author && (
              <p className="text-xs text-warm-500">von {framework.author}</p>
            )}
          </div>
        </div>
        <ChevronDown
          className={`w-5 h-5 text-warm-400 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
        />
      </button>

      {/* Content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: 'auto' }}
            exit={{ height: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-5 pt-0">
              {/* Summary */}
              <p className="text-warm-700 mb-4">{framework.summary}</p>

              {/* Example */}
              {framework.example && (
                <div className="bg-white/50 rounded-lg p-4 mb-4">
                  <p className="text-sm">
                    <span className="text-accent-600 mr-2">💡</span>
                    <span className="text-warm-600 italic">{framework.example}</span>
                  </p>
                </div>
              )}

              {/* How to Apply */}
              {framework.howToApply && framework.howToApply.length > 0 && (
                <div className="mb-4">
                  <h5 className="text-sm font-medium text-primary-800 mb-2">
                    So wendest du es an:
                  </h5>
                  <ul className="space-y-2">
                    {framework.howToApply.map((step, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-warm-700">
                        <span className="text-accent-600 flex-shrink-0">→</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Dimensions */}
              {framework.dimensions && framework.dimensions.length > 0 && (
                <div className="mb-4">
                  <h5 className="text-sm font-medium text-primary-800 mb-2">
                    Die 4 Dimensionen:
                  </h5>
                  <div className="grid grid-cols-2 gap-2">
                    {framework.dimensions.map((dim, i) => (
                      <div
                        key={i}
                        className="bg-white/50 rounded-lg p-3"
                      >
                        <p className="text-sm font-medium text-warm-800">{dim.name}</p>
                        <p className="text-xs text-warm-500 mt-1">{dim.question}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Categories (for transferable skills) */}
              {framework.categories && framework.categories.length > 0 && (
                <div>
                  <h5 className="text-sm font-medium text-primary-800 mb-2">
                    Kategorien:
                  </h5>
                  <div className="space-y-3">
                    {framework.categories.map((cat, i) => (
                      <div key={i}>
                        <p className="text-sm font-medium text-warm-800 mb-1">{cat.name}</p>
                        <div className="flex flex-wrap gap-1">
                          {cat.examples.map((ex, j) => (
                            <span
                              key={j}
                              className="px-2 py-1 bg-white/70 rounded text-xs text-warm-600"
                            >
                              {ex}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// =============================================================================
// FRAMEWORK SELECTOR (for choosing which framework to show)
// =============================================================================

interface FrameworkSelectorProps {
  availableFrameworks: string[];
  selectedFramework: string | null;
  onSelect: (frameworkId: string) => void;
}

export const FrameworkSelector: React.FC<FrameworkSelectorProps> = ({
  availableFrameworks,
  selectedFramework,
  onSelect
}) => {
  return (
    <div className="framework-selector">
      <p className="text-sm text-warm-600 mb-2">Hilfreiche Frameworks:</p>
      <div className="flex flex-wrap gap-2">
        {availableFrameworks.map(fwId => {
          const fw = FRAMEWORKS[fwId];
          if (!fw) return null;

          return (
            <button
              key={fwId}
              onClick={() => onSelect(fwId)}
              className={`
                px-3 py-1.5 rounded-lg text-sm transition-all
                ${selectedFramework === fwId
                  ? 'bg-accent-500 text-white'
                  : 'bg-warm-100 text-warm-700 hover:bg-warm-200'
                }
              `}
            >
              {fw.name}
            </button>
          );
        })}
      </div>
    </div>
  );
};

// =============================================================================
// INLINE FRAMEWORK HINT (small tooltip-style hint)
// =============================================================================

interface FrameworkHintProps {
  frameworkId: string;
  onExpand?: () => void;
}

export const FrameworkHint: React.FC<FrameworkHintProps> = ({
  frameworkId,
  onExpand
}) => {
  const framework = FRAMEWORKS[frameworkId];

  if (!framework) return null;

  return (
    <div className="framework-hint inline-flex items-center gap-1.5 bg-accent-50 border border-accent-200 rounded-lg px-3 py-1.5">
      <Lightbulb className="w-4 h-4 text-accent-600" />
      <span className="text-sm text-accent-800">
        Tipp: Denke an <strong>{framework.name}</strong>
      </span>
      {onExpand && (
        <button
          onClick={onExpand}
          className="text-xs text-accent-600 hover:text-accent-800 underline ml-1"
        >
          Mehr erfahren
        </button>
      )}
    </div>
  );
};

// =============================================================================
// RECHTSFORM COMPARISON TABLE
// =============================================================================

interface RechtsformOption {
  value: string;
  label: string;
  pros: string[];
  cons: string[];
}

interface RechtsformComparisonProps {
  options: RechtsformOption[];
  selectedValue?: string;
  onSelect?: (value: string) => void;
}

export const RechtsformComparison: React.FC<RechtsformComparisonProps> = ({
  options,
  selectedValue,
  onSelect
}) => {
  return (
    <div className="rechtsform-comparison overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-warm-200">
            <th className="text-left py-2 px-3 font-medium text-warm-700">Rechtsform</th>
            <th className="text-left py-2 px-3 font-medium text-green-700">Vorteile</th>
            <th className="text-left py-2 px-3 font-medium text-amber-700">Nachteile</th>
            <th className="py-2 px-3"></th>
          </tr>
        </thead>
        <tbody>
          {options.map(option => (
            <tr
              key={option.value}
              className={`border-b border-warm-100 ${
                selectedValue === option.value ? 'bg-primary-50' : ''
              }`}
            >
              <td className="py-3 px-3 font-medium text-warm-800">
                {option.label}
              </td>
              <td className="py-3 px-3">
                <ul className="space-y-1">
                  {option.pros.map((pro, i) => (
                    <li key={i} className="text-green-700 text-xs">+ {pro}</li>
                  ))}
                </ul>
              </td>
              <td className="py-3 px-3">
                <ul className="space-y-1">
                  {option.cons.map((con, i) => (
                    <li key={i} className="text-amber-700 text-xs">- {con}</li>
                  ))}
                </ul>
              </td>
              <td className="py-3 px-3">
                {onSelect && (
                  <button
                    onClick={() => onSelect(option.value)}
                    className={`px-3 py-1 rounded text-xs ${
                      selectedValue === option.value
                        ? 'bg-primary-500 text-white'
                        : 'bg-warm-100 text-warm-600 hover:bg-warm-200'
                    }`}
                  >
                    {selectedValue === option.value ? 'Ausgewählt' : 'Wählen'}
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FrameworkCard;
