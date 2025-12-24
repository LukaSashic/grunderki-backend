import { ReactNode } from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

type CardVariant = 'default' | 'elevated' | 'interactive' | 'accent' | 'outlined';

interface CardProps extends Omit<HTMLMotionProps<'div'>, 'children'> {
  children: ReactNode;
  variant?: CardVariant;
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  animated?: boolean;
  hoverable?: boolean;
}

const VARIANTS = {
  default: 'bg-white border border-warm-200 shadow-card',
  elevated: 'bg-white shadow-elevated border border-warm-100',
  interactive: 'bg-white border border-warm-200 shadow-card hover:shadow-elevated hover:border-primary-200 cursor-pointer',
  accent: 'bg-gradient-to-br from-primary-50 to-accent-50 border border-primary-100 shadow-card',
  outlined: 'bg-transparent border-2 border-warm-200'
};

const PADDING = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
  xl: 'p-8'
};

export const Card = ({
  children,
  variant = 'default',
  padding = 'md',
  animated = false,
  hoverable = false,
  className = '',
  ...props
}: CardProps) => {
  const baseClasses = `
    rounded-2xl transition-all duration-300
    ${VARIANTS[variant]}
    ${PADDING[padding]}
    ${className}
  `.trim();

  if (animated || hoverable) {
    return (
      <motion.div
        className={baseClasses}
        initial={animated ? { opacity: 0, y: 20 } : undefined}
        animate={animated ? { opacity: 1, y: 0 } : undefined}
        whileHover={hoverable ? { y: -2, scale: 1.01 } : undefined}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        {...props}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <div className={baseClasses} {...(props as any)}>
      {children}
    </div>
  );
};

interface CardHeaderProps {
  children: ReactNode;
  className?: string;
  action?: ReactNode;
}

export const CardHeader = ({ children, className = '', action }: CardHeaderProps) => (
  <div className={`flex items-center justify-between pb-4 border-b border-warm-100 ${className}`}>
    <div className="flex-1">{children}</div>
    {action && <div className="ml-4">{action}</div>}
  </div>
);

interface CardTitleProps {
  children: ReactNode;
  className?: string;
  subtitle?: string;
}

export const CardTitle = ({ children, className = '', subtitle }: CardTitleProps) => (
  <div className={className}>
    <h3 className="text-lg font-display font-semibold text-warm-900">{children}</h3>
    {subtitle && <p className="text-sm text-warm-500 mt-1">{subtitle}</p>}
  </div>
);

interface CardContentProps {
  children: ReactNode;
  className?: string;
}

export const CardContent = ({ children, className = '' }: CardContentProps) => (
  <div className={`pt-4 ${className}`}>{children}</div>
);

interface CardFooterProps {
  children: ReactNode;
  className?: string;
  align?: 'left' | 'center' | 'right' | 'between';
}

const ALIGN = {
  left: 'justify-start',
  center: 'justify-center',
  right: 'justify-end',
  between: 'justify-between'
};

export const CardFooter = ({ children, className = '', align = 'right' }: CardFooterProps) => (
  <div className={`flex items-center ${ALIGN[align]} pt-4 border-t border-warm-100 mt-4 ${className}`}>
    {children}
  </div>
);

export default Card;
