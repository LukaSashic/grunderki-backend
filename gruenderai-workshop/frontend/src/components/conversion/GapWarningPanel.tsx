import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, X, ChevronRight, Shield, AlertCircle, Info } from 'lucide-react';
import { Button, Card, Badge } from '@/components/common';
import type { Gap } from '@/types/workshop.types';

interface GapWarningPanelProps {
  gaps: Gap[];
  onClose?: () => void;
  onAddressGap?: (gapId: string) => void;
  position?: 'fixed' | 'inline';
}

const SEVERITY_CONFIG = {
  critical: {
    color: 'red',
    icon: AlertTriangle,
    bgClass: 'bg-red-50 border-red-200',
    textClass: 'text-red-800',
    badgeVariant: 'danger' as const,
    label: 'Kritisch'
  },
  warning: {
    color: 'amber',
    icon: AlertCircle,
    bgClass: 'bg-amber-50 border-amber-200',
    textClass: 'text-amber-800',
    badgeVariant: 'warning' as const,
    label: 'Warnung'
  },
  info: {
    color: 'blue',
    icon: Info,
    bgClass: 'bg-blue-50 border-blue-200',
    textClass: 'text-blue-800',
    badgeVariant: 'info' as const,
    label: 'Hinweis'
  }
};

export const GapWarningPanel = ({
  gaps,
  onClose,
  onAddressGap,
  position = 'inline'
}: GapWarningPanelProps) => {
  const [isMinimized, setIsMinimized] = useState(false);

  const criticalGaps = gaps.filter(g => g.severity === 'critical');
  const warningGaps = gaps.filter(g => g.severity === 'warning');
  const infoGaps = gaps.filter(g => g.severity === 'info');

  if (gaps.length === 0) return null;

  const containerClass = position === 'fixed'
    ? 'fixed bottom-4 right-4 z-40 w-80 max-h-[60vh] overflow-auto'
    : 'w-full';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={containerClass}
    >
      <Card
        variant="default"
        padding="none"
        className="border-red-200 shadow-elevated overflow-hidden"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 bg-gradient-to-r from-red-50 to-amber-50 border-b border-warm-200">
          <div className="flex items-center gap-2">
            <Shield size={20} className="text-red-500" />
            <div>
              <h3 className="font-semibold text-warm-900">GZ-Lücken erkannt</h3>
              <p className="text-xs text-warm-500">
                {gaps.length} Punkte benötigen Aufmerksamkeit
              </p>
            </div>
          </div>
          <div className="flex items-center gap-1">
            {onClose && (
              <button
                onClick={() => setIsMinimized(!isMinimized)}
                className="p-1.5 text-warm-400 hover:text-warm-600 hover:bg-warm-100 rounded transition-colors"
              >
                {isMinimized ? <ChevronRight size={16} /> : <X size={16} />}
              </button>
            )}
          </div>
        </div>

        {/* Content */}
        <AnimatePresence>
          {!isMinimized && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden"
            >
              <div className="p-4 space-y-4">
                {/* Critical gaps */}
                {criticalGaps.length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle size={16} className="text-red-500" />
                      <span className="text-sm font-semibold text-red-800">
                        Kritische Probleme ({criticalGaps.length})
                      </span>
                    </div>
                    <div className="space-y-2">
                      {criticalGaps.map((gap) => (
                        <GapItem
                          key={gap.id}
                          gap={gap}
                          onAddress={onAddressGap}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Warning gaps */}
                {warningGaps.length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <AlertCircle size={16} className="text-amber-500" />
                      <span className="text-sm font-semibold text-amber-800">
                        Warnungen ({warningGaps.length})
                      </span>
                    </div>
                    <div className="space-y-2">
                      {warningGaps.map((gap) => (
                        <GapItem
                          key={gap.id}
                          gap={gap}
                          onAddress={onAddressGap}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Info gaps */}
                {infoGaps.length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Info size={16} className="text-blue-500" />
                      <span className="text-sm font-semibold text-blue-800">
                        Hinweise ({infoGaps.length})
                      </span>
                    </div>
                    <div className="space-y-2">
                      {infoGaps.map((gap) => (
                        <GapItem
                          key={gap.id}
                          gap={gap}
                          onAddress={onAddressGap}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Score impact */}
                <div className="pt-3 border-t border-warm-200">
                  <p className="text-sm text-warm-600">
                    <span className="font-semibold text-red-600">
                      -{gaps.reduce((sum, g) => sum + g.scoreImpact, 0)}%
                    </span>
                    {' '}Auswirkung auf deinen GZ-Score
                  </p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </Card>
    </motion.div>
  );
};

interface GapItemProps {
  gap: Gap;
  onAddress?: (gapId: string) => void;
}

const GapItem = ({ gap, onAddress }: GapItemProps) => {
  const config = SEVERITY_CONFIG[gap.severity];
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      className={`${config.bgClass} border rounded-lg p-3`}
    >
      <div className="flex items-start gap-2">
        <Icon size={16} className={`${config.textClass} flex-shrink-0 mt-0.5`} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-sm font-medium ${config.textClass}`}>
              {gap.title}
            </span>
            <Badge variant={config.badgeVariant} size="xs">
              {config.label}
            </Badge>
          </div>
          <p className="text-xs text-warm-600 line-clamp-2">
            {gap.description}
          </p>
          {gap.suggestion && (
            <p className="text-xs text-warm-500 mt-1 italic">
              Tipp: {gap.suggestion}
            </p>
          )}
          {onAddress && (
            <button
              onClick={() => onAddress(gap.id)}
              className="mt-2 text-xs text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1"
            >
              Beheben
              <ChevronRight size={12} />
            </button>
          )}
        </div>
        <span className="text-xs font-medium text-red-600">
          -{gap.scoreImpact}%
        </span>
      </div>
    </motion.div>
  );
};

// Mini version for inline display
interface MiniGapWarningProps {
  criticalCount: number;
  warningCount: number;
  onClick?: () => void;
}

export const MiniGapWarning = ({ criticalCount, warningCount, onClick }: MiniGapWarningProps) => {
  if (criticalCount === 0 && warningCount === 0) return null;

  return (
    <motion.button
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      onClick={onClick}
      className={`
        flex items-center gap-2 px-3 py-1.5 rounded-full transition-all
        ${criticalCount > 0
          ? 'bg-red-100 text-red-700 hover:bg-red-200'
          : 'bg-amber-100 text-amber-700 hover:bg-amber-200'
        }
      `}
    >
      {criticalCount > 0 ? (
        <AlertTriangle size={14} />
      ) : (
        <AlertCircle size={14} />
      )}
      <span className="text-sm font-medium">
        {criticalCount + warningCount} Lücken
      </span>
    </motion.button>
  );
};

export default GapWarningPanel;
