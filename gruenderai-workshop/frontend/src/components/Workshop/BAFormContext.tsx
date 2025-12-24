/**
 * GründerAI Workshop - BA Form Context Component
 * Shows BA GZ 04 context for transparency - helps users understand
 * why each question matters for their Gründungszuschuss application
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileText, ChevronDown, AlertTriangle, CheckCircle, HelpCircle } from 'lucide-react';
import type { BAFormContext as BAFormContextType, GZDoorStatus } from '@/types/module1.types';

interface BAFormContextProps {
  context: BAFormContextType;
  gzDoorStatus: GZDoorStatus;
  compact?: boolean;
}

export const BAFormContext: React.FC<BAFormContextProps> = ({
  context,
  gzDoorStatus,
  compact = false
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getStatusConfig = (status: GZDoorStatus) => {
    switch (status) {
      case 'passed':
        return {
          label: 'Bestanden',
          icon: '✓',
          bgClass: 'bg-green-100',
          textClass: 'text-green-700',
          borderClass: 'border-green-200'
        };
      case 'checking':
        return {
          label: 'Prüfung',
          icon: '🔄',
          bgClass: 'bg-blue-100',
          textClass: 'text-blue-700',
          borderClass: 'border-blue-200'
        };
      case 'failed':
        return {
          label: 'Risiko',
          icon: '⚠️',
          bgClass: 'bg-red-100',
          textClass: 'text-red-700',
          borderClass: 'border-red-200'
        };
      default:
        return {
          label: 'Offen',
          icon: '🔒',
          bgClass: 'bg-warm-100',
          textClass: 'text-warm-600',
          borderClass: 'border-warm-200'
        };
    }
  };

  const statusConfig = getStatusConfig(gzDoorStatus);

  if (compact) {
    return (
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="inline-flex items-center gap-1.5 text-xs text-primary-600 hover:text-primary-800 transition-colors"
      >
        <FileText className="w-3 h-3" />
        <span className="font-mono">
          BA {context.formular} – Frage {context.frageNummer}
        </span>
        <HelpCircle className="w-3 h-3" />
      </button>
    );
  }

  return (
    <div className="ba-form-context mb-4">
      {/* Compact Header - Always Visible */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between gap-2 text-sm text-primary-600 hover:text-primary-800 transition-colors py-2"
      >
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4" />
          <span className="font-mono font-medium">
            BA {context.formular} – Frage {context.frageNummer}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Status Badge */}
          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusConfig.bgClass} ${statusConfig.textClass}`}>
            {statusConfig.icon} {statusConfig.label}
          </span>

          {/* Expand Icon */}
          <ChevronDown
            className={`w-4 h-4 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
          />
        </div>
      </button>

      {/* Expanded Content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className={`mt-2 bg-primary-50 border ${statusConfig.borderClass} rounded-xl p-4`}>
              {/* Original Wortlaut */}
              <blockquote className="border-l-4 border-primary-300 pl-4 mb-4 italic text-primary-800 text-sm">
                "{context.originalWortlaut}"
              </blockquote>

              {/* Warum wichtig */}
              <div className={`rounded-lg p-3 mb-3 ${
                context.warumWichtig.includes('KRITISCH') || context.warumWichtig.includes('65%')
                  ? 'bg-amber-50 border border-amber-200'
                  : 'bg-blue-50 border border-blue-100'
              }`}>
                <div className="flex items-start gap-2">
                  <AlertTriangle className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                    context.warumWichtig.includes('KRITISCH') || context.warumWichtig.includes('65%')
                      ? 'text-amber-600'
                      : 'text-blue-600'
                  }`} />
                  <div>
                    <span className={`font-medium text-sm ${
                      context.warumWichtig.includes('KRITISCH') || context.warumWichtig.includes('65%')
                        ? 'text-amber-900'
                        : 'text-blue-900'
                    }`}>
                      Warum das wichtig ist:
                    </span>
                    <p className={`text-sm mt-1 ${
                      context.warumWichtig.includes('KRITISCH') || context.warumWichtig.includes('65%')
                        ? 'text-amber-800'
                        : 'text-blue-800'
                    }`}>
                      {context.warumWichtig}
                    </p>
                  </div>
                </div>
              </div>

              {/* Wie wir helfen */}
              <div className="flex items-start gap-2 text-sm text-primary-700">
                <CheckCircle className="w-4 h-4 text-primary-600 mt-0.5 flex-shrink-0" />
                <p>{context.wieWirHelfen}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// =============================================================================
// BA FORM SUMMARY CARD (for module overview)
// =============================================================================

interface BAFormSummaryProps {
  relevantQuestions: number[];
  moduleTitle: string;
}

export const BAFormSummary: React.FC<BAFormSummaryProps> = ({
  relevantQuestions,
  moduleTitle
}) => {
  return (
    <div className="bg-warm-50 rounded-xl p-4 border border-warm-200">
      <div className="flex items-center gap-2 mb-3">
        <FileText className="w-5 h-5 text-primary-600" />
        <h4 className="font-medium text-warm-900">Agentur-Anforderungen</h4>
      </div>

      <p className="text-sm text-warm-600 mb-3">
        Dieses Modul ({moduleTitle}) beantwortet folgende Fragen im Gründungszuschuss-Antrag:
      </p>

      <div className="flex flex-wrap gap-2">
        {relevantQuestions.map(q => (
          <span
            key={q}
            className="px-3 py-1 bg-primary-100 text-primary-700 text-sm font-mono rounded-full"
          >
            Frage {q}
          </span>
        ))}
      </div>
    </div>
  );
};

export default BAFormContext;
