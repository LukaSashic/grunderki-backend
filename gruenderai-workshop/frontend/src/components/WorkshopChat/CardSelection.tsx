/**
 * CardSelection Component
 * Renders clickable cards for bounded question selection
 * Supports both single-select (immediate submit) and multi-select (with Weiter button)
 */

import { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, Edit3, ChevronRight, Sparkles, Square, CheckSquare, ArrowRight } from 'lucide-react';
import { clsx } from 'clsx';

// Success messages for feedback
const SUCCESS_MESSAGES = [
  'Gute Wahl! 👍',
  'Super! Weiter geht\'s! 🚀',
  'Perfekt! ✨',
  'Toll gewählt! 💪',
  'Ausgezeichnet! 🎯',
  'Das klingt gut! 👏',
];

export interface CardOption {
  id: string;
  label: string;
  description?: string;
  icon?: string;
  example?: string;
}

export interface CardSelectionProps {
  /** Question text displayed above cards */
  question: string;
  /** Available card options */
  options: CardOption[];
  /** Callback when a card is selected (single-select mode) */
  onSelect: (option: CardOption) => void;
  /** Callback when multiple cards are selected (multi-select mode) */
  onMultiSelect?: (options: CardOption[]) => void;
  /** Callback when "Sonstiges" (Other) is clicked */
  onCustomInput?: () => void;
  /** Whether multiple selections are allowed */
  multiSelect?: boolean;
  /** Currently selected option IDs (for controlled multiSelect) */
  selectedIds?: string[];
  /** Whether the component is disabled */
  disabled?: boolean;
  /** Optional hint text below the question */
  hint?: string;
  /** Show the "Sonstiges" (Other) option */
  showOtherOption?: boolean;
  /** Label for the other option */
  otherLabel?: string;
}

export function CardSelection({
  question,
  options,
  onSelect,
  onMultiSelect,
  onCustomInput,
  multiSelect = false,
  selectedIds: controlledSelectedIds = [],
  disabled = false,
  hint,
  showOtherOption = true,
  otherLabel = 'Sonstiges',
}: CardSelectionProps) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [successFeedback, setSuccessFeedback] = useState<string | null>(null);
  const [clickedId, setClickedId] = useState<string | null>(null);

  // Local state for multi-select mode
  const [localSelectedIds, setLocalSelectedIds] = useState<string[]>([]);

  // Use controlled or local state based on mode
  const selectedIds = multiSelect ? localSelectedIds : controlledSelectedIds;

  // Reset local selections when options change
  useEffect(() => {
    setSuccessFeedback(null);
    setClickedId(null);
    setLocalSelectedIds([]);
  }, [options]);

  const handleCardClick = useCallback(
    (option: CardOption) => {
      if (disabled) return;

      if (multiSelect) {
        // Toggle selection in multi-select mode
        setLocalSelectedIds(prev => {
          if (prev.includes(option.id)) {
            return prev.filter(id => id !== option.id);
          } else {
            return [...prev, option.id];
          }
        });
      } else {
        // Immediate submit in single-select mode
        setClickedId(option.id);
        const randomMessage = SUCCESS_MESSAGES[Math.floor(Math.random() * SUCCESS_MESSAGES.length)];
        setSuccessFeedback(randomMessage);

        setTimeout(() => {
          onSelect(option);
        }, 400);
      }
    },
    [disabled, multiSelect, onSelect]
  );

  const handleMultiSelectSubmit = useCallback(() => {
    if (disabled || localSelectedIds.length === 0) return;

    // Show success feedback
    const randomMessage = SUCCESS_MESSAGES[Math.floor(Math.random() * SUCCESS_MESSAGES.length)];
    setSuccessFeedback(randomMessage);

    // Get selected options
    const selectedOptions = options.filter(opt => localSelectedIds.includes(opt.id));

    setTimeout(() => {
      if (onMultiSelect) {
        onMultiSelect(selectedOptions);
      } else {
        // Fallback: Send as comma-separated labels via onSelect
        const combinedOption: CardOption = {
          id: localSelectedIds.join(','),
          label: selectedOptions.map(o => o.label).join(', '),
        };
        onSelect(combinedOption);
      }
    }, 400);
  }, [disabled, localSelectedIds, options, onMultiSelect, onSelect]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent, option: CardOption) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        handleCardClick(option);
      }
    },
    [handleCardClick]
  );

  const isSelected = (id: string) => selectedIds.includes(id);

  // Card animation variants
  const cardVariants = {
    hidden: { opacity: 0, y: 20, scale: 0.95 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        delay: i * 0.08,
        duration: 0.3,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    }),
    hover: {
      scale: 1.02,
      y: -4,
      transition: { duration: 0.2 },
    },
    tap: {
      scale: 0.98,
      transition: { duration: 0.1 },
    },
  };

  return (
    <div className="w-full space-y-4 relative">
      {/* Success Feedback Overlay */}
      <AnimatePresence>
        {successFeedback && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -20 }}
            className="absolute inset-0 z-20 flex items-center justify-center bg-white/90 backdrop-blur-sm rounded-xl"
          >
            <div className="text-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1, rotate: [0, 10, -10, 0] }}
                transition={{ duration: 0.4 }}
                className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-emerald-400 to-teal-500 mb-3"
              >
                <Sparkles className="w-8 h-8 text-white" />
              </motion.div>
              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-xl font-bold text-emerald-700"
              >
                {successFeedback}
              </motion.p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Question */}
      <div className="space-y-1">
        <p className="text-gray-800 font-medium text-lg">{question}</p>
        {hint && (
          <p className="text-sm text-gray-500 italic">{hint}</p>
        )}
      </div>

      {/* Multi-select instruction banner */}
      {multiSelect && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
          <div className="flex items-center gap-2 text-blue-800">
            <CheckSquare className="w-5 h-5 text-blue-600" />
            <span className="font-medium text-sm">
              Wähle eine oder mehrere Optionen aus
            </span>
          </div>
          <p className="text-xs text-blue-600 mt-1 ml-7">
            Klicke auf "Weiter", wenn du fertig bist
          </p>
          {localSelectedIds.length > 0 && (
            <p className="text-xs text-blue-700 mt-2 ml-7 font-medium">
              ✓ {localSelectedIds.length} ausgewählt
            </p>
          )}
        </div>
      )}

      {/* Cards Grid - Responsive with equal sizing */}
      <div className={clsx(
        'grid gap-3',
        // Smart grid: 1 col mobile, 2 cols tablet, 3 cols if many options
        options.length <= 2 ? 'grid-cols-1 sm:grid-cols-2' :
        options.length <= 4 ? 'grid-cols-2' :
        'grid-cols-2 lg:grid-cols-3'
      )}>
        <AnimatePresence mode="popLayout">
          {options.map((option, index) => {
            const selected = isSelected(option.id);
            const hovered = hoveredId === option.id;
            const clicked = clickedId === option.id;

            return (
              <motion.div
                key={option.id}
                custom={index}
                variants={cardVariants}
                initial="hidden"
                animate={clicked ? { scale: [1, 1.05, 1], transition: { duration: 0.3 } } : "visible"}
                whileHover={!disabled && !clicked ? 'hover' : undefined}
                whileTap={!disabled && !clicked ? 'tap' : undefined}
                onMouseEnter={() => setHoveredId(option.id)}
                onMouseLeave={() => setHoveredId(null)}
                onClick={() => !clicked && handleCardClick(option)}
                onKeyDown={(e) => handleKeyDown(e, option)}
                tabIndex={disabled || clicked ? -1 : 0}
                role={multiSelect ? "checkbox" : "button"}
                aria-checked={multiSelect ? selected : undefined}
                aria-pressed={!multiSelect ? selected : undefined}
                aria-disabled={disabled}
                className={clsx(
                  'relative rounded-xl border-2 p-4 cursor-pointer transition-all duration-200',
                  'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  'min-h-[80px] flex flex-col justify-center',
                  disabled && 'opacity-50 cursor-not-allowed',
                  clicked
                    ? 'border-emerald-500 bg-emerald-50 shadow-lg ring-2 ring-emerald-300'
                    : selected
                    ? 'border-blue-500 bg-blue-50 shadow-md ring-1 ring-blue-300'
                    : 'border-gray-200 bg-white hover:border-blue-300 hover:bg-gray-50',
                  hovered && !selected && !disabled && !clicked && 'shadow-lg'
                )}
              >
                {/* Checkbox indicator for multi-select */}
                {multiSelect && (
                  <div className="absolute top-3 left-3">
                    {selected ? (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-6 h-6 rounded bg-blue-500 flex items-center justify-center"
                      >
                        <Check className="w-4 h-4 text-white" />
                      </motion.div>
                    ) : (
                      <div className="w-6 h-6 rounded border-2 border-gray-300 bg-white" />
                    )}
                  </div>
                )}

                {/* Selection Indicator for single-select */}
                {!multiSelect && selected && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute top-2 right-2"
                  >
                    <div className="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center">
                      <Check className="w-4 h-4 text-white" />
                    </div>
                  </motion.div>
                )}

                {/* Card Content */}
                <div className={clsx(
                  'space-y-1',
                  multiSelect ? 'pl-8 pr-2' : 'pr-6'
                )}>
                  {/* Icon (optional emoji) */}
                  {option.icon && (
                    <span className="text-2xl">{option.icon}</span>
                  )}

                  {/* Label */}
                  <div className="font-semibold text-gray-900 text-sm sm:text-base">
                    {option.label}
                  </div>

                  {/* Description */}
                  {option.description && (
                    <p className="text-xs sm:text-sm text-gray-600 line-clamp-2">
                      {option.description}
                    </p>
                  )}

                  {/* Example */}
                  {option.example && (
                    <p className="text-xs text-gray-400 italic hidden sm:block">
                      z.B. {option.example}
                    </p>
                  )}
                </div>

                {/* Hover Arrow Indicator (single-select only) */}
                {!multiSelect && (
                  <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{
                      opacity: hovered && !selected ? 1 : 0,
                      x: hovered && !selected ? 0 : -10
                    }}
                    className="absolute right-3 top-1/2 -translate-y-1/2"
                  >
                    <ChevronRight className="w-5 h-5 text-blue-400" />
                  </motion.div>
                )}
              </motion.div>
            );
          })}

          {/* "Sonstiges" (Other) Option - MORE PROMINENT */}
          {showOtherOption && onCustomInput && (
            <motion.div
              custom={options.length}
              variants={cardVariants}
              initial="hidden"
              animate="visible"
              whileHover={!disabled ? 'hover' : undefined}
              whileTap={!disabled ? 'tap' : undefined}
              onClick={() => !disabled && onCustomInput()}
              onKeyDown={(e) => {
                if ((e.key === 'Enter' || e.key === ' ') && !disabled) {
                  e.preventDefault();
                  onCustomInput();
                }
              }}
              tabIndex={disabled ? -1 : 0}
              role="button"
              aria-disabled={disabled}
              className={clsx(
                'relative rounded-xl border-2 p-4 cursor-pointer transition-all duration-200',
                'focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2',
                'min-h-[90px] flex flex-col justify-center',
                disabled
                  ? 'opacity-50 cursor-not-allowed'
                  : 'border-purple-300 bg-gradient-to-br from-purple-50 to-indigo-50 hover:border-purple-500 hover:from-purple-100 hover:to-indigo-100 hover:shadow-lg ring-1 ring-purple-100'
              )}
            >
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-indigo-500 flex items-center justify-center flex-shrink-0 shadow-sm">
                    <Edit3 className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <div className="font-bold text-purple-900 text-base">
                      {otherLabel}
                    </div>
                    <p className="text-xs text-purple-600">
                      Eigene Antwort eingeben
                    </p>
                  </div>
                </div>
                <p className="text-xs text-purple-500 bg-purple-100/50 rounded-lg px-2 py-1 text-center">
                  Keine passende Option? Hier klicken!
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Multi-select "Weiter" button */}
      {multiSelect && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="pt-2"
        >
          <button
            onClick={handleMultiSelectSubmit}
            disabled={disabled || localSelectedIds.length === 0}
            className={clsx(
              'w-full flex items-center justify-center gap-2 py-3 px-6 rounded-xl font-semibold text-base transition-all duration-200',
              localSelectedIds.length > 0
                ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:from-blue-600 hover:to-indigo-700 shadow-md hover:shadow-lg'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            )}
          >
            <span>
              {localSelectedIds.length === 0
                ? 'Bitte mindestens eine Option wählen'
                : `Weiter mit ${localSelectedIds.length} ${localSelectedIds.length === 1 ? 'Auswahl' : 'Auswahlen'}`
              }
            </span>
            {localSelectedIds.length > 0 && <ArrowRight className="w-5 h-5" />}
          </button>

          {/* Tip about combinations */}
          {localSelectedIds.length >= 1 && localSelectedIds.length < options.length && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-xs text-center text-blue-600 mt-2 bg-blue-50 rounded-lg py-2 px-3"
            >
              💡 <strong>Tipp:</strong> Kombinationen erhöhen deine Flexibilität und zeigen der Agentur breite Marktabdeckung
            </motion.p>
          )}
        </motion.div>
      )}
    </div>
  );
}

export default CardSelection;
