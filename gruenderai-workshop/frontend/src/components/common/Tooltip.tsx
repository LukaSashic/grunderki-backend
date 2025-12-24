import { useState, ReactNode, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

type TooltipPosition = 'top' | 'bottom' | 'left' | 'right';

interface TooltipProps {
  content: ReactNode;
  children: ReactNode;
  position?: TooltipPosition;
  delay?: number;
  disabled?: boolean;
  maxWidth?: number;
}

const POSITIONS = {
  top: {
    tooltip: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    arrow: 'top-full left-1/2 -translate-x-1/2 border-t-warm-900 border-x-transparent border-b-transparent'
  },
  bottom: {
    tooltip: 'top-full left-1/2 -translate-x-1/2 mt-2',
    arrow: 'bottom-full left-1/2 -translate-x-1/2 border-b-warm-900 border-x-transparent border-t-transparent'
  },
  left: {
    tooltip: 'right-full top-1/2 -translate-y-1/2 mr-2',
    arrow: 'left-full top-1/2 -translate-y-1/2 border-l-warm-900 border-y-transparent border-r-transparent'
  },
  right: {
    tooltip: 'left-full top-1/2 -translate-y-1/2 ml-2',
    arrow: 'right-full top-1/2 -translate-y-1/2 border-r-warm-900 border-y-transparent border-l-transparent'
  }
};

const ANIMATION = {
  top: { initial: { opacity: 0, y: 5 }, animate: { opacity: 1, y: 0 } },
  bottom: { initial: { opacity: 0, y: -5 }, animate: { opacity: 1, y: 0 } },
  left: { initial: { opacity: 0, x: 5 }, animate: { opacity: 1, x: 0 } },
  right: { initial: { opacity: 0, x: -5 }, animate: { opacity: 1, x: 0 } }
};

export const Tooltip = ({
  content,
  children,
  position = 'top',
  delay = 200,
  disabled = false,
  maxWidth = 200
}: TooltipProps) => {
  const [isVisible, setIsVisible] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleMouseEnter = () => {
    if (disabled) return;
    timeoutRef.current = setTimeout(() => setIsVisible(true), delay);
  };

  const handleMouseLeave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  };

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const positionStyles = POSITIONS[position];
  const animation = ANIMATION[position];

  return (
    <div
      className="relative inline-block"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      <AnimatePresence>
        {isVisible && !disabled && (
          <motion.div
            className={`absolute z-50 ${positionStyles.tooltip}`}
            initial={animation.initial}
            animate={animation.animate}
            exit={animation.initial}
            transition={{ duration: 0.15 }}
            style={{ maxWidth }}
          >
            <div className="bg-warm-900 text-white text-sm rounded-lg px-3 py-2 shadow-lg">
              {content}
            </div>
            <div className={`absolute border-4 ${positionStyles.arrow}`} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Tooltip;
