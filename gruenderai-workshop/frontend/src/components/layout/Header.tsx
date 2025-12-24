import { motion } from 'framer-motion';
import { Menu, X, HelpCircle, LogOut, User, Settings } from 'lucide-react';
import { useState } from 'react';
import { ProgressRing } from '@/components/common';
import { useWorkshopStore } from '@/stores/workshopStore';

interface HeaderProps {
  onMenuToggle?: () => void;
  isMenuOpen?: boolean;
}

export const Header = ({ onMenuToggle, isMenuOpen }: HeaderProps) => {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const { gzReadinessScore, currentModule, userContext } = useWorkshopStore();

  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-lg border-b border-warm-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left side: Logo and menu toggle */}
          <div className="flex items-center gap-4">
            {/* Mobile menu toggle */}
            <button
              onClick={onMenuToggle}
              className="lg:hidden p-2 -ml-2 text-warm-600 hover:text-warm-800 hover:bg-warm-100 rounded-lg transition-colors"
              aria-label={isMenuOpen ? 'Menü schließen' : 'Menü öffnen'}
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-elegant">
                <span className="text-white font-display font-bold text-lg">G</span>
              </div>
              <div className="hidden sm:block">
                <h1 className="font-display font-bold text-lg text-warm-900">
                  GründerAI
                </h1>
                <p className="text-xs text-warm-500 -mt-0.5">Workshop</p>
              </div>
            </div>
          </div>

          {/* Center: Progress indicator (desktop) */}
          <div className="hidden md:flex items-center gap-6">
            <div className="flex items-center gap-3">
              <ProgressRing
                progress={gzReadinessScore}
                size="sm"
                showPercentage={false}
                color={gzReadinessScore >= 60 ? 'success' : gzReadinessScore >= 40 ? 'warning' : 'danger'}
              />
              <div>
                <p className="text-sm font-semibold text-warm-800">
                  {gzReadinessScore}% GZ-Ready
                </p>
                <p className="text-xs text-warm-500">
                  Modul {currentModule} von 6
                </p>
              </div>
            </div>
          </div>

          {/* Right side: Actions */}
          <div className="flex items-center gap-2">
            {/* Help button */}
            <button
              className="p-2 text-warm-500 hover:text-warm-700 hover:bg-warm-100 rounded-lg transition-colors"
              aria-label="Hilfe"
            >
              <HelpCircle size={20} />
            </button>

            {/* User menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center gap-2 p-2 hover:bg-warm-100 rounded-lg transition-colors"
              >
                <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                  <User size={16} className="text-primary-600" />
                </div>
                <span className="hidden sm:block text-sm font-medium text-warm-700 max-w-[120px] truncate">
                  {userContext.founderName || 'Gründer:in'}
                </span>
              </button>

              {/* Dropdown menu */}
              {showUserMenu && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setShowUserMenu(false)}
                  />
                  <motion.div
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 10, scale: 0.95 }}
                    className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-elevated border border-warm-100 py-2 z-20"
                  >
                    <div className="px-4 py-2 border-b border-warm-100">
                      <p className="text-sm font-semibold text-warm-900 truncate">
                        {userContext.founderName || 'Gründer:in'}
                      </p>
                      <p className="text-xs text-warm-500 truncate">
                        {userContext.businessName || 'Mein Unternehmen'}
                      </p>
                    </div>

                    <button className="w-full flex items-center gap-3 px-4 py-2 text-sm text-warm-700 hover:bg-warm-50 transition-colors">
                      <Settings size={16} />
                      Einstellungen
                    </button>

                    <button className="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                      <LogOut size={16} />
                      Abmelden
                    </button>
                  </motion.div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Mobile progress bar */}
      <div className="md:hidden px-4 pb-3">
        <div className="flex items-center justify-between text-xs text-warm-500 mb-1">
          <span>Modul {currentModule}/6</span>
          <span>{gzReadinessScore}% GZ-Ready</span>
        </div>
        <div className="w-full h-2 bg-warm-200 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${(currentModule / 6) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>
    </header>
  );
};

export default Header;
