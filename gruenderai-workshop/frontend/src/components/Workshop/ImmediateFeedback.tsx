import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, AlertTriangle, Info, Lightbulb, ArrowRight, TrendingUp } from 'lucide-react';
import { Button, Card, QualityGauge } from '@/components/common';
import type { FeedbackItem } from '@/types/workshop.types';

interface ImmediateFeedbackProps {
  feedback: FeedbackItem;
  onDismiss?: () => void;
  onAction?: () => void;
  actionLabel?: string;
  showScoreImpact?: boolean;
  scoreImpact?: number;
}

const FEEDBACK_STYLES = {
  success: {
    bg: 'bg-green-50',
    border: 'border-green-200',
    icon: CheckCircle,
    iconColor: 'text-green-500',
    titleColor: 'text-green-800',
    textColor: 'text-green-700'
  },
  warning: {
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    icon: AlertTriangle,
    iconColor: 'text-amber-500',
    titleColor: 'text-amber-800',
    textColor: 'text-amber-700'
  },
  info: {
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    icon: Info,
    iconColor: 'text-blue-500',
    titleColor: 'text-blue-800',
    textColor: 'text-blue-700'
  },
  tip: {
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    icon: Lightbulb,
    iconColor: 'text-purple-500',
    titleColor: 'text-purple-800',
    textColor: 'text-purple-700'
  }
};

export const ImmediateFeedback = ({
  feedback,
  onDismiss,
  onAction,
  actionLabel = 'Verstanden',
  showScoreImpact = false,
  scoreImpact
}: ImmediateFeedbackProps) => {
  const style = FEEDBACK_STYLES[feedback.type];
  const Icon = style.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ type: 'spring', damping: 20, stiffness: 300 }}
      className={`${style.bg} ${style.border} border rounded-xl p-4`}
    >
      <div className="flex items-start gap-3">
        <div className={`flex-shrink-0 ${style.iconColor}`}>
          <Icon size={24} />
        </div>

        <div className="flex-1 min-w-0">
          <h4 className={`font-semibold ${style.titleColor}`}>
            {feedback.title}
          </h4>
          <p className={`mt-1 text-sm ${style.textColor}`}>
            {feedback.message}
          </p>

          {/* Suggestions */}
          {feedback.suggestions && feedback.suggestions.length > 0 && (
            <div className="mt-3 space-y-2">
              {feedback.suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="flex items-start gap-2 text-sm"
                >
                  <ArrowRight size={14} className={`mt-0.5 ${style.iconColor} opacity-60`} />
                  <span className={style.textColor}>{suggestion}</span>
                </div>
              ))}
            </div>
          )}

          {/* Score impact */}
          {showScoreImpact && scoreImpact !== undefined && (
            <div className="mt-3 flex items-center gap-2">
              <TrendingUp size={16} className={scoreImpact > 0 ? 'text-green-500' : 'text-amber-500'} />
              <span className={`text-sm font-medium ${scoreImpact > 0 ? 'text-green-700' : 'text-amber-700'}`}>
                {scoreImpact > 0 ? '+' : ''}{scoreImpact}% GZ-Readiness
              </span>
            </div>
          )}

          {/* Actions */}
          {(onAction || onDismiss) && (
            <div className="mt-4 flex items-center gap-3">
              {onAction && (
                <Button
                  size="sm"
                  variant={feedback.type === 'success' ? 'primary' : 'secondary'}
                  onClick={onAction}
                >
                  {actionLabel}
                </Button>
              )}
              {onDismiss && (
                <button
                  onClick={onDismiss}
                  className={`text-sm ${style.textColor} hover:underline`}
                >
                  Schließen
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

interface FeedbackContainerProps {
  feedbackItems: FeedbackItem[];
  onDismiss?: (id: string) => void;
}

export const FeedbackContainer = ({ feedbackItems, onDismiss }: FeedbackContainerProps) => {
  return (
    <div className="space-y-3">
      <AnimatePresence mode="popLayout">
        {feedbackItems.map((item) => (
          <ImmediateFeedback
            key={item.id}
            feedback={item}
            onDismiss={onDismiss ? () => onDismiss(item.id) : undefined}
          />
        ))}
      </AnimatePresence>
    </div>
  );
};

interface ModuleFeedbackSummaryProps {
  feedbackItems: FeedbackItem[];
  moduleScore: number;
  moduleTitle: string;
  onContinue: () => void;
}

export const ModuleFeedbackSummary = ({
  feedbackItems,
  moduleScore,
  moduleTitle,
  onContinue
}: ModuleFeedbackSummaryProps) => {
  const successCount = feedbackItems.filter(f => f.type === 'success').length;
  const warningCount = feedbackItems.filter(f => f.type === 'warning').length;

  return (
    <Card variant="elevated" padding="lg">
      <div className="text-center mb-6">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', damping: 10, stiffness: 100 }}
        >
          <CheckCircle size={48} className="mx-auto text-green-500 mb-3" />
        </motion.div>
        <h3 className="text-xl font-display font-semibold text-warm-900">
          {moduleTitle} abgeschlossen!
        </h3>
      </div>

      {/* Score */}
      <div className="flex justify-center mb-6">
        <QualityGauge score={moduleScore} variant="radial" label="Modul-Score" />
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-green-50 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-green-600">{successCount}</p>
          <p className="text-sm text-green-700">Stärken</p>
        </div>
        <div className="bg-amber-50 rounded-xl p-4 text-center">
          <p className="text-2xl font-bold text-amber-600">{warningCount}</p>
          <p className="text-sm text-amber-700">Verbesserungen</p>
        </div>
      </div>

      {/* Key feedback items */}
      {feedbackItems.slice(0, 3).map((item) => (
        <div
          key={item.id}
          className={`flex items-start gap-2 p-3 rounded-lg mb-2 ${
            item.type === 'success' ? 'bg-green-50' :
            item.type === 'warning' ? 'bg-amber-50' : 'bg-blue-50'
          }`}
        >
          {item.type === 'success' ? (
            <CheckCircle size={16} className="text-green-500 mt-0.5" />
          ) : item.type === 'warning' ? (
            <AlertTriangle size={16} className="text-amber-500 mt-0.5" />
          ) : (
            <Info size={16} className="text-blue-500 mt-0.5" />
          )}
          <p className="text-sm text-warm-700">{item.title}</p>
        </div>
      ))}

      {/* Continue button */}
      <Button
        variant="accent"
        fullWidth
        onClick={onContinue}
        className="mt-6"
        rightIcon={<ArrowRight size={18} />}
      >
        Weiter zum nächsten Modul
      </Button>
    </Card>
  );
};

export default ImmediateFeedback;
