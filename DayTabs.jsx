import { motion } from 'framer-motion'
import { DAYS } from '../data/timetableData'

export default function DayTabs({ activeDay, onChange, todayCode }) {
  return (
    <div className="flex gap-1.5 overflow-x-auto pb-1">
      {DAYS.map((day) => {
        const active = activeDay === day
        return (
          <button
            key={day}
            onClick={() => onChange(day)}
            className="focus-ring relative shrink-0 rounded-full px-4 py-2 text-[13px] font-medium transition-colors"
          >
            {active && (
              <motion.div
                layoutId="day-pill"
                className="absolute inset-0 rounded-full bg-ink-light dark:bg-white"
                transition={{ type: 'spring', stiffness: 500, damping: 32 }}
              />
            )}
            <span className={`relative z-10 flex items-center gap-1.5 ${
              active ? 'text-white dark:text-black' : 'text-muted-light dark:text-muted-dark'
            }`}>
              {day}
              {day === todayCode && (
                <span className={`h-1.5 w-1.5 rounded-full ${active ? 'bg-white dark:bg-black' : 'bg-[#0071E3]'}`} />
              )}
            </span>
          </button>
        )
      })}
    </div>
  )
}
