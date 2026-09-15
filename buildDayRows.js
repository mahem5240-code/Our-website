import { PERIODS } from '../data/timetableData'
import { toMinutes } from './time'

// Returns an array of "rows" to render for one day: either a schedule entry
// (possibly spanning several base periods) or a break/lunch/free marker.
export function buildDayRows(entries) {
  const rows = []
  let i = 0
  while (i < PERIODS.length) {
    const period = PERIODS[i]
    const pStart = toMinutes(period.start)

    const entry = entries.find((e) => toMinutes(e.start) === pStart)
    if (entry) {
      rows.push({ kind: 'entry', entry })
      // skip any base periods fully covered by this entry's span
      const eEnd = toMinutes(entry.end)
      let j = i + 1
      while (j < PERIODS.length && toMinutes(PERIODS[j].start) < eEnd) j++
      i = j
      continue
    }

    if (period.kind === 'break' || period.kind === 'lunch') {
      rows.push({ kind: period.kind, period })
      i++
      continue
    }

    // free period — not covered by any entry
    rows.push({ kind: 'free', period })
    i++
  }
  return rows
}
