import { DAYS, PERIODS } from '../data/timetableData'

// "HH:MM" -> minutes since midnight
export const toMinutes = (hhmm) => {
  const [h, m] = hhmm.split(':').map(Number)
  return h * 60 + m
}

export const minutesToLabel = (mins) => {
  const h = Math.floor(mins / 60)
  const m = mins % 60
  const period = h >= 12 ? 'PM' : 'AM'
  const h12 = h % 12 === 0 ? 12 : h % 12
  return `${h12}:${String(m).padStart(2, '0')} ${period}`
}

export const jsDayToCode = (jsDay) => {
  // JS: 0=Sun..6=Sat. Our week: MON..SAT (Sunday = holiday / off)
  const map = { 1: 'MON', 2: 'TUE', 3: 'WED', 4: 'THU', 5: 'FRI', 6: 'SAT' }
  return map[jsDay] || null
}

export const getPeriodMeta = (start, end) => {
  return PERIODS.find((p) => p.start === start && p.end === end)
}

// Given a day's entry list + "now" in minutes, find current & next entry
export function findCurrentAndNext(entries, nowMinutes) {
  let current = null
  let next = null
  const sorted = [...entries].sort((a, b) => toMinutes(a.start) - toMinutes(b.start))
  for (const entry of sorted) {
    const s = toMinutes(entry.start)
    const e = toMinutes(entry.end)
    if (nowMinutes >= s && nowMinutes < e) current = entry
    if (nowMinutes < s && !next) next = entry
  }
  return { current, next }
}

export function isBreakSlot(start, end, nowMinutes) {
  const s = toMinutes(start)
  const e = toMinutes(end)
  return nowMinutes >= s && nowMinutes < e
}

export { DAYS }
