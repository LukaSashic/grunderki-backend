import { useState, ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { Card } from './Card';

interface ExpandableCardProps {
  title: string;
  subtitle?: string;
  icon?: ReactNode;
  children: ReactNode;
  defaultExpanded?: boolean;
  badge?: ReactNode;
  variant?: 'default' | 'elevated' | 'accent';
  onToggle?: (expanded: boolean) => void;
}

export const ExpandableCard = ({
  title,
  subtitle,
  icon,
  children,
  defaultExpanded = false,
  badge,
  variant = 'default',
  onToggle
}: ExpandableCardProps) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  const handleToggle = () => {
    const newState = !isExpanded;
    setIsExpanded(newState);
    onToggle?.(newState);
  };

  return (
    <Card variant={variant} padding="none">
      <button
        onClick={handleToggle}
        className="w-full p-4 flex items-center gap-3 text-left hover:bg-warm-50 transition-colors rounded-t-2xl focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
        aria-expanded={isExpanded}
      >
        {/* Icon */}
        {icon && (
          <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary-100 flex items-center justify-center text-primary-600">
            {icon}
          </div>
        )}

        {/* Title and subtitle */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-warm-900 truncate">{title}</h3>
            {badge}
          </div>
          {subtitle && (
            <p className="text-sm text-warm-500 truncate mt-0.5">{subtitle}</p>
          )}
        </div>

        {/* Expand icon */}
        <motion.div
          animate={{ rotate: isExpanded ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="flex-shrink-0 text-warm-400"
        >
          <ChevronDown size={20} />
        </motion.div>
      </button>

      {/* Expandable content */}
      <AnimatePresence initial={false}>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            <div className="p-4 pt-0 border-t border-warm-100">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  );
};

interface AccordionProps {
  items: {
    id: string;
    title: string;
    subtitle?: string;
    icon?: ReactNode;
    content: ReactNode;
    badge?: ReactNode;
  }[];
  allowMultiple?: boolean;
  defaultExpanded?: string[];
}

export const Accordion = ({
  items,
  allowMultiple = false,
  defaultExpanded = []
}: AccordionProps) => {
  const [expandedItems, setExpandedItems] = useState<string[]>(defaultExpanded);

  const handleToggle = (id: string) => {
    if (allowMultiple) {
      setExpandedItems(prev =>
        prev.includes(id)
          ? prev.filter(item => item !== id)
          : [...prev, id]
      );
    } else {
      setExpandedItems(prev =>
        prev.includes(id) ? [] : [id]
      );
    }
  };

  return (
    <div className="space-y-3">
      {items.map(item => (
        <Card key={item.id} variant="default" padding="none">
          <button
            onClick={() => handleToggle(item.id)}
            className="w-full p-4 flex items-center gap-3 text-left hover:bg-warm-50 transition-colors rounded-2xl focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            aria-expanded={expandedItems.includes(item.id)}
          >
            {item.icon && (
              <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary-100 flex items-center justify-center text-primary-600">
                {item.icon}
              </div>
            )}

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-warm-900">{item.title}</h3>
                {item.badge}
              </div>
              {item.subtitle && (
                <p className="text-sm text-warm-500 mt-0.5">{item.subtitle}</p>
              )}
            </div>

            <motion.div
              animate={{ rotate: expandedItems.includes(item.id) ? 90 : 0 }}
              transition={{ duration: 0.2 }}
              className="flex-shrink-0 text-warm-400"
            >
              <ChevronRight size={20} />
            </motion.div>
          </button>

          <AnimatePresence initial={false}>
            {expandedItems.includes(item.id) && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
                className="overflow-hidden"
              >
                <div className="p-4 pt-0 border-t border-warm-100">
                  {item.content}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      ))}
    </div>
  );
};

export default ExpandableCard;
