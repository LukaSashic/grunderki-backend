import { useState, ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Scale, ExternalLink, Info, BookOpen } from 'lucide-react';
import type { LegalCitation } from '@/types/workshop.types';

interface LegalMarginaliaProps {
  citation: LegalCitation;
  variant?: 'inline' | 'margin' | 'tooltip';
  children?: ReactNode;
}

export const LegalMarginalia = ({
  citation,
  variant = 'margin',
  children
}: LegalMarginaliaProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (variant === 'inline') {
    return (
      <span className="inline-flex items-center gap-1">
        {children}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="inline-flex items-center gap-1 text-xs text-primary-600 hover:text-primary-700 underline decoration-dotted"
        >
          <Scale size={12} />
          {citation.reference}
        </button>
        <AnimatePresence>
          {isExpanded && (
            <motion.span
              initial={{ opacity: 0, y: -5 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -5 }}
              className="ml-2 text-xs text-warm-600 bg-warm-100 px-2 py-1 rounded"
            >
              {citation.text}
            </motion.span>
          )}
        </AnimatePresence>
      </span>
    );
  }

  if (variant === 'tooltip') {
    return (
      <span className="relative inline-block group">
        {children}
        <span className="ml-1 inline-flex items-center cursor-help">
          <Info size={14} className="text-primary-500" />
        </span>
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
          <div className="bg-warm-900 text-white text-xs rounded-lg p-3 shadow-lg">
            <div className="flex items-start gap-2 mb-2">
              <Scale size={14} className="flex-shrink-0 mt-0.5 text-accent-400" />
              <span className="font-semibold">{citation.reference}</span>
            </div>
            <p className="text-warm-200">{citation.text}</p>
            {citation.url && (
              <a
                href={citation.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 flex items-center gap-1 text-accent-400 hover:text-accent-300"
              >
                <ExternalLink size={12} />
                Quelle ansehen
              </a>
            )}
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full border-8 border-transparent border-t-warm-900" />
          </div>
        </div>
      </span>
    );
  }

  // Default margin variant
  return (
    <div className="legal-marginalia">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-start gap-2 text-left group"
      >
        <Scale size={16} className="flex-shrink-0 mt-0.5 text-primary-500 group-hover:text-primary-600" />
        <div>
          <span className="text-sm font-medium text-primary-600 group-hover:text-primary-700">
            {citation.reference}
          </span>
          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="overflow-hidden"
              >
                <p className="text-xs text-warm-600 mt-1">{citation.text}</p>
                {citation.url && (
                  <a
                    href={citation.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-1 flex items-center gap-1 text-xs text-primary-500 hover:text-primary-600"
                  >
                    <ExternalLink size={10} />
                    Quelle
                  </a>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </button>
    </div>
  );
};

interface LegalCitationsListProps {
  citations: LegalCitation[];
  title?: string;
}

export const LegalCitationsList = ({
  citations,
  title = 'Rechtliche Grundlagen'
}: LegalCitationsListProps) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (citations.length === 0) return null;

  return (
    <div className="bg-warm-50 rounded-xl p-4 border border-warm-200">
      <div className="flex items-center gap-2 mb-3">
        <BookOpen size={18} className="text-primary-600" />
        <h4 className="font-semibold text-warm-900">{title}</h4>
      </div>

      <div className="space-y-2">
        {citations.map(citation => (
          <div
            key={citation.id}
            className="bg-white rounded-lg p-3 border border-warm-100"
          >
            <button
              onClick={() => setExpandedId(expandedId === citation.id ? null : citation.id)}
              className="w-full flex items-start gap-2 text-left"
            >
              <Scale size={14} className="flex-shrink-0 mt-0.5 text-primary-500" />
              <div className="flex-1">
                <span className="text-sm font-medium text-primary-700">
                  {citation.reference}
                </span>
              </div>
              <motion.span
                animate={{ rotate: expandedId === citation.id ? 180 : 0 }}
                className="text-warm-400"
              >
                <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                  <path d="M6 8L2 4h8L6 8z" />
                </svg>
              </motion.span>
            </button>

            <AnimatePresence>
              {expandedId === citation.id && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="overflow-hidden"
                >
                  <p className="text-xs text-warm-600 mt-2 pl-6">{citation.text}</p>
                  {citation.url && (
                    <a
                      href={citation.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-2 flex items-center gap-1 text-xs text-primary-500 hover:text-primary-600 pl-6"
                    >
                      <ExternalLink size={10} />
                      Gesetzestext ansehen
                    </a>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LegalMarginalia;
