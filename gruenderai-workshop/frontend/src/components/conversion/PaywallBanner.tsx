import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Lock, CheckCircle, ArrowRight, Sparkles, Shield, FileText, X, Star } from 'lucide-react';
import { Button, Card, Badge, ProgressRing } from '@/components/common';

interface PaywallBannerProps {
  currentScore: number;
  onUnlock: () => void;
  onDismiss?: () => void;
  variant?: 'banner' | 'modal' | 'inline';
  price?: number;
}

const FEATURES = [
  { icon: FileText, text: '6 vollständige Module' },
  { icon: Sparkles, text: 'KI-generierter Businessplan' },
  { icon: Shield, text: 'GZ-Compliance-Prüfung' },
  { icon: Star, text: 'Export als PDF, DOCX & Excel' }
];

export const PaywallBanner = ({
  currentScore,
  onUnlock,
  onDismiss,
  variant = 'banner',
  price = 149
}: PaywallBannerProps) => {
  const [isHovering, setIsHovering] = useState(false);

  if (variant === 'modal') {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-warm-900/70"
      >
        <motion.div
          initial={{ scale: 0.9, y: 20 }}
          animate={{ scale: 1, y: 0 }}
          exit={{ scale: 0.9, y: 20 }}
          className="w-full max-w-lg"
        >
          <Card variant="elevated" padding="none" className="overflow-hidden">
            {/* Header */}
            <div className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-accent-600 p-8 text-white text-center">
              {onDismiss && (
                <button
                  onClick={onDismiss}
                  className="absolute top-4 right-4 p-2 hover:bg-white/20 rounded-full transition-colors"
                >
                  <X size={20} />
                </button>
              )}

              <motion.div
                animate={{ rotate: [0, 5, -5, 0] }}
                transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
              >
                <Lock size={48} className="mx-auto mb-4" />
              </motion.div>

              <h2 className="text-2xl font-display font-bold mb-2">
                Workshop freischalten
              </h2>
              <p className="text-white/80">
                Erstelle deinen vollständigen GZ-konformen Businessplan
              </p>
            </div>

            {/* Current progress */}
            <div className="p-6 border-b border-warm-200">
              <div className="flex items-center justify-between mb-4">
                <span className="text-warm-600">Dein aktueller Fortschritt</span>
                <Badge variant="primary">{currentScore}% GZ-Ready</Badge>
              </div>

              <div className="w-full h-3 bg-warm-200 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${currentScore}%` }}
                  transition={{ duration: 1, delay: 0.3 }}
                />
              </div>

              <p className="text-sm text-warm-500 mt-2 text-center">
                Nur noch {100 - currentScore}% bis zur GZ-Bereitschaft!
              </p>
            </div>

            {/* Features */}
            <div className="p-6">
              <h3 className="font-semibold text-warm-900 mb-4">
                Was du bekommst:
              </h3>

              <div className="grid grid-cols-2 gap-3 mb-6">
                {FEATURES.map((feature, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className="flex items-center gap-2 p-3 bg-warm-50 rounded-lg"
                  >
                    <feature.icon size={18} className="text-primary-500" />
                    <span className="text-sm text-warm-700">{feature.text}</span>
                  </motion.div>
                ))}
              </div>

              {/* Price and CTA */}
              <div className="text-center mb-6">
                <div className="mb-4">
                  <span className="text-3xl font-bold text-warm-900">{price}€</span>
                  <span className="text-warm-500 ml-2">einmalig</span>
                </div>

                <p className="text-sm text-warm-500 mb-4">
                  Spare 350-850€ im Vergleich zu Beratern
                </p>

                <Button
                  variant="accent"
                  size="lg"
                  fullWidth
                  onClick={onUnlock}
                  rightIcon={<ArrowRight size={20} />}
                >
                  Jetzt freischalten
                </Button>
              </div>

              {/* Trust badges */}
              <div className="flex items-center justify-center gap-4 text-xs text-warm-500">
                <div className="flex items-center gap-1">
                  <Shield size={14} />
                  <span>Sichere Zahlung</span>
                </div>
                <div className="flex items-center gap-1">
                  <CheckCircle size={14} />
                  <span>14 Tage Garantie</span>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    );
  }

  if (variant === 'inline') {
    return (
      <Card variant="default" padding="lg" className="border-primary-200 bg-gradient-to-br from-primary-50 to-accent-50">
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-shrink-0">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center shadow-gold-glow">
              <Lock size={28} className="text-white" />
            </div>
          </div>

          <div className="flex-1 text-center md:text-left">
            <h3 className="text-lg font-display font-bold text-warm-900 mb-1">
              Schalte den vollständigen Workshop frei
            </h3>
            <p className="text-warm-600">
              Erstelle deinen GZ-konformen Businessplan mit KI-Unterstützung
            </p>
          </div>

          <div className="flex flex-col items-center md:items-end gap-2">
            <div className="text-center md:text-right">
              <span className="text-2xl font-bold text-warm-900">{price}€</span>
              <span className="text-warm-500 text-sm ml-1">einmalig</span>
            </div>
            <Button
              variant="accent"
              onClick={onUnlock}
              rightIcon={<ArrowRight size={16} />}
            >
              Freischalten
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  // Default banner variant
  return (
    <motion.div
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="fixed bottom-0 left-0 right-0 z-40 bg-gradient-to-r from-primary-600 to-accent-600 text-white p-4 shadow-xl"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      <div className="max-w-4xl mx-auto flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <motion.div
            animate={{ rotate: isHovering ? [0, -10, 10, 0] : 0 }}
            transition={{ duration: 0.5 }}
          >
            <Lock size={32} />
          </motion.div>
          <div>
            <p className="font-semibold">
              Vollständiger Workshop für nur {price}€
            </p>
            <p className="text-sm text-white/80">
              GZ-konformer Businessplan in unter 3 Stunden
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {onDismiss && (
            <button
              onClick={onDismiss}
              className="text-white/60 hover:text-white transition-colors"
            >
              Später
            </button>
          )}
          <Button
            variant="secondary"
            onClick={onUnlock}
            className="bg-white text-primary-700 hover:bg-white/90 border-white"
            rightIcon={<ArrowRight size={16} />}
          >
            Freischalten
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

export default PaywallBanner;
