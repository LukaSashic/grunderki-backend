import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, ArrowLeft, CheckCircle, HelpCircle, Loader2 } from 'lucide-react';
import { Button, Card, Input, TextArea, Badge } from '@/components/common';
import { useWorkshopStore } from '@/stores/workshopStore';
import { assessmentApi } from '@/services/api';

interface AssessmentPageProps {
  onComplete: (score: number) => void;
  onBack: () => void;
}

interface BackendQuestion {
  id: string;
  questionNumber: number;
  question: string;
  type: 'textarea' | 'multiple_choice' | 'multiple_select' | 'text';
  options?: Array<{
    id: string;
    label: string;
    description?: string;
  }>;
  maxLength?: number;
  required: boolean;
  helpText?: string;
  gzHint?: string;
}

export const AssessmentPage = ({ onComplete, onBack }: AssessmentPageProps) => {
  const [questions, setQuestions] = useState<BackendQuestion[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string | string[]>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { setUserContext } = useWorkshopStore();

  const currentQ = questions[currentQuestion];
  const progress = questions.length > 0 ? ((currentQuestion + 1) / questions.length) * 100 : 0;
  const isLastQuestion = currentQuestion === questions.length - 1;

  // Check if current question is answered
  const canProceed = currentQ && (() => {
    const answer = answers[currentQ.id];
    if (!answer) return false;
    if (Array.isArray(answer)) return answer.length > 0;
    return answer.toString().trim() !== '';
  })();

  useEffect(() => {
    // Start assessment session and get questions
    const startSession = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await assessmentApi.start();
        setSessionId(response.session_id);
        if (response.questions && response.questions.length > 0) {
          setQuestions(response.questions as BackendQuestion[]);
        } else {
          setError('Keine Fragen vom Server erhalten');
        }
      } catch (err) {
        console.error('Failed to start assessment:', err);
        setError('Verbindung zum Server fehlgeschlagen');
      } finally {
        setIsLoading(false);
      }
    };
    startSession();
  }, []);

  const handleAnswer = (value: string | string[]) => {
    if (currentQ) {
      setAnswers(prev => ({ ...prev, [currentQ.id]: value }));
    }
  };

  const handleMultiSelect = (optionId: string) => {
    if (!currentQ) return;
    const currentAnswers = (answers[currentQ.id] as string[]) || [];
    if (currentAnswers.includes(optionId)) {
      handleAnswer(currentAnswers.filter(id => id !== optionId));
    } else {
      handleAnswer([...currentAnswers, optionId]);
    }
  };

  const handleNext = async () => {
    if (!canProceed) return;

    if (isLastQuestion) {
      setIsSubmitting(true);
      try {
        // Submit assessment
        const response = await assessmentApi.submit(sessionId || '', answers as Record<string, string | string[] | number>);

        // Update store with user context
        const firstAnswer = answers[questions[0]?.id];
        setUserContext({
          businessName: typeof firstAnswer === 'string' ? firstAnswer.substring(0, 50) : '',
          businessType: (answers['assess_zielgruppe'] as string) || '',
          founderName: ''
        });

        onComplete(response.gz_readiness_score || 45);
      } catch (err) {
        console.error('Failed to submit assessment:', err);
        // Still proceed with a default score
        onComplete(45);
      } finally {
        setIsSubmitting(false);
      }
    } else {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handleBack = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    } else {
      onBack();
    }
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-warm-50 to-primary-50 flex items-center justify-center p-4">
        <div className="text-center">
          <Loader2 size={48} className="animate-spin text-primary-500 mx-auto mb-4" />
          <p className="text-warm-600">Assessment wird geladen...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error || questions.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-warm-50 to-primary-50 flex items-center justify-center p-4">
        <Card variant="elevated" padding="lg" className="max-w-md text-center">
          <p className="text-red-600 mb-4">{error || 'Keine Fragen verfügbar'}</p>
          <div className="flex gap-3 justify-center">
            <Button variant="secondary" onClick={onBack}>
              Zurück
            </Button>
            <Button variant="primary" onClick={() => window.location.reload()}>
              Erneut versuchen
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-warm-50 to-primary-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <Badge variant="primary" size="md" className="mb-4">
            Kostenloser GZ-Readiness Check
          </Badge>
          <h1 className="text-2xl font-display font-bold text-warm-900 mb-2">
            Lass uns deine Gründungsidee prüfen
          </h1>
          <p className="text-warm-600">
            Beantworte {questions.length} kurze Fragen und erfahre, wie bereit du für den Gründungszuschuss bist
          </p>
        </motion.div>

        {/* Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-warm-500">
              Frage {currentQuestion + 1} von {questions.length}
            </span>
            <span className="text-sm font-medium text-primary-600">
              {Math.round(progress)}%
            </span>
          </div>
          <div className="w-full h-2 bg-warm-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full"
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Question Card */}
        <AnimatePresence mode="wait">
          {currentQ && (
            <motion.div
              key={currentQuestion}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Card variant="elevated" padding="lg">
                {/* Question */}
                <div className="mb-6">
                  <div className="flex items-start justify-between gap-4 mb-4">
                    <h2 className="text-xl font-semibold text-warm-900">
                      {currentQ.question}
                    </h2>
                    {currentQ.helpText && (
                      <div className="group relative">
                        <HelpCircle size={20} className="text-warm-400 cursor-help" />
                        <div className="absolute right-0 top-full mt-2 w-64 p-3 bg-warm-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
                          {currentQ.helpText}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* GZ Hint */}
                  {currentQ.gzHint && (
                    <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                      <p className="text-sm text-amber-800">
                        <strong>GZ-Hinweis:</strong> {currentQ.gzHint}
                      </p>
                    </div>
                  )}

                  {/* Answer input based on type */}
                  {currentQ.type === 'textarea' && (
                    <TextArea
                      value={(answers[currentQ.id] as string) || ''}
                      onChange={(e) => handleAnswer(e.target.value)}
                      placeholder={currentQ.helpText || 'Deine Antwort...'}
                      rows={4}
                      maxLength={currentQ.maxLength}
                      showCount={!!currentQ.maxLength}
                    />
                  )}

                  {currentQ.type === 'text' && (
                    <Input
                      value={(answers[currentQ.id] as string) || ''}
                      onChange={(e) => handleAnswer(e.target.value)}
                      placeholder={currentQ.helpText || 'Deine Antwort...'}
                    />
                  )}

                  {currentQ.type === 'multiple_choice' && currentQ.options && (
                    <div className="space-y-3">
                      {currentQ.options.map((option) => (
                        <motion.button
                          key={option.id}
                          onClick={() => handleAnswer(option.id)}
                          className={`w-full p-4 text-left rounded-xl border-2 transition-all ${
                            answers[currentQ.id] === option.id
                              ? 'border-primary-500 bg-primary-50'
                              : 'border-warm-200 hover:border-warm-300 bg-white'
                          }`}
                          whileHover={{ scale: 1.01 }}
                          whileTap={{ scale: 0.99 }}
                        >
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="font-medium text-warm-900">{option.label}</p>
                              {option.description && (
                                <p className="text-sm text-warm-500 mt-0.5">{option.description}</p>
                              )}
                            </div>
                            {answers[currentQ.id] === option.id && (
                              <CheckCircle size={20} className="text-primary-500" />
                            )}
                          </div>
                        </motion.button>
                      ))}
                    </div>
                  )}

                  {currentQ.type === 'multiple_select' && currentQ.options && (
                    <div className="space-y-3">
                      <p className="text-sm text-warm-500 mb-2">
                        Mehrfachauswahl möglich
                      </p>
                      {currentQ.options.map((option) => {
                        const selectedAnswers = (answers[currentQ.id] as string[]) || [];
                        const isSelected = selectedAnswers.includes(option.id);

                        return (
                          <motion.button
                            key={option.id}
                            onClick={() => handleMultiSelect(option.id)}
                            className={`w-full p-4 text-left rounded-xl border-2 transition-all ${
                              isSelected
                                ? 'border-primary-500 bg-primary-50'
                                : 'border-warm-200 hover:border-warm-300 bg-white'
                            }`}
                            whileHover={{ scale: 1.01 }}
                            whileTap={{ scale: 0.99 }}
                          >
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="font-medium text-warm-900">{option.label}</p>
                                {option.description && (
                                  <p className="text-sm text-warm-500 mt-0.5">{option.description}</p>
                                )}
                              </div>
                              {isSelected && (
                                <CheckCircle size={20} className="text-primary-500" />
                              )}
                            </div>
                          </motion.button>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Navigation */}
                <div className="flex items-center justify-between pt-6 border-t border-warm-100">
                  <Button
                    variant="ghost"
                    onClick={handleBack}
                    leftIcon={<ArrowLeft size={18} />}
                  >
                    Zurück
                  </Button>

                  <Button
                    variant={isLastQuestion ? 'accent' : 'primary'}
                    onClick={handleNext}
                    disabled={!canProceed}
                    isLoading={isSubmitting}
                    rightIcon={<ArrowRight size={18} />}
                  >
                    {isLastQuestion ? 'Auswerten' : 'Weiter'}
                  </Button>
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Question dots */}
        <div className="flex justify-center gap-2 mt-6">
          {questions.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentQuestion
                  ? 'w-6 bg-primary-500'
                  : index < currentQuestion
                    ? 'bg-green-500'
                    : 'bg-warm-300'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default AssessmentPage;
