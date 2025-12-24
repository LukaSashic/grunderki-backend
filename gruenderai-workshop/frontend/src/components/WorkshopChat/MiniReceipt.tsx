/**
 * MiniReceipt Component
 * Shows a "receipt-style" summary at checkpoints for motivation
 * Displays collected data, progress, and next steps
 */

import { motion, AnimatePresence } from 'framer-motion';
import { Check, ChevronRight, Sparkles, Target, Clock } from 'lucide-react';
import { clsx } from 'clsx';

export interface ReceiptItem {
  label: string;
  value: string;
  isHighlight?: boolean;
}

export interface MiniReceiptProps {
  /** Title of the receipt */
  title: string;
  /** Subtitle or section name */
  subtitle?: string;
  /** Items to display */
  items: ReceiptItem[];
  /** Progress percentage */
  progress?: number;
  /** Time spent */
  timeSpent?: string;
  /** Next section hint */
  nextHint?: string;
  /** Whether to show in expanded mode */
  isExpanded?: boolean;
  /** Callback when "Continue" is clicked */
  onContinue?: () => void;
  /** Whether this is a final summary */
  isFinal?: boolean;
}

export function MiniReceipt({
  title,
  subtitle,
  items,
  progress,
  timeSpent,
  nextHint,
  isExpanded = true,
  onContinue,
  isFinal = false,
}: MiniReceiptProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className={clsx(
        'bg-gradient-to-br rounded-xl shadow-lg overflow-hidden',
        isFinal
          ? 'from-emerald-500 to-teal-600 text-white'
          : 'from-white to-gray-50 border border-gray-200'
      )}
    >
      {/* Header */}
      <div
        className={clsx(
          'px-5 py-4 border-b',
          isFinal ? 'border-emerald-400/30' : 'border-gray-100'
        )}
      >
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2">
              {isFinal ? (
                <Sparkles className="w-5 h-5 text-yellow-300" />
              ) : (
                <Check className="w-5 h-5 text-emerald-500" />
              )}
              <h3
                className={clsx(
                  'font-bold text-lg',
                  isFinal ? 'text-white' : 'text-gray-900'
                )}
              >
                {title}
              </h3>
            </div>
            {subtitle && (
              <p
                className={clsx(
                  'text-sm mt-0.5',
                  isFinal ? 'text-emerald-100' : 'text-gray-500'
                )}
              >
                {subtitle}
              </p>
            )}
          </div>

          {/* Progress Badge */}
          {progress !== undefined && (
            <div
              className={clsx(
                'px-3 py-1 rounded-full text-sm font-medium',
                isFinal
                  ? 'bg-white/20 text-white'
                  : 'bg-emerald-100 text-emerald-700'
              )}
            >
              {progress}% erledigt
            </div>
          )}
        </div>
      </div>

      {/* Items (Receipt Lines) */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className={clsx('px-5 py-4', isFinal ? 'space-y-2' : 'space-y-3')}>
              {items.map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className={clsx(
                    'flex justify-between items-start gap-4 text-sm',
                    item.isHighlight && !isFinal && 'bg-blue-50 -mx-2 px-2 py-1.5 rounded-lg'
                  )}
                >
                  <span
                    className={clsx(
                      'font-medium flex-shrink-0',
                      isFinal ? 'text-emerald-100' : 'text-gray-500'
                    )}
                  >
                    {item.label}:
                  </span>
                  <span
                    className={clsx(
                      'text-right',
                      isFinal
                        ? 'text-white font-medium'
                        : item.isHighlight
                        ? 'text-blue-700 font-semibold'
                        : 'text-gray-900'
                    )}
                  >
                    {item.value}
                  </span>
                </motion.div>
              ))}
            </div>

            {/* Divider Line (Receipt Style) */}
            <div
              className={clsx(
                'mx-5 border-t border-dashed',
                isFinal ? 'border-emerald-400/30' : 'border-gray-200'
              )}
            />

            {/* Footer */}
            <div className="px-5 py-4 space-y-3">
              {/* Time & Next Hint */}
              <div className="flex items-center justify-between text-sm">
                {timeSpent && (
                  <div
                    className={clsx(
                      'flex items-center gap-1.5',
                      isFinal ? 'text-emerald-100' : 'text-gray-500'
                    )}
                  >
                    <Clock className="w-4 h-4" />
                    <span>{timeSpent}</span>
                  </div>
                )}

                {nextHint && !isFinal && (
                  <div className="flex items-center gap-1.5 text-blue-600">
                    <Target className="w-4 h-4" />
                    <span className="font-medium">{nextHint}</span>
                  </div>
                )}
              </div>

              {/* Continue Button */}
              {onContinue && (
                <motion.button
                  onClick={onContinue}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={clsx(
                    'w-full flex items-center justify-center gap-2 py-3 rounded-lg font-medium transition-all',
                    isFinal
                      ? 'bg-white text-emerald-600 hover:bg-emerald-50'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  )}
                >
                  <span>{isFinal ? 'Ergebnisse ansehen' : 'Weiter'}</span>
                  <ChevronRight className="w-4 h-4" />
                </motion.button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Collapsed View */}
      {!isExpanded && (
        <div className="px-5 py-3 flex items-center justify-between text-sm">
          <span className={clsx(isFinal ? 'text-emerald-100' : 'text-gray-500')}>
            {items.length} Angaben erfasst
          </span>
          {onContinue && (
            <button
              onClick={onContinue}
              className={clsx(
                'flex items-center gap-1 font-medium',
                isFinal ? 'text-white' : 'text-blue-600'
              )}
            >
              <span>Details</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          )}
        </div>
      )}
    </motion.div>
  );
}

export default MiniReceipt;
