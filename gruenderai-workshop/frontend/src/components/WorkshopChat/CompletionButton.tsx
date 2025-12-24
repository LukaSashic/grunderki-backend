/**
 * CompletionButton Component
 * Shows when user can complete a module early (ab 75% fill)
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, ChevronRight, Loader2, Sparkles, AlertTriangle } from 'lucide-react';
import { clsx } from 'clsx';
import type { CompletionStatus as CompletionStatusType } from '@/stores/workshopChatStore';

interface CompletionButtonProps {
  completionStatus: CompletionStatusType | null;
  onComplete: () => Promise<void>;
  isLoading?: boolean;
  currentSectionTitle?: string;
}

export function CompletionButton({
  completionStatus,
  onComplete,
  isLoading = false,
  currentSectionTitle,
}: CompletionButtonProps) {
  const [isConfirming, setIsConfirming] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);

  // Don't show if no status or button shouldn't be shown
  if (!completionStatus || !completionStatus.showCompletionButton) {
    return null;
  }

  const { fillPercentage, canComplete, isOptimal, remainingForOptimal } = completionStatus;

  const handleClick = async () => {
    if (!canComplete || isLoading || isCompleting) return;

    // If not optimal, show confirmation first
    if (!isOptimal && !isConfirming) {
      setIsConfirming(true);
      return;
    }

    setIsCompleting(true);
    try {
      await onComplete();
    } finally {
      setIsCompleting(false);
      setIsConfirming(false);
    }
  };

  const handleCancel = () => {
    setIsConfirming(false);
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 20 }}
        className="border-t border-gray-200 bg-gradient-to-r from-emerald-50 to-blue-50 px-4 py-3"
      >
        <div className="max-w-4xl mx-auto">
          {/* Confirmation View */}
          {isConfirming ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col sm:flex-row items-center gap-3"
            >
              <div className="flex items-center gap-2 text-amber-700">
                <AlertTriangle className="w-5 h-5 flex-shrink-0" />
                <span className="text-sm">
                  Noch {remainingForOptimal} Fragen für optimale Qualität. Trotzdem abschließen?
                </span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleCancel}
                  className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Weitermachen
                </button>
                <button
                  onClick={handleClick}
                  disabled={isCompleting}
                  className={clsx(
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all',
                    'bg-emerald-600 hover:bg-emerald-700 text-white'
                  )}
                >
                  {isCompleting ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <CheckCircle className="w-4 h-4" />
                  )}
                  Ja, abschließen
                </button>
              </div>
            </motion.div>
          ) : (
            /* Normal View */
            <div className="flex items-center justify-between gap-4">
              {/* Left: Status Info */}
              <div className="flex items-center gap-3">
                {/* Progress Ring */}
                <div className="relative w-10 h-10">
                  <svg className="w-10 h-10 -rotate-90" viewBox="0 0 36 36">
                    <path
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none"
                      stroke="#e5e7eb"
                      strokeWidth="3"
                    />
                    <path
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none"
                      stroke={isOptimal ? '#10b981' : '#3b82f6'}
                      strokeWidth="3"
                      strokeDasharray={`${fillPercentage}, 100`}
                      strokeLinecap="round"
                    />
                  </svg>
                  <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-gray-700">
                    {Math.round(fillPercentage)}%
                  </span>
                </div>

                {/* Status Text */}
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {isOptimal ? (
                      <span className="flex items-center gap-1 text-emerald-700">
                        <Sparkles className="w-4 h-4" />
                        Perfekt ausgefüllt!
                      </span>
                    ) : (
                      <span>Modul bereit zum Abschluss</span>
                    )}
                  </p>
                  <p className="text-xs text-gray-500">
                    {isOptimal
                      ? `${currentSectionTitle || 'Modul'} vollständig`
                      : `${remainingForOptimal} weitere Fragen für optimale Qualität`}
                  </p>
                </div>
              </div>

              {/* Right: Action Button */}
              <button
                onClick={handleClick}
                disabled={!canComplete || isLoading || isCompleting}
                className={clsx(
                  'flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all',
                  canComplete && !isLoading
                    ? isOptimal
                      ? 'bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white shadow-md hover:shadow-lg'
                      : 'bg-white border-2 border-emerald-500 text-emerald-700 hover:bg-emerald-50'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                )}
              >
                {isCompleting ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <CheckCircle className="w-4 h-4" />
                )}
                <span>
                  {isOptimal ? 'Modul abschließen' : 'Fertig'}
                </span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}

export default CompletionButton;
