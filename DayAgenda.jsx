import { motion } from 'framer-motion'
import SubjectCard, { BreakCard } from './SubjectCard'
import { buildDayRows } from '../utils/buildDayRows'
import { toMinutes } from '../utils/time'
import EmptyState from './EmptyState'

export default function DayAgenda({ year, dayCode, isToday, nowMinutes }) {
  const entries = year.schedule[dayCode] || []
  const rows = buildDayRows(entries)

  if (rows.every((r) => r.kind !== 'entry')) {
    return <EmptyState title="No classes" subtitle="This day is free on the schedule." />
  }

  return (
    <div className="flex flex-col gap-2.5">
      {rows.map((row, idx) => {
        if (row.kind === 'entry') {
          const { entry } = row
          const subject = year.subjects[entry.code]
          const isCurrent = isToday && nowMinutes >= toMinutes(entry.start) && nowMinutes < toMinutes(entry.end)
          const isNext =
            isToday &&
            !isCurrent &&
            nowMinutes < toMinutes(entry.start) &&
            rows
              .filter((r) => r.kind === 'entry' && toMinutes(r.entry.start) > nowMinutes)
              .sort((a, b) => toMinutes(a.entry.start) - toMinutes(b.entry.start))[0]?.entry === entry

          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.03, duration: 0.25 }}
            >
              <SubjectCard entry={entry} subject={subject} isCurrent={isCurrent} isNext={isNext} />
            </motion.div>
          )
        }
        if (row.kind === 'break' || row.kind === 'lunch') {
          return (
            <div key={idx} className="px-1">
              <BreakCard kind={row.kind} compact />
            </div>
          )
        }
        return (
          <div
            key={idx}
            className="flex min-h-[56px] items-center justify-center rounded-2xl border border-dashed border-line-light text-[12px] text-muted-light dark:border-line-dark dark:text-muted-dark"
          >
            Free period
          </div>
        )
      })}
    </div>
  )
}
