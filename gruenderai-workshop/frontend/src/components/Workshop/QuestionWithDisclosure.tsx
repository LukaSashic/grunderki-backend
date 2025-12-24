import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HelpCircle, ChevronDown, Lightbulb, BookOpen, AlertCircle, CheckCircle } from 'lucide-react';
import { Input, TextArea, Button, Card, Badge } from '@/components/common';
import { LegalMarginalia } from '@/components/common';
import type { DisclosureLevel, QuestionWithDisclosure as QuestionType, LegalCitation } from '@/types/workshop.types';

interface QuestionWithDisclosureProps {
  question: QuestionType;
  value: string | string[] | number;
  onChange: (value: string | string[] | number) => void;
  disclosureLevel: DisclosureLevel;
  onDisclosureLevelChange?: (level: DisclosureLevel) => void;
  showHints: boolean;
  error?: string;
  isValidating?: boolean;
}

export const QuestionWithDisclosure = ({
  question,
  value,
  onChange,
  disclosureLevel,
  onDisclosureLevelChange,
  showHints,
  error,
  isValidating
}: QuestionWithDisclosureProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [currentLevel, setCurrentLevel] = useState<DisclosureLevel>(disclosureLevel);

  const handleLevelChange = useCallback((level: DisclosureLevel) => {
    setCurrentLevel(level);
    onDisclosureLevelChange?.(level);
  }, [onDisclosureLevelChange]);

  const getLevelContent = () => {
    switch (currentLevel) {
      case 'essential':
        return question.levels.essential;
      case 'helpful':
        return { ...question.levels.essential, ...question.levels.helpful };
      case 'complete':
        return { ...question.levels.essential, ...question.levels.helpful, ...question.levels.complete };
    }
  };

  const content = getLevelContent();

  return (
    <Card variant="default" padding="lg" className="relative">
      {/* Question header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            {question.gzRelevance && (
              <Badge variant="accent" size="xs">
                GZ-relevant
              </Badge>
            )}
            {question.required && (
              <Badge variant="warning" size="xs">
                Pflichtfeld
              </Badge>
            )}
          </div>

          <h3 className="text-lg font-semibold text-warm-900">
            {question.text}
          </h3>

          {content.description && (
            <p className="mt-2 text-warm-600">
              {content.description}
            </p>
          )}
        </div>

        {/* Disclosure level toggle */}
        <div className="flex-shrink-0">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 text-warm-400 hover:text-warm-600 hover:bg-warm-100 rounded-lg transition-colors"
            aria-label="Mehr Informationen"
          >
            <HelpCircle size={20} />
          </button>
        </div>
      </div>

      {/* Disclosure level selector */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden mb-4"
          >
            <div className="bg-warm-50 rounded-xl p-4 border border-warm-200">
              <p className="text-sm font-medium text-warm-700 mb-3">
                Wie viel Hilfe möchtest du?
              </p>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => handleLevelChange('essential')}
                  className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
                    currentLevel === 'essential'
                      ? 'bg-primary-500 text-white'
                      : 'bg-white border border-warm-200 text-warm-700 hover:bg-warm-100'
                  }`}
                >
                  Nur das Wichtigste
                </button>
                <button
                  onClick={() => handleLevelChange('helpful')}
                  className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
                    currentLevel === 'helpful'
                      ? 'bg-primary-500 text-white'
                      : 'bg-white border border-warm-200 text-warm-700 hover:bg-warm-100'
                  }`}
                >
                  Mit Tipps
                </button>
                <button
                  onClick={() => handleLevelChange('complete')}
                  className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
                    currentLevel === 'complete'
                      ? 'bg-primary-500 text-white'
                      : 'bg-white border border-warm-200 text-warm-700 hover:bg-warm-100'
                  }`}
                >
                  Ausfuehrliche Anleitung
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Examples (if available and level allows) */}
      {content.examples && content.examples.length > 0 && showHints && (
        <div className="mb-4 p-4 bg-blue-50 rounded-xl border border-blue-100">
          <div className="flex items-center gap-2 text-blue-700 mb-2">
            <Lightbulb size={16} />
            <span className="text-sm font-medium">Beispiele</span>
          </div>
          <ul className="space-y-1">
            {content.examples.map((example, index) => (
              <li key={index} className="text-sm text-blue-800 flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                {example}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Tips (if available and level is helpful or complete) */}
      {content.tips && content.tips.length > 0 && (currentLevel === 'helpful' || currentLevel === 'complete') && (
        <div className="mb-4 p-4 bg-amber-50 rounded-xl border border-amber-100">
          <div className="flex items-center gap-2 text-amber-700 mb-2">
            <BookOpen size={16} />
            <span className="text-sm font-medium">Tipps</span>
          </div>
          <ul className="space-y-1">
            {content.tips.map((tip, index) => (
              <li key={index} className="text-sm text-amber-800 flex items-start gap-2">
                <span className="text-amber-400 mt-1">•</span>
                {tip}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Input field */}
      <div className="relative">
        {question.type === 'text' && (
          <Input
            value={value as string}
            onChange={(e) => onChange(e.target.value)}
            placeholder={question.placeholder}
            error={error}
            disabled={isValidating}
          />
        )}

        {question.type === 'textarea' && (
          <TextArea
            value={value as string}
            onChange={(e) => onChange(e.target.value)}
            placeholder={question.placeholder}
            rows={4}
            maxLength={question.maxLength}
            showCount={!!question.maxLength}
            error={error}
            disabled={isValidating}
          />
        )}

        {question.type === 'select' && question.options && (
          <div className="space-y-2">
            {question.options.map((option) => (
              <button
                key={option.value}
                onClick={() => onChange(option.value)}
                className={`w-full p-3 text-left rounded-xl border-2 transition-all ${
                  value === option.value
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-warm-200 hover:border-warm-300 bg-white'
                }`}
              >
                <span className="font-medium text-warm-800">{option.label}</span>
                {option.description && (
                  <p className="text-sm text-warm-500 mt-0.5">{option.description}</p>
                )}
              </button>
            ))}
          </div>
        )}

        {question.type === 'number' && (
          <Input
            type="number"
            value={value as number}
            onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
            placeholder={question.placeholder}
            error={error}
            disabled={isValidating}
          />
        )}
      </div>

      {/* Validation status */}
      {isValidating && (
        <div className="mt-3 flex items-center gap-2 text-warm-500">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2" fill="none" opacity="0.3" />
              <path d="M8 2a6 6 0 0 1 6 6" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" />
            </svg>
          </motion.div>
          <span className="text-sm">Wird geprueft...</span>
        </div>
      )}

      {/* Legal citations (if any) */}
      {question.legalCitations && question.legalCitations.length > 0 && (
        <div className="mt-4 pt-4 border-t border-warm-100">
          <div className="space-y-2">
            {question.legalCitations.map((citation) => (
              <LegalMarginalia
                key={citation.id}
                citation={citation}
                variant="inline"
              />
            ))}
          </div>
        </div>
      )}
    </Card>
  );
};

export default QuestionWithDisclosure;
