import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface ProgressRingProps {
  progress: number; // 0-100
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showPercentage?: boolean;
  label?: string;
  animated?: boolean;
  color?: 'primary' | 'accent' | 'success' | 'warning' | 'danger';
  thickness?: number;
}

const SIZES = {
  sm: { width: 48, fontSize: 'text-xs' },
  md: { width: 80, fontSize: 'text-sm' },
  lg: { width: 120, fontSize: 'text-lg' },
  xl: { width: 160, fontSize: 'text-2xl' }
};

const COLORS = {
  primary: 'stroke-primary-500',
  accent: 'stroke-accent-500',
  success: 'stroke-green-500',
  warning: 'stroke-amber-500',
  danger: 'stroke-red-500'
};

const BG_COLORS = {
  primary: 'stroke-primary-100',
  accent: 'stroke-accent-100',
  success: 'stroke-green-100',
  warning: 'stroke-amber-100',
  danger: 'stroke-red-100'
};

export const ProgressRing = ({
  progress,
  size = 'md',
  showPercentage = true,
  label,
  animated = true,
  color = 'primary',
  thickness = 8
}: ProgressRingProps) => {
  const [animatedProgress, setAnimatedProgress] = useState(animated ? 0 : progress);
  const { width, fontSize } = SIZES[size];
  const radius = (width - thickness) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (animatedProgress / 100) * circumference;

  useEffect(() => {
    if (animated) {
      const timer = setTimeout(() => {
        setAnimatedProgress(progress);
      }, 100);
      return () => clearTimeout(timer);
    } else {
      setAnimatedProgress(progress);
    }
  }, [progress, animated]);

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width, height: width }}>
        <svg
          className="transform -rotate-90"
          width={width}
          height={width}
        >
          {/* Background circle */}
          <circle
            className={BG_COLORS[color]}
            strokeWidth={thickness}
            fill="none"
            r={radius}
            cx={width / 2}
            cy={width / 2}
          />
          {/* Progress circle */}
          <motion.circle
            className={COLORS[color]}
            strokeWidth={thickness}
            strokeLinecap="round"
            fill="none"
            r={radius}
            cx={width / 2}
            cy={width / 2}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: animated ? 1 : 0, ease: 'easeOut' }}
            style={{
              strokeDasharray: circumference
            }}
          />
        </svg>

        {/* Center content */}
        {showPercentage && (
          <div className="absolute inset-0 flex items-center justify-center">
            <motion.span
              className={`font-semibold text-warm-800 ${fontSize}`}
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: animated ? 0.5 : 0, duration: 0.3 }}
            >
              {Math.round(animatedProgress)}%
            </motion.span>
          </div>
        )}
      </div>

      {label && (
        <motion.span
          className="text-sm text-warm-600 text-center font-medium"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: animated ? 0.7 : 0 }}
        >
          {label}
        </motion.span>
      )}
    </div>
  );
};

export default ProgressRing;
