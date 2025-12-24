/**
 * LoadingWithMicrotips Component
 * Premium Loading Experience mit kontextuellen Tipps
 *
 * Macht Wartezeit zu Lernzeit!
 */

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, Sparkles, Lightbulb, TrendingUp, Heart } from 'lucide-react';
import { clsx } from 'clsx';

// =============================================================================
// TYPES
// =============================================================================

export interface Microtip {
  icon: string;
  text: string;
  category: 'insight' | 'stat' | 'tip' | 'encouragement';
}

interface LoadingWithMicrotipsProps {
  /** Array of microtips to display */
  tips?: Microtip[];
  /** Is currently loading */
  isLoading: boolean;
  /** Minimum display duration in ms (default: 2000) */
  minDuration?: number;
  /** Tip rotation interval in ms (default: 2500) */
  rotationInterval?: number;
  /** Custom loading text */
  loadingText?: string;
  /** Variant: 'inline' for chat, 'fullscreen' for overlay */
  variant?: 'inline' | 'fullscreen' | 'compact';
  /** Additional className */
  className?: string;
}

// =============================================================================
// DEFAULT TIPS (Fallback wenn keine Tips vom Backend kommen)
// =============================================================================

const DEFAULT_TIPS: Microtip[] = [
  { icon: '💡', text: 'Die besten Ideen brauchen einen klaren Businessplan.', category: 'insight' },
  { icon: '📊', text: '85% der erfolgreichen Gruender haben einen Businessplan.', category: 'stat' },
  { icon: '🎯', text: 'Je spezifischer deine Zielgruppe, desto erfolgreicher dein Marketing.', category: 'tip' },
  { icon: '💪', text: 'Du bist auf dem richtigen Weg - weiter so!', category: 'encouragement' },
  { icon: '🚀', text: 'Der Gruendungszuschuss wird 6-9 Monate gezahlt.', category: 'stat' },
  { icon: '✨', text: 'Mit jedem Schritt wird dein Businessplan besser.', category: 'encouragement' },
];

// =============================================================================
// HELPER COMPONENTS
// =============================================================================

function getCategoryIcon(category: Microtip['category']) {
  switch (category) {
    case 'insight':
      return <Lightbulb className="w-4 h-4" />;
    case 'stat':
      return <TrendingUp className="w-4 h-4" />;
    case 'tip':
      return <Sparkles className="w-4 h-4" />;
    case 'encouragement':
      return <Heart className="w-4 h-4" />;
    default:
      return <Sparkles className="w-4 h-4" />;
  }
}

function getCategoryColor(category: Microtip['category']) {
  switch (category) {
    case 'insight':
      return 'text-amber-600 bg-amber-50 border-amber-200';
    case 'stat':
      return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'tip':
      return 'text-emerald-600 bg-emerald-50 border-emerald-200';
    case 'encouragement':
      return 'text-pink-600 bg-pink-50 border-pink-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function LoadingWithMicrotips({
  tips = DEFAULT_TIPS,
  isLoading,
  minDuration = 2000,
  rotationInterval = 2500,
  loadingText = 'Analysiere deine Antwort...',
  variant = 'inline',
  className,
}: LoadingWithMicrotipsProps) {
  const [currentTipIndex, setCurrentTipIndex] = useState(0);
  const [showContent, setShowContent] = useState(false);
  const [startTime, setStartTime] = useState<number | null>(null);

  // Track loading start time
  useEffect(() => {
    if (isLoading && startTime === null) {
      setStartTime(Date.now());
      setShowContent(true);
    }
  }, [isLoading, startTime]);

  // Handle minimum duration
  useEffect(() => {
    if (!isLoading && startTime !== null) {
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, minDuration - elapsed);

      if (remaining > 0) {
        const timer = setTimeout(() => {
          setShowContent(false);
          setStartTime(null);
        }, remaining);
        return () => clearTimeout(timer);
      } else {
        setShowContent(false);
        setStartTime(null);
      }
    }
  }, [isLoading, startTime, minDuration]);

  // Rotate tips
  useEffect(() => {
    if (!showContent || tips.length <= 1) return;

    const interval = setInterval(() => {
      setCurrentTipIndex((prev) => (prev + 1) % tips.length);
    }, rotationInterval);

    return () => clearInterval(interval);
  }, [showContent, tips.length, rotationInterval]);

  const currentTip = tips[currentTipIndex] || DEFAULT_TIPS[0];

  if (!showContent) return null;

  // Compact variant (for inline chat bubbles)
  if (variant === 'compact') {
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        className={clsx('flex items-center gap-3 p-3 rounded-xl bg-white shadow-sm border border-gray-100', className)}
      >
        <Loader2 className="w-5 h-5 text-primary-500 animate-spin flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <p className="text-sm text-gray-600 truncate">{loadingText}</p>
        </div>
      </motion.div>
    );
  }

  // Inline variant (for chat area)
  if (variant === 'inline') {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        className={clsx('mx-4 my-3', className)}
      >
        <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-2xl p-5 border border-primary-100 shadow-sm">
          {/* Loading Header */}
          <div className="flex items-center gap-3 mb-4">
            <div className="relative">
              <div className="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center">
                <Loader2 className="w-5 h-5 text-primary-500 animate-spin" />
              </div>
              <motion.div
                className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-primary-500"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              />
            </div>
            <div>
              <p className="font-medium text-primary-900">{loadingText}</p>
              <p className="text-xs text-primary-600">Einen Moment bitte...</p>
            </div>
          </div>

          {/* Microtip Display */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentTipIndex}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className={clsx(
                'flex items-start gap-3 p-4 rounded-xl border-2',
                getCategoryColor(currentTip.category)
              )}
            >
              <span className="text-2xl flex-shrink-0">{currentTip.icon}</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium leading-relaxed">{currentTip.text}</p>
              </div>
              <div className="flex-shrink-0 opacity-50">
                {getCategoryIcon(currentTip.category)}
              </div>
            </motion.div>
          </AnimatePresence>

          {/* Progress Dots */}
          {tips.length > 1 && (
            <div className="flex justify-center gap-1.5 mt-4">
              {tips.map((_, idx) => (
                <motion.div
                  key={idx}
                  className={clsx(
                    'h-1.5 rounded-full transition-all duration-300',
                    idx === currentTipIndex
                      ? 'w-6 bg-primary-500'
                      : 'w-1.5 bg-primary-200'
                  )}
                />
              ))}
            </div>
          )}
        </div>
      </motion.div>
    );
  }

  // Fullscreen variant (overlay)
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className={clsx(
        'fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center p-6',
        className
      )}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8"
      >
        {/* Loading Animation */}
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="w-20 h-20 rounded-full bg-gradient-to-r from-primary-100 to-blue-100 flex items-center justify-center">
              <Loader2 className="w-10 h-10 text-primary-500 animate-spin" />
            </div>
            <motion.div
              className="absolute inset-0 rounded-full border-4 border-primary-200"
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            />
          </div>
        </div>

        {/* Loading Text */}
        <h3 className="text-xl font-bold text-center text-gray-900 mb-2">
          {loadingText}
        </h3>
        <p className="text-sm text-gray-500 text-center mb-6">
          Waehrend ich nachdenke, hier ein Tipp fuer dich:
        </p>

        {/* Microtip */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentTipIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
            className={clsx(
              'p-5 rounded-2xl border-2 mb-6',
              getCategoryColor(currentTip.category)
            )}
          >
            <div className="flex items-start gap-4">
              <span className="text-3xl">{currentTip.icon}</span>
              <p className="text-base font-medium leading-relaxed flex-1">
                {currentTip.text}
              </p>
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Progress Dots */}
        {tips.length > 1 && (
          <div className="flex justify-center gap-2">
            {tips.map((_, idx) => (
              <motion.div
                key={idx}
                className={clsx(
                  'h-2 rounded-full transition-all duration-300',
                  idx === currentTipIndex
                    ? 'w-8 bg-primary-500'
                    : 'w-2 bg-gray-200'
                )}
              />
            ))}
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

export default LoadingWithMicrotips;
