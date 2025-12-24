import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, ArrowRight, FileText, Download, Star } from 'lucide-react';
import { Button, Card, QualityGauge, Badge, ProgressRing } from '@/components/common';
import type { ModuleNumber, FeedbackItem, Gap, ChapterInfo } from '@/types/workshop.types';

interface ModuleSummaryProps {
  moduleNumber: ModuleNumber;
  moduleTitle: string;
  score: number;
  feedbackItems: FeedbackItem[];
  gaps: Gap[];
  generatedChapters: ChapterInfo[];
  timeSpent: number; // in minutes
  onViewChapters: () => void;
  onContinue: () => void;
  isLastModule?: boolean;
}

export const ModuleSummary = ({
  moduleNumber,
  moduleTitle,
  score,
  feedbackItems,
  gaps,
  generatedChapters,
  timeSpent,
  onViewChapters,
  onContinue,
  isLastModule = false
}: ModuleSummaryProps) => {
  const strengths = feedbackItems.filter(f => f.type === 'success');
  const improvements = feedbackItems.filter(f => f.type === 'warning' || f.type === 'info');
  const criticalGaps = gaps.filter(g => g.severity === 'critical');

  return (
    <div className="space-y-6">
      {/* Header with celebration */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', damping: 10, stiffness: 100, delay: 0.2 }}
          className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center shadow-lg"
        >
          <CheckCircle size={40} className="text-white" />
        </motion.div>

        <h2 className="text-2xl font-display font-bold text-warm-900">
          Modul {moduleNumber}: {moduleTitle}
        </h2>
        <p className="text-warm-600 mt-1">
          erfolgreich abgeschlossen!
        </p>
      </motion.div>

      {/* Score card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.3 }}
      >
        <Card variant="accent" padding="lg">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <ProgressRing progress={score} size="lg" color={score >= 60 ? 'success' : 'warning'} />
              <div>
                <p className="text-sm text-warm-600">Dein Modul-Score</p>
                <p className="text-2xl font-bold text-warm-900">{score}%</p>
              </div>
            </div>

            <div className="flex flex-col gap-2 text-center sm:text-right">
              <div className="flex items-center gap-2 justify-center sm:justify-end">
                <Star className="text-amber-500" size={18} />
                <span className="text-sm text-warm-600">
                  {strengths.length} Stärken identifiziert
                </span>
              </div>
              <p className="text-xs text-warm-500">
                Bearbeitungszeit: {timeSpent} Minuten
              </p>
            </div>
          </div>
        </Card>
      </motion.div>

      {/* Generated chapters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <Card padding="lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <FileText className="text-primary-500" size={20} />
              <h3 className="font-semibold text-warm-900">
                Generierte Kapitel
              </h3>
            </div>
            <Badge variant="success" size="sm">
              {generatedChapters.length} Kapitel
            </Badge>
          </div>

          <div className="space-y-2 mb-4">
            {generatedChapters.map((chapter, index) => (
              <motion.div
                key={chapter.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="flex items-center gap-3 p-3 bg-green-50 rounded-lg"
              >
                <CheckCircle size={18} className="text-green-500 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-warm-800 truncate">
                    {chapter.number} {chapter.title}
                  </p>
                </div>
                <QualityGauge
                  score={chapter.progress || 100}
                  size="sm"
                  variant="compact"
                  showIcon={false}
                />
              </motion.div>
            ))}
          </div>

          <Button
            variant="secondary"
            size="sm"
            onClick={onViewChapters}
            leftIcon={<FileText size={16} />}
          >
            Kapitel ansehen
          </Button>
        </Card>
      </motion.div>

      {/* Strengths and improvements */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Strengths */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card padding="md">
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle size={18} className="text-green-500" />
              <h4 className="font-semibold text-warm-900">Stärken</h4>
            </div>
            {strengths.length > 0 ? (
              <ul className="space-y-2">
                {strengths.slice(0, 4).map((item) => (
                  <li key={item.id} className="flex items-start gap-2 text-sm">
                    <span className="text-green-500 mt-1">•</span>
                    <span className="text-warm-700">{item.title}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-warm-500">Keine Stärken identifiziert</p>
            )}
          </Card>
        </motion.div>

        {/* Areas for improvement */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card padding="md">
            <div className="flex items-center gap-2 mb-3">
              <AlertTriangle size={18} className="text-amber-500" />
              <h4 className="font-semibold text-warm-900">Verbesserungen</h4>
            </div>
            {improvements.length > 0 ? (
              <ul className="space-y-2">
                {improvements.slice(0, 4).map((item) => (
                  <li key={item.id} className="flex items-start gap-2 text-sm">
                    <span className="text-amber-500 mt-1">•</span>
                    <span className="text-warm-700">{item.title}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-warm-500">Keine Verbesserungen nötig</p>
            )}
          </Card>
        </motion.div>
      </div>

      {/* Critical gaps warning */}
      {criticalGaps.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <Card variant="default" padding="md" className="border-red-200 bg-red-50">
            <div className="flex items-start gap-3">
              <AlertTriangle size={24} className="text-red-500 flex-shrink-0" />
              <div>
                <h4 className="font-semibold text-red-800">
                  Kritische Lücken gefunden
                </h4>
                <p className="text-sm text-red-700 mt-1">
                  Diese Punkte solltest du vor dem Abschluss verbessern:
                </p>
                <ul className="mt-2 space-y-1">
                  {criticalGaps.map((gap) => (
                    <li key={gap.id} className="text-sm text-red-600 flex items-start gap-2">
                      <span className="text-red-400 mt-1">•</span>
                      {gap.description}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Continue button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="flex justify-center"
      >
        <Button
          variant="accent"
          size="lg"
          onClick={onContinue}
          rightIcon={<ArrowRight size={20} />}
        >
          {isLastModule ? 'Businessplan abschließen' : `Weiter zu Modul ${(moduleNumber + 1) as ModuleNumber}`}
        </Button>
      </motion.div>
    </div>
  );
};

export default ModuleSummary;
