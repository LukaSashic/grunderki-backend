import { forwardRef, ButtonHTMLAttributes, ReactNode } from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import { Loader2 } from 'lucide-react';

type ButtonVariant = 'primary' | 'secondary' | 'accent' | 'ghost' | 'danger' | 'outline';
type ButtonSize = 'sm' | 'md' | 'lg' | 'xl';

interface ButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'color'> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  fullWidth?: boolean;
  animated?: boolean;
}

const VARIANTS = {
  primary: 'bg-primary-600 hover:bg-primary-700 text-white shadow-elegant hover:shadow-elevated active:bg-primary-800 disabled:bg-primary-300',
  secondary: 'bg-warm-100 hover:bg-warm-200 text-warm-800 border border-warm-200 hover:border-warm-300 active:bg-warm-300 disabled:bg-warm-50 disabled:text-warm-400',
  accent: 'bg-gradient-to-r from-accent-500 to-accent-600 hover:from-accent-600 hover:to-accent-700 text-white shadow-gold-glow hover:shadow-lg active:from-accent-700 active:to-accent-800 disabled:from-accent-200 disabled:to-accent-300',
  ghost: 'bg-transparent hover:bg-warm-100 text-warm-700 active:bg-warm-200 disabled:text-warm-400',
  danger: 'bg-red-600 hover:bg-red-700 text-white shadow-sm hover:shadow active:bg-red-800 disabled:bg-red-300',
  outline: 'bg-transparent border-2 border-primary-500 text-primary-600 hover:bg-primary-50 active:bg-primary-100 disabled:border-primary-200 disabled:text-primary-300'
};

const SIZES = {
  sm: 'px-3 py-1.5 text-sm gap-1.5 rounded-lg',
  md: 'px-4 py-2 text-base gap-2 rounded-xl',
  lg: 'px-6 py-3 text-lg gap-2 rounded-xl',
  xl: 'px-8 py-4 text-xl gap-3 rounded-2xl'
};

const ICON_SIZES = {
  sm: 14,
  md: 18,
  lg: 20,
  xl: 24
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      animated = true,
      children,
      disabled,
      className = '',
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || isLoading;

    const baseClasses = `
      inline-flex items-center justify-center
      font-semibold transition-all duration-200
      focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
      disabled:cursor-not-allowed
      ${VARIANTS[variant]}
      ${SIZES[size]}
      ${fullWidth ? 'w-full' : ''}
      ${className}
    `.trim();

    const content = (
      <>
        {isLoading ? (
          <Loader2 size={ICON_SIZES[size]} className="animate-spin" />
        ) : leftIcon ? (
          <span className="flex-shrink-0">{leftIcon}</span>
        ) : null}
        {children && <span>{children}</span>}
        {rightIcon && !isLoading && (
          <span className="flex-shrink-0">{rightIcon}</span>
        )}
      </>
    );

    if (animated && !isDisabled) {
      return (
        <motion.button
          ref={ref}
          className={baseClasses}
          disabled={isDisabled}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          transition={{ type: 'spring', stiffness: 400, damping: 17 }}
          {...(props as HTMLMotionProps<'button'>)}
        >
          {content}
        </motion.button>
      );
    }

    return (
      <button
        ref={ref}
        className={baseClasses}
        disabled={isDisabled}
        {...props}
      >
        {content}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
