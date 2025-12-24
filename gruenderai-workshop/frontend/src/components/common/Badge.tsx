import { ReactNode } from 'react';
import { motion } from 'framer-motion';

type BadgeVariant = 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'accent';
type BadgeSize = 'xs' | 'sm' | 'md' | 'lg';

interface BadgeProps {
  children: ReactNode;
  variant?: BadgeVariant;
  size?: BadgeSize;
  rounded?: boolean;
  animated?: boolean;
  icon?: ReactNode;
  removable?: boolean;
  onRemove?: () => void;
}

const VARIANTS = {
  default: 'bg-warm-100 text-warm-700 border-warm-200',
  primary: 'bg-primary-100 text-primary-700 border-primary-200',
  secondary: 'bg-warm-200 text-warm-800 border-warm-300',
  success: 'bg-green-100 text-green-700 border-green-200',
  warning: 'bg-amber-100 text-amber-700 border-amber-200',
  danger: 'bg-red-100 text-red-700 border-red-200',
  info: 'bg-blue-100 text-blue-700 border-blue-200',
  accent: 'bg-gradient-to-r from-accent-100 to-accent-200 text-accent-800 border-accent-300'
};

const SIZES = {
  xs: 'px-1.5 py-0.5 text-xs',
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base'
};

export const Badge = ({
  children,
  variant = 'default',
  size = 'sm',
  rounded = false,
  animated = false,
  icon,
  removable = false,
  onRemove
}: BadgeProps) => {
  const baseClasses = `
    inline-flex items-center gap-1 font-medium border
    ${VARIANTS[variant]}
    ${SIZES[size]}
    ${rounded ? 'rounded-full' : 'rounded-md'}
  `.trim();

  const content = (
    <>
      {icon && <span className="flex-shrink-0">{icon}</span>}
      <span>{children}</span>
      {removable && (
        <button
          onClick={onRemove}
          className="ml-0.5 hover:bg-black/10 rounded-full p-0.5 transition-colors"
          aria-label="Entfernen"
        >
          <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
            <path d="M9.5 3.2L8.8 2.5 6 5.3 3.2 2.5l-.7.7L5.3 6 2.5 8.8l.7.7L6 6.7l2.8 2.8.7-.7L6.7 6l2.8-2.8z" />
          </svg>
        </button>
      )}
    </>
  );

  if (animated) {
    return (
      <motion.span
        className={baseClasses}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 500, damping: 25 }}
      >
        {content}
      </motion.span>
    );
  }

  return <span className={baseClasses}>{content}</span>;
};

interface StatusBadgeProps {
  status: 'pending' | 'in_progress' | 'completed' | 'error' | 'locked';
  size?: BadgeSize;
  showIcon?: boolean;
}

const STATUS_CONFIG = {
  pending: { variant: 'default' as const, label: 'Ausstehend', icon: '○' },
  in_progress: { variant: 'primary' as const, label: 'In Bearbeitung', icon: '◐' },
  completed: { variant: 'success' as const, label: 'Abgeschlossen', icon: '●' },
  error: { variant: 'danger' as const, label: 'Fehler', icon: '!' },
  locked: { variant: 'secondary' as const, label: 'Gesperrt', icon: '🔒' }
};

export const StatusBadge = ({ status, size = 'sm', showIcon = true }: StatusBadgeProps) => {
  const config = STATUS_CONFIG[status];

  return (
    <Badge variant={config.variant} size={size} rounded>
      {showIcon && <span className="mr-0.5">{config.icon}</span>}
      {config.label}
    </Badge>
  );
};

interface ModuleBadgeProps {
  moduleNumber: number;
  isActive?: boolean;
  isCompleted?: boolean;
  size?: BadgeSize;
}

export const ModuleBadge = ({
  moduleNumber,
  isActive = false,
  isCompleted = false,
  size = 'md'
}: ModuleBadgeProps) => {
  let variant: BadgeVariant = 'default';
  if (isCompleted) variant = 'success';
  else if (isActive) variant = 'primary';

  return (
    <Badge variant={variant} size={size} rounded>
      Modul {moduleNumber}
    </Badge>
  );
};

interface ScoreBadgeProps {
  score: number;
  showLabel?: boolean;
  size?: BadgeSize;
}

export const ScoreBadge = ({ score, showLabel = true, size = 'md' }: ScoreBadgeProps) => {
  let variant: BadgeVariant = 'danger';
  let label = 'Kritisch';

  if (score >= 80) {
    variant = 'success';
    label = 'Exzellent';
  } else if (score >= 60) {
    variant = 'primary';
    label = 'Gut';
  } else if (score >= 40) {
    variant = 'warning';
    label = 'Ausreichend';
  }

  return (
    <Badge variant={variant} size={size} rounded animated>
      {score}%{showLabel && ` - ${label}`}
    </Badge>
  );
};

export default Badge;
