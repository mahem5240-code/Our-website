import { motion } from 'framer-motion'
import { FlaskConical } from 'lucide-react'
import { DAYS, PERIODS } from '../data/timetableData'
import { colorFor } from '../utils/colors'
import { toMinutes } from '../utils/time'

// Precompute, per day, the row-start / row-span for each schedule entry and
// for the shared break/lunch rows, based on PERIODS order.
function layoutDay(entries) {
  const blocks = []
  let i = 0
  while (i < PERIODS.length) {
    const period = PERIODS[i]
    const pStart = toMinutes(period.start)
    const entry = entries.find((e) => toMinutes(e.start) === pStart)
    if (entry) {
      const eEnd = toMinutes(entry.end)
      let span = 1
      let j = i + 1
      while (j < PERIODS.length && toMinutes(PERIODS[j].start) < eEnd) {
        span++
        j++
      }
      blocks.push({ kind: 'entry', entry, rowStart: i + 2, rowSpan: span })
      i = j
      continue
    }
    if (period.kind === 'break' || period.kind === 'lunch') {
      i++
      continue
    }
    blocks.push({ kind: 'free', rowStart: i + 2, rowSpan: 1 })
    i++
  }
  return blocks
}

export default function WeeklyGrid({ year, todayCode, nowMinutes }) {
  const templateRows = `56px ${PERIODS.map((p) => (p.kind ? '34px' : '96px')).join(' ')}`

  return (
    <div className="overflow-x-auto rounded-3xl border border-line-light bg-white p-2 dark:border-line-dark dark:bg-surface-dark">
      <div
        className="grid min-w-[880px] gap-2"
        style={{
          gridTemplateColumns: `92px repeat(6, minmax(120px, 1fr))`,
          gridTemplateRows: templateRows,
        }}
      >
        {/* Corner */}
        <div className="sticky left-0 z-10 flex items-end pb-2 text-[11px] font-medium text-muted-light dark:text-muted-dark">
          Time
        </div>
        {/* Day headers */}
        {DAYS.map((day) => (
          <div
            key={day}
            className={`flex flex-col items-center justify-center rounded-xl pb-2 text-center ${
              day === todayCode ? 'text-ink-light dark:text-ink-dark' : 'text-muted-light dark:text-muted-dark'
            }`}
          >
            <span className="text-[13px] font-semibold">{day}</span>
            {day === todayCode && <span className="mt-0.5 h-1 w-1 rounded-full bg-[#0071E3]" />}
          </div>
        ))}

        {/* Time labels */}
        {PERIODS.map((p, idx) => (
          <div
            key={p.id}
            style={{ gridRow: idx + 2, gridColumn: 1 }}
            className="sticky left-0 z-10 flex items-center bg-white pr-2 text-[10.5px] leading-tight text-muted-light dark:bg-surface-dark dark:text-muted-dark"
          >
            {p.kind ? (
              <span className="uppercase tracking-wide">{p.kind}</span>
            ) : (
              <span>{p.label.replace(' AM', '').replace(' PM', '')}</span>
            )}
          </div>
        ))}

        {/* Break/Lunch background bands spanning all day columns */}
        {PERIODS.map((p, idx) =>
          p.kind ? (
            <div
              key={`band-${p.id}`}
              style={{ gridRow: idx + 2, gridColumn: '2 / span 6' }}
              className="rounded-lg bg-black/[0.02] dark:bg-white/[0.03]"
            />
          ) : null
        )}

        {/* Day columns */}
        {DAYS.map((day, dIdx) => {
          const blocks = layoutDay(year.schedule[day] || [])
          return blocks.map((block, bIdx) => {
            if (block.kind === 'free') {
              return (
                <div
                  key={`${day}-free-${bIdx}`}
                  style={{ gridRow: block.rowStart, gridColumn: dIdx + 2 }}
                  className="rounded-xl border border-dashed border-line-light/70 dark:border-line-dark/70"
                />
              )
            }
            const { entry } = block
            const subject = year.subjects[entry.code]
            const c = colorFor(subject?.color)
            const isCurrent =
              day === todayCode && nowMinutes >= toMinutes(entry.start) && nowMinutes < toMinutes(entry.end)
            const isLab = subject?.isLab || entry.type === 'lab'

            return (
              <motion.div
                key={`${day}-${bIdx}`}
                whileHover={{ scale: 1.015 }}
                transition={{ type: 'spring', stiffness: 400, damping: 26 }}
                style={{ gridRow: `${block.rowStart} / span ${block.rowSpan}`, gridColumn: dIdx + 2 }}
                className={`group relative flex flex-col justify-between overflow-hidden rounded-xl border p-2 text-left ${
                  isCurrent
                    ? `border-transparent ${c.bg} ring-2 ${c.ring}`
                    : 'border-line-light bg-white dark:border-line-dark dark:bg-[#242426]'
                }`}
              >
                {isCurrent && (
                  <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 animate-pulseSoft rounded-full bg-[#30D158]" />
                )}
                <div className="flex items-center gap-1">
                  <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${c.dot}`} />
                  {isLab && <FlaskConical size={10} className={c.text} />}
                  <p className="truncate text-[11px] font-semibold text-ink-light dark:text-ink-dark">
                    {entry.code}
                  </p>
                </div>
                <p className="truncate text-[10px] text-muted-light dark:text-muted-dark">
                  {subject?.faculty}
                </p>
              </motion.div>
            )
          })
        })}
      </div>
    </div>
  )
}
