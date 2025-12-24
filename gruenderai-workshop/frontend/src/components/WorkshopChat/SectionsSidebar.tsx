/**
 * SectionsSidebar Component
 * Shows workshop sections with progress indicators
 */

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle2,
  Circle,
  Lock,
  PlayCircle,
  ChevronLeft,
  ChevronRight,
  Clock,
  FileText,
  Download,
  Eye,
  Sparkles,
} from 'lucide-react';
import { clsx } from 'clsx';
import type { SectionInfo, SectionPreviewDetail } from '@/services/workshopChatApi';
import { workshopChatApi } from '@/services/workshopChatApi';
import { TextPreview } from './TextPreview';

interface SectionsSidebarProps {
  sections: SectionInfo[];
  currentSectionId: string;
  progress: number;
  canExport: boolean;
  estimatedTime: string;
  isOpen: boolean;
  onToggle: () => void;
  onExport?: () => void;
  sessionId?: string;
  /** Progress within the current section (0-100) based on messages */
  currentSectionProgress?: number;
}

export function SectionsSidebar({
  sections,
  currentSectionId,
  progress,
  canExport,
  estimatedTime,
  isOpen,
  onToggle,
  onExport,
  sessionId,
  currentSectionProgress = 0,
}: SectionsSidebarProps) {
  // Preview state
  const [previewSection, setPreviewSection] = useState<SectionPreviewDetail | null>(null);
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  // Load section preview
  const handleSectionClick = useCallback(async (section: SectionInfo) => {
    if (!sessionId) return;
    if (section.status === 'locked') return;

    // Only load preview if section has been started
    if (section.status === 'completed' || section.status === 'in_progress') {
      setIsLoadingPreview(true);
      setPreviewError(null);
      setIsPreviewOpen(true);

      try {
        const preview = await workshopChatApi.getSectionPreview(sessionId, section.id);
        setPreviewSection(preview);
      } catch (err) {
        console.error('Failed to load preview:', err);
        setPreviewError('Vorschau konnte nicht geladen werden.');
        setPreviewSection({
          session_id: sessionId,
          section_id: section.id,
          section_titel: section.titel,
          section_nummer: section.nummer,
          status: section.status,
          generated_text: null,
          quality_score: section.quality_score,
          collected_data: null,
          completed_at: section.completed_at,
        });
      } finally {
        setIsLoadingPreview(false);
      }
    }
  }, [sessionId]);

  const closePreview = useCallback(() => {
    setIsPreviewOpen(false);
    setPreviewSection(null);
    setPreviewError(null);
  }, []);

  const getStatusIcon = (status: SectionInfo['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-emerald-500" />;
      case 'in_progress':
        return <PlayCircle className="w-5 h-5 text-blue-500 animate-pulse" />;
      case 'available':
        return <Circle className="w-5 h-5 text-gray-400" />;
      case 'locked':
      default:
        return <Lock className="w-5 h-5 text-gray-300" />;
    }
  };

  return (
    <>
      {/* Toggle Button (when collapsed) */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            onClick={onToggle}
            className="fixed left-0 top-1/2 -translate-y-1/2 z-20 bg-white shadow-lg rounded-r-lg p-2 border border-l-0 border-gray-200"
          >
            <ChevronRight className="w-5 h-5 text-gray-600" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <AnimatePresence>
        {isOpen && (
          <motion.aside
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="w-80 bg-white border-r border-gray-200 flex flex-col h-full overflow-hidden"
          >
            {/* Header */}
            <div className="p-4 border-b border-gray-100 flex items-center justify-between">
              <div>
                <h2 className="font-semibold text-gray-900">Workshop</h2>
                <p className="text-sm text-gray-500">7 Sektionen</p>
              </div>
              <button
                onClick={onToggle}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ChevronLeft className="w-5 h-5 text-gray-600" />
              </button>
            </div>

            {/* Compact Progress Overview */}
            <div className="px-4 py-3 bg-gradient-to-r from-blue-50 to-emerald-50 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="flex -space-x-1">
                    {sections.slice(0, 6).map((section, idx) => (
                      <div
                        key={section.id}
                        className={`w-5 h-5 rounded-full border-2 border-white flex items-center justify-center text-[10px] font-bold ${
                          section.status === 'completed'
                            ? 'bg-emerald-500 text-white'
                            : section.id === currentSectionId
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 text-gray-500'
                        }`}
                      >
                        {section.status === 'completed' ? '✓' : idx + 1}
                      </div>
                    ))}
                  </div>
                  <span className="text-sm font-medium text-gray-700">
                    {sections.filter(s => s.status === 'completed').length}/6 Module
                  </span>
                </div>
                {estimatedTime && (
                  <div className="flex items-center gap-1 text-xs text-gray-500">
                    <Clock className="w-3 h-3" />
                    <span>{estimatedTime}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Sections List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-2">
              {sections.map((section) => (
                <motion.div
                  key={section.id}
                  layout
                  className={clsx(
                    'rounded-xl p-3 transition-all duration-200',
                    section.id === currentSectionId
                      ? 'bg-blue-50 border-2 border-blue-200'
                      : section.status === 'completed'
                      ? 'bg-emerald-50 border border-emerald-100 cursor-pointer hover:border-emerald-200'
                      : section.status === 'locked'
                      ? 'bg-gray-50 border border-gray-100 opacity-60'
                      : 'bg-white border border-gray-100 hover:border-gray-200 cursor-pointer'
                  )}
                  onClick={() => handleSectionClick(section)}
                >
                  <div className="flex items-start gap-3">
                    {/* Status Icon */}
                    <div className="flex-shrink-0 mt-0.5">
                      {getStatusIcon(section.status)}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span
                            className={clsx(
                              'text-xs font-medium px-2 py-0.5 rounded-full',
                              section.status === 'completed'
                                ? 'bg-emerald-100 text-emerald-700'
                                : section.status === 'in_progress'
                                ? 'bg-blue-100 text-blue-700'
                                : 'bg-gray-100 text-gray-600'
                            )}
                          >
                            {section.nummer}
                          </span>
                          <span className="text-xs text-gray-400">
                            {section.geschaetzte_dauer}
                          </span>
                        </div>

                        {/* Preview Button for completed sections */}
                        {section.status === 'completed' && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleSectionClick(section);
                            }}
                            className="p-1 hover:bg-emerald-100 rounded transition-colors"
                            title="Vorschau anzeigen"
                          >
                            <Eye className="w-4 h-4 text-emerald-600" />
                          </button>
                        )}
                      </div>

                      <h3
                        className={clsx(
                          'font-medium mt-1 truncate',
                          section.status === 'locked'
                            ? 'text-gray-400'
                            : 'text-gray-900'
                        )}
                      >
                        {section.titel}
                      </h3>

                      <p
                        className={clsx(
                          'text-xs mt-0.5 truncate',
                          section.status === 'locked'
                            ? 'text-gray-300'
                            : 'text-gray-500'
                        )}
                      >
                        {section.untertitel}
                      </p>

                      {/* In-Progress Mini Progress Bar */}
                      {section.status === 'in_progress' && currentSectionProgress > 0 && (
                        <div className="mt-2">
                          <div className="flex items-center justify-between text-xs text-blue-600 mb-1">
                            <span>Fortschritt</span>
                            <span className="font-medium">{Math.round(currentSectionProgress)}%</span>
                          </div>
                          <div className="h-1.5 bg-blue-100 rounded-full overflow-hidden">
                            <motion.div
                              className="h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full"
                              initial={{ width: 0 }}
                              animate={{ width: `${currentSectionProgress}%` }}
                              transition={{ duration: 0.5, ease: 'easeOut' }}
                            />
                          </div>
                        </div>
                      )}

                      {/* Quality Score */}
                      {section.quality_score !== null && (
                        <div className="flex items-center gap-1 mt-2">
                          <Sparkles className="w-3 h-3 text-emerald-500" />
                          <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                            <div
                              className={clsx(
                                'h-full rounded-full',
                                section.quality_score >= 8
                                  ? 'bg-emerald-500'
                                  : section.quality_score >= 5
                                  ? 'bg-yellow-500'
                                  : 'bg-red-500'
                              )}
                              style={{
                                width: `${section.quality_score * 10}%`,
                              }}
                            />
                          </div>
                          <span className="text-xs text-gray-500">
                            {section.quality_score}/10
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Export Section - Only show after some progress */}
            {progress >= 30 && (
              <div className="p-4 border-t border-gray-100 bg-gray-50 space-y-2">
                {/* Full Export Button - only when ready */}
                {canExport ? (
                  <>
                    <button
                      onClick={onExport}
                      className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-medium transition-all bg-gradient-to-r from-blue-600 to-emerald-600 text-white hover:shadow-lg"
                    >
                      <Download className="w-5 h-5" />
                      <span>Businessplan exportieren</span>
                    </button>
                    <p className="text-xs text-center text-gray-500">
                      PDF, DOCX & Excel Finanzplan
                    </p>
                  </>
                ) : (
                  <>
                    {/* Preview Button - available early */}
                    <button
                      onClick={onExport}
                      className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-medium transition-all border-2 border-blue-200 text-blue-700 bg-blue-50 hover:bg-blue-100 hover:border-blue-300"
                    >
                      <Eye className="w-5 h-5" />
                      <span>Vorschau ansehen</span>
                    </button>
                    <p className="text-xs text-center text-gray-500">
                      Entwurf mit Wasserzeichen
                    </p>

                    {/* Progress to full export */}
                    <div className="mt-2 p-2 bg-gray-100 rounded-lg">
                      <div className="flex items-center justify-between text-xs mb-1">
                        <span className="text-gray-600">Bis zum Export</span>
                        <span className="font-medium text-blue-600">{85 - progress}% verbleibend</span>
                      </div>
                      <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-blue-400 to-emerald-400 rounded-full transition-all"
                          style={{ width: `${(progress / 85) * 100}%` }}
                        />
                      </div>
                    </div>
                  </>
                )}
              </div>
            )}
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Text Preview Panel */}
      {previewSection && (
        <TextPreview
          sectionId={previewSection.section_id}
          sectionTitle={previewSection.section_titel}
          sectionNummer={previewSection.section_nummer}
          generatedText={previewSection.generated_text}
          qualityScore={previewSection.quality_score}
          status={previewSection.status}
          isOpen={isPreviewOpen}
          onClose={closePreview}
          isLoading={isLoadingPreview}
          error={previewError}
        />
      )}
    </>
  );
}

export default SectionsSidebar;
