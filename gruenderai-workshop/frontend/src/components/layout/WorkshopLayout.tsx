import { useState, ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface WorkshopLayoutProps {
  children: ReactNode;
  showSidebar?: boolean;
}

export const WorkshopLayout = ({ children, showSidebar = true }: WorkshopLayoutProps) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-warm-50 to-warm-100">
      {/* Header */}
      <Header
        onMenuToggle={() => setIsSidebarOpen(!isSidebarOpen)}
        isMenuOpen={isSidebarOpen}
      />

      <div className="flex">
        {/* Sidebar */}
        {showSidebar && (
          <Sidebar
            isOpen={isSidebarOpen}
            onClose={() => setIsSidebarOpen(false)}
          />
        )}

        {/* Main content */}
        <main className={`
          flex-1 min-h-[calc(100vh-4rem)]
          ${showSidebar ? 'lg:ml-0' : ''}
        `}>
          <AnimatePresence mode="wait">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="h-full"
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
};

interface ContentContainerProps {
  children: ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const MAX_WIDTHS = {
  sm: 'max-w-screen-sm',
  md: 'max-w-screen-md',
  lg: 'max-w-screen-lg',
  xl: 'max-w-screen-xl',
  '2xl': 'max-w-screen-2xl',
  full: 'max-w-full'
};

const PADDINGS = {
  none: '',
  sm: 'px-4 py-4',
  md: 'px-4 sm:px-6 lg:px-8 py-6',
  lg: 'px-4 sm:px-6 lg:px-8 py-8'
};

export const ContentContainer = ({
  children,
  maxWidth = 'lg',
  padding = 'md'
}: ContentContainerProps) => {
  return (
    <div className={`${MAX_WIDTHS[maxWidth]} mx-auto ${PADDINGS[padding]}`}>
      {children}
    </div>
  );
};

interface TwoColumnLayoutProps {
  leftColumn: ReactNode;
  rightColumn: ReactNode;
  leftWidth?: '1/3' | '1/2' | '2/3';
  gap?: 'sm' | 'md' | 'lg';
  stackOnMobile?: boolean;
}

const LEFT_WIDTHS = {
  '1/3': 'lg:w-1/3',
  '1/2': 'lg:w-1/2',
  '2/3': 'lg:w-2/3'
};

const RIGHT_WIDTHS = {
  '1/3': 'lg:w-2/3',
  '1/2': 'lg:w-1/2',
  '2/3': 'lg:w-1/3'
};

const GAPS = {
  sm: 'gap-4',
  md: 'gap-6',
  lg: 'gap-8'
};

export const TwoColumnLayout = ({
  leftColumn,
  rightColumn,
  leftWidth = '2/3',
  gap = 'md',
  stackOnMobile = true
}: TwoColumnLayoutProps) => {
  return (
    <div className={`flex ${stackOnMobile ? 'flex-col lg:flex-row' : 'flex-row'} ${GAPS[gap]}`}>
      <div className={`w-full ${LEFT_WIDTHS[leftWidth]}`}>
        {leftColumn}
      </div>
      <div className={`w-full ${RIGHT_WIDTHS[leftWidth]}`}>
        {rightColumn}
      </div>
    </div>
  );
};

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  badge?: ReactNode;
  actions?: ReactNode;
  backLink?: {
    label: string;
    onClick: () => void;
  };
}

export const PageHeader = ({
  title,
  subtitle,
  badge,
  actions,
  backLink
}: PageHeaderProps) => {
  return (
    <div className="mb-8">
      {backLink && (
        <button
          onClick={backLink.onClick}
          className="flex items-center gap-1 text-sm text-warm-500 hover:text-warm-700 mb-4 transition-colors"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M10 12l-4-4 4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" fill="none" />
          </svg>
          {backLink.label}
        </button>
      )}

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl sm:text-3xl font-display font-bold text-warm-900">
              {title}
            </h1>
            {badge}
          </div>
          {subtitle && (
            <p className="mt-2 text-warm-600">
              {subtitle}
            </p>
          )}
        </div>

        {actions && (
          <div className="flex items-center gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkshopLayout;
