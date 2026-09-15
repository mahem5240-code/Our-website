import { motion, AnimatePresence } from 'framer-motion'
import { ArrowRight, CalendarX2, FlaskConical } from 'lucide-react'
import { colorFor } from '../utils/colors'
import { minutesToLabel, toMinutes } from '../utils/time'

export default function StatusBanner({ dayCode, year, current, next, nowMinutes }) {
  if (!dayCode) {
    return (
      <div className="relative overflow-hidden rounded-3xl border border-line-light bg-white p-6 dark:border-line-dark dark:bg-surface-dark">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-black/5 dark:bg-white/10">
            <CalendarX2 size={20} className="text-muted-light dark:text-muted-dark" />
          </div>
          <div>
            <p className="text-[15px] font-semibold text-ink-light dark:text-ink-dark">No classes today</p>
            <p className="text-[13px] text-muted-light dark:text-muted-dark">Enjoy your Sunday — see you Monday.</p>
          </div>
        </div>
      </div>
    )
  }

  if (!current && !next) {
    return (
      <div className="relative overflow-hidden rounded-3xl border border-line-light bg-white p-6 dark:border-line-dark dark:bg-surface-dark">
        <p className="text-[15px] font-semibold text-ink-light dark:text-ink-dark">Classes are done for today 🎉</p>
        <p className="mt-1 text-[13px] text-muted-light dark:text-muted-dark">Nothing left on {year.label}'s schedule.</p>
      </div>
    )
  }

  const subj = current
    ? year.subjects[current.code]
    : next
    ? year.subjects[next.code]
    : null
  const c = colorFor(subj?.color)

  let progress = 0
  if (current) {
    const s = toMinutes(current.start)
    const e = toMinutes(current.end)
    progress = Math.min(100, Math.max(0, ((nowMinutes - s) / (e - s)) * 100))
  }

  return (
    <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${c.grad} p-6 text-white shadow-soft`}>
      <div className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 rounded-full bg-white/10 blur-2xl" />
      <div className="relative flex items-start justify-between gap-4">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-white/20 px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wide">
              {current ? 'Now' : 'Up next'}
            </span>
            {(subj?.isLab || current?.type === 'lab') && (
              <span className="flex items-center gap-1 rounded-full bg-white/20 px-2 py-0.5 text-[10.5px] font-medium">
                <FlaskConical size={11} /> Lab
              </span>
            )}
          </div>
          <AnimatePresence mode="wait">
            <motion.h2
              key={(current || next)?.code}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              className="mt-2 truncate text-[22px] font-bold leading-tight sm:text-2xl"
            >
              {subj?.name || (current || next)?.code}
            </motion.h2>
          </AnimatePresence>
          <p className="mt-1 text-[13px] text-white/85">{subj?.faculty}</p>
        </div>
        <div className="shrink-0 text-right">
          <p className="text-[13px] font-medium text-white/90">
            {minutesToLabel(toMinutes((current || next).start))} – {minutesToLabel(toMinutes((current || next).end))}
          </p>
          {next && current && (
            <p className="mt-1 flex items-center justify-end gap-1 text-[11.5px] text-white/75">
              Next: {year.subjects[next.code]?.name?.split(' ').slice(0, 2).join(' ') || next.code}
              <ArrowRight size={11} />
            </p>
          )}
        </div>
      </div>

      {current && (
        <div className="relative mt-5 h-1.5 w-full overflow-hidden rounded-full bg-white/20">
          <motion.div
            className="h-full rounded-full bg-white"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          />
        </div>
      )}
    </div>
  )
}
