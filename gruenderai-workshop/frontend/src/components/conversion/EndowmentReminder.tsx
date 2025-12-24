import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Clock, TrendingUp, FileText, Star, Gift, X, Sparkles } from 'lucide-react';
import { Button, Card, Badge, ProgressRing } from '@/components/common';
import type { Investment } from '@/types/workshop.types';

interface EndowmentReminderProps {
  investments: Investment[];
  totalTimeInvested: number; // in minutes
  gzReadinessScore: number;
  completedModules: number;
  generatedChapters: number;
  onContinue: () => void;
  onViewProgress?: () => void;
  variant?: 'banner' | 'modal' | 'card';
}

export const EndowmentReminder = ({
  investments,
  totalTimeInvested,
  gzReadinessScore,
  completedModules,
  generatedChapters,
  onContinue,
  onViewProgress,
  variant = 'card'
}: EndowmentReminderProps) => {
  const [isExpanded, setIsExpanded] = useState(variant === 'modal');

  const formatTime = (minutes: number) => {
    if (minutes < 60) return `${minutes} Min.`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
  };

  // Calculate estimated monetary value of the work
  const estimatedValue = Math.round(completedModules * 50 + generatedChapters * 25);

  if (variant === 'banner') {
    return (
      <motion.div
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-gradient-to-r from-primary-600 to-accent-600 text-white px-4 py-3"
      >
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Gift size={24} className="flex-shrink-0" />
            <div>
              <p className="font-medium">
                Du hast bereits {formatTime(totalTimeInvested)} investiert!
              </p>
              <p className="text-sm text-white/80">
                {completedModules} Module abgeschlossen, {generatedChapters} Kapitel generiert
              </p>
            </div>
          </div>
          <Button
            variant="secondary"
            size="sm"
            onClick={onContinue}
            className="bg-white/20 border-white/30 text-white hover:bg-white/30"
          >
            Weitermachen
          </Button>
        </div>
      </motion.div>
    );
  }

  if (variant === 'modal') {
    return (
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-warm-900/70"
            onClick={() => setIsExpanded(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="w-full max-w-md"
              onClick={(e) => e.stopPropagation()}
            >
              <Card variant="elevated" padding="none" className="overflow-hidden">
                {/* Header with gradient */}
                <div className="bg-gradient-to-br from-primary-500 to-accent-500 p-6 text-white text-center relative">
                  <button
                    onClick={() => setIsExpanded(false)}
                    className="absolute top-3 right-3 p-1 hover:bg-white/20 rounded-full transition-colors"
                  >
                    <X size={20} />
                  </button>

                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', delay: 0.2 }}
                    className="w-16 h-16 mx-auto mb-4 rounded-full bg-white/20 flex items-center justify-center"
                  >
                    <Sparkles size={32} />
                  </motion.div>

                  <h2 className="text-xl font-display font-bold mb-2">
                    Dein Fortschritt ist wertvoll!
                  </h2>
                  <p className="text-white/80">
                    Du hast bereits so viel erreicht
                  </p>
                </div>

                {/* Stats */}
                <div className="p-6">
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="text-center">
                      <div className="w-12 h-12 mx-auto mb-2 rounded-full bg-primary-100 flex items-center justify-center">
                        <Clock size={20} className="text-primary-600" />
                      </div>
                      <p className="text-lg font-bold text-warm-900">
                        {formatTime(totalTimeInvested)}
                      </p>
                      <p className="text-xs text-warm-500">investiert</p>
                    </div>

                    <div className="text-center">
                      <div className="w-12 h-12 mx-auto mb-2 rounded-full bg-green-100 flex items-center justify-center">
                        <FileText size={20} className="text-green-600" />
                      </div>
                      <p className="text-lg font-bold text-warm-900">
                        {generatedChapters}
                      </p>
                      <p className="text-xs text-warm-500">Kapitel</p>
                    </div>

                    <div className="text-center">
                      <div className="w-12 h-12 mx-auto mb-2 rounded-full bg-accent-100 flex items-center justify-center">
                        <Star size={20} className="text-accent-600" />
                      </div>
                      <p className="text-lg font-bold text-warm-900">
                        {gzReadinessScore}%
                      </p>
                      <p className="text-xs text-warm-500">GZ-Ready</p>
                    </div>
                  </div>

                  {/* Value proposition */}
                  <div className="bg-warm-50 rounded-xl p-4 mb-6">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-warm-600">
                        Geschätzter Wert deiner Arbeit
                      </span>
                      <span className="text-lg font-bold text-green-600">
                        ~{estimatedValue}€
                      </span>
                    </div>
                    <p className="text-xs text-warm-500 mt-1">
                      Basierend auf durchschnittlichen Beraterkosten
                    </p>
                  </div>

                  {/* Action buttons */}
                  <div className="space-y-3">
                    <Button
                      variant="accent"
                      fullWidth
                      onClick={() => {
                        setIsExpanded(false);
                        onContinue();
                      }}
                      rightIcon={<TrendingUp size={18} />}
                    >
                      Workshop fortsetzen
                    </Button>

                    {onViewProgress && (
                      <Button
                        variant="secondary"
                        fullWidth
                        onClick={onViewProgress}
                      >
                        Fortschritt ansehen
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    );
  }

  // Default card variant
  return (
    <Card
      variant="accent"
      padding="lg"
      className="relative overflow-hidden"
    >
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-accent-300/20 to-transparent rounded-full -translate-y-1/2 translate-x-1/2" />

      <div className="relative">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-400 to-accent-600 flex items-center justify-center shadow-gold-glow">
              <Gift size={24} className="text-white" />
            </div>
            <div>
              <h3 className="font-display font-semibold text-warm-900">
                Dein Investment
              </h3>
              <p className="text-sm text-warm-500">
                Bereits {formatTime(totalTimeInvested)} investiert
              </p>
            </div>
          </div>

          <Badge variant="accent" size="sm">
            ~{estimatedValue}€ Wert
          </Badge>
        </div>

        {/* Progress stats */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="bg-white/60 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-warm-900">{completedModules}</p>
            <p className="text-xs text-warm-500">Module</p>
          </div>
          <div className="bg-white/60 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-warm-900">{generatedChapters}</p>
            <p className="text-xs text-warm-500">Kapitel</p>
          </div>
          <div className="bg-white/60 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-warm-900">{gzReadinessScore}%</p>
            <p className="text-xs text-warm-500">GZ-Ready</p>
          </div>
        </div>

        {/* Message */}
        <p className="text-sm text-warm-600 mb-4">
          Lass deine Arbeit nicht verloren gehen! Mach weiter und sichere dir deinen Gründungszuschuss.
        </p>

        {/* Action */}
        <Button
          variant="accent"
          fullWidth
          onClick={onContinue}
          rightIcon={<TrendingUp size={18} />}
        >
          Jetzt weitermachen
        </Button>
      </div>
    </Card>
  );
};

// Compact version for inline use
interface MiniEndowmentProps {
  timeInvested: number;
  chaptersGenerated: number;
}

export const MiniEndowment = ({ timeInvested, chaptersGenerated }: MiniEndowmentProps) => {
  const formatTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`;
    return `${Math.floor(minutes / 60)}h`;
  };

  return (
    <div className="inline-flex items-center gap-3 px-3 py-1.5 bg-accent-50 rounded-full border border-accent-200">
      <div className="flex items-center gap-1 text-xs text-accent-700">
        <Clock size={12} />
        <span>{formatTime(timeInvested)}</span>
      </div>
      <div className="w-px h-3 bg-accent-200" />
      <div className="flex items-center gap-1 text-xs text-accent-700">
        <FileText size={12} />
        <span>{chaptersGenerated} Kapitel</span>
      </div>
    </div>
  );
};

export default EndowmentReminder;
