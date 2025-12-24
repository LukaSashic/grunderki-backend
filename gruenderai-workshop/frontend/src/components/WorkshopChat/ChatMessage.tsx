/**
 * ChatMessage Component
 * Renders a single chat message with typing animation for assistant
 * Supports card-based questions via UI hints
 */

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { User, Bot, Loader2 } from 'lucide-react';
import { clsx } from 'clsx';
import type { LocalMessage } from '@/stores/workshopChatStore';
import { CardSelection, type CardOption } from './CardSelection';
import { CustomInputModal } from './CustomInputModal';

interface ChatMessageProps {
  message: LocalMessage;
  /** Callback when a card is selected or custom input is submitted */
  onCardSelect?: (value: string) => void;
  /** Whether card selection is disabled (e.g., when loading) */
  disabled?: boolean;
  /** Whether this is the last message (to show card selection) */
  isLastMessage?: boolean;
}

export function ChatMessage({
  message,
  onCardSelect,
  disabled = false,
  isLastMessage = false,
}: ChatMessageProps) {
  const isUser = message.role === 'user';
  const isLoading = message.isLoading;
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [selectedCard, setSelectedCard] = useState<string | null>(null);

  // Check if this message has card options to display
  const hasCardOptions =
    !isUser &&
    isLastMessage &&
    message.uiHint?.type === 'cards' &&
    message.uiHint.options &&
    message.uiHint.options.length > 0;

  // Handle card selection
  const handleCardSelect = useCallback(
    (option: CardOption) => {
      setSelectedCard(option.id);
      if (onCardSelect) {
        onCardSelect(option.label);
      }
    },
    [onCardSelect]
  );

  // Handle custom input submission
  const handleCustomSubmit = useCallback(
    (value: string) => {
      setShowCustomInput(false);
      if (onCardSelect) {
        onCardSelect(value);
      }
    },
    [onCardSelect]
  );

  // Render formatted message content
  const renderContent = () => {
    return message.content.split('\n').map((line, idx) => {
      // Bold text
      const formattedLine = line.replace(
        /\*\*(.*?)\*\*/g,
        '<strong>$1</strong>'
      );

      // Bullet points
      if (line.trim().startsWith('- ')) {
        return (
          <div key={idx} className="flex gap-2 ml-2">
            <span className="text-emerald-500">•</span>
            <span
              dangerouslySetInnerHTML={{
                __html: formattedLine.replace(/^- /, ''),
              }}
            />
          </div>
        );
      }

      // Numbered lists
      if (/^\d+\.\s/.test(line.trim())) {
        return (
          <div key={idx} className="ml-2">
            <span dangerouslySetInnerHTML={{ __html: formattedLine }} />
          </div>
        );
      }

      // Regular paragraph
      return line.trim() ? (
        <p
          key={idx}
          className="mb-2 last:mb-0"
          dangerouslySetInnerHTML={{ __html: formattedLine }}
        />
      ) : (
        <br key={idx} />
      );
    });
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className={clsx(
          'flex gap-3 p-4',
          isUser ? 'flex-row-reverse' : 'flex-row'
        )}
      >
        {/* Avatar */}
        <div
          className={clsx(
            'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center',
            isUser
              ? 'bg-blue-600 text-white'
              : 'bg-gradient-to-br from-emerald-500 to-teal-600 text-white'
          )}
        >
          {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
        </div>

        {/* Message Bubble */}
        <div
          className={clsx(
            'rounded-2xl px-4 py-3',
            isUser
              ? 'max-w-[80%] bg-blue-600 text-white rounded-tr-sm'
              : hasCardOptions
              ? 'max-w-[90%] bg-white shadow-md border border-gray-100 rounded-tl-sm'
              : 'max-w-[80%] bg-white shadow-md border border-gray-100 rounded-tl-sm'
          )}
        >
          {isLoading ? (
            <div className="flex items-center gap-2 text-gray-500">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm">Schreibt...</span>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Message Text */}
              <div
                className={clsx(
                  'prose prose-sm max-w-none',
                  isUser ? 'prose-invert' : 'prose-gray'
                )}
              >
                {renderContent()}
              </div>

              {/* Card Selection (only for last assistant message with cards) */}
              {hasCardOptions && !selectedCard && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2, duration: 0.3 }}
                  className="mt-4 pt-4 border-t border-gray-100"
                >
                  <CardSelection
                    question={message.uiHint?.question || ''}
                    options={message.uiHint?.options || []}
                    onSelect={handleCardSelect}
                    onCustomInput={() => setShowCustomInput(true)}
                    disabled={disabled}
                    hint={message.uiHint?.hint}
                    multiSelect={message.uiHint?.multiSelect}
                    showOtherOption={true}
                  />
                </motion.div>
              )}

              {/* Show selected card confirmation */}
              {hasCardOptions && selectedCard && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-4 pt-4 border-t border-gray-100"
                >
                  <div className="flex items-center gap-2 text-sm text-emerald-600">
                    <span className="w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center">
                      ✓
                    </span>
                    <span>Auswahl getroffen</span>
                  </div>
                </motion.div>
              )}
            </div>
          )}

          {/* Timestamp */}
          <div
            className={clsx(
              'text-xs mt-2 opacity-60',
              isUser ? 'text-blue-100' : 'text-gray-400'
            )}
          >
            {message.timestamp.toLocaleTimeString('de-DE', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        </div>
      </motion.div>

      {/* Custom Input Modal */}
      {hasCardOptions && (
        <CustomInputModal
          isOpen={showCustomInput}
          onClose={() => setShowCustomInput(false)}
          onSubmit={handleCustomSubmit}
          title={message.uiHint?.question || 'Ihre Antwort'}
          placeholder={message.uiHint?.placeholder}
          hint={message.uiHint?.hint}
          examples={message.uiHint?.examples}
          maxLength={message.uiHint?.maxLength}
          minLength={message.uiHint?.minLength}
          isLoading={disabled}
        />
      )}
    </>
  );
}

export default ChatMessage;
