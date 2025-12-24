import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, XCircle, Info } from 'lucide-react';

interface QualityGaugeProps {
  score: number; // 0-100
  label?: string;
  showIcon?: boolean;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'bar' | 'radial' | 'compact';
  animated?: boolean;
}

const getScoreLevel = (score: number) => {
  if (score >= 80) return { level: 'excellent', color: 'green', label: 'Exzellent' };
  if (score >= 60) return { level: 'good', color: 'primary', label: 'Gut' };
  if (score >= 40) return { level: 'fair', color: 'amber', label: 'Ausreichend' };
  if (score >= 20) return { level: 'needs_work', color: 'orange', label: 'Verbesserungswuerdig' };
  return { level: 'critical', color: 'red', label: 'Kritisch' };
};

const ICONS = {
  excellent: CheckCircle,
  good: CheckCircle,
  fair: Info,
  needs_work: AlertTriangle,
  critical: XCircle
};

const COLORS = {
  green: {
    bg: 'bg-green-100',
    fill: 'bg-green-500',
    text: 'text-green-700',
    border: 'border-green-200'
  },
  primary: {
    bg: 'bg-primary-100',
    fill: 'bg-primary-500',
    text: 'text-primary-700',
    border: 'border-primary-200'
  },
  amber: {
    bg: 'bg-amber-100',
    fill: 'bg-amber-500',
    text: 'text-amber-700',
    border: 'border-amber-200'
  },
  orange: {
    bg: 'bg-orange-100',
    fill: 'bg-orange-500',
    text: 'text-orange-700',
    border: 'border-orange-200'
  },
  red: {
    bg: 'bg-red-100',
    fill: 'bg-red-500',
    text: 'text-red-700',
    border: 'border-red-200'
  }
};

const SIZES = {
  sm: { height: 'h-2', iconSize: 16, textSize: 'text-xs' },
  md: { height: 'h-3', iconSize: 20, textSize: 'text-sm' },
  lg: { height: 'h-4', iconSize: 24, textSize: 'text-base' }
};

export const QualityGauge = ({
  score,
  label,
  showIcon = true,
  size = 'md',
  variant = 'bar',
  animated = true
}: QualityGaugeProps) => {
  const { level, color, label: scoreLabel } = useMemo(() => getScoreLevel(score), [score]);
  const Icon = ICONS[level as keyof typeof ICONS];
  const colorScheme = COLORS[color as keyof typeof COLORS];
  const sizeConfig = SIZES[size];

  if (variant === 'compact') {
    return (
      <div className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full ${colorScheme.bg} ${colorScheme.border} border`}>
        {showIcon && <Icon size={sizeConfig.iconSize - 4} className={colorScheme.text} />}
        <span className={`${sizeConfig.textSize} font-medium ${colorScheme.text}`}>
          {score}%
        </span>
      </div>
    );
  }

  if (variant === 'radial') {
    const radius = 40;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
      <div className="flex flex-col items-center gap-2">
        <div className="relative w-24 h-24">
          <svg className="transform -rotate-90 w-full h-full">
            <circle
              className={colorScheme.bg.replace('bg-', 'stroke-')}
              strokeWidth="8"
              fill="none"
              r={radius}
              cx="48"
              cy="48"
            />
            <motion.circle
              className={colorScheme.fill.replace('bg-', 'stroke-')}
              strokeWidth="8"
              strokeLinecap="round"
              fill="none"
              r={radius}
              cx="48"
              cy="48"
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset }}
              transition={{ duration: animated ? 1 : 0, ease: 'easeOut' }}
              style={{ strokeDasharray: circumference }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            {showIcon && <Icon size={20} className={colorScheme.text} />}
            <span className={`text-lg font-bold ${colorScheme.text}`}>{score}%</span>
          </div>
        </div>
        {label && (
          <span className={`${sizeConfig.textSize} text-warm-600 text-center`}>
            {label}
          </span>
        )}
      </div>
    );
  }

  // Default bar variant
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {showIcon && <Icon size={sizeConfig.iconSize} className={colorScheme.text} />}
          {label && (
            <span className={`${sizeConfig.textSize} font-medium text-warm-700`}>
              {label}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className={`${sizeConfig.textSize} font-medium ${colorScheme.text}`}>
            {scoreLabel}
          </span>
          <span className={`${sizeConfig.textSize} font-bold ${colorScheme.text}`}>
            {score}%
          </span>
        </div>
      </div>

      <div className={`w-full ${colorScheme.bg} rounded-full ${sizeConfig.height} overflow-hidden`}>
        <motion.div
          className={`${sizeConfig.height} ${colorScheme.fill} rounded-full`}
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: animated ? 1 : 0, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
};

export default QualityGauge;
