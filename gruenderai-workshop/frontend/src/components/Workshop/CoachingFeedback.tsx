/**
 * GründerAI Workshop - Coaching Feedback Component
 * Shows AI coaching response after user submits an answer
 * Includes: Insight, Challenge, Suggestion, Example, Encouragement
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle,
  Lightbulb,
  MessageCircle,
  BookOpen,
  ArrowRight,
  RefreshCw,
  Sparkles,
  Copy,
  Check
} from 'lucide-react';
import { Button } from '@/components/common';
import type { CoachingResponse } from '@/types/module1.types';

interface CoachingFeedbackProps {
  response: CoachingResponse;
  onAccept: () => void;
  onIterate: () => void;
  isLoading?: boolean;
  iterationCount?: number;
}

export const CoachingFeedback: React.FC<CoachingFeedbackProps> = ({
  response,
  onAccept,
  onIterate,
  isLoading = false,
  iterationCount = 0
}) => {
  const [copiedImproved, setCopiedImproved] = useState(false);

  const handleCopyImproved = async () => {
    if (response.improvedVersion) {
      await navigator.clipboard.writeText(response.improvedVersion);
      setCopiedImproved(true);
      setTimeout(() => setCopiedImproved(false), 2000);
    }
  };

  // Loading State
  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="coaching-loading bg-gradient-to-r from-primary-50 to-accent-50 rounded-xl p-8 text-center"
      >
        <div className="flex justify-center mb-4">
          <div className="typing-indicator flex gap-1">
            <motion.span
              className="w-2 h-2 bg-primary-500 rounded-full"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
            />
            <motion.span
              className="w-2 h-2 bg-primary-500 rounded-full"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
            />
            <motion.span
              className="w-2 h-2 bg-primary-500 rounded-full"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
            />
          </div>
        </div>
        <p className="text-warm-600 font-medium">Dein Coach denkt nach...</p>
        <p className="text-warm-500 text-sm mt-1">
          Analysiere deine Antwort für personalisiertes Feedback
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="coaching-feedback bg-gradient-to-r from-primary-50 to-accent-50 rounded-xl p-6 border border-primary-200"
    >
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
          <Sparkles className="w-4 h-4 text-white" />
        </div>
        <div>
          <h4 className="font-medium text-primary-900">Dein GründerAI Coach</h4>
          <p className="text-xs text-primary-600">
            {iterationCount > 0 ? `Verbesserung #${iterationCount + 1}` : 'Feedback zu deiner Antwort'}
          </p>
        </div>
      </div>

      {/* Insight - Was gut ist */}
      {response.insight && (
        <div className="feedback-section mb-4">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <span className="font-medium text-green-900">Gut gemacht</span>
          </div>
          <p className="text-warm-700 pl-7">{response.insight}</p>
        </div>
      )}

      {/* Challenge - Was verbessert werden kann */}
      {response.challenge && (
        <div className="feedback-section mb-4">
          <div className="flex items-center gap-2 mb-2">
            <Lightbulb className="w-5 h-5 text-amber-600" />
            <span className="font-medium text-amber-900">Denk mal darüber nach</span>
          </div>
          <p className="text-warm-700 pl-7">{response.challenge}</p>
        </div>
      )}

      {/* Suggestion - Konkreter Impuls */}
      {response.suggestion && (
        <div className="feedback-section mb-4 bg-white/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <MessageCircle className="w-5 h-5 text-primary-600" />
            <span className="font-medium text-primary-900">Coaching-Frage</span>
          </div>
          <p className="text-warm-800 italic pl-7">"{response.suggestion}"</p>
        </div>
      )}

      {/* Example - Praxis-Beispiel */}
      {response.example && (
        <div className="feedback-section mb-4">
          <div className="flex items-center gap-2 mb-2">
            <BookOpen className="w-5 h-5 text-blue-600" />
            <span className="font-medium text-blue-900">Beispiel aus der Praxis</span>
          </div>
          <p className="text-warm-700 pl-7">{response.example}</p>
        </div>
      )}

      {/* Improved Version - AI Vorschlag */}
      {response.improvedVersion && (
        <div className="feedback-section mb-4 bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-green-600" />
              <span className="font-medium text-green-900">Formulierungsvorschlag</span>
            </div>
            <button
              onClick={handleCopyImproved}
              className="flex items-center gap-1 text-xs text-green-700 hover:text-green-900 transition-colors"
            >
              {copiedImproved ? (
                <>
                  <Check className="w-3 h-3" />
                  Kopiert!
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" />
                  Kopieren
                </>
              )}
            </button>
          </div>
          <p className="text-green-800 text-sm pl-7 whitespace-pre-wrap">
            {response.improvedVersion}
          </p>
        </div>
      )}

      {/* Encouragement */}
      {response.encouragement && (
        <div className="feedback-section mb-6 text-center">
          <p className="text-primary-700 font-medium">{response.encouragement}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3">
        {response.shouldIterate ? (
          <>
            <Button
              variant="primary"
              onClick={onIterate}
              leftIcon={<RefreshCw className="w-4 h-4" />}
              className="flex-1"
            >
              Antwort verbessern
            </Button>
            <Button
              variant="secondary"
              onClick={onAccept}
            >
              So ist gut
            </Button>
          </>
        ) : (
          <Button
            variant="accent"
            onClick={onAccept}
            rightIcon={<ArrowRight className="w-4 h-4" />}
            className="w-full"
          >
            Weiter zur nächsten Frage
          </Button>
        )}
      </div>

      {/* Iteration hint */}
      {response.shouldIterate && iterationCount < 2 && (
        <p className="text-xs text-warm-500 text-center mt-3">
          Du kannst bis zu 3x nachbessern. Iteration {iterationCount + 1}/3
        </p>
      )}
    </motion.div>
  );
};

// =============================================================================
// QUICK COACHING TIPS (for real-time hints while typing)
// =============================================================================

interface QuickCoachingTipProps {
  tip: string;
  type: 'info' | 'warning' | 'success';
  onDismiss?: () => void;
}

export const QuickCoachingTip: React.FC<QuickCoachingTipProps> = ({
  tip,
  type,
  onDismiss
}) => {
  const styles = {
    info: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      icon: Lightbulb,
      iconColor: 'text-blue-500',
      textColor: 'text-blue-800'
    },
    warning: {
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      icon: Lightbulb,
      iconColor: 'text-amber-500',
      textColor: 'text-amber-800'
    },
    success: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      icon: CheckCircle,
      iconColor: 'text-green-500',
      textColor: 'text-green-800'
    }
  };

  const style = styles[type];
  const Icon = style.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={`flex items-start gap-2 p-3 rounded-lg ${style.bg} ${style.border} border`}
    >
      <Icon className={`w-4 h-4 mt-0.5 flex-shrink-0 ${style.iconColor}`} />
      <p className={`text-sm ${style.textColor} flex-1`}>{tip}</p>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className={`text-xs ${style.textColor} hover:underline`}
        >
          ×
        </button>
      )}
    </motion.div>
  );
};

// =============================================================================
// COACHING SKELETON (loading placeholder)
// =============================================================================

export const CoachingSkeleton: React.FC = () => {
  return (
    <div className="coaching-skeleton bg-warm-50 rounded-xl p-6 animate-pulse">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-full bg-warm-200" />
        <div className="space-y-1">
          <div className="h-4 w-32 bg-warm-200 rounded" />
          <div className="h-3 w-24 bg-warm-200 rounded" />
        </div>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <div className="h-4 w-20 bg-warm-200 rounded" />
          <div className="h-4 w-full bg-warm-200 rounded" />
          <div className="h-4 w-3/4 bg-warm-200 rounded" />
        </div>

        <div className="space-y-2">
          <div className="h-4 w-24 bg-warm-200 rounded" />
          <div className="h-4 w-full bg-warm-200 rounded" />
        </div>
      </div>

      <div className="flex gap-3 mt-6">
        <div className="h-10 flex-1 bg-warm-200 rounded-lg" />
        <div className="h-10 w-24 bg-warm-200 rounded-lg" />
      </div>
    </div>
  );
};

export default CoachingFeedback;
