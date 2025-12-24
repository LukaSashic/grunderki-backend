import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Download, FileText, Table, File, CheckCircle, Sparkles, Share2, RefreshCw } from 'lucide-react';
import { Button, Card, ProgressRing, QualityGauge, Badge } from '@/components/common';
import { WorkshopLayout, ContentContainer, PageHeader, TwoColumnLayout } from '@/components/layout';
import { useWorkshopStore } from '@/stores/workshopStore';
import { documentsApi } from '@/services/api';

interface ResultsPageProps {
  onRestart: () => void;
}

const GENERATED_CHAPTERS = [
  { id: '1', title: 'Executive Summary', status: 'completed' },
  { id: '2.1', title: 'Geschäftsidee', status: 'completed' },
  { id: '2.2', title: 'Kundennutzen', status: 'completed' },
  { id: '2.3', title: 'Zielgruppe', status: 'completed' },
  { id: '3.1', title: 'Unternehmerprofil', status: 'completed' },
  { id: '3.2', title: 'Fachliche Qualifikation', status: 'completed' },
  { id: '3.3', title: 'Kaufmännische Kenntnisse', status: 'completed' },
  { id: '3.4', title: 'Team', status: 'completed' },
  { id: '3.5', title: 'Rechtliche Voraussetzungen', status: 'completed' },
  { id: '3.6', title: 'Standort', status: 'completed' },
  { id: '4.1', title: 'Marktanalyse', status: 'completed' },
  { id: '4.2', title: 'Wettbewerbsanalyse', status: 'completed' },
  { id: '5.1', title: 'Marketing-Strategie', status: 'completed' },
  { id: '5.2', title: 'Vertriebsstrategie', status: 'completed' },
  { id: '5.3', title: 'Preisgestaltung', status: 'completed' },
  { id: '6.1', title: 'Umsatzplanung', status: 'completed' },
  { id: '6.2', title: 'Kostenplanung', status: 'completed' },
  { id: '6.3', title: 'Liquiditätsplanung', status: 'completed' },
  { id: '6.4', title: 'Kapitalbedarf', status: 'completed' },
  { id: '7', title: 'SWOT-Analyse', status: 'completed' },
  { id: '8', title: 'Risikoanalyse', status: 'completed' },
  { id: '9', title: 'Meilensteine', status: 'completed' }
];

export const ResultsPage = ({ onRestart }: ResultsPageProps) => {
  const { sessionId, gzReadinessScore, userContext } = useWorkshopStore();
  const [isGenerating, setIsGenerating] = useState(false);
  const [documentsReady, setDocumentsReady] = useState(false);
  const [downloadCounts, setDownloadCounts] = useState({
    pdf: 0,
    docx: 0,
    xlsx: 0
  });

  useEffect(() => {
    // Simulate document generation
    const timer = setTimeout(() => {
      setDocumentsReady(true);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  const handleDownload = async (format: 'pdf' | 'docx' | 'xlsx' | 'all') => {
    if (!sessionId) return;

    const urls = {
      pdf: documentsApi.downloadPdf(sessionId),
      docx: documentsApi.downloadDocx(sessionId),
      xlsx: documentsApi.downloadXlsx(sessionId),
      all: documentsApi.downloadAll(sessionId)
    };

    window.open(urls[format], '_blank');

    if (format !== 'all') {
      setDownloadCounts(prev => ({
        ...prev,
        [format]: prev[format] + 1
      }));
    }
  };

  return (
    <WorkshopLayout showSidebar={false}>
      <ContentContainer maxWidth="xl" padding="lg">
        {/* Celebration header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', damping: 10, delay: 0.2 }}
            className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center shadow-lg"
          >
            <Sparkles size={48} className="text-white" />
          </motion.div>

          <Badge variant="success" size="lg" className="mb-4">
            <CheckCircle size={16} className="mr-2" />
            Workshop abgeschlossen!
          </Badge>

          <h1 className="text-3xl sm:text-4xl font-display font-bold text-warm-900 mb-4">
            Dein Businessplan ist fertig!
          </h1>
          <p className="text-xl text-warm-600 max-w-2xl mx-auto">
            Herzlichen Glückwunsch! Du hast alle 6 Module erfolgreich abgeschlossen und deinen
            GZ-konformen Businessplan erstellt.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left column: Score and Stats */}
          <div className="lg:col-span-1 space-y-6">
            {/* Final score */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Card variant="accent" padding="lg">
                <div className="text-center">
                  <h3 className="font-semibold text-warm-700 mb-4">
                    Dein GZ-Readiness Score
                  </h3>
                  <ProgressRing
                    progress={gzReadinessScore}
                    size="xl"
                    color="success"
                  />
                  <p className="mt-4 text-sm text-warm-600">
                    Du bist bereit für den Gründungszuschuss!
                  </p>
                </div>
              </Card>
            </motion.div>

            {/* Quick stats */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Card padding="lg">
                <h3 className="font-semibold text-warm-900 mb-4">Workshop-Statistik</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-warm-600">Abgeschlossene Module</span>
                    <span className="font-bold text-warm-900">6/6</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-warm-600">Generierte Kapitel</span>
                    <span className="font-bold text-warm-900">{GENERATED_CHAPTERS.length}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-warm-600">Geschätzte Zeit gespart</span>
                    <span className="font-bold text-green-600">~20 Stunden</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-warm-600">Kosten gespart</span>
                    <span className="font-bold text-green-600">~500€</span>
                  </div>
                </div>
              </Card>
            </motion.div>
          </div>

          {/* Center: Download options */}
          <div className="lg:col-span-2 space-y-6">
            {/* Download cards */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Card variant="elevated" padding="lg">
                <h3 className="font-display font-semibold text-warm-900 mb-6">
                  Deine Dokumente herunterladen
                </h3>

                {!documentsReady ? (
                  <div className="text-center py-8">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                      className="w-12 h-12 mx-auto mb-4"
                    >
                      <RefreshCw size={48} className="text-primary-500" />
                    </motion.div>
                    <p className="text-warm-600">Dokumente werden generiert...</p>
                  </div>
                ) : (
                  <div className="grid sm:grid-cols-3 gap-4">
                    {/* PDF */}
                    <Card variant="interactive" padding="md" hoverable>
                      <div className="text-center">
                        <div className="w-14 h-14 mx-auto mb-3 rounded-xl bg-red-100 flex items-center justify-center">
                          <FileText size={28} className="text-red-600" />
                        </div>
                        <h4 className="font-semibold text-warm-900 mb-1">PDF</h4>
                        <p className="text-xs text-warm-500 mb-3">
                          Professionell formatiert
                        </p>
                        <Button
                          variant="primary"
                          size="sm"
                          fullWidth
                          onClick={() => handleDownload('pdf')}
                          leftIcon={<Download size={16} />}
                        >
                          Download
                        </Button>
                      </div>
                    </Card>

                    {/* DOCX */}
                    <Card variant="interactive" padding="md" hoverable>
                      <div className="text-center">
                        <div className="w-14 h-14 mx-auto mb-3 rounded-xl bg-blue-100 flex items-center justify-center">
                          <File size={28} className="text-blue-600" />
                        </div>
                        <h4 className="font-semibold text-warm-900 mb-1">Word</h4>
                        <p className="text-xs text-warm-500 mb-3">
                          Bearbeitbar
                        </p>
                        <Button
                          variant="primary"
                          size="sm"
                          fullWidth
                          onClick={() => handleDownload('docx')}
                          leftIcon={<Download size={16} />}
                        >
                          Download
                        </Button>
                      </div>
                    </Card>

                    {/* XLSX */}
                    <Card variant="interactive" padding="md" hoverable>
                      <div className="text-center">
                        <div className="w-14 h-14 mx-auto mb-3 rounded-xl bg-green-100 flex items-center justify-center">
                          <Table size={28} className="text-green-600" />
                        </div>
                        <h4 className="font-semibold text-warm-900 mb-1">Excel</h4>
                        <p className="text-xs text-warm-500 mb-3">
                          Finanzplan mit Formeln
                        </p>
                        <Button
                          variant="primary"
                          size="sm"
                          fullWidth
                          onClick={() => handleDownload('xlsx')}
                          leftIcon={<Download size={16} />}
                        >
                          Download
                        </Button>
                      </div>
                    </Card>
                  </div>
                )}

                {/* Download all button */}
                {documentsReady && (
                  <div className="mt-6 pt-6 border-t border-warm-200">
                    <Button
                      variant="accent"
                      fullWidth
                      size="lg"
                      onClick={() => handleDownload('all')}
                      leftIcon={<Download size={20} />}
                    >
                      Alle Dokumente herunterladen (ZIP)
                    </Button>
                  </div>
                )}
              </Card>
            </motion.div>

            {/* Generated chapters overview */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <Card padding="lg">
                <h3 className="font-semibold text-warm-900 mb-4">
                  Generierte Kapitel ({GENERATED_CHAPTERS.length})
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-64 overflow-y-auto">
                  {GENERATED_CHAPTERS.map((chapter, index) => (
                    <motion.div
                      key={chapter.id}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.7 + index * 0.03 }}
                      className="flex items-center gap-2 p-2 bg-green-50 rounded-lg"
                    >
                      <CheckCircle size={14} className="text-green-500 flex-shrink-0" />
                      <span className="text-sm text-warm-700 truncate">
                        {chapter.id}. {chapter.title}
                      </span>
                    </motion.div>
                  ))}
                </div>
              </Card>
            </motion.div>

            {/* Next steps */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
            >
              <Card variant="default" padding="lg" className="bg-gradient-to-br from-primary-50 to-accent-50">
                <h3 className="font-semibold text-warm-900 mb-4">Nächste Schritte</h3>
                <ol className="space-y-3">
                  <li className="flex items-start gap-3">
                    <span className="w-6 h-6 rounded-full bg-primary-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">1</span>
                    <p className="text-warm-700">Lade alle Dokumente herunter und prüfe sie</p>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-6 h-6 rounded-full bg-primary-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">2</span>
                    <p className="text-warm-700">Vereinbare einen Termin bei der fachkundigen Stelle</p>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-6 h-6 rounded-full bg-primary-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">3</span>
                    <p className="text-warm-700">Reiche deinen Antrag beim Arbeitsamt ein</p>
                  </li>
                </ol>
              </Card>
            </motion.div>

            {/* Action buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button
                variant="secondary"
                size="lg"
                leftIcon={<Share2 size={18} />}
                className="flex-1"
              >
                Teilen
              </Button>
              <Button
                variant="ghost"
                size="lg"
                onClick={onRestart}
                className="flex-1"
              >
                Neuen Workshop starten
              </Button>
            </div>
          </div>
        </div>
      </ContentContainer>
    </WorkshopLayout>
  );
};

export default ResultsPage;
