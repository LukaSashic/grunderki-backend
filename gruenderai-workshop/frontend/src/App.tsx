import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import {
  LandingPage,
  AssessmentPage,
  AssessmentResultPage,
  WorkshopPage,
  WorkshopModule1Page,
  ResultsPage,
  WorkshopChatPage,
} from '@/pages';
import { useWorkshopStore } from '@/stores/workshopStore';

type AppView = 'landing' | 'assessment' | 'assessment-result' | 'workshop-module1' | 'workshop' | 'results';

// Legacy App Component for non-routed pages
function LegacyApp() {
  const navigate = useNavigate();
  const [currentView, setCurrentView] = useState<AppView>('landing');
  const [assessmentScore, setAssessmentScore] = useState(0);
  const { reset } = useWorkshopStore();

  // Check for saved session on mount
  useEffect(() => {
    const savedSession = localStorage.getItem('gruenderai-workshop');
    if (savedSession) {
      try {
        const session = JSON.parse(savedSession);
        if (session.state?.currentModule >= 1) {
          // User has progress, offer to continue
          const shouldContinue = window.confirm(
            'Du hast einen laufenden Workshop. Möchtest du fortfahren?'
          );
          if (shouldContinue) {
            // Resume at the right module
            if (session.state.currentModule === 1) {
              setCurrentView('workshop-module1');
            } else {
              setCurrentView('workshop');
            }
          }
        }
      } catch (e) {
        console.error('Failed to parse saved session:', e);
      }
    }
  }, []);

  const handleStartAssessment = () => {
    setCurrentView('assessment');
  };

  const handleAssessmentComplete = (score: number) => {
    setAssessmentScore(score);
    setCurrentView('assessment-result');
  };

  const handleStartWorkshop = () => {
    // Navigate to the new chat-based workshop
    navigate('/workshop-chat');
  };

  const handleModule1Complete = () => {
    // After Module 1, continue to the rest of the workshop
    setCurrentView('workshop');
  };

  const handleWorkshopComplete = () => {
    setCurrentView('results');
  };

  const handleRestart = () => {
    reset();
    setCurrentView('landing');
  };

  const handleBack = () => {
    switch (currentView) {
      case 'assessment':
        setCurrentView('landing');
        break;
      case 'assessment-result':
        setCurrentView('landing');
        break;
      case 'workshop-module1':
        setCurrentView('assessment-result');
        break;
      case 'workshop':
        setCurrentView('workshop-module1');
        break;
      default:
        setCurrentView('landing');
    }
  };

  return (
    <div className="min-h-screen bg-warm-50">
      <AnimatePresence mode="wait">
        {currentView === 'landing' && (
          <LandingPage
            key="landing"
            onStartAssessment={handleStartAssessment}
          />
        )}

        {currentView === 'assessment' && (
          <AssessmentPage
            key="assessment"
            onComplete={handleAssessmentComplete}
            onBack={handleBack}
          />
        )}

        {currentView === 'assessment-result' && (
          <AssessmentResultPage
            key="assessment-result"
            score={assessmentScore}
            onStartWorkshop={handleStartWorkshop}
            onBack={handleBack}
          />
        )}

        {currentView === 'workshop-module1' && (
          <WorkshopModule1Page
            key="workshop-module1"
            onComplete={handleModule1Complete}
          />
        )}

        {currentView === 'workshop' && (
          <WorkshopPage
            key="workshop"
            onComplete={handleWorkshopComplete}
          />
        )}

        {currentView === 'results' && (
          <ResultsPage
            key="results"
            onRestart={handleRestart}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

// Main App with Router
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* New Chat-based Workshop */}
        <Route path="/workshop-chat" element={<WorkshopChatPage />} />

        {/* Legacy routes */}
        <Route path="/*" element={<LegacyApp />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
