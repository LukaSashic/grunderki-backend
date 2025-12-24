/**
 * TextPreview Component
 * Shows a preview of generated business plan text for a section
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  FileText,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  Loader2,
  AlertCircle,
  Sparkles,
} from 'lucide-react';
import { clsx } from 'clsx';

export interface TextPreviewProps {
  sectionId: string;
  sectionTitle: string;
  sectionNummer: number;
  generatedText: string | null;
  qualityScore: number | null;
  status: string;
  isOpen: boolean;
  onClose: () => void;
  isLoading?: boolean;
  error?: string | null;
}

export function TextPreview({
  sectionId,
  sectionTitle,
  sectionNummer,
  generatedText,
  qualityScore,
  status,
  isOpen,
  onClose,
  isLoading = false,
  error = null,
}: TextPreviewProps) {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  // Reset copied state after 2 seconds
  useEffect(() => {
    if (copied) {
      const timer = setTimeout(() => setCopied(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [copied]);

  const handleCopy = async () => {
    if (!generatedText) return;

    try {
      await navigator.clipboard.writeText(generatedText);
      setCopied(true);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  // Format text with paragraphs
  const formatText = (text: string) => {
    return text.split('\n\n').map((paragraph, index) => (
      <p key={index} className="mb-3 last:mb-0">
        {paragraph}
      </p>
    ));
  };

  // Quality badge color
  const getQualityColor = (score: number | null) => {
    if (score === null) return 'bg-gray-100 text-gray-500';
    if (score >= 8) return 'bg-emerald-100 text-emerald-700';
    if (score >= 5) return 'bg-yellow-100 text-yellow-700';
    return 'bg-red-100 text-red-700';
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: '100%', opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: '100%', opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl border-l border-gray-200 z-40 flex flex-col"
        >
          {/* Header */}
          <div className="p-4 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-emerald-50">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="w-7 h-7 rounded-full bg-gradient-to-r from-blue-500 to-emerald-500 text-white flex items-center justify-center text-sm font-bold">
                  {sectionNummer}
                </span>
                <h3 className="font-semibold text-gray-900">{sectionTitle}</h3>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-white/50 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            {/* Status & Quality */}
            <div className="flex items-center gap-2 mt-2">
              <span
                className={clsx(
                  'text-xs font-medium px-2 py-0.5 rounded-full',
                  status === 'completed'
                    ? 'bg-emerald-100 text-emerald-700'
                    : status === 'in_progress'
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 text-gray-600'
                )}
              >
                {status === 'completed'
                  ? 'Abgeschlossen'
                  : status === 'in_progress'
                  ? 'In Bearbeitung'
                  : 'Ausstehend'}
              </span>

              {qualityScore !== null && (
                <span
                  className={clsx(
                    'text-xs font-medium px-2 py-0.5 rounded-full flex items-center gap-1',
                    getQualityColor(qualityScore)
                  )}
                >
                  <Sparkles className="w-3 h-3" />
                  Qualitaet: {qualityScore}/10
                </span>
              )}
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto">
            {isLoading ? (
              <div className="flex flex-col items-center justify-center h-full p-8 text-gray-500">
                <Loader2 className="w-8 h-8 animate-spin mb-3" />
                <span className="text-sm">Text wird geladen...</span>
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center h-full p-8 text-red-500">
                <AlertCircle className="w-8 h-8 mb-3" />
                <span className="text-sm text-center">{error}</span>
              </div>
            ) : generatedText ? (
              <div className="p-4">
                {/* Preview Card */}
                <div className="bg-gray-50 rounded-xl border border-gray-100 overflow-hidden">
                  {/* Card Header */}
                  <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full flex items-center justify-between p-3 bg-white border-b border-gray-100 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-blue-500" />
                      <span className="text-sm font-medium text-gray-700">
                        Generierter Text
                      </span>
                    </div>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-gray-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-gray-400" />
                    )}
                  </button>

                  {/* Card Content */}
                  <AnimatePresence>
                    {isExpanded && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="overflow-hidden"
                      >
                        <div className="p-4 text-sm text-gray-700 leading-relaxed max-h-[400px] overflow-y-auto">
                          {formatText(generatedText)}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

                {/* Copy Button */}
                <button
                  onClick={handleCopy}
                  className={clsx(
                    'w-full mt-4 flex items-center justify-center gap-2 py-3 rounded-xl font-medium transition-all',
                    copied
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  )}
                >
                  {copied ? (
                    <>
                      <Check className="w-4 h-4" />
                      <span>Kopiert!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      <span>Text kopieren</span>
                    </>
                  )}
                </button>

                {/* Info Text */}
                <p className="text-xs text-gray-400 text-center mt-3">
                  Dieser Text wird in Ihren finalen Businessplan übernommen und kann im
                  Word-Dokument weiter bearbeitet werden.
                </p>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full p-8 text-gray-400">
                <FileText className="w-12 h-12 mb-3 opacity-50" />
                <span className="text-sm text-center">
                  {status === 'in_progress'
                    ? 'Text wird nach Abschluss der Sektion generiert.'
                    : 'Noch kein Text generiert.'}
                </span>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-gray-100 bg-gray-50">
            <div className="text-xs text-gray-500 text-center">
              <span className="font-medium">Tipp:</span> Der finale Businessplan
              kombiniert alle Sektionen zu einem vollstaendigen Dokument.
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default TextPreview;
