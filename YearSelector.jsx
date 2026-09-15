import { motion } from 'framer-motion'
import { YEARS, YEAR_ORDER } from '../data/timetableData'

export default function YearSelector({ activeYear, onChange }) {
  return (
    <div
      role="tablist"
      aria-label="Select year"
      className="relative flex w-full max-w-md gap-1 rounded-2xl bg-black/5 p-1 dark:bg-white/[0.06]"
    >
      {YEAR_ORDER.map((yid) => {
        const year = YEARS[yid]
        const active = activeYear === yid
        return (
          <button
            key={yid}
            role="tab"
            aria-selected={active}
            onClick={() => onChange(yid)}
            className="focus-ring relative flex-1 rounded-xl px-3 py-2 text-sm font-medium transition-colors"
          >
            {active && (
              <motion.div
                layoutId="year-pill"
                className="absolute inset-0 rounded-xl bg-white shadow-soft dark:bg-[#3A3A3C]"
                transition={{ type: 'spring', stiffness: 500, damping: 32 }}
              />
            )}
            <span
              className={`relative z-10 ${
                active
                  ? 'text-ink-light dark:text-ink-dark'
                  : 'text-muted-light dark:text-muted-dark'
              }`}
            >
              {year.label}
            </span>
          </button>
        )
      })}
    </div>
  )
}
