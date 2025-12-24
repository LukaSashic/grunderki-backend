/**
 * ChatInput Component
 * Text input with send button for chat messages
 */

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  isLoading?: boolean;
  placeholder?: string;
}

export function ChatInput({
  onSend,
  disabled = false,
  isLoading = false,
  placeholder = 'Schreib hier deine Antwort...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        150
      )}px`;
    }
  }, [message]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (message.trim() && !disabled && !isLoading) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-gray-200 bg-white p-4"
    >
      <div className="flex items-end gap-3 max-w-4xl mx-auto">
        {/* Text Input */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled || isLoading}
            rows={1}
            className={clsx(
              'w-full resize-none rounded-2xl border px-4 py-3 pr-12',
              'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
              'transition-all duration-200',
              'placeholder:text-gray-400',
              disabled || isLoading
                ? 'bg-gray-100 text-gray-500 cursor-not-allowed'
                : 'bg-gray-50 hover:bg-white'
            )}
          />

          {/* Character counter for long messages */}
          {message.length > 200 && (
            <div
              className={clsx(
                'absolute bottom-1 right-14 text-xs',
                message.length > 500 ? 'text-orange-500' : 'text-gray-400'
              )}
            >
              {message.length}/1000
            </div>
          )}
        </div>

        {/* Send Button */}
        <motion.button
          type="submit"
          disabled={!message.trim() || disabled || isLoading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={clsx(
            'flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center',
            'transition-all duration-200',
            message.trim() && !disabled && !isLoading
              ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          )}
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </motion.button>
      </div>

      {/* Helper text */}
      <div className="text-xs text-gray-400 text-center mt-2">
        Enter = senden · Shift+Enter = Zeilenumbruch
      </div>
    </form>
  );
}

export default ChatInput;
