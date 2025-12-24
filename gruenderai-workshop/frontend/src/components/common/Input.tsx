import { forwardRef, InputHTMLAttributes, TextareaHTMLAttributes, ReactNode, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye, EyeOff, AlertCircle, CheckCircle, HelpCircle } from 'lucide-react';

type InputSize = 'sm' | 'md' | 'lg';
type InputVariant = 'default' | 'filled' | 'outlined';

interface BaseInputProps {
  label?: string;
  error?: string;
  hint?: string;
  success?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  size?: InputSize;
  variant?: InputVariant;
  fullWidth?: boolean;
  tooltip?: string;
}

interface TextInputProps extends BaseInputProps, Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url';
}

interface TextAreaProps extends BaseInputProps, Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, 'size'> {
  rows?: number;
  autoResize?: boolean;
  maxLength?: number;
  showCount?: boolean;
}

const SIZES = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2.5 text-base',
  lg: 'px-5 py-3.5 text-lg'
};

const VARIANTS = {
  default: 'bg-white border-warm-300 focus:border-primary-500 focus:ring-primary-500',
  filled: 'bg-warm-100 border-transparent focus:bg-white focus:border-primary-500 focus:ring-primary-500',
  outlined: 'bg-transparent border-2 border-warm-300 focus:border-primary-500 focus:ring-0'
};

export const Input = forwardRef<HTMLInputElement, TextInputProps>(
  (
    {
      label,
      error,
      hint,
      success,
      leftIcon,
      rightIcon,
      size = 'md',
      variant = 'default',
      fullWidth = true,
      tooltip,
      type = 'text',
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = useState(false);
    const [showTooltip, setShowTooltip] = useState(false);
    const isPassword = type === 'password';
    const inputType = isPassword && showPassword ? 'text' : type;

    const baseClasses = `
      block rounded-xl border transition-all duration-200
      placeholder:text-warm-400
      focus:outline-none focus:ring-2 focus:ring-offset-0
      disabled:bg-warm-100 disabled:text-warm-500 disabled:cursor-not-allowed
      ${SIZES[size]}
      ${VARIANTS[variant]}
      ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}
      ${success ? 'border-green-500 focus:border-green-500 focus:ring-green-500' : ''}
      ${leftIcon ? 'pl-10' : ''}
      ${rightIcon || isPassword || error || success ? 'pr-10' : ''}
      ${fullWidth ? 'w-full' : ''}
      ${className}
    `.trim();

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {/* Label with optional tooltip */}
        {label && (
          <div className="flex items-center gap-1 mb-1.5">
            <label className="block text-sm font-medium text-warm-700">
              {label}
            </label>
            {tooltip && (
              <div className="relative">
                <button
                  type="button"
                  onMouseEnter={() => setShowTooltip(true)}
                  onMouseLeave={() => setShowTooltip(false)}
                  className="text-warm-400 hover:text-warm-500"
                >
                  <HelpCircle size={14} />
                </button>
                <AnimatePresence>
                  {showTooltip && (
                    <motion.div
                      initial={{ opacity: 0, y: -5 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -5 }}
                      className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 bg-warm-900 text-white text-xs rounded-lg shadow-lg z-50"
                    >
                      {tooltip}
                      <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-warm-900" />
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )}
          </div>
        )}

        {/* Input container */}
        <div className="relative">
          {/* Left icon */}
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-warm-400">
              {leftIcon}
            </div>
          )}

          {/* Input element */}
          <input
            ref={ref}
            type={inputType}
            className={baseClasses}
            disabled={disabled}
            {...props}
          />

          {/* Right icons container */}
          <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1">
            {isPassword && (
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-warm-400 hover:text-warm-600"
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            )}
            {error && <AlertCircle size={18} className="text-red-500" />}
            {success && !error && <CheckCircle size={18} className="text-green-500" />}
            {rightIcon && !error && !success && !isPassword && rightIcon}
          </div>
        </div>

        {/* Error or hint message */}
        <AnimatePresence mode="wait">
          {error && (
            <motion.p
              initial={{ opacity: 0, y: -5 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -5 }}
              className="mt-1.5 text-sm text-red-600 flex items-center gap-1"
            >
              {error}
            </motion.p>
          )}
          {!error && hint && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-1.5 text-sm text-warm-500"
            >
              {hint}
            </motion.p>
          )}
        </AnimatePresence>
      </div>
    );
  }
);

Input.displayName = 'Input';

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  (
    {
      label,
      error,
      hint,
      success,
      size = 'md',
      variant = 'default',
      fullWidth = true,
      rows = 4,
      autoResize = false,
      maxLength,
      showCount = false,
      className = '',
      disabled,
      value,
      onChange,
      ...props
    },
    ref
  ) => {
    const [charCount, setCharCount] = useState(
      typeof value === 'string' ? value.length : 0
    );

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      if (showCount || maxLength) {
        setCharCount(e.target.value.length);
      }
      if (autoResize) {
        e.target.style.height = 'auto';
        e.target.style.height = `${e.target.scrollHeight}px`;
      }
      onChange?.(e);
    };

    const baseClasses = `
      block rounded-xl border transition-all duration-200
      placeholder:text-warm-400
      focus:outline-none focus:ring-2 focus:ring-offset-0
      disabled:bg-warm-100 disabled:text-warm-500 disabled:cursor-not-allowed
      resize-none
      ${SIZES[size]}
      ${VARIANTS[variant]}
      ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}
      ${success ? 'border-green-500 focus:border-green-500 focus:ring-green-500' : ''}
      ${fullWidth ? 'w-full' : ''}
      ${className}
    `.trim();

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label className="block text-sm font-medium text-warm-700 mb-1.5">
            {label}
          </label>
        )}

        <div className="relative">
          <textarea
            ref={ref}
            rows={rows}
            className={baseClasses}
            disabled={disabled}
            value={value}
            onChange={handleChange}
            maxLength={maxLength}
            {...props}
          />

          {/* Status icon */}
          {(error || success) && (
            <div className="absolute right-3 top-3">
              {error && <AlertCircle size={18} className="text-red-500" />}
              {success && !error && <CheckCircle size={18} className="text-green-500" />}
            </div>
          )}
        </div>

        {/* Footer with error/hint and character count */}
        <div className="flex items-center justify-between mt-1.5">
          <AnimatePresence mode="wait">
            {error && (
              <motion.p
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -5 }}
                className="text-sm text-red-600"
              >
                {error}
              </motion.p>
            )}
            {!error && hint && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-sm text-warm-500"
              >
                {hint}
              </motion.p>
            )}
          </AnimatePresence>

          {(showCount || maxLength) && (
            <span className={`text-sm ${maxLength && charCount >= maxLength ? 'text-red-500' : 'text-warm-400'}`}>
              {charCount}{maxLength && `/${maxLength}`}
            </span>
          )}
        </div>
      </div>
    );
  }
);

TextArea.displayName = 'TextArea';

export default Input;
