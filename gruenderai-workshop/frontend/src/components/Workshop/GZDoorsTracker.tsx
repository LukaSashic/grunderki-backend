/**
 * GründerAI Workshop - GZ Doors Tracker Component
 * Visual tracker for the 7 critical BA GZ 04 questions
 * Shows status of each "door" that must be passed for GZ approval
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Lock, CheckCircle, AlertTriangle, Loader, Info } from 'lucide-react';
import type { GZDoor, GZDoorStatus } from '@/types/module1.types';

interface GZDoorsTrackerProps {
  doors: GZDoor[];
  variant?: 'header' | 'sidebar' | 'full';
  onDoorClick?: (doorId: string) => void;
}

export const GZDoorsTracker: React.FC<GZDoorsTrackerProps> = ({
  doors,
  variant = 'header',
  onDoorClick
}) => {
  const [hoveredDoor, setHoveredDoor] = useState<string | null>(null);

  const passedCount = doors.filter(d => d.status === 'passed').length;
  const totalCount = doors.length;

  const getDoorStyle = (status: GZDoorStatus) => {
    switch (status) {
      case 'passed':
        return {
          bgClass: 'bg-green-500',
          textClass: 'text-white',
          icon: CheckCircle,
          label: '✓'
        };
      case 'checking':
        return {
          bgClass: 'bg-blue-500 animate-pulse',
          textClass: 'text-white',
          icon: Loader,
          label: '...'
        };
      case 'failed':
        return {
          bgClass: 'bg-red-500',
          textClass: 'text-white',
          icon: AlertTriangle,
          label: '!'
        };
      default:
        return {
          bgClass: 'bg-warm-200',
          textClass: 'text-warm-500',
          icon: Lock,
          label: ''
        };
    }
  };

  // Header variant - compact horizontal display
  if (variant === 'header') {
    return (
      <div className="gz-doors-tracker flex items-center gap-2 px-4 py-2 bg-warm-50 rounded-full border border-warm-200">
        <span className="text-xs text-warm-500 font-medium mr-1">GZ-Status:</span>

        <div className="flex items-center gap-1">
          {doors.map((door) => {
            const style = getDoorStyle(door.status);

            return (
              <div
                key={door.id}
                className="relative"
                onMouseEnter={() => setHoveredDoor(door.id)}
                onMouseLeave={() => setHoveredDoor(null)}
              >
                <motion.button
                  onClick={() => onDoorClick?.(door.id)}
                  className={`
                    w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold
                    transition-all duration-300 ${style.bgClass} ${style.textClass}
                    hover:scale-110 hover:shadow-md
                  `}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {door.status === 'locked' ? door.baQuestion : style.label}
                </motion.button>

                {/* Tooltip on Hover */}
                {hoveredDoor === door.id && (
                  <motion.div
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="absolute top-full left-1/2 -translate-x-1/2 mt-2 z-50"
                  >
                    <div className="bg-warm-900 text-white rounded-lg px-3 py-2 text-xs max-w-xs whitespace-nowrap shadow-lg">
                      <p className="font-medium mb-1">Frage {door.baQuestion}: {door.title}</p>
                      <p className="text-warm-300 text-[10px]">Modul {door.moduleId}</p>
                      {/* Arrow */}
                      <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-warm-900 transform rotate-45" />
                    </div>
                  </motion.div>
                )}
              </div>
            );
          })}
        </div>

        <span className="text-xs text-warm-500 ml-1">
          {passedCount}/{totalCount}
        </span>
      </div>
    );
  }

  // Sidebar variant - vertical list with more detail
  if (variant === 'sidebar') {
    return (
      <div className="gz-doors-tracker bg-white rounded-xl border border-warm-200 p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-medium text-warm-900">GZ-Türen</h3>
          <span className={`text-sm font-bold ${
            passedCount === totalCount ? 'text-green-600' :
            passedCount > 0 ? 'text-primary-600' : 'text-warm-400'
          }`}>
            {passedCount}/{totalCount}
          </span>
        </div>

        <div className="space-y-2">
          {doors.map((door) => {
            const style = getDoorStyle(door.status);
            const Icon = style.icon;

            return (
              <button
                key={door.id}
                onClick={() => onDoorClick?.(door.id)}
                className={`
                  w-full flex items-center gap-3 p-2 rounded-lg transition-all
                  ${door.status === 'passed' ? 'bg-green-50' :
                    door.status === 'checking' ? 'bg-blue-50' :
                    door.status === 'failed' ? 'bg-red-50' :
                    'bg-warm-50'}
                  hover:shadow-sm
                `}
              >
                <div className={`
                  w-8 h-8 rounded-lg flex items-center justify-center
                  ${style.bgClass} ${style.textClass}
                `}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="flex-1 text-left">
                  <p className="text-sm font-medium text-warm-800">
                    Frage {door.baQuestion}
                  </p>
                  <p className="text-xs text-warm-500">{door.title}</p>
                </div>
              </button>
            );
          })}
        </div>

        <div className="mt-4 pt-4 border-t border-warm-200">
          <p className="text-xs text-warm-500 text-center">
            Alle 7 Türen müssen "grün" sein für GZ-Bewilligung
          </p>
        </div>
      </div>
    );
  }

  // Full variant - detailed view with tips
  return (
    <div className="gz-doors-tracker">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-display text-lg font-semibold text-warm-900">
          Die 7 GZ-Türen
        </h3>
        <div className="flex items-center gap-2">
          <div className="w-full h-2 bg-warm-200 rounded-full w-24 overflow-hidden">
            <motion.div
              className="h-full bg-green-500 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${(passedCount / totalCount) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <span className="text-sm font-bold text-warm-700">
            {passedCount}/{totalCount}
          </span>
        </div>
      </div>

      <p className="text-sm text-warm-600 mb-6">
        Jede "Tür" entspricht einer kritischen Frage im Gründungszuschuss-Antrag.
        Die fachkundige Stelle prüft alle 7 Punkte. Alle müssen bestanden werden.
      </p>

      <div className="grid gap-4">
        {doors.map((door) => {
          const style = getDoorStyle(door.status);
          const Icon = style.icon;

          return (
            <motion.div
              key={door.id}
              className={`
                rounded-xl border-2 p-4 transition-all
                ${door.status === 'passed' ? 'border-green-300 bg-green-50' :
                  door.status === 'checking' ? 'border-blue-300 bg-blue-50' :
                  door.status === 'failed' ? 'border-red-300 bg-red-50' :
                  'border-warm-200 bg-warm-50'}
              `}
              layout
            >
              <div className="flex items-start gap-4">
                <div className={`
                  w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0
                  ${style.bgClass} ${style.textClass}
                `}>
                  <Icon className="w-6 h-6" />
                </div>

                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-sm font-bold text-warm-500">
                      Frage {door.baQuestion}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      door.status === 'passed' ? 'bg-green-200 text-green-800' :
                      door.status === 'checking' ? 'bg-blue-200 text-blue-800' :
                      door.status === 'failed' ? 'bg-red-200 text-red-800' :
                      'bg-warm-200 text-warm-600'
                    }`}>
                      Modul {door.moduleId}
                    </span>
                  </div>

                  <h4 className="font-medium text-warm-900 mb-2">{door.title}</h4>

                  <p className="text-sm text-warm-600 mb-3">{door.fullQuestion}</p>

                  {/* Tips - show for non-passed doors */}
                  {door.status !== 'passed' && door.tips.length > 0 && (
                    <div className="bg-white/50 rounded-lg p-3">
                      <div className="flex items-center gap-1 text-xs font-medium text-warm-700 mb-2">
                        <Info className="w-3 h-3" />
                        <span>Tipps zum Bestehen:</span>
                      </div>
                      <ul className="space-y-1">
                        {door.tips.map((tip, i) => (
                          <li key={i} className="text-xs text-warm-600 flex items-start gap-2">
                            <span className="text-primary-500">→</span>
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

// =============================================================================
// MINI VERSION FOR INLINE USE
// =============================================================================

interface GZDoorMiniProps {
  status: GZDoorStatus;
  questionNumber: number;
  title?: string;
}

export const GZDoorMini: React.FC<GZDoorMiniProps> = ({
  status,
  questionNumber,
  title
}) => {
  const style = (() => {
    switch (status) {
      case 'passed':
        return { bg: 'bg-green-500', text: 'text-white', label: '✓' };
      case 'checking':
        return { bg: 'bg-blue-500', text: 'text-white', label: '...' };
      case 'failed':
        return { bg: 'bg-red-500', text: 'text-white', label: '!' };
      default:
        return { bg: 'bg-warm-200', text: 'text-warm-500', label: String(questionNumber) };
    }
  })();

  return (
    <div className="inline-flex items-center gap-1.5">
      <div className={`
        w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold
        ${style.bg} ${style.text}
      `}>
        {status === 'locked' ? questionNumber : style.label}
      </div>
      {title && <span className="text-xs text-warm-600">{title}</span>}
    </div>
  );
};

export default GZDoorsTracker;
