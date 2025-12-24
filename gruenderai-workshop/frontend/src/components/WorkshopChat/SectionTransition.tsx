/**
 * SectionTransition Component
 * Shows natural transition between workshop sections with summary & action buttons
 *
 * CRITICAL: NO HALLUCINATIONS
 * - Only show explicitly confirmed items (from collectedData)
 * - Differentiate: Green (complete), Yellow (partial), Gray (missing)
 * - Full text only shown when GZ score >= 70%
 */

import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle2,
  ArrowRight,
  FileText,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  Edit3,
  Plus,
  Sparkles,
  HelpCircle,
  MessageCircle,
  AlertTriangle,
  Circle,
  Pencil,
  PartyPopper,
} from 'lucide-react';
import { clsx } from 'clsx';
import { useState, useEffect } from 'react';
import type { SectionTransition as TransitionState } from '@/stores/workshopChatStore';

// =============================================================================
// TYPES
// =============================================================================

type ItemStatus = 'complete' | 'partial' | 'missing';

interface CollectedItem {
  label: string;
  value?: string;
  status: ItemStatus;
  /** Note explaining partial/missing status */
  note?: string;
  /** Field ID for editing */
  fieldId?: string;
}

interface SectionTransitionProps {
  transition: TransitionState;
  onContinue: () => void;
  onDismiss: () => void;
  onEdit?: () => void;
  onAddDetails?: () => void;
  /** Callback when user wants to edit a specific field */
  onEditField?: (fieldId: string, label: string) => void;
  /** Explicitly collected data - NO INFERENCE */
  collectedData?: CollectedItem[];
}

// =============================================================================
// CONFETTI COMPONENT
// =============================================================================

function ConfettiPiece({ delay, x }: { delay: number; x: number }) {
  const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ec4899', '#8b5cf6'];
  const color = colors[Math.floor(Math.random() * colors.length)];

  return (
    <motion.div
      initial={{ y: -20, x, opacity: 1, rotate: 0 }}
      animate={{
        y: 400,
        x: x + (Math.random() - 0.5) * 100,
        opacity: 0,
        rotate: Math.random() * 720 - 360
      }}
      transition={{
        duration: 2 + Math.random(),
        delay,
        ease: 'easeOut'
      }}
      className="absolute top-0 w-3 h-3 rounded-sm"
      style={{ backgroundColor: color, left: `${x}%` }}
    />
  );
}

function Confetti({ isActive }: { isActive: boolean }) {
  if (!isActive) return null;

  const pieces = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    delay: Math.random() * 0.5,
    x: Math.random() * 100,
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-50">
      {pieces.map((piece) => (
        <ConfettiPiece key={piece.id} delay={piece.delay} x={piece.x} />
      ))}
    </div>
  );
}

// =============================================================================
// SECTION-SPECIFIC EXPECTED FIELDS
// =============================================================================

const SECTION_EXPECTED_FIELDS: Record<string, { field: string; label: string }[]> = {
  'sektion_1_geschaeftsmodell': [
    { field: 'geschaeftsidee', label: 'Geschäftsidee' },
    { field: 'angebot_detail', label: 'Angebot (konkret)' },
    { field: 'zielgruppe_primaer', label: 'Zielgruppe' },
    { field: 'usp', label: 'Alleinstellungsmerkmal (USP)' },
    { field: 'preismodell', label: 'Preismodell' },
    { field: 'raeumlichkeiten', label: 'Räumlichkeiten/Standort' },
  ],
  'sektion_2_unternehmen': [
    { field: 'gruender_name', label: 'Name' },
    { field: 'fachliche_ausbildung', label: 'Fachliche Qualifikation' },
    { field: 'berufserfahrung', label: 'Berufserfahrung' },
    { field: 'kaufmaennische_kenntnisse', label: 'Kaufmännische Kenntnisse' },
    { field: 'rechtsform', label: 'Rechtsform' },
    { field: 'standort', label: 'Standort' },
  ],
  'sektion_3_markt': [
    { field: 'marktgroesse', label: 'Marktgröße' },
    { field: 'wettbewerber', label: 'Wettbewerber' },
    { field: 'differenzierung', label: 'Differenzierung' },
  ],
  'sektion_4_marketing': [
    { field: 'preise', label: 'Preisgestaltung' },
    { field: 'vertriebskanaele', label: 'Vertriebskanäle' },
    { field: 'erste_kunden', label: 'Kundengewinnung' },
  ],
  'sektion_5_finanzen': [
    { field: 'kapitalbedarf', label: 'Kapitalbedarf' },
    { field: 'umsatzprognose', label: 'Umsatzprognose' },
    { field: 'fixkosten', label: 'Fixkosten' },
    { field: 'break_even', label: 'Break-Even' },
  ],
  'sektion_6_strategie': [
    { field: 'staerken', label: 'Stärken' },
    { field: 'schwaechen', label: 'Schwächen' },
    { field: 'chancen', label: 'Chancen' },
    { field: 'risiken', label: 'Risiken' },
    { field: 'meilensteine', label: 'Meilensteine' },
  ],
};

// =============================================================================
// GZ SCORE EXPLANATIONS
// =============================================================================

const GZ_SCORE_EXPLANATIONS: Record<string, { threshold: number; explanation: string }[]> = {
  'sektion_1_geschaeftsmodell': [
    { threshold: 90, explanation: 'Geschäftsidee klar beschrieben, USP überzeugend, Zielgruppe definiert' },
    { threshold: 70, explanation: 'Grundlagen vorhanden. Tipp: USP konkretisieren, Zielgruppe präziser beschreiben' },
    { threshold: 50, explanation: 'Konzept noch vage. Fehlend: Klarer Kundennutzen, konkrete Zielgruppe' },
    { threshold: 0, explanation: 'Wichtige Punkte fehlen: Angebot, Zielgruppe, Alleinstellungsmerkmal' },
  ],
  'sektion_2_unternehmen': [
    { threshold: 90, explanation: 'Qualifikationen überzeugend, Rechtsform begründet, Standort analysiert' },
    { threshold: 70, explanation: 'Gute Basis. Tipp: Fachliche Qualifikationen detaillierter beschreiben' },
    { threshold: 50, explanation: 'Mehr Details zu Berufserfahrung und kaufmännischen Kenntnissen nötig' },
    { threshold: 0, explanation: 'Kritisch: Frage 8 & 9 (Qualifikationen) sind Hauptablehnungsgründe!' },
  ],
  'sektion_3_markt': [
    { threshold: 90, explanation: 'Marktgröße realistisch, Wettbewerber analysiert, Differenzierung klar' },
    { threshold: 70, explanation: 'Solide Analyse. Tipp: 2-3 konkrete Wettbewerber benennen' },
    { threshold: 50, explanation: 'Marktgröße fehlt oder zu vage. Wettbewerbsvorteile konkretisieren' },
    { threshold: 0, explanation: 'Marktanalyse unvollständig - dies prüft die Agentur besonders' },
  ],
  'sektion_4_marketing': [
    { threshold: 90, explanation: 'Preise begründet, Vertriebskanäle klar, Akquise-Plan konkret' },
    { threshold: 70, explanation: 'Guter Plan. Tipp: Erste 100 Kunden konkreter beschreiben' },
    { threshold: 50, explanation: 'Marketing-Strategie noch zu allgemein, Preiskalkulation fehlt' },
    { threshold: 0, explanation: 'Vertriebsplan fehlt - wie erreichst du Kunden?' },
  ],
  'sektion_5_finanzen': [
    { threshold: 90, explanation: 'Kapitalbedarf realistisch, Break-Even plausibel, 3-Jahres-Plan vollständig' },
    { threshold: 70, explanation: 'Zahlen vorhanden. Tipp: Worst-Case-Szenario ergänzen' },
    { threshold: 50, explanation: 'Finanzplan unvollständig - Fragen 13-15 sind kritisch!' },
    { threshold: 0, explanation: 'ACHTUNG: Finanzplan ist Hauptgrund für Ablehnungen!' },
  ],
  'sektion_6_strategie': [
    { threshold: 90, explanation: 'SWOT vollständig, Meilensteine realistisch, Risiken adressiert' },
    { threshold: 70, explanation: 'Gute Strategie. Tipp: Risiko-Gegenmaßnahmen konkretisieren' },
    { threshold: 50, explanation: 'SWOT-Analyse unvollständig, Meilensteine fehlen' },
    { threshold: 0, explanation: 'Strategischer Plan fehlt noch' },
  ],
};

function getGzExplanation(sectionId: string | null, score: number): string {
  if (!sectionId) return '';
  const explanations = GZ_SCORE_EXPLANATIONS[sectionId] || [];
  for (const item of explanations) {
    if (score >= item.threshold) {
      return item.explanation;
    }
  }
  return 'Vervollständige diese Sektion für bessere GZ-Konformität';
}

// =============================================================================
// STATUS ICON COMPONENT
// =============================================================================

function StatusIcon({ status }: { status: ItemStatus }) {
  switch (status) {
    case 'complete':
      return <Check className="w-4 h-4 text-emerald-500 flex-shrink-0" />;
    case 'partial':
      return <AlertTriangle className="w-4 h-4 text-amber-500 flex-shrink-0" />;
    case 'missing':
      return <Circle className="w-4 h-4 text-gray-300 flex-shrink-0" />;
  }
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function SectionTransition({
  transition,
  onContinue,
  onDismiss,
  onEdit,
  onAddDetails,
  onEditField,
  collectedData,
}: SectionTransitionProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [showGzTooltip, setShowGzTooltip] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);

  // Trigger confetti on mount
  useEffect(() => {
    if (transition.isActive) {
      setShowConfetti(true);
      const timer = setTimeout(() => setShowConfetti(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [transition.isActive]);

  if (!transition.isActive) return null;

  const handleCopy = async () => {
    if (transition.generatedText) {
      await navigator.clipboard.writeText(transition.generatedText);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const gzScore = transition.gzScore ?? 0;
  const gzExplanation = getGzExplanation(transition.completedSectionId, gzScore);

  // Get expected fields for this section
  const expectedFields = transition.completedSectionId
    ? SECTION_EXPECTED_FIELDS[transition.completedSectionId] || []
    : [];

  // Build display items from collectedData or show expected fields as missing
  const displayItems: CollectedItem[] = collectedData && collectedData.length > 0
    ? collectedData
    : expectedFields.map(field => ({
        label: field.label,
        status: 'missing' as ItemStatus,
        note: 'Noch nicht besprochen',
        fieldId: field.field,
      }));

  // Count statuses
  const completeCount = displayItems.filter(i => i.status === 'complete').length;
  const partialCount = displayItems.filter(i => i.status === 'partial').length;
  const missingCount = displayItems.filter(i => i.status === 'missing').length;

  const gzScoreColor =
    gzScore >= 80
      ? 'text-emerald-600'
      : gzScore >= 60
      ? 'text-amber-600'
      : 'text-red-600';

  const gzScoreBg =
    gzScore >= 80
      ? 'bg-emerald-50 border-emerald-200'
      : gzScore >= 60
      ? 'bg-amber-50 border-amber-200'
      : 'bg-red-50 border-red-200';

  const gzScoreRingColor =
    gzScore >= 80
      ? 'stroke-emerald-500'
      : gzScore >= 60
      ? 'stroke-amber-500'
      : 'stroke-red-500';

  // Only show full text if GZ score >= 70%
  const canShowFullText = gzScore >= 70 && transition.generatedText;

  // Extract module number from next section for button text
  const nextModuleMatch = transition.nextSectionTitle?.match(/Modul\s*(\d+)/i);
  const nextModuleNum = nextModuleMatch ? nextModuleMatch[1] : null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto"
    >
      {/* Confetti Animation */}
      <Confetti isActive={showConfetti} />

      <motion.div
        initial={{ scale: 0.9, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.9, opacity: 0, y: 20 }}
        className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col relative"
      >
        {/* Header with Success Animation */}
        <div className="p-6 bg-gradient-to-r from-emerald-500 to-teal-600 text-white relative overflow-hidden">
          <div className="absolute inset-0 opacity-10">
            <Sparkles className="absolute top-2 right-8 w-12 h-12" />
            <Sparkles className="absolute bottom-4 left-12 w-8 h-8" />
          </div>

          <div className="relative">
            <div className="flex items-center gap-3 mb-3">
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
                className="w-14 h-14 rounded-full bg-white/20 flex items-center justify-center"
              >
                <motion.div
                  animate={{ rotate: [0, 10, -10, 0] }}
                  transition={{ delay: 0.5, duration: 0.5 }}
                >
                  <PartyPopper className="w-8 h-8" />
                </motion.div>
              </motion.div>
              <div>
                <motion.h2
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 }}
                  className="text-2xl font-bold"
                >
                  Super, das klingt gut! 🎉
                </motion.h2>
                <p className="text-emerald-100 text-sm">
                  {transition.completedSectionTitle || 'Sektion'} abgeschlossen
                </p>
              </div>
            </div>

            <p className="text-emerald-50 text-sm leading-relaxed">
              Hier eine kurze Zusammenfassung – passt das so, oder möchtest du etwas ändern?
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">

          {/* GZ Score Card */}
          {transition.gzScore !== null && (
            <div className={clsx('rounded-xl p-4 border relative', gzScoreBg)}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {/* Circular Progress */}
                  <div className="relative w-14 h-14">
                    <svg className="w-14 h-14 transform -rotate-90">
                      <circle
                        cx="28"
                        cy="28"
                        r="24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="4"
                        className="text-gray-200"
                      />
                      <motion.circle
                        cx="28"
                        cy="28"
                        r="24"
                        fill="none"
                        strokeWidth="4"
                        strokeLinecap="round"
                        className={gzScoreRingColor}
                        initial={{ strokeDasharray: '0 150' }}
                        animate={{ strokeDasharray: `${gzScore * 1.5} 150` }}
                        transition={{ duration: 1, ease: 'easeOut' }}
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className={clsx('text-lg font-bold', gzScoreColor)}>
                        {gzScore}%
                      </span>
                    </div>
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-gray-800">
                        GZ-Konformität
                      </span>
                      <button
                        onMouseEnter={() => setShowGzTooltip(true)}
                        onMouseLeave={() => setShowGzTooltip(false)}
                        onClick={() => setShowGzTooltip(!showGzTooltip)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        <HelpCircle className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-xs text-gray-500">
                      Gründungszuschuss-Anforderungen
                    </p>
                  </div>
                </div>
              </div>

              {/* Explanation */}
              <div className="mt-3 pt-3 border-t border-gray-200/50">
                <p className="text-sm text-gray-700">
                  {gzExplanation}
                </p>
              </div>

              {/* Tooltip */}
              <AnimatePresence>
                {showGzTooltip && (
                  <motion.div
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 5 }}
                    className="absolute top-full left-0 right-0 mt-2 p-3 bg-gray-900 text-white text-xs rounded-lg shadow-lg z-10"
                  >
                    <p className="font-medium mb-1">Was bedeutet der GZ-Score?</p>
                    <p className="text-gray-300">
                      Der Score zeigt, wie gut deine Angaben die Anforderungen der
                      Agentur für Arbeit erfüllen. 80%+ bedeutet, dass die fachkundige
                      Stelle diesen Bereich positiv bewerten wird.
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          )}

          {/* Summary with 3 Clear Categories */}
          <div className="space-y-3">
            {/* Category 1: GREEN - Bereits besprochen (complete) */}
            {completeCount > 0 && (
              <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-200">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center">
                    <Check className="w-4 h-4 text-white" />
                  </div>
                  <span className="font-semibold text-emerald-800">
                    Bereits besprochen
                  </span>
                  <span className="text-xs text-emerald-600 bg-emerald-100 px-2 py-0.5 rounded-full">
                    {completeCount} von {displayItems.length}
                  </span>
                </div>
                <ul className="space-y-2">
                  {displayItems.filter(i => i.status === 'complete').map((item, idx) => (
                    <motion.li
                      key={idx}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.03 }}
                      className="flex items-start gap-2 text-sm group"
                    >
                      <Check className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-emerald-900">
                            {item.label}
                          </span>
                          {onEditField && item.fieldId && (
                            <button
                              onClick={() => onEditField(item.fieldId!, item.label)}
                              className="opacity-0 group-hover:opacity-100 text-xs text-emerald-600 hover:text-emerald-800 flex items-center gap-0.5 transition-opacity"
                            >
                              <Pencil className="w-3 h-3" />
                              <span>Ändern</span>
                            </button>
                          )}
                        </div>
                        {item.value && (
                          <span className="text-emerald-700 text-xs mt-0.5 block">
                            {item.value}
                          </span>
                        )}
                      </div>
                    </motion.li>
                  ))}
                </ul>
              </div>
            )}

            {/* Category 2: YELLOW - Wird vertieft (partial) */}
            {partialCount > 0 && (
              <div className="bg-amber-50 rounded-xl p-4 border border-amber-200">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-6 h-6 rounded-full bg-amber-500 flex items-center justify-center">
                    <AlertTriangle className="w-4 h-4 text-white" />
                  </div>
                  <span className="font-semibold text-amber-800">
                    Wird vertieft
                  </span>
                  <span className="text-xs text-amber-600 bg-amber-100 px-2 py-0.5 rounded-full">
                    {partialCount} Punkte
                  </span>
                </div>
                <p className="text-xs text-amber-700 mb-3">
                  Diese Themen vertiefen wir in den nächsten Modulen.
                </p>
                <ul className="space-y-2">
                  {displayItems.filter(i => i.status === 'partial').map((item, idx) => (
                    <motion.li
                      key={idx}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.03 }}
                      className="flex items-start gap-2 text-sm"
                    >
                      <AlertTriangle className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
                      <div className="flex-1 min-w-0">
                        <span className="font-medium text-amber-900">
                          {item.label}
                        </span>
                        {item.note && (
                          <p className="text-xs text-amber-600 mt-0.5">
                            {item.note}
                          </p>
                        )}
                      </div>
                    </motion.li>
                  ))}
                </ul>
              </div>
            )}

            {/* Category 3: GRAY - Noch offen (missing) */}
            {missingCount > 0 && (
              <div className="bg-gray-100 rounded-xl p-4 border border-gray-200">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-6 h-6 rounded-full bg-gray-400 flex items-center justify-center">
                    <Circle className="w-4 h-4 text-white" />
                  </div>
                  <span className="font-semibold text-gray-700">
                    Noch offen
                  </span>
                  <span className="text-xs text-gray-500 bg-gray-200 px-2 py-0.5 rounded-full">
                    {missingCount} Punkte
                  </span>
                </div>
                <p className="text-xs text-gray-500 mb-3">
                  Diese Punkte behandeln wir in späteren Modulen.
                </p>
                <ul className="space-y-2">
                  {displayItems.filter(i => i.status === 'missing').map((item, idx) => (
                    <motion.li
                      key={idx}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.03 }}
                      className="flex items-start gap-2 text-sm"
                    >
                      <Circle className="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5" />
                      <div className="flex-1 min-w-0">
                        <span className="text-gray-600">
                          {item.label}
                        </span>
                      </div>
                    </motion.li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Full Text - Only if GZ >= 70% */}
          {canShowFullText && (
            <div className="border border-gray-200 rounded-xl overflow-hidden">
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full px-4 py-3 bg-white flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-600">
                    Businessplan-Entwurf (Vorschau)
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCopy();
                    }}
                    className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
                    title="In Zwischenablage kopieren"
                  >
                    {isCopied ? (
                      <Check className="w-4 h-4 text-emerald-600" />
                    ) : (
                      <Copy className="w-4 h-4 text-gray-400" />
                    )}
                  </button>
                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-gray-400" />
                  )}
                </div>
              </button>

              <AnimatePresence>
                {isExpanded && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="border-t border-gray-100"
                  >
                    <div className="p-4 bg-gray-50 max-h-48 overflow-y-auto">
                      <p className="text-xs text-amber-600 mb-2 flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" />
                        Entwurf – basiert nur auf bestätigten Angaben
                      </p>
                      <div className="prose prose-sm max-w-none text-gray-600 whitespace-pre-wrap text-xs">
                        {transition.generatedText}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          )}

          {/* Message when full text is hidden */}
          {!canShowFullText && transition.generatedText && (
            <div className="p-3 bg-gray-100 rounded-lg text-center">
              <p className="text-xs text-gray-500">
                Der vollständige Businessplan-Text wird ab 70% GZ-Konformität angezeigt.
              </p>
            </div>
          )}
        </div>

        {/* Footer - Action Buttons */}
        <div className="p-5 bg-gray-50 border-t border-gray-200">
          {/* Primary CTA - BIG GREEN BUTTON */}
          <motion.button
            onClick={onContinue}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full py-4 px-6 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl font-bold text-lg hover:shadow-xl transition-all flex items-center justify-center gap-3 mb-4"
          >
            <CheckCircle2 className="w-6 h-6" />
            <span>
              {transition.nextSectionTitle
                ? `Ja, weiter zu ${nextModuleNum ? `Modul ${nextModuleNum}` : transition.nextSectionTitle}!`
                : 'Ja, passt – weiter!'
              }
            </span>
            <ArrowRight className="w-6 h-6" />
          </motion.button>

          {/* Secondary Actions */}
          <div className="flex gap-2">
            <button
              onClick={onEdit || onDismiss}
              className="flex-1 py-2.5 px-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-100 transition-colors flex items-center justify-center gap-2 text-sm"
            >
              <Edit3 className="w-4 h-4" />
              <span>Etwas ändern</span>
            </button>
            <button
              onClick={onAddDetails || onDismiss}
              className="flex-1 py-2.5 px-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-100 transition-colors flex items-center justify-center gap-2 text-sm"
            >
              <Plus className="w-4 h-4" />
              <span>Mehr Details</span>
            </button>
          </div>

          <button
            onClick={onDismiss}
            className="w-full mt-3 py-2 text-sm text-gray-500 hover:text-gray-700 flex items-center justify-center gap-1 transition-colors"
          >
            <MessageCircle className="w-4 h-4" />
            <span>Zurück zum Chat</span>
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default SectionTransition;
