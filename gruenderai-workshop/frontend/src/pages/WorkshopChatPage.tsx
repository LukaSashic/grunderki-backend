/**
 * WorkshopChatPage
 * Main page for the interactive chat-based business plan workshop
 */

import { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
  Loader2,
  AlertCircle,
  Download,
  FileText,
  FileSpreadsheet,
  Archive,
  X,
  Clock,
  CheckCircle2,
  Shield,
  Sparkles,
  HelpCircle,
  ChevronDown,
  Rocket,
} from 'lucide-react';
import { clsx } from 'clsx';

import { ChatWindow, ChatInput, SectionsSidebar, SectionTransition, CompletionButton } from '@/components/WorkshopChat';
import { Sidebar } from '@/components/Workshop';
import { SidebarProvider } from '@/contexts/SidebarContext';
import { useWorkshopChatStore } from '@/stores/workshopChatStore';
import { workshopChatApi } from '@/services/workshopChatApi';

export function WorkshopChatPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isStarting, setIsStarting] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [showFaq, setShowFaq] = useState(true);
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  // Store
  const {
    sessionId,
    messages,
    isLoading,
    isTyping,
    progress,
    currentSection,
    sections,
    canExport,
    estimatedRemainingTime,
    isSidebarOpen,
    userName,
    sectionTransition,
    sectionStartMessageIndex,
    completionStatus,
    setSession,
    addUserMessage,
    handleStartResponse,
    handleMessageResponse,
    updateStatus,
    toggleSidebar,
    setTyping,
    dismissTransition,
    continueToNextSection,
    reset,
  } = useWorkshopChatStore();

  // Initialize workshop on mount
  useEffect(() => {
    const initWorkshop = async () => {
      // If we have a session, load its status
      if (sessionId) {
        try {
          const status = await workshopChatApi.getStatus(sessionId);
          updateStatus(status);

          // Load messages
          const messagesData = await workshopChatApi.getMessages(sessionId);
          if (messagesData.messages.length > 0) {
            // Messages already in store from persist
          }
        } catch (err) {
          console.error('Failed to load session:', err);
          // Session might be invalid, start fresh
          reset();
        }
      }
    };

    initWorkshop();
  }, [sessionId, updateStatus, reset]);

  // Start new workshop
  const handleStartWorkshop = useCallback(async () => {
    setIsStarting(true);
    setError(null);

    try {
      const response = await workshopChatApi.start({
        user_name: userName || undefined,
      });

      handleStartResponse(response);
      setSession(response.session_id);

      // Load sections
      const status = await workshopChatApi.getStatus(response.session_id);
      updateStatus(status);
    } catch (err) {
      console.error('Failed to start workshop:', err);
      setError('Workshop konnte nicht gestartet werden. Bitte versuch es erneut.');
    } finally {
      setIsStarting(false);
    }
  }, [userName, handleStartResponse, setSession, updateStatus]);

  // Send message
  const handleSendMessage = useCallback(
    async (content: string) => {
      if (!sessionId) return;

      // Special handling for sidebar/preview requests
      const lowerContent = content.toLowerCase();
      if (lowerContent.includes('sidebar') || lowerContent.includes('vorschau')) {
        // Open sidebar if not already open
        if (!isSidebarOpen) {
          toggleSidebar();
        }
        // Add user message but don't wait for AI response
        addUserMessage(content);
        // Show hint to click on section for preview
        setTimeout(() => {
          handleMessageResponse({
            session_id: sessionId,
            assistant_message: '👆 Die Sidebar ist jetzt geöffnet! Klicke auf "Geschäftsmodell" links, um die Vorschau deines bisherigen Textes zu sehen.',
            progress,
            current_section: currentSection,
            current_step: 'preview_hint',
            validation_status: 'incomplete',
          });
        }, 300);
        return;
      }

      addUserMessage(content);
      setTyping(true);
      setError(null);

      try {
        const response = await workshopChatApi.sendMessage({
          session_id: sessionId,
          message: content,
        });

        handleMessageResponse(response);

        // Refresh status for sections
        const status = await workshopChatApi.getStatus(sessionId);
        updateStatus(status);
      } catch (err) {
        console.error('Failed to send message:', err);
        setError('Nachricht konnte nicht gesendet werden. Bitte versuch es erneut.');
        setTyping(false);
      }
    },
    [sessionId, addUserMessage, setTyping, handleMessageResponse, updateStatus, isSidebarOpen, toggleSidebar, progress, currentSection]
  );

  // Export handler
  const handleExport = useCallback(
    async (format: 'pdf' | 'docx' | 'xlsx' | 'all') => {
      if (!sessionId) return;

      setIsExporting(true);

      try {
        const urls = workshopChatApi.getDownloadUrls(sessionId);

        if (format === 'all') {
          window.open(urls.all, '_blank');
        } else if (format === 'xlsx') {
          window.open(urls.xlsx, '_blank');
        } else {
          window.open(urls[format], '_blank');
        }
      } catch (err) {
        console.error('Export failed:', err);
        setError('Export fehlgeschlagen. Bitte versuch es erneut.');
      } finally {
        setIsExporting(false);
        setShowExportModal(false);
      }
    },
    [sessionId]
  );

  // Handle user-initiated section completion
  const handleCompleteSection = useCallback(async () => {
    if (!sessionId) return;

    try {
      const response = await workshopChatApi.completeSection(sessionId);

      if (response.success) {
        // Refresh status to get updated sections
        const status = await workshopChatApi.getStatus(sessionId);
        updateStatus(status);

        // Add system message about completion
        handleMessageResponse({
          session_id: sessionId,
          assistant_message: response.message,
          progress: status.progress,
          current_section: status.current_section,
          current_step: status.current_step,
          validation_status: 'complete',
          section_completed: true,
          completed_section_id: response.section_id,
          next_section_id: response.next_section_id,
          generated_text: response.generated_text,
          collected_data: response.collected_data,
        });
      } else {
        setError(response.message);
      }
    } catch (err) {
      console.error('Failed to complete section:', err);
      setError('Modul konnte nicht abgeschlossen werden. Bitte versuch es erneut.');
    }
  }, [sessionId, updateStatus, handleMessageResponse]);

  // Get current section title
  const currentSectionTitle = sections.find((s) => s.id === currentSection)?.titel;

  // Calculate micro-progress within current section
  // Uses sectionStartMessageIndex to reset progress per module
  // Start at 0% - user earns every percent themselves (clearer & more motivating)
  const messagesInCurrentSection = messages.length - sectionStartMessageIndex;
  const currentSectionProgress = Math.min(
    Math.floor(messagesInCurrentSection / 2) * 15, // Each Q&A pair adds 15%
    95 // Cap at 95% until section completes
  );

  // No session yet - show start screen
  if (!sessionId) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50">
        {/* Header */}
        <header className="p-4 flex justify-between items-center max-w-5xl mx-auto">
          <span className="font-bold text-xl bg-gradient-to-r from-blue-600 to-emerald-600 bg-clip-text text-transparent">
            GründerAI
          </span>
          <button
            onClick={() => setShowFaq(!showFaq)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 text-sm"
          >
            <HelpCircle className="w-4 h-4" />
            <span className="hidden sm:inline">Häufige Fragen</span>
          </button>
        </header>

        {/* Main Content */}
        <main className="max-w-5xl mx-auto px-4 py-8 md:py-16">
          <div className="grid md:grid-cols-2 gap-12 items-center">

            {/* Left: Value Proposition */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              {/* Badge */}
              <div className="inline-flex items-center gap-2 bg-emerald-100 text-emerald-800 px-3 py-1.5 rounded-full text-sm font-medium">
                <Shield className="w-4 h-4" />
                Erfüllt die Anforderungen der Agentur für Arbeit
              </div>

              {/* Headline */}
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 leading-tight">
                Dein Businessplan in{' '}
                <span className="bg-gradient-to-r from-blue-600 to-emerald-600 bg-clip-text text-transparent">
                  2–3 Stunden
                </span>
              </h1>

              {/* Subheadline */}
              <p className="text-lg text-gray-600">
                KI-geführter Workshop für deinen Gründungszuschuss-Antrag.
              </p>

              {/* Key Benefits */}
              <ul className="space-y-3">
                {[
                  { icon: Sparkles, text: 'Geführte Fragen statt leere Seite' },
                  { icon: Clock, text: '6 Module, Schritt für Schritt' },
                  { icon: FileText, text: 'PDF, Word & Excel Export' },
                ].map((item, idx) => (
                  <li key={idx} className="flex items-center gap-3 text-gray-700">
                    <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                      <item.icon className="w-4 h-4 text-blue-600" />
                    </div>
                    <span>{item.text}</span>
                  </li>
                ))}
              </ul>

              {/* CTA Button */}
              <div className="pt-4">
                {error && (
                  <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                    <span className="text-sm">{error}</span>
                  </div>
                )}

                <button
                  onClick={handleStartWorkshop}
                  disabled={isStarting}
                  className={clsx(
                    'w-full sm:w-auto px-8 py-4 rounded-xl font-semibold text-white transition-all flex items-center justify-center gap-2',
                    isStarting
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-600 to-emerald-600 hover:shadow-lg hover:scale-[1.02]'
                  )}
                >
                  {isStarting ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Wird gestartet...
                    </>
                  ) : (
                    <>
                      <Rocket className="w-5 h-5" />
                      Jetzt starten – kostenlos
                    </>
                  )}
                </button>

                <p className="text-xs text-gray-400 mt-3 flex items-center gap-1">
                  <Shield className="w-3 h-3" />
                  Fortschritt wird automatisch gespeichert
                </p>
              </div>
            </motion.div>

            {/* Right: Module Preview */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6"
            >
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">
                Dein Weg zum Businessplan
              </h3>

              {/* Module Steps */}
              <div className="space-y-3">
                {[
                  { num: 1, title: 'Geschäftsmodell', time: '25 Min', desc: 'Zeige, warum Kunden bei DIR kaufen' },
                  { num: 2, title: 'Dein Unternehmen', time: '20 Min', desc: 'Überzeuge mit deinen Qualifikationen' },
                  { num: 3, title: 'Markt & Wettbewerb', time: '25 Min', desc: 'Finde die Lücke im Markt' },
                  { num: 4, title: 'Marketing', time: '20 Min', desc: 'Dein Plan für die ersten 100 Kunden' },
                  { num: 5, title: 'Finanzplanung', time: '35 Min', desc: 'Beweise: Dein Plan rechnet sich' },
                  { num: 6, title: 'Strategie', time: '20 Min', desc: 'Dein Fahrplan zum Erfolg' },
                ].map((module, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm font-bold text-gray-600">
                      {module.num}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-gray-900">{module.title}</span>
                        <span className="text-xs text-gray-400">{module.time}</span>
                      </div>
                      <p className="text-sm text-gray-500 truncate">{module.desc}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Total Time */}
              <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
                <span className="text-sm text-gray-600">Gesamtdauer</span>
                <div className="flex items-center gap-2 text-emerald-600 font-semibold">
                  <Clock className="w-4 h-4" />
                  ca. 2,5 Stunden
                </div>
              </div>
            </motion.div>
          </div>

          {/* FAQ Section - Accordion Style */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-12 max-w-2xl mx-auto"
          >
            <button
              onClick={() => setShowFaq(!showFaq)}
              className="w-full flex items-center justify-between p-4 bg-white rounded-xl border border-gray-200 hover:border-blue-300 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center">
                  <HelpCircle className="w-4 h-4 text-blue-600" />
                </div>
                <span className="font-semibold text-gray-900">Häufige Fragen</span>
              </div>
              <ChevronDown className={clsx(
                'w-5 h-5 text-gray-400 transition-transform',
                showFaq && 'rotate-180'
              )} />
            </button>

            <AnimatePresence>
              {showFaq && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mt-3 space-y-2 overflow-hidden"
                >
                  {[
                    {
                      q: 'Was ist der Gründungszuschuss?',
                      a: 'Der Gründungszuschuss ist eine Förderung der Agentur für Arbeit für ALG-I-Empfänger, die sich selbstständig machen wollen. Er beträgt 6 Monate ALG I + 300€/Monat.',
                    },
                    {
                      q: 'Brauche ich Vorkenntnisse?',
                      a: 'Nein! Der Workshop führt dich Schritt für Schritt durch alle Themen. Du beantwortest einfache Fragen und die KI erstellt daraus deinen Businessplan.',
                    },
                    {
                      q: 'Was passiert mit meinen Daten?',
                      a: 'Deine Daten werden sicher gespeichert und nur für die Erstellung deines Businessplans verwendet. Du kannst jederzeit pausieren und später weitermachen.',
                    },
                    {
                      q: 'Kann ich den Plan später bearbeiten?',
                      a: 'Ja! Du erhältst deinen Businessplan als Word-Dokument, das du frei anpassen kannst. Der Excel-Finanzplan enthält Formeln zur einfachen Anpassung.',
                    },
                  ].map((faq, idx) => (
                    <div key={idx} className="bg-white rounded-lg border border-gray-100 overflow-hidden">
                      <button
                        onClick={() => setExpandedFaq(expandedFaq === idx ? null : idx)}
                        className="w-full px-4 py-3 flex items-center justify-between text-left hover:bg-gray-50 transition-colors"
                      >
                        <span className="font-medium text-gray-900 text-sm">{faq.q}</span>
                        <ChevronDown className={clsx(
                          'w-4 h-4 text-gray-400 transition-transform flex-shrink-0 ml-2',
                          expandedFaq === idx && 'rotate-180'
                        )} />
                      </button>
                      <AnimatePresence>
                        {expandedFaq === idx && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="px-4 pb-3"
                          >
                            <p className="text-sm text-gray-600">{faq.a}</p>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </main>
      </div>
    );
  }

  return (
    <SidebarProvider sessionId={sessionId}>
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="text-gray-600 hover:text-gray-900 transition-colors"
          >
            <span className="font-semibold text-lg bg-gradient-to-r from-blue-600 to-emerald-600 bg-clip-text text-transparent">
              GründerAI
            </span>
          </button>
          <span className="text-gray-300">|</span>
          <span className="text-sm text-gray-600">Workshop</span>
        </div>

        <div className="flex items-center gap-4">
          {/* Step-based Progress Indicator */}
          <div className="flex items-center gap-3">
            {/* Module Steps */}
            <div className="flex items-center gap-1.5">
              {[1, 2, 3, 4, 5, 6].map((step) => {
                const sectionId = `sektion_${step}_`;
                const sectionStatus = sections.find(s => s.id.startsWith(sectionId))?.status;
                const isCompleted = sectionStatus === 'completed';
                const isCurrent = sections.find(s => s.id.startsWith(sectionId))?.id === currentSection;

                return (
                  <div
                    key={step}
                    className={clsx(
                      'w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium transition-all',
                      isCompleted
                        ? 'bg-emerald-500 text-white'
                        : isCurrent
                        ? 'bg-blue-500 text-white ring-2 ring-blue-200'
                        : 'bg-gray-200 text-gray-500'
                    )}
                    title={sections.find(s => s.id.startsWith(sectionId))?.titel || `Modul ${step}`}
                  >
                    {isCompleted ? '✓' : step}
                  </div>
                );
              })}
            </div>

            {/* Current Module Label */}
            <div className="hidden sm:block text-sm">
              <span className="text-gray-500">Modul </span>
              <span className="font-semibold text-gray-900">
                {sections.findIndex(s => s.id === currentSection) + 1 || 1}
              </span>
              <span className="text-gray-500"> von 6</span>
            </div>
          </div>

          {/* Export Button */}
          {canExport && (
            <button
              onClick={() => setShowExportModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-emerald-600 text-white rounded-lg font-medium hover:shadow-lg transition-all"
            >
              <Download className="w-4 h-4" />
              <span>Exportieren</span>
            </button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <SectionsSidebar
          sections={sections}
          currentSectionId={currentSection}
          progress={progress}
          canExport={canExport}
          estimatedTime={estimatedRemainingTime}
          isOpen={isSidebarOpen}
          onToggle={toggleSidebar}
          onExport={() => setShowExportModal(true)}
          sessionId={sessionId}
          currentSectionProgress={currentSectionProgress}
        />

        {/* Chat Area */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* Error Banner */}
          {error && (
            <div className="bg-red-50 border-b border-red-200 px-4 py-2 flex items-center justify-between">
              <div className="flex items-center gap-2 text-red-700">
                <AlertCircle className="w-4 h-4" />
                <span className="text-sm">{error}</span>
              </div>
              <button
                onClick={() => setError(null)}
                className="text-red-500 hover:text-red-700"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Chat Window */}
          <ChatWindow
            messages={messages}
            isTyping={isTyping}
            currentSection={currentSection}
            onCardSelect={handleSendMessage}
            disabled={isLoading || isTyping}
          />

          {/* Completion Button - shows when user can finish module early */}
          <CompletionButton
            completionStatus={completionStatus}
            onComplete={handleCompleteSection}
            isLoading={isLoading || isTyping}
            currentSectionTitle={currentSectionTitle}
          />

          {/* Chat Input */}
          <ChatInput
            onSend={handleSendMessage}
            disabled={!sessionId}
            isLoading={isLoading || isTyping}
            placeholder="Schreib hier deine Antwort..."
          />
        </main>

        {/* Intelligent Sidebar (Right) - Checklist, Tips, Progress */}
        <Sidebar />
      </div>

      {/* Export Modal */}
      {showExportModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-2xl shadow-xl max-w-md w-full p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">
                Businessplan exportieren
              </h2>
              <button
                onClick={() => setShowExportModal(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            <div className="space-y-3">
              <button
                onClick={() => handleExport('pdf')}
                disabled={isExporting}
                className="w-full flex items-center gap-3 p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all"
              >
                <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-red-600" />
                </div>
                <div className="text-left">
                  <div className="font-medium text-gray-900">PDF Dokument</div>
                  <div className="text-sm text-gray-500">
                    Druckfertig für die fachkundige Stelle
                  </div>
                </div>
              </button>

              <button
                onClick={() => handleExport('docx')}
                disabled={isExporting}
                className="w-full flex items-center gap-3 p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all"
              >
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-blue-600" />
                </div>
                <div className="text-left">
                  <div className="font-medium text-gray-900">Word Dokument</div>
                  <div className="text-sm text-gray-500">
                    Bearbeitbar für weitere Anpassungen
                  </div>
                </div>
              </button>

              <button
                onClick={() => handleExport('xlsx')}
                disabled={isExporting}
                className="w-full flex items-center gap-3 p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all"
              >
                <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                  <FileSpreadsheet className="w-5 h-5 text-emerald-600" />
                </div>
                <div className="text-left">
                  <div className="font-medium text-gray-900">Excel Finanzplan</div>
                  <div className="text-sm text-gray-500">
                    Mit Formeln für 36 Monate
                  </div>
                </div>
              </button>

              <div className="pt-2 border-t border-gray-100">
                <button
                  onClick={() => handleExport('all')}
                  disabled={isExporting}
                  className="w-full flex items-center justify-center gap-2 p-4 bg-gradient-to-r from-blue-600 to-emerald-600 text-white rounded-xl font-medium hover:shadow-lg transition-all"
                >
                  {isExporting ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Archive className="w-5 h-5" />
                  )}
                  <span>Alle Dokumente als ZIP</span>
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}

      {/* Section Transition Modal */}
      <SectionTransition
        transition={sectionTransition}
        collectedData={sectionTransition.collectedData}
        onContinue={async () => {
          continueToNextSection();
          // Refresh status after transition
          if (sessionId) {
            try {
              const status = await workshopChatApi.getStatus(sessionId);
              updateStatus(status);
            } catch (err) {
              console.error('Failed to refresh status:', err);
            }
          }
        }}
        onDismiss={dismissTransition}
        onEdit={() => {
          // Dismiss transition and allow user to edit in chat
          dismissTransition();
          // Focus on chat input (user can type to make changes)
        }}
        onAddDetails={() => {
          // Dismiss transition and allow user to add more details
          dismissTransition();
          // User can continue adding details in the chat
        }}
      />
    </div>
    </SidebarProvider>
  );
}

export default WorkshopChatPage;
