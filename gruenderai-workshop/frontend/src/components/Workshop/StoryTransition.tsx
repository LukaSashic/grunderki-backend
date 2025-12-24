import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Sparkles, Target, TrendingUp, Users, Calculator, Megaphone } from 'lucide-react';
import { Button, ProgressRing } from '@/components/common';
import type { ModuleNumber } from '@/types/workshop.types';

interface StoryTransitionProps {
  fromModule: ModuleNumber;
  toModule: ModuleNumber;
  previousSummary: string;
  nextPreview: string;
  score: number;
  onContinue: () => void;
  isLoading?: boolean;
}

const MODULE_ICONS = {
  1: Target,
  2: Users,
  3: TrendingUp,
  4: Megaphone,
  5: Calculator,
  6: Sparkles
};

const MODULE_COLORS = {
  1: 'from-primary-500 to-primary-700',
  2: 'from-blue-500 to-blue-700',
  3: 'from-green-500 to-green-700',
  4: 'from-purple-500 to-purple-700',
  5: 'from-amber-500 to-amber-700',
  6: 'from-red-500 to-red-700'
};

const MODULE_TITLES = {
  1: 'Geschäftsidee & Gründerprofil',
  2: 'Zielgruppe & Personas',
  3: 'Markt & Wettbewerb',
  4: 'Marketing & Vertrieb',
  5: 'Finanzplanung',
  6: 'Strategie & Abschluss'
};

export const StoryTransition = ({
  fromModule,
  toModule,
  previousSummary,
  nextPreview,
  score,
  onContinue,
  isLoading = false
}: StoryTransitionProps) => {
  const [phase, setPhase] = useState<'summary' | 'preview' | 'ready'>('summary');
  const FromIcon = MODULE_ICONS[fromModule];
  const ToIcon = MODULE_ICONS[toModule];

  useEffect(() => {
    const timer1 = setTimeout(() => setPhase('preview'), 2000);
    const timer2 = setTimeout(() => setPhase('ready'), 4000);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-warm-900 to-primary-900">
      <div className="max-w-2xl mx-auto px-6 text-center">
        <AnimatePresence mode="wait">
          {/* Phase 1: Summary of completed module */}
          {phase === 'summary' && (
            <motion.div
              key="summary"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="space-y-6"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', damping: 10, stiffness: 100, delay: 0.2 }}
                className={`w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br ${MODULE_COLORS[fromModule]} flex items-center justify-center shadow-lg`}
              >
                <FromIcon size={40} className="text-white" />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <h2 className="text-2xl font-display font-bold text-white mb-2">
                  Modul {fromModule} abgeschlossen!
                </h2>
                <p className="text-warm-300 text-lg">
                  {MODULE_TITLES[fromModule]}
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="flex justify-center"
              >
                <ProgressRing progress={score} size="lg" color="accent" />
              </motion.div>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 }}
                className="text-warm-200"
              >
                {previousSummary}
              </motion.p>
            </motion.div>
          )}

          {/* Phase 2: Preview of next module */}
          {phase === 'preview' && (
            <motion.div
              key="preview"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="space-y-6"
            >
              <motion.div
                initial={{ x: -100, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="flex items-center justify-center gap-4"
              >
                <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${MODULE_COLORS[fromModule]} flex items-center justify-center opacity-50`}>
                  <FromIcon size={32} className="text-white" />
                </div>

                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  <ArrowRight size={32} className="text-accent-400" />
                </motion.div>

                <motion.div
                  initial={{ x: 100, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.5 }}
                  className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${MODULE_COLORS[toModule]} flex items-center justify-center shadow-lg ring-4 ring-accent-400/30`}
                >
                  <ToIcon size={40} className="text-white" />
                </motion.div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
              >
                <h2 className="text-2xl font-display font-bold text-white mb-2">
                  Weiter zu Modul {toModule}
                </h2>
                <p className="text-accent-400 text-lg font-medium">
                  {MODULE_TITLES[toModule]}
                </p>
              </motion.div>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9 }}
                className="text-warm-200"
              >
                {nextPreview}
              </motion.p>
            </motion.div>
          )}

          {/* Phase 3: Ready to continue */}
          {phase === 'ready' && (
            <motion.div
              key="ready"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="space-y-8"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1, rotate: [0, 10, -10, 0] }}
                transition={{ type: 'spring', damping: 10, stiffness: 100 }}
                className={`w-24 h-24 mx-auto rounded-2xl bg-gradient-to-br ${MODULE_COLORS[toModule]} flex items-center justify-center shadow-xl ring-4 ring-white/20`}
              >
                <ToIcon size={48} className="text-white" />
              </motion.div>

              <div>
                <h2 className="text-3xl font-display font-bold text-white mb-3">
                  Bereit für {MODULE_TITLES[toModule]}?
                </h2>
                <p className="text-warm-300 max-w-md mx-auto">
                  {nextPreview}
                </p>
              </div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <Button
                  variant="accent"
                  size="lg"
                  onClick={onContinue}
                  isLoading={isLoading}
                  rightIcon={<ArrowRight size={20} />}
                >
                  Modul {toModule} starten
                </Button>
              </motion.div>

              {/* Progress indicator */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="flex justify-center gap-2"
              >
                {[1, 2, 3, 4, 5, 6].map((num) => (
                  <div
                    key={num}
                    className={`w-3 h-3 rounded-full transition-all duration-300 ${
                      num < toModule
                        ? 'bg-green-500'
                        : num === toModule
                          ? 'bg-accent-400 ring-2 ring-accent-400/30'
                          : 'bg-warm-600'
                    }`}
                  />
                ))}
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default StoryTransition;
