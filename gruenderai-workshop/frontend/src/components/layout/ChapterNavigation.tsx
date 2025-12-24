import { motion } from 'framer-motion';
import { CheckCircle, Circle, Lock, ChevronRight } from 'lucide-react';
import type { ChapterInfo } from '@/types/workshop.types';

interface ChapterNavigationProps {
  chapters: ChapterInfo[];
  currentChapter: string;
  onChapterSelect: (chapterId: string) => void;
}

export const ChapterNavigation = ({
  chapters,
  currentChapter,
  onChapterSelect
}: ChapterNavigationProps) => {
  return (
    <nav className="chapter-navigation bg-warm-50 rounded-xl p-4 border border-warm-200">
      <h3 className="text-sm font-semibold text-warm-700 mb-3">
        Businessplan Kapitel
      </h3>

      <div className="space-y-1">
        {chapters.map((chapter, index) => {
          const isCurrent = chapter.id === currentChapter;
          const isCompleted = chapter.status === 'completed';
          const isLocked = chapter.status === 'locked';
          const isPending = chapter.status === 'pending';

          return (
            <motion.button
              key={chapter.id}
              onClick={() => !isLocked && onChapterSelect(chapter.id)}
              disabled={isLocked}
              className={`
                w-full flex items-center gap-3 p-2.5 rounded-lg text-left
                transition-all duration-200 group
                ${isCurrent
                  ? 'bg-primary-100 border border-primary-200'
                  : isCompleted
                    ? 'hover:bg-green-50'
                    : isLocked
                      ? 'opacity-50 cursor-not-allowed'
                      : 'hover:bg-warm-100'
                }
              `}
              whileHover={!isLocked ? { x: 4 } : undefined}
            >
              {/* Status icon */}
              <div className={`
                flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center
                ${isCurrent
                  ? 'bg-primary-500 text-white'
                  : isCompleted
                    ? 'bg-green-500 text-white'
                    : 'bg-warm-200 text-warm-400'
                }
              `}>
                {isCompleted ? (
                  <CheckCircle size={14} />
                ) : isLocked ? (
                  <Lock size={12} />
                ) : isCurrent ? (
                  <span className="text-xs font-bold">{index + 1}</span>
                ) : (
                  <Circle size={14} />
                )}
              </div>

              {/* Chapter info */}
              <div className="flex-1 min-w-0">
                <p className={`
                  text-sm font-medium truncate
                  ${isCurrent
                    ? 'text-primary-900'
                    : isCompleted
                      ? 'text-green-800'
                      : 'text-warm-700'
                  }
                `}>
                  {chapter.number} {chapter.title}
                </p>
                {chapter.progress !== undefined && chapter.progress > 0 && !isCompleted && (
                  <div className="mt-1 w-full h-1 bg-warm-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary-400 rounded-full"
                      style={{ width: `${chapter.progress}%` }}
                    />
                  </div>
                )}
              </div>

              {/* Arrow indicator */}
              {isCurrent && (
                <ChevronRight
                  size={16}
                  className="text-primary-400"
                />
              )}
            </motion.button>
          );
        })}
      </div>
    </nav>
  );
};

interface MiniChapterNavProps {
  chapters: ChapterInfo[];
  currentChapter: string;
}

export const MiniChapterNav = ({ chapters, currentChapter }: MiniChapterNavProps) => {
  const currentIndex = chapters.findIndex(c => c.id === currentChapter);
  const totalChapters = chapters.length;
  const completedChapters = chapters.filter(c => c.status === 'completed').length;

  return (
    <div className="flex items-center gap-2">
      {/* Dots */}
      <div className="flex gap-1">
        {chapters.map((chapter, index) => (
          <div
            key={chapter.id}
            className={`
              w-2 h-2 rounded-full transition-all duration-200
              ${chapter.id === currentChapter
                ? 'w-6 bg-primary-500'
                : chapter.status === 'completed'
                  ? 'bg-green-500'
                  : 'bg-warm-300'
              }
            `}
          />
        ))}
      </div>

      {/* Counter */}
      <span className="text-xs text-warm-500">
        {completedChapters}/{totalChapters}
      </span>
    </div>
  );
};

export default ChapterNavigation;
