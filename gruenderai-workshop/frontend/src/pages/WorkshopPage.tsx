import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, ArrowLeft, Save, Info } from 'lucide-react';
import { WorkshopLayout, ContentContainer, PageHeader, TwoColumnLayout } from '@/components/layout';
import { QuestionWithDisclosure, ModuleProgress, RecapCard, ImmediateFeedback, StoryTransition, ModuleSummary } from '@/components/workshop';
import { GapWarningPanel, EndowmentReminder } from '@/components/conversion';
import { Button, Card, Badge } from '@/components/common';
import { useWorkshopStore } from '@/stores/workshopStore';
import { useScaffolding } from '@/hooks/useScaffolding';
import { useSpacedRepetition } from '@/hooks/useSpacedRepetition';
import { useAdaptiveDifficulty } from '@/hooks/useAdaptiveDifficulty';
import { workshopApi } from '@/services/api';
import type { ModuleNumber, Question, DisclosureLevel, FeedbackItem, Gap } from '@/types/workshop.types';

interface WorkshopPageProps {
  onComplete: () => void;
}

// Sample questions for demonstration
const SAMPLE_QUESTIONS: Record<ModuleNumber, Question[]> = {
  1: [
    {
      id: 'q1_idea',
      text: 'Beschreibe deine Geschäftsidee in 2-3 Sätzen',
      type: 'textarea',
      placeholder: 'Was bietest du an und warum ist es einzigartig?',
      required: true,
      gzRelevance: true
    },
    {
      id: 'q1_qualification',
      text: 'Welche fachlichen Qualifikationen bringst du mit?',
      type: 'textarea',
      placeholder: 'Ausbildung, Berufserfahrung, Zertifikate...',
      required: true,
      gzRelevance: true
    },
    {
      id: 'q1_motivation',
      text: 'Warum möchtest du dich selbstständig machen?',
      type: 'textarea',
      placeholder: 'Was treibt dich an?',
      required: true
    }
  ],
  2: [
    {
      id: 'q2_target',
      text: 'Wer ist dein idealer Kunde?',
      type: 'textarea',
      placeholder: 'Beschreibe deinen typischen Kunden...',
      required: true,
      gzRelevance: true
    }
  ],
  3: [
    {
      id: 'q3_market',
      text: 'Wie groß ist dein Zielmarkt?',
      type: 'textarea',
      placeholder: 'Beschreibe die Marktgröße...',
      required: true
    }
  ],
  4: [
    {
      id: 'q4_marketing',
      text: 'Wie gewinnst du neue Kunden?',
      type: 'textarea',
      placeholder: 'Deine Marketing-Strategie...',
      required: true
    }
  ],
  5: [
    {
      id: 'q5_revenue',
      text: 'Mit welchen Einnahmen rechnest du im ersten Jahr?',
      type: 'number',
      placeholder: 'Geschätzte Einnahmen in Euro',
      required: true,
      gzRelevance: true
    }
  ],
  6: [
    {
      id: 'q6_risks',
      text: 'Welche Risiken siehst du für dein Geschäft?',
      type: 'textarea',
      placeholder: 'Hauptrisiken und wie du damit umgehst...',
      required: true
    }
  ]
};

const MODULE_TITLES: Record<ModuleNumber, string> = {
  1: 'Geschäftsidee & Gründerprofil',
  2: 'Zielgruppe & Personas',
  3: 'Markt & Wettbewerb',
  4: 'Marketing & Vertrieb',
  5: 'Finanzplanung',
  6: 'Strategie & Abschluss'
};

export const WorkshopPage = ({ onComplete }: WorkshopPageProps) => {
  const {
    sessionId,
    currentModule,
    moduleProgress,
    gzReadinessScore,
    answers,
    setAnswer,
    updateProgress,
    nextModule
  } = useWorkshopStore();

  const { config: scaffolding, getGuidanceMessage, getProgressMessage } = useScaffolding(currentModule);
  const { conceptsNeedingRecap, getRecapMessage } = useSpacedRepetition(currentModule, answers);
  const { settings: adaptiveSettings, recordResponse } = useAdaptiveDifficulty(currentModule);

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [disclosureLevel, setDisclosureLevel] = useState<DisclosureLevel>('essential');
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [feedback, setFeedback] = useState<FeedbackItem[]>([]);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [showModuleSummary, setShowModuleSummary] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const questions = SAMPLE_QUESTIONS[currentModule] || [];
  const currentQuestion = questions[currentQuestionIndex];
  const currentAnswer = currentQuestion ? answers[currentQuestion.id] : '';

  // Calculate progress
  const answeredCount = questions.filter(q => answers[q.id] && answers[q.id].toString().trim() !== '').length;
  const progress = (answeredCount / questions.length) * 100;

  useEffect(() => {
    updateProgress(currentModule, progress);
  }, [progress, currentModule, updateProgress]);

  const handleAnswerChange = useCallback((value: string | string[] | number) => {
    if (currentQuestion) {
      setAnswer(currentQuestion.id, value);
    }
  }, [currentQuestion, setAnswer]);

  const handleNext = async () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);

      // Record response pattern
      recordResponse({
        avgResponseTime: 20000,
        correctnessRate: 0.8,
        helpRequestCount: 0,
        skipCount: 0,
        editCount: 0
      });
    } else {
      // Module complete
      setShowModuleSummary(true);
    }
  };

  const handleBack = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleModuleComplete = async () => {
    if (currentModule < 6) {
      setIsTransitioning(true);
    } else {
      onComplete();
    }
  };

  const handleTransitionContinue = () => {
    setIsTransitioning(false);
    setShowModuleSummary(false);
    setCurrentQuestionIndex(0);
    nextModule();
  };

  const canProceed = currentAnswer && currentAnswer.toString().trim() !== '';

  // Show story transition
  if (isTransitioning) {
    return (
      <StoryTransition
        fromModule={currentModule}
        toModule={(currentModule + 1) as ModuleNumber}
        previousSummary={`Du hast ${MODULE_TITLES[currentModule]} erfolgreich abgeschlossen.`}
        nextPreview={`Als nächstes: ${MODULE_TITLES[(currentModule + 1) as ModuleNumber]}`}
        score={gzReadinessScore}
        onContinue={handleTransitionContinue}
      />
    );
  }

  // Show module summary
  if (showModuleSummary) {
    return (
      <WorkshopLayout>
        <ContentContainer maxWidth="lg" padding="lg">
          <ModuleSummary
            moduleNumber={currentModule}
            moduleTitle={MODULE_TITLES[currentModule]}
            score={Math.min(gzReadinessScore + 10, 100)}
            feedbackItems={[
              { id: '1', type: 'success', title: 'Geschäftsidee klar definiert', message: 'Deine Idee ist gut strukturiert.' },
              { id: '2', type: 'info', title: 'Qualifikationen dokumentiert', message: 'Deine Erfahrungen sind überzeugend.' }
            ]}
            gaps={gaps}
            generatedChapters={[
              { id: '2.1', number: '2.1', title: 'Geschäftsidee', status: 'completed', progress: 100 }
            ]}
            timeSpent={25}
            onViewChapters={() => {}}
            onContinue={handleModuleComplete}
            isLastModule={currentModule === 6}
          />
        </ContentContainer>
      </WorkshopLayout>
    );
  }

  return (
    <WorkshopLayout>
      <ContentContainer maxWidth="xl" padding="lg">
        {/* Page header */}
        <PageHeader
          title={MODULE_TITLES[currentModule]}
          subtitle={getProgressMessage()}
          badge={<Badge variant="primary">Modul {currentModule}</Badge>}
        />

        <TwoColumnLayout
          leftWidth="2/3"
          leftColumn={
            <div className="space-y-6">
              {/* Guidance message */}
              {scaffolding.guidanceLevel !== 'none' && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <Card variant="accent" padding="md">
                    <div className="flex items-center gap-3">
                      <Info size={20} className="text-primary-500 flex-shrink-0" />
                      <p className="text-warm-700">{getGuidanceMessage()}</p>
                    </div>
                  </Card>
                </motion.div>
              )}

              {/* Recap cards for spaced repetition */}
              {conceptsNeedingRecap.length > 0 && (
                <div className="space-y-3">
                  {conceptsNeedingRecap.slice(0, 1).map((concept) => (
                    <RecapCard
                      key={concept.conceptId}
                      conceptName={concept.conceptName}
                      previousAnswer={getRecapMessage(concept.conceptId) || ''}
                      previousModule={concept.modules[0]?.moduleNumber || 1}
                      currentStage={concept.modules.find(m => m.moduleNumber === currentModule)?.stage || 'reinforce'}
                    />
                  ))}
                </div>
              )}

              {/* Current question */}
              <AnimatePresence mode="wait">
                {currentQuestion && (
                  <motion.div
                    key={currentQuestion.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <QuestionWithDisclosure
                      question={{
                        ...currentQuestion,
                        levels: {
                          essential: { description: currentQuestion.placeholder },
                          helpful: { description: currentQuestion.placeholder, tips: ['Sei konkret und spezifisch'] },
                          complete: { description: currentQuestion.placeholder, tips: ['Sei konkret', 'Nutze Beispiele'], examples: ['Beispiel 1', 'Beispiel 2'] }
                        }
                      }}
                      value={currentAnswer}
                      onChange={handleAnswerChange}
                      disclosureLevel={disclosureLevel}
                      onDisclosureLevelChange={setDisclosureLevel}
                      showHints={scaffolding.hints === 'always_visible'}
                    />
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Immediate feedback */}
              {feedback.length > 0 && (
                <div className="space-y-3">
                  {feedback.map((item) => (
                    <ImmediateFeedback
                      key={item.id}
                      feedback={item}
                      onDismiss={() => setFeedback(prev => prev.filter(f => f.id !== item.id))}
                    />
                  ))}
                </div>
              )}

              {/* Navigation */}
              <div className="flex items-center justify-between pt-4">
                <Button
                  variant="ghost"
                  onClick={handleBack}
                  disabled={currentQuestionIndex === 0}
                  leftIcon={<ArrowLeft size={18} />}
                >
                  Zurück
                </Button>

                <div className="flex items-center gap-3">
                  <Button
                    variant="secondary"
                    leftIcon={<Save size={16} />}
                    onClick={() => {}}
                  >
                    Speichern
                  </Button>

                  <Button
                    variant={currentQuestionIndex === questions.length - 1 ? 'accent' : 'primary'}
                    onClick={handleNext}
                    disabled={!canProceed}
                    isLoading={isLoading}
                    rightIcon={<ArrowRight size={18} />}
                  >
                    {currentQuestionIndex === questions.length - 1 ? 'Modul abschließen' : 'Weiter'}
                  </Button>
                </div>
              </div>
            </div>
          }
          rightColumn={
            <div className="space-y-6 sticky top-24">
              {/* Module progress */}
              <ModuleProgress
                currentModule={currentModule}
                moduleProgress={moduleProgress}
                gzReadinessScore={gzReadinessScore}
                currentQuestion={currentQuestionIndex + 1}
                totalQuestions={questions.length}
              />

              {/* Gap warnings */}
              {gaps.length > 0 && (
                <GapWarningPanel gaps={gaps} />
              )}

              {/* Endowment reminder */}
              <EndowmentReminder
                investments={[]}
                totalTimeInvested={(currentModule - 1) * 25 + currentQuestionIndex * 5}
                gzReadinessScore={gzReadinessScore}
                completedModules={currentModule - 1}
                generatedChapters={(currentModule - 1) * 3}
                onContinue={() => {}}
                variant="card"
              />
            </div>
          }
        />
      </ContentContainer>
    </WorkshopLayout>
  );
};

export default WorkshopPage;
