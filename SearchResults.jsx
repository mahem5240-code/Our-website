import { motion } from 'framer-motion'
import { FlaskConical } from 'lucide-react'
import { YEARS, YEAR_ORDER, DAY_LABELS } from '../data/timetableData'
import { colorFor } from '../utils/colors'
import { minutesToLabel, toMinutes } from '../utils/time'
import EmptyState from './EmptyState'

export default function SearchResults({ query }) {
  const q = query.trim().toLowerCase()
  const results = []

  YEAR_ORDER.forEach((yid) => {
    const year = YEARS[yid]
    Object.entries(year.schedule).forEach(([day, entries]) => {
      entries.forEach((entry) => {
        const subject = year.subjects[entry.code]
        const haystack = `${entry.code} ${subject?.name || ''} ${subject?.faculty || ''}`.toLowerCase()
        if (haystack.includes(q)) {
          results.push({ year, day, entry, subject })
        }
      })
    })
  })

  if (results.length === 0) {
    return <EmptyState title="No matches" subtitle={`Nothing found for "${query}"`} />
  }

  return (
    <div className="flex flex-col gap-2.5">
      <p className="px-1 text-[12px] font-medium text-muted-light dark:text-muted-dark">
        {results.length} result{results.length !== 1 ? 's' : ''} for &ldquo;{query}&rdquo;
      </p>
      {results.map((r, idx) => {
        const c = colorFor(r.subject?.color)
        const isLab = r.subject?.isLab || r.entry.type === 'lab'
        return (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.02 }}
            className="flex items-center gap-3 rounded-2xl border border-line-light bg-white p-3.5 dark:border-line-dark dark:bg-surface-dark"
          >
            <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${c.bg}`}>
              {isLab ? <FlaskConical size={15} className={c.text} /> : <span className={`h-2 w-2 rounded-full ${c.dot}`} />}
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-[13.5px] font-semibold text-ink-light dark:text-ink-dark">
                {r.subject?.name || r.entry.code}
              </p>
              <p className="truncate text-[11.5px] text-muted-light dark:text-muted-dark">
                {r.subject?.faculty} · {r.year.label}
              </p>
            </div>
            <div className="shrink-0 text-right">
              <p className="text-[12px] font-medium text-ink-light dark:text-ink-dark">{DAY_LABELS[r.day]}</p>
              <p className="text-[11px] text-muted-light dark:text-muted-dark">
                {minutesToLabel(toMinutes(r.entry.start))}
              </p>
            </div>
          </motion.div>
        )
      })}
    </div>
  )
}
