/**
 * ChatWindow Component
 * Main chat interface with message list and auto-scroll
 *
 * V2: Tips werden vom Backend geladen mit Fallback auf lokale Tips
 */

import { useRef, useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Lightbulb } from 'lucide-react';
import { ChatMessage } from './ChatMessage';
import type { LocalMessage } from '@/stores/workshopChatStore';
import { microTipsApi, type MicroTip as ApiMicroTip } from '@/services/api';

// =============================================================================
// MODUL-SPEZIFISCHE MICRO TIPS - Fallback wenn Backend nicht erreichbar
// =============================================================================

// Tip-Typen für visuelle Unterscheidung
type TipType = 'fact' | 'warning' | 'motivation' | 'expert' | 'success';

interface MicroTip {
  type: TipType;
  text: string;
}

// Farben und Icons pro Tip-Typ
const TIP_STYLES: Record<TipType, { bg: string; border: string; text: string; icon: string }> = {
  fact: { bg: 'from-blue-50 to-indigo-50', border: 'border-blue-200', text: 'text-blue-900', icon: '📊' },
  warning: { bg: 'from-amber-50 to-orange-50', border: 'border-amber-200', text: 'text-amber-900', icon: '⚠️' },
  motivation: { bg: 'from-emerald-50 to-teal-50', border: 'border-emerald-200', text: 'text-emerald-900', icon: '💪' },
  expert: { bg: 'from-purple-50 to-pink-50', border: 'border-purple-200', text: 'text-purple-900', icon: '🎓' },
  success: { bg: 'from-green-50 to-emerald-50', border: 'border-green-200', text: 'text-green-900', icon: '✨' },
};

const MODULE_TIPS: Record<string, MicroTip[]> = {
  // MODUL 1: Geschäftsmodell - Mix aus allen Typen
  "sektion_1_geschaeftsmodell": [
    { type: 'fact', text: '80% der Startups scheitern an fehlendem Product-Market-Fit.' },
    { type: 'motivation', text: 'Du machst das richtig! Klare Idee = klarer Erfolg.' },
    { type: 'warning', text: 'Vorsicht: "Für alle" heißt oft "für niemanden".' },
    { type: 'expert', text: 'Die Agentur prüft Frage 7 besonders kritisch – Klarheit zählt!' },
    { type: 'fact', text: 'USP = Unique Selling Proposition. Was macht DICH einzigartig?' },
    { type: 'motivation', text: 'Jede große Firma hat mal klein angefangen. Du bist auf dem richtigen Weg!' },
    { type: 'warning', text: 'Zu billige Preise signalisieren oft minderwertige Qualität.' },
    { type: 'expert', text: 'Der "Oma-Test": Versteht jeder deine Idee in einem Satz?' },
    { type: 'success', text: 'Gute Geschäftsideen lösen echte Probleme – so wie deine!' },
    { type: 'fact', text: 'Nischenmärkte: Lieber 100 begeisterte als 1000 gleichgültige Kunden.' },
  ],

  // MODUL 2: Zielgruppe & Personas
  "sektion_2_zielgruppe": [
    { type: 'fact', text: 'B2B-Kunden haben 5x längere Entscheidungszyklen als B2C.' },
    { type: 'motivation', text: 'Super Fortschritt! Du verstehst deine Kunden immer besser.' },
    { type: 'warning', text: '"Alle" ist keine Zielgruppe – Fokus ist dein Freund!' },
    { type: 'expert', text: 'Antragstipp: Konkrete Personas überzeugen die Agentur für Arbeit.' },
    { type: 'fact', text: 'Kaufkraft prüfen: Hat deine Zielgruppe das Budget?' },
    { type: 'motivation', text: 'Je besser du deine Kunden kennst, desto einfacher wird alles!' },
    { type: 'warning', text: 'Klassischer Fehler: Erst Produkt, dann Kunden suchen.' },
    { type: 'expert', text: 'Gib deinem Idealkunden einen Namen – "Lisa, 42, Lehrerin..."' },
    { type: 'success', text: 'Klare Zielgruppe = einfacheres Marketing = mehr Erfolg!' },
    { type: 'fact', text: 'Wo hält sich deine Zielgruppe auf? Online? Offline? Events?' },
  ],

  // MODUL 3: Markt & Wettbewerb
  "sektion_3_markt": [
    { type: 'fact', text: 'TAM → SAM → SOM: Vom Gesamtmarkt zum realistischen Ziel.' },
    { type: 'motivation', text: 'Wettbewerber zu haben ist gut – sie beweisen, dass der Markt existiert!' },
    { type: 'warning', text: 'Ohne Marktanalyse keine Bewilligung – die Agentur schaut genau hin.' },
    { type: 'expert', text: 'Frage 11: "Wie groß ist der Kuchen, und welches Stück willst du?"' },
    { type: 'fact', text: 'Google-Suche: Such wie dein Kunde suchen würde.' },
    { type: 'motivation', text: 'Du positionierst dich gerade als Experte in deinem Bereich!' },
    { type: 'warning', text: 'Blue Ocean klingt verlockend, aber Red Oceans sind oft profitabler.' },
    { type: 'expert', text: 'Die fachkundige Stelle will sehen: Kennst du deine Top-3 Wettbewerber?' },
    { type: 'success', text: 'Kluge Marktanalyse zeigt: Du weißt, worauf du dich einlässt!' },
    { type: 'fact', text: 'Positionierung: Billiger, besser, schneller oder spezialisierter?' },
  ],

  // MODUL 4: Marketing & Vertrieb
  "sektion_4_marketing": [
    { type: 'fact', text: 'CAC (Customer Acquisition Cost): Was kostet ein neuer Kunde?' },
    { type: 'motivation', text: 'Die beste Werbung: Ein zufriedener Kunde, der dich empfiehlt!' },
    { type: 'warning', text: 'Lieber 1 Kanal richtig als 5 halbherzig bespielen.' },
    { type: 'expert', text: 'Antragstipp: Zeige einen konkreten Marketing-Plan!' },
    { type: 'fact', text: 'Customer Journey: Vom ersten Kontakt bis zur Zahlung.' },
    { type: 'motivation', text: 'Content Marketing: Gib Wert, bevor du verkaufst – das wirkt!' },
    { type: 'warning', text: 'Ohne Marketing-Budget kein Wachstum – plane realistisch.' },
    { type: 'expert', text: 'Verkaufen ist helfen: Du löst das Problem deines Kunden!' },
    { type: 'success', text: 'Guter Vertriebsplan = vorhersagbarer Umsatz = weniger Stress!' },
    { type: 'fact', text: 'Empfehlungsmarketing hat die höchste Conversion-Rate.' },
  ],

  // MODUL 5: Finanzplanung
  "sektion_5_finanzen": [
    { type: 'fact', text: 'Gründungszuschuss: ALG I + 300€ für 6 Monate, dann 9 Monate nur 300€.' },
    { type: 'motivation', text: 'Zahlen können einschüchtern – aber du meisterst das!' },
    { type: 'warning', text: 'Fragen 13-15: Hier scheitern die meisten – sei realistisch!' },
    { type: 'expert', text: 'Frage 15 (Lebensunterhalt) ist die kritischste – kannst du davon leben?' },
    { type: 'fact', text: 'Break-Even: Ab wann verdienst du mehr als du ausgibst?' },
    { type: 'motivation', text: 'Finanzplan fertig = Klarheit über deine Zukunft = Sicherheit!' },
    { type: 'warning', text: 'Umsatzprognose: Konservativ rechnen, nicht Best-Case!' },
    { type: 'expert', text: 'Mindestens 3 Monate Puffer für Unvorhergesehenes einplanen.' },
    { type: 'success', text: 'Solide Zahlen zeigen der Agentur: Du meinst es ernst!' },
    { type: 'fact', text: 'Fixe Kosten (Miete) vs. variable Kosten (Material) – kenne den Unterschied.' },
  ],

  // MODUL 6: Strategie & Abschluss
  "sektion_6_strategie": [
    { type: 'fact', text: 'SWOT: Stärken, Schwächen, Chancen, Risiken – kenne alle vier!' },
    { type: 'motivation', text: 'Fast geschafft! Dein Businessplan ist fast fertig!' },
    { type: 'warning', text: 'Risiken zu verschweigen wirkt unprofessionell – benenne sie!' },
    { type: 'expert', text: 'Die Agentur fragt auch nach Exit-Strategie – plane langfristig.' },
    { type: 'fact', text: 'Meilensteine: Was erreichst du in Monat 1, 3, 6, 12?' },
    { type: 'motivation', text: 'Du hast es fast geschafft – nur noch wenige Fragen!' },
    { type: 'warning', text: 'Skalierung ohne Plan führt oft zu Chaos – denk voraus.' },
    { type: 'expert', text: 'Die beste Strategie ist flexibel – Anpassen ist keine Schwäche.' },
    { type: 'success', text: 'Dein Businessplan ist deine Roadmap zum Erfolg!' },
    { type: 'fact', text: 'Netzwerk: Mentor:innen, Partner:innen, Berater:innen – wer kann dir helfen?' },
  ],
};

// Branchenspezifische Bonus-Tips
const BUSINESS_CATEGORY_TIPS: Record<string, MicroTip[]> = {
  "gastronomie": [
    { type: 'warning', text: 'Gastronomie: Hygiene-Vorschriften beachten – das prüft das Gesundheitsamt!' },
    { type: 'fact', text: 'Gastro-Marge: Essen ~30%, Getränke ~60%. Kalkuliere entsprechend!' },
    { type: 'expert', text: 'Sitzplätze × Umschlag × Bon = Umsatzpotenzial. Rechne das durch!' },
  ],
  "dienstleistung_online": [
    { type: 'fact', text: 'Online-Dienstleister haben oft 80%+ Marge – nutze diesen Vorteil!' },
    { type: 'motivation', text: 'Ortsunabhängig arbeiten = mehr Freiheit = bessere Work-Life-Balance!' },
    { type: 'warning', text: 'Online-Konkurrenz ist global – positioniere dich klar!' },
  ],
  "handwerk": [
    { type: 'fact', text: 'Handwerk: Meisterpflicht beachten! Prüfe, ob du sie brauchst.' },
    { type: 'expert', text: 'Handwerkskammer = fachkundige Stelle. Die kennen deine Branche!' },
    { type: 'motivation', text: 'Handwerk hat goldenen Boden – und der Fachkräftemangel hilft dir!' },
  ],
  "ecommerce": [
    { type: 'warning', text: 'E-Commerce: Retourenquote ~30-40% bei Mode. Kalkuliere das ein!' },
    { type: 'fact', text: 'CAC (Kundengewinnungskosten) im E-Com oft €20-50+. Kenne deine Zahlen!' },
    { type: 'expert', text: 'Amazon & Co. dominieren – finde deine Nische!' },
  ],
  "beratung": [
    { type: 'fact', text: 'Beratungs-Tagessätze: Junior €400-800, Senior €1.200-2.500+.' },
    { type: 'motivation', text: 'Deine Expertise ist wertvoll – lass dir das auch bezahlen!' },
    { type: 'warning', text: 'Beratung = Vertrauen. Ohne Referenzen wird der Start schwer.' },
  ],
};

// Fallback-Tips für unbekannte Sektionen
const GENERAL_TIPS: MicroTip[] = [
  { type: 'fact', text: 'Der Gründungszuschuss beträgt ALG I + 300€/Monat für 6 Monate.' },
  { type: 'warning', text: '65% der GZ-Ablehnungen scheitern an mangelnden Fachkenntnissen.' },
  { type: 'motivation', text: 'Du investierst in deine Zukunft – das zahlt sich aus!' },
  { type: 'expert', text: 'Fachkundige Stelle: IHK, Steuerberatung oder Gründungszentrum.' },
  { type: 'fact', text: 'Mindestens 15 Stunden/Woche = hauptberuflich selbstständig.' },
  { type: 'success', text: 'Jeder Schritt bringt dich deinem Ziel näher. Weiter so!' },
  { type: 'warning', text: 'Die ersten 3 Monate sind kritisch – plane einen Puffer ein!' },
  { type: 'expert', text: 'Konkrete Zahlen wirken überzeugender als vage Schätzungen.' },
];

// Helper: Holt die lokalen Fallback-Tips für die aktuelle Sektion + Business Category
function getLocalTipsForSection(sectionId?: string, businessCategory?: string): MicroTip[] {
  let tips: MicroTip[] = [];

  // Sektion-spezifische Tips
  if (sectionId) {
    if (MODULE_TIPS[sectionId]) {
      tips = [...MODULE_TIPS[sectionId]];
    } else {
      // Partial Match (z.B. "modul_1_geschaeftsidee" → "sektion_1_geschaeftsmodell")
      const sectionNumber = sectionId.match(/(\d)/)?.[1];
      if (sectionNumber) {
        const matchingKey = Object.keys(MODULE_TIPS).find(key => key.includes(`_${sectionNumber}_`));
        if (matchingKey) tips = [...MODULE_TIPS[matchingKey]];
      }
    }
  }

  // Branchenspezifische Tips hinzufügen
  if (businessCategory && BUSINESS_CATEGORY_TIPS[businessCategory]) {
    tips = [...tips, ...BUSINESS_CATEGORY_TIPS[businessCategory]];
  }

  // Fallback
  if (tips.length === 0) tips = [...GENERAL_TIPS];

  // Shuffle für Abwechslung
  return tips.sort(() => Math.random() - 0.5);
}

// Konvertiert API-Tips zu lokalen Tips
function convertApiTips(apiTips: ApiMicroTip[]): MicroTip[] {
  return apiTips.map(tip => ({
    text: tip.text,
    type: tip.type as TipType,
  }));
}

interface ChatWindowProps {
  messages: LocalMessage[];
  isTyping?: boolean;
  currentSection?: string;
  /** Business category for industry-specific tips */
  businessCategory?: string;
  /** Callback when a card is selected */
  onCardSelect?: (value: string) => void;
  /** Whether card selection is disabled */
  disabled?: boolean;
}

export function ChatWindow({
  messages,
  isTyping = false,
  currentSection,
  businessCategory,
  onCardSelect,
  disabled = false,
}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [currentTipIndex, setCurrentTipIndex] = useState(0);
  const [tips, setTips] = useState<MicroTip[]>([]);
  const [isLoadingTips, setIsLoadingTips] = useState(false);

  // Fetch tips from backend when section changes
  const fetchTips = useCallback(async () => {
    if (!currentSection) {
      // Use local fallback if no section
      setTips(getLocalTipsForSection(undefined, businessCategory));
      return;
    }

    setIsLoadingTips(true);
    try {
      const response = await microTipsApi.getTips(
        currentSection,
        businessCategory || undefined,
        true // shuffle
      );

      if (response.tips && response.tips.length > 0) {
        setTips(convertApiTips(response.tips));
      } else {
        // Fallback to local tips if backend returns empty
        setTips(getLocalTipsForSection(currentSection, businessCategory));
      }
    } catch (error) {
      console.warn('[ChatWindow] Failed to fetch tips from backend, using fallback:', error);
      // Fallback to local tips on error
      setTips(getLocalTipsForSection(currentSection, businessCategory));
    } finally {
      setIsLoadingTips(false);
    }
  }, [currentSection, businessCategory]);

  // Fetch tips when section or business category changes
  useEffect(() => {
    fetchTips();
  }, [fetchTips]);

  // Current tip with fallback
  const currentTips = tips.length > 0 ? tips : getLocalTipsForSection(currentSection, businessCategory);
  const currentTip = currentTips[currentTipIndex] || currentTips[0];
  const tipStyle = TIP_STYLES[currentTip?.type || 'fact'];

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // Rotate micro tips every 4 seconds while typing
  useEffect(() => {
    if (!isTyping) {
      // Start with random tip when not typing
      setCurrentTipIndex(Math.floor(Math.random() * currentTips.length));
      return;
    }

    const interval = setInterval(() => {
      setCurrentTipIndex((prev) => (prev + 1) % currentTips.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [isTyping, currentTips.length]);

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto bg-gradient-to-b from-gray-50 to-white"
    >
      {/* Header with current section */}
      {currentSection && (
        <div className="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-gray-100 px-4 py-2">
          <p className="text-sm text-gray-600 text-center">
            Aktuelle Sektion: <span className="font-medium">{currentSection}</span>
          </p>
        </div>
      )}

      {/* Messages */}
      <div className="max-w-4xl mx-auto py-4">
        <AnimatePresence initial={false}>
          {messages.map((message, index) => (
            <ChatMessage
              key={message.id}
              message={message}
              onCardSelect={onCardSelect}
              disabled={disabled || isTyping}
              isLastMessage={index === messages.length - 1}
            />
          ))}
        </AnimatePresence>

        {/* Typing Indicator with Dynamic Micro Tips */}
        <AnimatePresence>
          {isTyping && currentTip && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex gap-3 p-4"
            >
              {/* Dynamic Icon based on tip type */}
              <motion.div
                key={currentTip.type}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-xl"
              >
                {tipStyle.icon}
              </motion.div>

              {/* Tip Card with dynamic styling */}
              <motion.div
                key={`tip-${currentTipIndex}`}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className={`bg-gradient-to-r ${tipStyle.bg} shadow-md border ${tipStyle.border} rounded-2xl rounded-tl-sm px-4 py-3 max-w-md`}
              >
                {/* Header: Makes clear AI is working */}
                <div className="flex items-center gap-2 mb-2 pb-2 border-b border-gray-200/50">
                  <div className="flex gap-1">
                    <motion.span
                      animate={{ opacity: [0.4, 1, 0.4] }}
                      transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                      className="w-1.5 h-1.5 bg-emerald-500 rounded-full"
                    />
                    <motion.span
                      animate={{ opacity: [0.4, 1, 0.4] }}
                      transition={{ duration: 1, repeat: Infinity, delay: 0.15 }}
                      className="w-1.5 h-1.5 bg-emerald-500 rounded-full"
                    />
                    <motion.span
                      animate={{ opacity: [0.4, 1, 0.4] }}
                      transition={{ duration: 1, repeat: Infinity, delay: 0.3 }}
                      className="w-1.5 h-1.5 bg-emerald-500 rounded-full"
                    />
                  </div>
                  <span className="text-xs text-gray-600 font-medium">
                    GründerAI bereitet deine Antwort vor
                  </span>
                </div>

                {/* Tip Type Label */}
                <p className="text-xs text-gray-500 mb-1">
                  {currentTip.type === 'fact' && '📊 Fakt'}
                  {currentTip.type === 'warning' && '⚠️ Achtung'}
                  {currentTip.type === 'motivation' && '💪 Motivation'}
                  {currentTip.type === 'expert' && '🎓 Experten-Tipp'}
                  {currentTip.type === 'success' && '✨ Du machst das toll!'}
                </p>

                {/* Rotating Micro Tips */}
                <AnimatePresence mode="wait">
                  <motion.p
                    key={currentTipIndex}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -5 }}
                    transition={{ duration: 0.3 }}
                    className={`text-sm ${tipStyle.text} font-medium`}
                  >
                    {currentTip.text}
                  </motion.p>
                </AnimatePresence>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Empty State */}
        {messages.length === 0 && !isTyping && (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-emerald-100 to-teal-100 flex items-center justify-center mb-4">
              <Bot className="w-10 h-10 text-emerald-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Willkommen beim GründerAI Workshop
            </h3>
            <p className="text-gray-500 max-w-md">
              Starte deinen interaktiven Workshop zur Erstellung eines
              Gründungszuschuss-konformen Businessplans.
            </p>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

export default ChatWindow;
