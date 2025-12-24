/**
 * CustomInputModal Component
 * Modal for entering custom text when "Sonstiges" (Other) is selected
 */

import { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Send, Lightbulb } from 'lucide-react';
import { clsx } from 'clsx';

export interface CustomInputModalProps {
  /** Whether the modal is open */
  isOpen: boolean;
  /** Callback to close the modal */
  onClose: () => void;
  /** Callback when user submits their custom input */
  onSubmit: (value: string) => void;
  /** Title/question displayed in the modal */
  title: string;
  /** Placeholder text for the input */
  placeholder?: string;
  /** Optional hint/tip to help the user */
  hint?: string;
  /** Example answers to inspire the user */
  examples?: string[];
  /** Maximum character count */
  maxLength?: number;
  /** Minimum character count */
  minLength?: number;
  /** Whether to show the modal in loading state */
  isLoading?: boolean;
}

export function CustomInputModal({
  isOpen,
  onClose,
  onSubmit,
  title,
  placeholder = 'Ihre Antwort eingeben...',
  hint,
  examples = [],
  maxLength = 500,
  minLength = 3,
  isLoading = false,
}: CustomInputModalProps) {
  const [value, setValue] = useState('');
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Focus textarea when modal opens
  useEffect(() => {
    if (isOpen && textareaRef.current) {
      setTimeout(() => textareaRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // Reset state when modal closes
  useEffect(() => {
    if (!isOpen) {
      setValue('');
      setError(null);
    }
  }, [isOpen]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  }, [value]);

  const handleSubmit = useCallback(() => {
    const trimmedValue = value.trim();

    // Validation
    if (trimmedValue.length < minLength) {
      setError(`Bitte mindestens ${minLength} Zeichen eingeben`);
      return;
    }

    if (trimmedValue.length > maxLength) {
      setError(`Maximal ${maxLength} Zeichen erlaubt`);
      return;
    }

    setError(null);
    onSubmit(trimmedValue);
  }, [value, minLength, maxLength, onSubmit]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      // Submit on Enter (without Shift)
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
      }
      // Close on Escape
      if (e.key === 'Escape') {
        onClose();
      }
    },
    [handleSubmit, onClose]
  );

  const handleExampleClick = useCallback((example: string) => {
    setValue(example);
    setError(null);
    textareaRef.current?.focus();
  }, []);

  const isValidLength = value.trim().length >= minLength && value.trim().length <= maxLength;
  const characterCount = value.length;
  const isNearLimit = characterCount > maxLength * 0.8;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2, ease: [0.25, 0.46, 0.45, 0.94] }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none"
          >
            <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full pointer-events-auto">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-100">
                <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  aria-label="Schliessen"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>

              {/* Content */}
              <div className="p-4 space-y-4">
                {/* Hint */}
                {hint && (
                  <div className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg">
                    <Lightbulb className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-blue-700">{hint}</p>
                  </div>
                )}

                {/* Textarea */}
                <div className="relative">
                  <textarea
                    ref={textareaRef}
                    value={value}
                    onChange={(e) => {
                      setValue(e.target.value);
                      setError(null);
                    }}
                    onKeyDown={handleKeyDown}
                    placeholder={placeholder}
                    disabled={isLoading}
                    rows={3}
                    className={clsx(
                      'w-full rounded-xl border-2 p-4 pr-12 resize-none transition-all',
                      'focus:outline-none focus:ring-0',
                      'placeholder:text-gray-400',
                      error
                        ? 'border-red-300 focus:border-red-500'
                        : 'border-gray-200 focus:border-blue-500',
                      isLoading && 'opacity-50 cursor-not-allowed'
                    )}
                  />

                  {/* Character Counter */}
                  <div
                    className={clsx(
                      'absolute bottom-3 right-3 text-xs',
                      isNearLimit ? 'text-orange-500' : 'text-gray-400',
                      characterCount > maxLength && 'text-red-500'
                    )}
                  >
                    {characterCount}/{maxLength}
                  </div>
                </div>

                {/* Error Message */}
                {error && (
                  <motion.p
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-sm text-red-600"
                  >
                    {error}
                  </motion.p>
                )}

                {/* Examples */}
                {examples.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">
                      Beispiele zur Inspiration:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {examples.map((example, index) => (
                        <button
                          key={index}
                          onClick={() => handleExampleClick(example)}
                          className={clsx(
                            'px-3 py-1.5 text-sm rounded-full border transition-all',
                            'hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700',
                            'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                            'border-gray-200 text-gray-600 bg-gray-50'
                          )}
                        >
                          {example}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Footer */}
              <div className="flex items-center justify-end gap-3 p-4 border-t border-gray-100">
                <button
                  onClick={onClose}
                  disabled={isLoading}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  Abbrechen
                </button>
                <motion.button
                  onClick={handleSubmit}
                  disabled={!isValidLength || isLoading}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={clsx(
                    'flex items-center gap-2 px-5 py-2 rounded-xl font-medium transition-all',
                    isValidLength && !isLoading
                      ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-md'
                      : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  )}
                >
                  <Send className="w-4 h-4" />
                  Absenden
                </motion.button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

export default CustomInputModal;
