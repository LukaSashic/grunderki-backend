import { motion } from 'framer-motion';
import { RefreshCw, Quote, ChevronRight, ArrowRight } from 'lucide-react';
import { Card, Badge } from '@/components/common';

interface RecapCardProps {
  conceptName: string;
  previousAnswer: string;
  previousModule: number;
  currentStage: string;
  onViewPrevious?: () => void;
}

const STAGE_LABELS: Record<string, { label: string; color: string }> = {
  introduce: { label: 'Eingeführt', color: 'primary' },
  reinforce: { label: 'Vertiefung', color: 'blue' },
  apply: { label: 'Anwendung', color: 'green' },
  validate: { label: 'Validierung', color: 'purple' }
};

export const RecapCard = ({
  conceptName,
  previousAnswer,
  previousModule,
  currentStage,
  onViewPrevious
}: RecapCardProps) => {
  const stageConfig = STAGE_LABELS[currentStage] || STAGE_LABELS.reinforce;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
    >
      <Card
        variant="default"
        padding="md"
        className="bg-gradient-to-br from-primary-50 to-blue-50 border-primary-100"
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <RefreshCw size={16} className="text-primary-500" />
            <span className="text-sm font-medium text-primary-700">
              Erinnerung: {conceptName}
            </span>
          </div>
          <Badge variant={stageConfig.color as any} size="xs">
            {stageConfig.label}
          </Badge>
        </div>

        {/* Previous answer quote */}
        <div className="relative pl-4 border-l-2 border-primary-300 mb-3">
          <Quote size={14} className="absolute -left-2 -top-1 text-primary-300 bg-primary-50 rounded" />
          <p className="text-sm text-warm-700 italic">
            "{previousAnswer.length > 150
              ? `${previousAnswer.substring(0, 150)}...`
              : previousAnswer}"
          </p>
          <p className="text-xs text-warm-500 mt-1">
            Deine Antwort aus Modul {previousModule}
          </p>
        </div>

        {/* Connection prompt */}
        <div className="flex items-center gap-2 text-sm text-primary-600">
          <ArrowRight size={14} />
          <span>Nutze dieses Wissen für die nächste Frage...</span>
        </div>

        {/* Optional view previous button */}
        {onViewPrevious && (
          <button
            onClick={onViewPrevious}
            className="mt-3 text-xs text-primary-500 hover:text-primary-700 flex items-center gap-1"
          >
            Zur ursprünglichen Frage
            <ChevronRight size={12} />
          </button>
        )}
      </Card>
    </motion.div>
  );
};

interface ConceptProgressionProps {
  conceptId: string;
  conceptName: string;
  stages: Array<{
    moduleNumber: number;
    stage: string;
    completed: boolean;
  }>;
  currentModule: number;
}

export const ConceptProgression = ({
  conceptId,
  conceptName,
  stages,
  currentModule
}: ConceptProgressionProps) => {
  return (
    <div className="p-3 bg-warm-50 rounded-lg border border-warm-200">
      <p className="text-sm font-medium text-warm-800 mb-2">{conceptName}</p>

      <div className="flex items-center gap-1">
        {stages.map((stage, index) => {
          const isCompleted = stage.completed;
          const isCurrent = stage.moduleNumber === currentModule;
          const stageConfig = STAGE_LABELS[stage.stage];

          return (
            <div key={`${conceptId}-${stage.moduleNumber}`} className="flex items-center">
              <div
                className={`
                  px-2 py-1 rounded text-xs font-medium
                  ${isCompleted
                    ? 'bg-green-100 text-green-700'
                    : isCurrent
                      ? 'bg-primary-100 text-primary-700 ring-2 ring-primary-300'
                      : 'bg-warm-200 text-warm-500'
                  }
                `}
                title={`Modul ${stage.moduleNumber}: ${stageConfig?.label || stage.stage}`}
              >
                M{stage.moduleNumber}
              </div>
              {index < stages.length - 1 && (
                <ChevronRight size={14} className="text-warm-400 mx-0.5" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RecapCard;
