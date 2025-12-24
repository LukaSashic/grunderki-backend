import { motion, AnimatePresence } from 'framer-motion';
import {
  Lightbulb,
  Users,
  TrendingUp,
  Megaphone,
  Calculator,
  Target,
  CheckCircle,
  Lock,
  Play,
  ChevronRight
} from 'lucide-react';
import { useWorkshopStore } from '@/stores/workshopStore';
import { ProgressRing, QualityGauge } from '@/components/common';
import type { ModuleNumber } from '@/types/workshop.types';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const MODULE_INFO = [
  {
    number: 1 as ModuleNumber,
    title: 'Geschäftsidee',
    subtitle: 'Gründerprofil',
    icon: Lightbulb,
    color: 'primary'
  },
  {
    number: 2 as ModuleNumber,
    title: 'Zielgruppe',
    subtitle: 'Personas',
    icon: Users,
    color: 'blue'
  },
  {
    number: 3 as ModuleNumber,
    title: 'Markt',
    subtitle: 'Wettbewerb',
    icon: TrendingUp,
    color: 'green'
  },
  {
    number: 4 as ModuleNumber,
    title: 'Marketing',
    subtitle: 'Vertrieb',
    icon: Megaphone,
    color: 'purple'
  },
  {
    number: 5 as ModuleNumber,
    title: 'Finanzen',
    subtitle: 'Finanzplan',
    icon: Calculator,
    color: 'amber'
  },
  {
    number: 6 as ModuleNumber,
    title: 'Strategie',
    subtitle: 'Abschluss',
    icon: Target,
    color: 'red'
  }
];

const getModuleStatus = (
  moduleNumber: ModuleNumber,
  currentModule: ModuleNumber,
  progress: number
) => {
  if (moduleNumber < currentModule) return 'completed';
  if (moduleNumber === currentModule) return 'active';
  return 'locked';
};

export const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  const { currentModule, moduleProgress, gzReadinessScore, userContext } = useWorkshopStore();

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-warm-900/50 z-40 lg:hidden"
            onClick={onClose}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -300 }}
        animate={{ x: isOpen ? 0 : -300 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-80 bg-white border-r border-warm-200
          flex flex-col
          lg:translate-x-0
        `}
      >
        {/* Business info */}
        <div className="p-6 border-b border-warm-100">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-400 to-accent-600 flex items-center justify-center shadow-gold-glow">
              <span className="text-white font-display font-bold text-xl">
                {userContext.businessName?.[0] || 'B'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="font-display font-semibold text-warm-900 truncate">
                {userContext.businessName || 'Mein Business'}
              </h2>
              <p className="text-sm text-warm-500 truncate">
                {userContext.businessType || 'Branche wählen'}
              </p>
            </div>
          </div>

          {/* GZ Readiness Score */}
          <div className="bg-gradient-to-br from-primary-50 to-accent-50 rounded-xl p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-warm-700">
                GZ-Readiness
              </span>
              <span className="text-sm font-bold text-primary-600">
                {gzReadinessScore}%
              </span>
            </div>
            <QualityGauge
              score={gzReadinessScore}
              size="sm"
              showIcon={false}
            />
          </div>
        </div>

        {/* Module navigation */}
        <nav className="flex-1 overflow-y-auto p-4">
          <div className="space-y-2">
            {MODULE_INFO.map((module) => {
              const status = getModuleStatus(
                module.number,
                currentModule,
                moduleProgress[module.number]
              );
              const Icon = module.icon;
              const progress = moduleProgress[module.number];

              return (
                <motion.button
                  key={module.number}
                  className={`
                    w-full flex items-center gap-3 p-3 rounded-xl text-left
                    transition-all duration-200 group
                    ${status === 'active'
                      ? 'bg-primary-50 border-2 border-primary-200 shadow-card'
                      : status === 'completed'
                        ? 'bg-green-50 hover:bg-green-100 border border-green-200'
                        : 'bg-warm-50 border border-warm-200 opacity-60 cursor-not-allowed'
                    }
                  `}
                  disabled={status === 'locked'}
                  whileHover={status !== 'locked' ? { scale: 1.02 } : undefined}
                  whileTap={status !== 'locked' ? { scale: 0.98 } : undefined}
                >
                  {/* Status indicator */}
                  <div className={`
                    w-10 h-10 rounded-xl flex items-center justify-center
                    transition-all duration-200
                    ${status === 'active'
                      ? 'bg-primary-500 text-white shadow-elegant'
                      : status === 'completed'
                        ? 'bg-green-500 text-white'
                        : 'bg-warm-200 text-warm-400'
                    }
                  `}>
                    {status === 'completed' ? (
                      <CheckCircle size={20} />
                    ) : status === 'locked' ? (
                      <Lock size={18} />
                    ) : status === 'active' ? (
                      <Play size={18} />
                    ) : (
                      <Icon size={20} />
                    )}
                  </div>

                  {/* Module info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={`
                        text-xs font-medium px-1.5 py-0.5 rounded
                        ${status === 'active'
                          ? 'bg-primary-100 text-primary-700'
                          : status === 'completed'
                            ? 'bg-green-100 text-green-700'
                            : 'bg-warm-200 text-warm-500'
                        }
                      `}>
                        {module.number}
                      </span>
                      <span className={`
                        font-semibold truncate
                        ${status === 'active'
                          ? 'text-primary-900'
                          : status === 'completed'
                            ? 'text-green-900'
                            : 'text-warm-500'
                        }
                      `}>
                        {module.title}
                      </span>
                    </div>
                    <p className={`
                      text-xs truncate mt-0.5
                      ${status === 'active' ? 'text-primary-600' : 'text-warm-400'}
                    `}>
                      {module.subtitle}
                    </p>

                    {/* Progress bar for active module */}
                    {status === 'active' && progress > 0 && (
                      <div className="mt-2 w-full h-1.5 bg-primary-200 rounded-full overflow-hidden">
                        <motion.div
                          className="h-full bg-primary-500 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${progress}%` }}
                        />
                      </div>
                    )}
                  </div>

                  {/* Arrow for active */}
                  {status === 'active' && (
                    <ChevronRight
                      size={20}
                      className="text-primary-400 group-hover:text-primary-600 transition-colors"
                    />
                  )}
                </motion.button>
              );
            })}
          </div>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-warm-100">
          <div className="text-center">
            <p className="text-xs text-warm-500">
              Powered by
            </p>
            <p className="text-sm font-semibold text-primary-600">
              GründerAI Workshop
            </p>
          </div>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;
