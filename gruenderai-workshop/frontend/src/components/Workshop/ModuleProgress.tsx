import { motion } from 'framer-motion';
import { CheckCircle, Circle, Clock, Target } from 'lucide-react';
import { ProgressRing, Badge } from '@/components/common';
import type { ModuleNumber } from '@/types/workshop.types';

interface ModuleProgressProps {
  currentModule: ModuleNumber;
  moduleProgress: Record<number, number>;
  gzReadinessScore: number;
  currentQuestion?: number;
  totalQuestions?: number;
}

const MODULE_NAMES: Record<ModuleNumber, string> = {
  1: 'Geschäftsidee',
  2: 'Zielgruppe',
  3: 'Markt',
  4: 'Marketing',
  5: 'Finanzen',
  6: 'Strategie'
};

export const ModuleProgress = ({
  currentModule,
  moduleProgress,
  gzReadinessScore,
  currentQuestion,
  totalQuestions
}: ModuleProgressProps) => {
  const completedModules = Object.entries(moduleProgress)
    .filter(([_, progress]) => progress === 100)
    .length;

  return (
    <div className="bg-white rounded-xl border border-warm-200 p-4 shadow-card">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Target size={18} className="text-primary-500" />
          <span className="font-semibold text-warm-900">Fortschritt</span>
        </div>
        <Badge variant="primary" size="sm">
          {completedModules}/6 Module
        </Badge>
      </div>

      {/* GZ Readiness Score */}
      <div className="flex items-center justify-center mb-4">
        <ProgressRing
          progress={gzReadinessScore}
          size="md"
          color={gzReadinessScore >= 60 ? 'success' : gzReadinessScore >= 40 ? 'warning' : 'danger'}
          label="GZ-Readiness"
        />
      </div>

      {/* Module dots */}
      <div className="flex justify-center gap-2 mb-4">
        {([1, 2, 3, 4, 5, 6] as ModuleNumber[]).map((num) => {
          const progress = moduleProgress[num];
          const isCompleted = progress === 100;
          const isCurrent = num === currentModule;

          return (
            <motion.div
              key={num}
              className={`relative flex flex-col items-center`}
              whileHover={{ scale: 1.1 }}
            >
              <div
                className={`
                  w-8 h-8 rounded-full flex items-center justify-center
                  transition-all duration-300
                  ${isCompleted
                    ? 'bg-green-500 text-white'
                    : isCurrent
                      ? 'bg-primary-500 text-white ring-4 ring-primary-100'
                      : 'bg-warm-200 text-warm-500'
                  }
                `}
              >
                {isCompleted ? (
                  <CheckCircle size={16} />
                ) : (
                  <span className="text-xs font-bold">{num}</span>
                )}
              </div>
              {isCurrent && (
                <motion.div
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="absolute -bottom-5 text-xs text-primary-600 font-medium whitespace-nowrap"
                >
                  Aktiv
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Current module info */}
      <div className="border-t border-warm-100 pt-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-warm-600">
            Modul {currentModule}: {MODULE_NAMES[currentModule]}
          </span>
          <span className="text-sm font-medium text-warm-900">
            {moduleProgress[currentModule]}%
          </span>
        </div>

        {/* Progress bar */}
        <div className="w-full h-2 bg-warm-200 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${moduleProgress[currentModule]}%` }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          />
        </div>

        {/* Question progress */}
        {currentQuestion !== undefined && totalQuestions !== undefined && (
          <p className="text-xs text-warm-500 mt-2 text-center">
            Frage {currentQuestion} von {totalQuestions}
          </p>
        )}
      </div>
    </div>
  );
};

interface QuestionProgressBarProps {
  currentQuestion: number;
  totalQuestions: number;
  answeredQuestions: number[];
}

export const QuestionProgressBar = ({
  currentQuestion,
  totalQuestions,
  answeredQuestions
}: QuestionProgressBarProps) => {
  return (
    <div className="flex items-center gap-1">
      {Array.from({ length: totalQuestions }, (_, i) => i + 1).map((num) => {
        const isAnswered = answeredQuestions.includes(num);
        const isCurrent = num === currentQuestion;

        return (
          <motion.div
            key={num}
            className={`
              h-2 rounded-full transition-all duration-300
              ${isCurrent
                ? 'w-8 bg-primary-500'
                : isAnswered
                  ? 'w-4 bg-green-500'
                  : 'w-4 bg-warm-200'
              }
            `}
            initial={false}
            animate={{
              width: isCurrent ? 32 : 16,
              backgroundColor: isCurrent ? '#3b82f6' : isAnswered ? '#22c55e' : '#e5e5e5'
            }}
          />
        );
      })}
    </div>
  );
};

interface TimeEstimateProps {
  estimatedMinutes: number;
  variant?: 'default' | 'compact';
}

export const TimeEstimate = ({ estimatedMinutes, variant = 'default' }: TimeEstimateProps) => {
  if (variant === 'compact') {
    return (
      <div className="flex items-center gap-1 text-warm-500">
        <Clock size={14} />
        <span className="text-xs">{estimatedMinutes} Min.</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 bg-warm-100 rounded-lg">
      <Clock size={16} className="text-warm-500" />
      <span className="text-sm text-warm-600">
        ca. {estimatedMinutes} Minuten
      </span>
    </div>
  );
};

export default ModuleProgress;
