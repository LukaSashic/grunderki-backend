import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle, AlertTriangle, TrendingUp, Shield, Lock, Star } from 'lucide-react';
import { Button, Card, ProgressRing, Badge } from '@/components/common';
import { useWorkshopStore } from '@/stores/workshopStore';

interface AssessmentResultPageProps {
  score: number;
  onStartWorkshop: () => void;
  onBack: () => void;
}

export const AssessmentResultPage = ({ score, onStartWorkshop, onBack }: AssessmentResultPageProps) => {
  const setGzReadinessScore = useWorkshopStore((state) => state.setGzReadinessScore);

  // Set the score in the store on mount
  useEffect(() => {
    setGzReadinessScore(score);
  }, [score, setGzReadinessScore]);

  const getScoreAnalysis = () => {
    if (score >= 80) {
      return {
        title: 'Exzellent vorbereitet!',
        message: 'Du bist sehr gut auf den Gründungszuschuss vorbereitet. Der Workshop hilft dir, deine Unterlagen zu perfektionieren.',
        variant: 'success' as const,
        icon: CheckCircle
      };
    }
    if (score >= 60) {
      return {
        title: 'Guter Start!',
        message: 'Du hast eine solide Basis. Im Workshop werden wir gemeinsam die verbleibenden Lücken schließen.',
        variant: 'primary' as const,
        icon: TrendingUp
      };
    }
    if (score >= 40) {
      return {
        title: 'Potenzial erkannt!',
        message: 'Mit dem Workshop kannst du deinen Score deutlich verbessern. Wir zeigen dir genau, was zu tun ist.',
        variant: 'warning' as const,
        icon: AlertTriangle
      };
    }
    return {
      title: 'Lass uns gemeinsam starten!',
      message: 'Der Workshop führt dich Schritt für Schritt zu einem überzeugenden Businessplan.',
      variant: 'default' as const,
      icon: Shield
    };
  };

  const analysis = getScoreAnalysis();
  const Icon = analysis.icon;

  const STRENGTHS_AND_GAPS = [
    {
      type: score >= 50 ? 'strength' : 'gap',
      text: 'Geschäftsidee definiert',
      score: Math.min(score + 10, 100)
    },
    {
      type: score >= 40 ? 'strength' : 'gap',
      text: 'Zielgruppe identifiziert',
      score: Math.min(score, 100)
    },
    {
      type: score >= 60 ? 'strength' : 'gap',
      text: 'Fachliche Qualifikation',
      score: Math.min(score + 20, 100)
    },
    {
      type: 'gap',
      text: 'Finanzplanung erstellen',
      score: 0
    },
    {
      type: 'gap',
      text: 'Marktanalyse durchführen',
      score: 0
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-warm-50 to-primary-50 py-8 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <Badge variant="accent" size="md" className="mb-4">
            Dein GZ-Readiness Score
          </Badge>
        </motion.div>

        {/* Score Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <Card variant="elevated" padding="lg" className="mb-6">
            <div className="flex flex-col md:flex-row items-center gap-8">
              {/* Score ring */}
              <div className="flex-shrink-0">
                <ProgressRing
                  progress={score}
                  size="xl"
                  color={score >= 60 ? 'success' : score >= 40 ? 'warning' : 'danger'}
                  label="GZ-Readiness"
                />
              </div>

              {/* Analysis */}
              <div className="flex-1 text-center md:text-left">
                <div className="flex items-center justify-center md:justify-start gap-2 mb-2">
                  <Icon size={24} className={
                    analysis.variant === 'success' ? 'text-green-500' :
                    analysis.variant === 'primary' ? 'text-primary-500' :
                    analysis.variant === 'warning' ? 'text-amber-500' :
                    'text-warm-500'
                  } />
                  <h2 className="text-2xl font-display font-bold text-warm-900">
                    {analysis.title}
                  </h2>
                </div>
                <p className="text-warm-600 mb-4">
                  {analysis.message}
                </p>

                {/* Quick stats */}
                <div className="flex flex-wrap justify-center md:justify-start gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-green-600">
                      {STRENGTHS_AND_GAPS.filter(s => s.type === 'strength').length}
                    </p>
                    <p className="text-xs text-warm-500">Stärken</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-amber-600">
                      {STRENGTHS_AND_GAPS.filter(s => s.type === 'gap').length}
                    </p>
                    <p className="text-xs text-warm-500">Zu verbessern</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-primary-600">6</p>
                    <p className="text-xs text-warm-500">Module</p>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Strengths and Gaps */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card variant="default" padding="lg" className="mb-6">
            <h3 className="font-display font-semibold text-warm-900 mb-4">
              Deine Analyse
            </h3>

            <div className="space-y-3">
              {STRENGTHS_AND_GAPS.map((item, index) => (
                <motion.div
                  key={item.text}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  className={`flex items-center gap-3 p-3 rounded-lg ${
                    item.type === 'strength' ? 'bg-green-50' : 'bg-amber-50'
                  }`}
                >
                  {item.type === 'strength' ? (
                    <CheckCircle size={20} className="text-green-500 flex-shrink-0" />
                  ) : (
                    <AlertTriangle size={20} className="text-amber-500 flex-shrink-0" />
                  )}
                  <span className="flex-1 text-warm-800">{item.text}</span>
                  {item.type === 'gap' && (
                    <Lock size={16} className="text-warm-400" />
                  )}
                </motion.div>
              ))}
            </div>

            <div className="mt-4 p-4 bg-primary-50 rounded-lg border border-primary-100">
              <p className="text-sm text-primary-800">
                <strong>Im Workshop erhältst du:</strong> Detaillierte Anleitungen zu jedem Punkt,
                KI-generierte Textvorschläge und automatische GZ-Konformitätsprüfung.
              </p>
            </div>
          </Card>
        </motion.div>

        {/* Pricing CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card variant="accent" padding="lg">
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Star size={20} className="text-accent-500 fill-current" />
                <span className="text-sm font-medium text-warm-600">Einmaliges Angebot</span>
              </div>

              <h3 className="text-2xl font-display font-bold text-warm-900 mb-2">
                Vollständiger Workshop
              </h3>
              <p className="text-warm-600 mb-4">
                Von {score}% auf 100% GZ-Readiness in unter 3 Stunden
              </p>

              <div className="mb-6">
                <span className="text-4xl font-bold text-warm-900">149€</span>
                <span className="text-warm-500 ml-2">einmalig</span>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Button
                  variant="accent"
                  size="lg"
                  onClick={onStartWorkshop}
                  rightIcon={<ArrowRight size={20} />}
                >
                  Workshop starten
                </Button>
                <Button variant="ghost" onClick={onBack}>
                  Später fortsetzen
                </Button>
              </div>

              <p className="mt-4 text-xs text-warm-500">
                14 Tage Geld-zurück-Garantie • Sichere Zahlung mit PayPal
              </p>
            </div>
          </Card>
        </motion.div>

        {/* Trust badges */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="flex flex-wrap justify-center gap-6 mt-8 text-warm-500"
        >
          <div className="flex items-center gap-2">
            <Shield size={18} />
            <span className="text-sm">Erfüllt Agentur-Anforderungen</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle size={18} />
            <span className="text-sm">95% Erfolgsquote</span>
          </div>
          <div className="flex items-center gap-2">
            <Lock size={18} />
            <span className="text-sm">SSL-verschlüsselt</span>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AssessmentResultPage;
