/**
 * BATipp Component
 * Shows micro-education about Bundesagentur fur Arbeit requirements
 * Displays GZ compliance tips in a friendly, non-intrusive way
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Lightbulb, ChevronDown, ChevronUp, AlertTriangle, Info, CheckCircle } from 'lucide-react';
import { clsx } from 'clsx';

export type TippType = 'info' | 'warning' | 'success';

export interface BATippProps {
  /** The tip type - affects styling */
  type?: TippType;
  /** Short title/headline */
  title: string;
  /** The main tip content */
  content: string;
  /** Optional detailed explanation (expandable) */
  details?: string;
  /** Legal reference (e.g., "BA GZ 04, Frage 8") */
  legalRef?: string;
  /** Optional example */
  example?: string;
  /** Whether to start expanded */
  defaultExpanded?: boolean;
  /** Whether the tip can be dismissed */
  dismissable?: boolean;
  /** Callback when dismissed */
  onDismiss?: () => void;
}

const typeConfig = {
  info: {
    bgGradient: 'from-blue-50 to-blue-100/50',
    borderColor: 'border-blue-200',
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600',
    titleColor: 'text-blue-900',
    textColor: 'text-blue-700',
    Icon: Info,
  },
  warning: {
    bgGradient: 'from-amber-50 to-amber-100/50',
    borderColor: 'border-amber-200',
    iconBg: 'bg-amber-100',
    iconColor: 'text-amber-600',
    titleColor: 'text-amber-900',
    textColor: 'text-amber-700',
    Icon: AlertTriangle,
  },
  success: {
    bgGradient: 'from-emerald-50 to-emerald-100/50',
    borderColor: 'border-emerald-200',
    iconBg: 'bg-emerald-100',
    iconColor: 'text-emerald-600',
    titleColor: 'text-emerald-900',
    textColor: 'text-emerald-700',
    Icon: CheckCircle,
  },
};

export function BATipp({
  type = 'info',
  title,
  content,
  details,
  legalRef,
  example,
  defaultExpanded = false,
  dismissable = false,
  onDismiss,
}: BATippProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [isDismissed, setIsDismissed] = useState(false);

  const config = typeConfig[type];
  const { Icon } = config;

  const handleDismiss = () => {
    setIsDismissed(true);
    onDismiss?.();
  };

  if (isDismissed) {
    return null;
  }

  const hasExpandableContent = details || example;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={clsx(
        'rounded-xl border overflow-hidden',
        `bg-gradient-to-br ${config.bgGradient}`,
        config.borderColor
      )}
    >
      {/* Header */}
      <div className="px-4 py-3">
        <div className="flex items-start gap-3">
          {/* Icon */}
          <div
            className={clsx(
              'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
              config.iconBg
            )}
          >
            <Icon className={clsx('w-4 h-4', config.iconColor)} />
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2">
              <div>
                <h4 className={clsx('font-semibold text-sm', config.titleColor)}>
                  {title}
                </h4>
                {legalRef && (
                  <span
                    className={clsx(
                      'text-xs font-medium opacity-70',
                      config.textColor
                    )}
                  >
                    {legalRef}
                  </span>
                )}
              </div>

              {/* Dismiss Button */}
              {dismissable && (
                <button
                  onClick={handleDismiss}
                  className={clsx(
                    'text-xs opacity-50 hover:opacity-100 transition-opacity',
                    config.textColor
                  )}
                >
                  Verstanden
                </button>
              )}
            </div>

            <p className={clsx('text-sm mt-1', config.textColor)}>{content}</p>

            {/* Expand Button */}
            {hasExpandableContent && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className={clsx(
                  'flex items-center gap-1 text-xs font-medium mt-2',
                  config.iconColor,
                  'hover:underline'
                )}
              >
                {isExpanded ? (
                  <>
                    <ChevronUp className="w-3 h-3" />
                    <span>Weniger anzeigen</span>
                  </>
                ) : (
                  <>
                    <ChevronDown className="w-3 h-3" />
                    <span>Mehr erfahren</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Expandable Content */}
      <AnimatePresence>
        {isExpanded && hasExpandableContent && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div
              className={clsx(
                'px-4 pb-4 pt-2 border-t',
                config.borderColor,
                'bg-white/50'
              )}
            >
              {/* Details */}
              {details && (
                <div className="text-sm text-gray-600 mb-3">{details}</div>
              )}

              {/* Example */}
              {example && (
                <div className="bg-white rounded-lg p-3 border border-gray-100">
                  <div className="flex items-center gap-1.5 text-xs font-medium text-gray-500 mb-1">
                    <Lightbulb className="w-3 h-3" />
                    <span>Beispiel</span>
                  </div>
                  <p className="text-sm text-gray-700 italic">{example}</p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default BATipp;
