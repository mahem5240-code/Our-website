import { motion } from 'framer-motion'
import { FlaskConical, Clock } from 'lucide-react'
import { colorFor } from '../utils/colors'
import { minutesToLabel, toMinutes } from '../utils/time'

export default function SubjectCard({ entry, subject, isCurrent, isNext, compact = false }) {
  const c = colorFor(subject?.color)
  const isLab = subject?.isLab || entry.type === 'lab'

  return (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ type: 'spring', stiffness: 400, damping: 28 }}
      className={`group relative flex h-full flex-col justify-between rounded-2xl border p-3.5 ${
        isCurrent
          ? `border-transparent ${c.bg} ring-2 ${c.ring}`
          : 'border-line-light bg-white dark:border-line-dark dark:bg-surface-dark'
      } ${compact ? 'min-h-[92px]' : 'min-h-[104px]'}`}
    >
      {isCurrent && (
        <motion.span
          layoutId={`live-${entry.code}-${entry.start}`}
          className="absolute right-3 top-3 flex items-center gap-1 rounded-full bg-black/80 px-2 py-0.5 text-[10px] font-semibold text-white dark:bg-white dark:text-black"
        >
          <span className="h-1.5 w-1.5 animate-pulseSoft rounded-full bg-[#30D158]" />
          Live
        </motion.span>
      )}
      {isNext && !isCurrent && (
        <span className="absolute right-3 top-3 rounded-full bg-black/5 px-2 py-0.5 text-[10px] font-semibold text-muted-light dark:bg-white/10 dark:text-muted-dark">
          Next
        </span>
      )}

      <div>
        <div className="flex items-center gap-1.5">
          <span className={`h-2 w-2 rounded-full ${c.dot}`} />
          {isLab && <FlaskConical size={12} className={c.text} strokeWidth={2.5} />}
          <p className="text-[11px] font-medium uppercase tracking-wide text-muted-light dark:text-muted-dark">
            {entry.code}
          </p>
        </div>
        <p className="mt-1 text-[13.5px] font-semibold leading-snug text-ink-light dark:text-ink-dark">
          {subject?.name || entry.code}
        </p>
      </div>

      <div className="mt-2 flex items-center justify-between">
        <p className="truncate text-[11.5px] text-muted-light dark:text-muted-dark">
          {subject?.faculty}
        </p>
        <div className="flex shrink-0 items-center gap-1 text-[11px] text-muted-light dark:text-muted-dark">
          <Clock size={11} />
          {minutesToLabel(toMinutes(entry.start))}
        </div>
      </div>
    </motion.div>
  )
}

export function BreakCard({ kind, compact }) {
  const isLunch = kind === 'lunch'
  return (
    <div
      className={`flex h-full ${compact ? 'min-h-[46px]' : 'min-h-[104px]'} flex-col items-center justify-center gap-1 rounded-2xl border border-dashed border-line-light bg-black/[0.015] text-center dark:border-line-dark dark:bg-white/[0.02]`}
    >
      <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-light dark:text-muted-dark">
        {isLunch ? '🍽 Lunch' : '☕ Break'}
      </span>
    </div>
  )
}
