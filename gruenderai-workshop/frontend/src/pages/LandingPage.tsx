import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle, Star, Shield, Clock, FileText, TrendingUp, Users } from 'lucide-react';
import { Button, Card, Badge } from '@/components/common';

interface LandingPageProps {
  onStartAssessment: () => void;
}

const FEATURES = [
  {
    icon: Shield,
    title: 'GZ-Konform',
    description: 'Erfüllt alle Anforderungen des Arbeitsamts'
  },
  {
    icon: Clock,
    title: 'Unter 3 Stunden',
    description: 'Professioneller Businessplan in kurzer Zeit'
  },
  {
    icon: FileText,
    title: 'Komplette Dokumente',
    description: 'PDF, Word & Excel mit einem Klick'
  },
  {
    icon: TrendingUp,
    title: 'KI-Optimiert',
    description: 'Intelligente Vorschläge für deinen Erfolg'
  }
];

const TESTIMONIALS = [
  {
    name: 'Sarah M.',
    role: 'Grafikdesignerin',
    quote: 'In nur 2 Stunden hatte ich meinen kompletten Businessplan fertig. Der Gründungszuschuss wurde beim ersten Versuch genehmigt!',
    rating: 5
  },
  {
    name: 'Thomas K.',
    role: 'IT-Beratung',
    quote: 'Die KI hat mir geholfen, Lücken in meinem Konzept zu finden, die ich selbst übersehen hätte.',
    rating: 5
  },
  {
    name: 'Lisa B.',
    role: 'Coaching',
    quote: 'Viel günstiger als eine Beratung und das Ergebnis war professioneller als erwartet.',
    rating: 5
  }
];

export const LandingPage = ({ onStartAssessment }: LandingPageProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-warm-50 to-primary-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-600/10 to-accent-600/10" />

        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24 relative">
          <div className="text-center max-w-3xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Badge variant="accent" size="md" className="mb-6">
                <Star size={14} className="mr-1" />
                Über 500 erfolgreiche Anträge
              </Badge>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-display font-bold text-warm-900 mb-6">
                Dein Businessplan für den{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-accent-600">
                  Gründungszuschuss
                </span>
              </h1>

              <p className="text-xl text-warm-600 mb-8 max-w-2xl mx-auto">
                Erstelle in unter 3 Stunden einen professionellen, GZ-konformen Businessplan.
                Mit KI-Unterstützung und Schritt-für-Schritt Anleitung.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Button
                  variant="accent"
                  size="xl"
                  onClick={onStartAssessment}
                  rightIcon={<ArrowRight size={20} />}
                >
                  Kostenlos starten
                </Button>
                <p className="text-sm text-warm-500">
                  Keine Kreditkarte erforderlich
                </p>
              </div>
            </motion.div>

            {/* Trust indicators */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mt-12 flex flex-wrap items-center justify-center gap-8"
            >
              <div className="flex items-center gap-2">
                <CheckCircle size={20} className="text-green-500" />
                <span className="text-warm-600">95% Erfolgsquote</span>
              </div>
              <div className="flex items-center gap-2">
                <Users size={20} className="text-primary-500" />
                <span className="text-warm-600">500+ Gründer:innen</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield size={20} className="text-accent-500" />
                <span className="text-warm-600">Erfüllt Agentur-Anforderungen</span>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-display font-bold text-warm-900 mb-4">
              Alles was du brauchst
            </h2>
            <p className="text-warm-600 max-w-2xl mx-auto">
              Von der Geschäftsidee bis zum fertigen Antrag - wir begleiten dich durch jeden Schritt
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {FEATURES.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card variant="interactive" padding="lg" hoverable className="h-full">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-100 to-accent-100 flex items-center justify-center mb-4">
                    <feature.icon size={24} className="text-primary-600" />
                  </div>
                  <h3 className="font-semibold text-warm-900 mb-2">{feature.title}</h3>
                  <p className="text-sm text-warm-600">{feature.description}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 bg-gradient-to-br from-primary-50 to-accent-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-display font-bold text-warm-900 mb-4">
              So funktioniert's
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: 1,
                title: 'Kostenloser Check',
                description: '5 Fragen beantworten und deine GZ-Readiness erfahren'
              },
              {
                step: 2,
                title: '6 Module durcharbeiten',
                description: 'Strukturierte Fragen mit KI-Unterstützung beantworten'
              },
              {
                step: 3,
                title: 'Businessplan erhalten',
                description: 'Fertiger Plan als PDF, Word und Excel zum Download'
              }
            ].map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                className="text-center"
              >
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center mx-auto mb-4 shadow-lg">
                  <span className="text-2xl font-bold text-white">{item.step}</span>
                </div>
                <h3 className="text-lg font-semibold text-warm-900 mb-2">{item.title}</h3>
                <p className="text-warm-600">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-display font-bold text-warm-900 mb-4">
              Erfolgsgeschichten
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {TESTIMONIALS.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card variant="default" padding="lg" className="h-full">
                  <div className="flex gap-1 mb-4">
                    {Array.from({ length: testimonial.rating }).map((_, i) => (
                      <Star key={i} size={16} className="text-accent-500 fill-current" />
                    ))}
                  </div>
                  <p className="text-warm-600 mb-4 italic">"{testimonial.quote}"</p>
                  <div>
                    <p className="font-semibold text-warm-900">{testimonial.name}</p>
                    <p className="text-sm text-warm-500">{testimonial.role}</p>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing CTA */}
      <section className="py-16 bg-gradient-to-br from-primary-600 to-accent-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-display font-bold mb-6">
            Starte jetzt - kostenlos!
          </h2>
          <p className="text-xl text-white/80 mb-8">
            Mach den GZ-Readiness Check und erfahre, wie gut du vorbereitet bist
          </p>

          <div className="inline-flex flex-col sm:flex-row items-center gap-6 mb-8">
            <div className="text-center">
              <p className="text-4xl font-bold">0€</p>
              <p className="text-white/70">Assessment</p>
            </div>
            <div className="hidden sm:block w-px h-12 bg-white/30" />
            <div className="text-center">
              <p className="text-4xl font-bold">149€</p>
              <p className="text-white/70">Vollständiger Workshop</p>
            </div>
          </div>

          <Button
            variant="secondary"
            size="xl"
            onClick={onStartAssessment}
            className="bg-white text-primary-700 hover:bg-white/90 border-white"
            rightIcon={<ArrowRight size={20} />}
          >
            Kostenlosen Check starten
          </Button>

          <p className="mt-6 text-sm text-white/60">
            Spare 350-850€ im Vergleich zu traditioneller Beratung
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-warm-900 text-warm-400">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm">
            © 2024 GründerAI. Alle Rechte vorbehalten.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
