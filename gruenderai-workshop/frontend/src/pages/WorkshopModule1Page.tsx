/**
 * GründerAI Workshop - Module 1 Page
 * AI-Coached Workshop: Geschäftsidee & Gründerprofil
 *
 * This is NOT a static form with 3 fields.
 * This is an AI-guided coaching session with:
 * - 6-8 questions with conditional logic
 * - Personalized AI feedback after EACH answer
 * - Framework teaching (Jobs-to-be-Done, etc.)
 * - BA GZ 04 transparency
 * - Personality-aware coaching
 */

import { useState, useCallback, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowRight,
  ArrowLeft,
  Save,
  HelpCircle,
  ChevronDown,
  Sparkles,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';
import { Button, Card, Badge, ProgressRing } from '@/components/common';
import {
  BAFormContext,
  GZDoorsTracker,
  CoachingFeedback,
  FrameworkCard,
  CoachingSkeleton
} from '@/components/Workshop';
import { useWorkshopStore } from '@/stores/workshopStore';
import { useGZDoors } from '@/hooks/useGZDoors';
import { usePersonality } from '@/hooks/usePersonality';
import { coachingService } from '@/services/coachingService';
import { MODULE_1_QUESTIONS, getVisibleQuestions, getModule1Progress } from '@/data/module1Questions';
import type {
  Module1Question,
  Module1Answers,
  CoachingResponse,
  CoachingExchange,
  GZDoorStatus
} from '@/types/module1.types';

interface WorkshopModule1PageProps {
  onComplete: () => void;
  onBack?: () => void;
}

export const WorkshopModule1Page: React.FC<WorkshopModule1PageProps> = ({
  onComplete,
  onBack
}) => {
  // =========================================================================
  // STATE
  // =========================================================================

  // Question navigation
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Module1Answers>({});
  const [currentAnswer, setCurrentAnswer] = useState<string>('');

  // Coaching state
  const [coachingResponse, setCoachingResponse] = useState<CoachingResponse | null>(null);
  const [coachingHistory, setCoachingHistory] = useState<CoachingExchange[]>([]);
  const [isCoachingLoading, setIsCoachingLoading] = useState(false);
  const [iterationCount, setIterationCount] = useState(0);

  // UI state
  const [showFramework, setShowFramework] = useState(false);
  const [showBAContext, setShowBAContext] = useState(false);

  // Time tracking
  const [startTime] = useState(Date.now());
  const [questionStartTime, setQuestionStartTime] = useState(Date.now());

  // =========================================================================
  // HOOKS
  // =========================================================================

  const { sessionId, setAnswer: storeSetAnswer, gzReadinessScore, setGzReadinessScore } = useWorkshopStore();
  const { doors, updateDoorStatus, evaluateAllDoors } = useGZDoors(1);
  const { personalityProfile, getCoachingTone, needsExtraEncouragement } = usePersonality();

  // =========================================================================
  // COMPUTED VALUES
  // =========================================================================

  // Get visible questions based on conditional logic
  const visibleQuestions = useMemo(
    () => getVisibleQuestions(answers),
    [answers]
  );

  // Current question
  const currentQuestion = visibleQuestions[currentQuestionIndex];

  // Progress percentage
  const progressPercent = useMemo(
    () => getModule1Progress(answers),
    [answers]
  );

  // Time spent in minutes
  const timeSpentMinutes = Math.round((Date.now() - startTime) / 60000);

  // Answered questions count
  const answeredCount = visibleQuestions.filter(q => {
    const ans = answers[q.id as keyof Module1Answers];
    return ans !== undefined && ans !== '';
  }).length;

  // =========================================================================
  // HANDLERS
  // =========================================================================

  // Handle answer change for textarea
  const handleTextareaChange = useCallback((value: string) => {
    setCurrentAnswer(value);
  }, []);

  // Handle answer change for multiple choice
  const handleMultipleChoiceSelect = useCallback((value: string) => {
    setCurrentAnswer(value);
  }, []);

  // Submit answer and get coaching response
  const handleSubmitAnswer = async () => {
    if (!currentQuestion || !currentAnswer) return;

    setIsCoachingLoading(true);

    try {
      const response = await coachingService.getCoachingResponseWithRetry({
        sessionId,
        questionId: currentQuestion.id,
        userAnswer: currentAnswer,
        questionContext: currentQuestion,
        personalityProfile,
        previousAnswers: answers,
        iterationCount
      });

      setCoachingResponse(response);

      // Update GZ door status if applicable
      if (currentQuestion.gzDoorId && response.gzDoorUpdate) {
        updateDoorStatus(
          response.gzDoorUpdate.doorId,
          response.gzDoorUpdate.newStatus
        );
      } else if (currentQuestion.gzDoorId) {
        // Evaluate door based on response
        const newStatus: GZDoorStatus = response.shouldIterate ? 'checking' : 'passed';
        updateDoorStatus(currentQuestion.gzDoorId, newStatus);
      }

      // Add to coaching history
      const exchange: CoachingExchange = {
        questionId: currentQuestion.id,
        userAnswer: currentAnswer,
        aiResponse: response,
        iteration: iterationCount,
        timestamp: new Date()
      };
      setCoachingHistory(prev => [...prev, exchange]);

    } catch (error) {
      console.error('Coaching error:', error);
    } finally {
      setIsCoachingLoading(false);
    }
  };

  // Accept answer and move to next question
  const handleAcceptAnswer = () => {
    if (!currentQuestion) return;

    // Save answer
    const newAnswers = {
      ...answers,
      [currentQuestion.id]: currentAnswer
    } as Module1Answers;
    setAnswers(newAnswers);
    storeSetAnswer(currentQuestion.id, currentAnswer);

    // Re-evaluate GZ doors
    evaluateAllDoors(newAnswers, coachingHistory);

    // Update GZ readiness score
    const scoreImpact = calculateScoreImpact(newAnswers);
    setGzReadinessScore(Math.min(gzReadinessScore + scoreImpact, 100));

    // Reset coaching state
    setCoachingResponse(null);
    setCurrentAnswer('');
    setIterationCount(0);
    setQuestionStartTime(Date.now());

    // Move to next question or complete module
    if (currentQuestionIndex < visibleQuestions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      handleModuleComplete();
    }
  };

  // Iterate on current answer
  const handleIterate = () => {
    setIterationCount(prev => prev + 1);
    setCoachingResponse(null);
    // Keep the current answer for user to improve
  };

  // Go back to previous question
  const handleBack = () => {
    if (currentQuestionIndex > 0) {
      // Save current answer if any
      if (currentAnswer && currentQuestion) {
        setAnswers(prev => ({
          ...prev,
          [currentQuestion.id]: currentAnswer
        } as Module1Answers));
      }

      setCurrentQuestionIndex(prev => prev - 1);
      setCoachingResponse(null);
      setIterationCount(0);

      // Load previous answer
      const prevQuestion = visibleQuestions[currentQuestionIndex - 1];
      const prevAnswer = answers[prevQuestion.id as keyof Module1Answers];
      setCurrentAnswer(prevAnswer?.toString() || '');
    }
  };

  // Complete the module
  const handleModuleComplete = () => {
    // Final evaluation
    evaluateAllDoors(answers, coachingHistory);

    // Call onComplete callback
    onComplete();
  };

  // Calculate score impact from answers
  const calculateScoreImpact = (currentAnswers: Module1Answers): number => {
    let impact = 0;

    // Fachliche Qualifikation
    if (currentAnswers.q2_hintergrund) {
      const scores: Record<string, number> = { 'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1 };
      impact += scores[currentAnswers.q2_hintergrund] || 0;
    }

    // Kaufmännische Kenntnisse
    if (currentAnswers.q3_kaufmaennisch) {
      const scores: Record<string, number> = { 'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1 };
      impact += scores[currentAnswers.q3_kaufmaennisch] || 0;
    }

    // Bonus for detailed answers
    if (currentAnswers.q1_angebot && currentAnswers.q1_angebot.length > 200) {
      impact += 2;
    }

    return impact;
  };

  // Load previous answer when question changes
  useEffect(() => {
    if (currentQuestion) {
      const savedAnswer = answers[currentQuestion.id as keyof Module1Answers];
      setCurrentAnswer(savedAnswer?.toString() || '');
    }
  }, [currentQuestionIndex]);

  // Check if can proceed
  const canSubmit = currentAnswer && currentAnswer.toString().trim() !== '';

  // =========================================================================
  // RENDER
  // =========================================================================

  if (!currentQuestion) {
    return (
      <div className="min-h-screen bg-warm-50 flex items-center justify-center">
        <p className="text-warm-600">Laden...</p>
      </div>
    );
  }

  return (
    <div className="workshop-module1 min-h-screen bg-warm-50">
      {/* ===================================================================
          HEADER
      =================================================================== */}
      <header className="sticky top-0 z-50 bg-white border-b border-warm-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Title */}
            <div>
              <h1 className="font-display text-xl text-primary-900">
                Modul 1: Geschäftsidee & Gründerprofil
              </h1>
              <p className="text-sm text-warm-500">
                Frage {currentQuestionIndex + 1} von {visibleQuestions.length}
              </p>
            </div>

            {/* GZ Doors Tracker */}
            <GZDoorsTracker doors={doors} variant="header" />
          </div>

          {/* Progress Bar */}
          <div className="mt-3">
            <div className="h-1.5 bg-warm-200 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${((currentQuestionIndex + 1) / visibleQuestions.length) * 100}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>
        </div>
      </header>

      {/* ===================================================================
          MAIN CONTENT
      =================================================================== */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* ---------------------------------------------------------------
              LEFT COLUMN: Question & Coaching
          --------------------------------------------------------------- */}
          <div className="lg:col-span-2 space-y-6">
            {/* BA Form Context (Transparency) */}
            {currentQuestion.baFormContext && (
              <BAFormContext
                context={currentQuestion.baFormContext}
                gzDoorStatus={
                  currentQuestion.gzDoorId
                    ? doors.find(d => d.id === currentQuestion.gzDoorId)?.status || 'locked'
                    : 'locked'
                }
              />
            )}

            {/* Framework Teaching */}
            {currentQuestion.frameworkToTeach && showFramework && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <FrameworkCard frameworkId={currentQuestion.frameworkToTeach} />
              </motion.div>
            )}

            {/* Question Card */}
            <Card variant="default" padding="lg" className="border-2 border-warm-200">
              {/* Tags */}
              <div className="flex flex-wrap gap-2 mb-4">
                {currentQuestion.gzRelevant && (
                  <Badge variant="primary" size="sm">
                    GZ-relevant
                  </Badge>
                )}
                {currentQuestion.required && (
                  <Badge variant="warning" size="sm">
                    Pflichtfeld
                  </Badge>
                )}
                {iterationCount > 0 && (
                  <Badge variant="accent" size="sm">
                    Verbesserung #{iterationCount + 1}
                  </Badge>
                )}
                <Badge variant="default" size="sm">
                  {currentQuestion.phase === 'geschaeftsidee' ? 'Geschäftsidee' :
                   currentQuestion.phase === 'gruenderprofil' ? 'Gründerprofil' :
                   currentQuestion.phase === 'geschaeftsmodell' ? 'Geschäftsmodell' :
                   'Formales'}
                </Badge>
              </div>

              {/* Question */}
              <h2 className="text-xl font-display font-semibold text-primary-900 mb-2">
                {currentQuestion.question}
              </h2>

              {currentQuestion.subtext && (
                <p className="text-warm-600 mb-4">{currentQuestion.subtext}</p>
              )}

              {/* Personality-based hint */}
              {needsExtraEncouragement() && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
                  <p className="text-sm text-green-800">
                    <Sparkles className="w-4 h-4 inline mr-1" />
                    Du schaffst das! Nimm dir Zeit und antworte so gut du kannst.
                  </p>
                </div>
              )}

              {/* Answer Input */}
              {currentQuestion.type === 'textarea' ? (
                <div className="relative">
                  <textarea
                    value={currentAnswer}
                    onChange={(e) => handleTextareaChange(e.target.value)}
                    className="w-full h-40 p-4 border-2 border-warm-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none transition-all"
                    placeholder={currentQuestion.placeholder || 'Deine Antwort...'}
                    disabled={isCoachingLoading}
                  />
                  <div className="absolute bottom-3 right-3 text-xs text-warm-400">
                    {currentAnswer.length}/{currentQuestion.maxLength || 500}
                  </div>
                </div>
              ) : currentQuestion.type === 'multiple_choice' && currentQuestion.options ? (
                <div className="space-y-3">
                  {currentQuestion.options.map((option) => (
                    <button
                      key={option.value}
                      onClick={() => handleMultipleChoiceSelect(option.value)}
                      disabled={isCoachingLoading}
                      className={`w-full p-4 text-left rounded-xl border-2 transition-all ${
                        currentAnswer === option.value
                          ? 'border-primary-500 bg-primary-50 shadow-md'
                          : 'border-warm-200 hover:border-warm-300 bg-white'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        {option.icon && (
                          <span className="text-2xl flex-shrink-0">{option.icon}</span>
                        )}
                        <div className="flex-1">
                          <p className="font-medium text-warm-900">{option.label}</p>
                          {option.example && (
                            <p className="text-sm text-warm-500 mt-1">{option.example}</p>
                          )}
                          {/* Pros/Cons for Rechtsform */}
                          {option.pros && option.cons && (
                            <div className="mt-2 flex gap-4 text-xs">
                              <div>
                                <span className="text-green-600 font-medium">+</span>
                                {option.pros.slice(0, 2).map((pro, i) => (
                                  <span key={i} className="text-green-700 ml-1">{pro}</span>
                                ))}
                              </div>
                              <div>
                                <span className="text-amber-600 font-medium">-</span>
                                {option.cons.slice(0, 1).map((con, i) => (
                                  <span key={i} className="text-amber-700 ml-1">{con}</span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                        {currentAnswer === option.value && (
                          <CheckCircle className="w-5 h-5 text-primary-500 flex-shrink-0" />
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              ) : null}

              {/* Framework Help Toggle */}
              {currentQuestion.frameworkToTeach && (
                <button
                  onClick={() => setShowFramework(!showFramework)}
                  className="mt-4 text-sm text-primary-600 hover:text-primary-800 flex items-center gap-1"
                >
                  <HelpCircle className="w-4 h-4" />
                  {showFramework ? 'Framework ausblenden' : `Hilfe: Was ist "${currentQuestion.frameworkToTeach}"?`}
                </button>
              )}
            </Card>

            {/* Coaching Feedback */}
            <AnimatePresence mode="wait">
              {isCoachingLoading && <CoachingSkeleton key="skeleton" />}

              {coachingResponse && !isCoachingLoading && (
                <CoachingFeedback
                  key="feedback"
                  response={coachingResponse}
                  onAccept={handleAcceptAnswer}
                  onIterate={handleIterate}
                  iterationCount={iterationCount}
                />
              )}
            </AnimatePresence>

            {/* Navigation (before coaching) */}
            {!coachingResponse && !isCoachingLoading && (
              <div className="flex items-center justify-between pt-4">
                <Button
                  variant="ghost"
                  onClick={handleBack}
                  disabled={currentQuestionIndex === 0}
                  leftIcon={<ArrowLeft className="w-4 h-4" />}
                >
                  Zurück
                </Button>

                <div className="flex items-center gap-3">
                  <Button
                    variant="secondary"
                    leftIcon={<Save className="w-4 h-4" />}
                    onClick={() => {
                      if (currentQuestion && currentAnswer) {
                        setAnswers(prev => ({
                          ...prev,
                          [currentQuestion.id]: currentAnswer
                        } as Module1Answers));
                      }
                    }}
                  >
                    Speichern
                  </Button>

                  <Button
                    variant={currentQuestionIndex === visibleQuestions.length - 1 ? 'accent' : 'primary'}
                    onClick={handleSubmitAnswer}
                    disabled={!canSubmit}
                    isLoading={isCoachingLoading}
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    {isCoachingLoading ? 'Coach analysiert...' : 'Antwort prüfen'}
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* ---------------------------------------------------------------
              RIGHT COLUMN: Sidebar
          --------------------------------------------------------------- */}
          <aside className="space-y-6">
            {/* Progress Card */}
            <Card variant="default" padding="md">
              <h3 className="font-medium text-warm-900 mb-4">Dein Fortschritt</h3>

              <div className="flex justify-center mb-4">
                <ProgressRing
                  progress={progressPercent}
                  size="lg"
                  color={progressPercent >= 70 ? 'success' : 'primary'}
                />
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-warm-600">Fragen beantwortet:</span>
                  <span className="font-medium text-warm-900">
                    {answeredCount}/{visibleQuestions.length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-warm-600">GZ-Readiness:</span>
                  <span className="font-medium text-primary-600">
                    {gzReadinessScore}%
                  </span>
                </div>
              </div>
            </Card>

            {/* GZ Doors Sidebar */}
            <GZDoorsTracker doors={doors.filter(d => d.moduleId === 1)} variant="sidebar" />

            {/* Endowment Reminder */}
            <Card variant="accent" padding="md">
              <h3 className="font-medium text-accent-900 mb-3">
                Bereits investiert
              </h3>

              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-warm-600">
                    <Clock className="w-4 h-4" />
                    <span>Zeit:</span>
                  </div>
                  <span className="font-medium text-warm-900">{timeSpentMinutes} Min</span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-warm-600">
                    <CheckCircle className="w-4 h-4" />
                    <span>Antworten:</span>
                  </div>
                  <span className="font-medium text-warm-900">{answeredCount}</span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-warm-600">
                    <Sparkles className="w-4 h-4" />
                    <span>Coaching:</span>
                  </div>
                  <span className="font-medium text-warm-900">
                    {coachingHistory.length} Feedbacks
                  </span>
                </div>
              </div>
            </Card>

            {/* Agentur-Anforderungen Info */}
            <Card variant="default" padding="md" className="bg-warm-50">
              <div className="flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-warm-700 font-medium">
                    Modul 1 beantwortet diese Agentur-Fragen:
                  </p>
                  <div className="flex gap-2 mt-2">
                    {[7, 8, 9].map(q => (
                      <span
                        key={q}
                        className="px-2 py-1 bg-primary-100 text-primary-700 text-xs font-mono rounded"
                      >
                        Frage {q}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </Card>
          </aside>
        </div>
      </main>
    </div>
  );
};

export default WorkshopModule1Page;
