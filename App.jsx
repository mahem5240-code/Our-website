import { useEffect, useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { CalendarRange, LayoutGrid, Sun } from 'lucide-react'
import { YEARS, YEAR_ORDER } from './data/timetableData'
import { findCurrentAndNext, jsDayToCode, toMinutes } from './utils/time'
import useNow from './hooks/useNow'

import Header from './components/Header'
import YearSelector from './components/YearSelector'
import DayTabs from './components/DayTabs'
import StatusBanner from './components/StatusBanner'
import StatsRow from './components/StatsRow'
import DayAgenda from './components/DayAgenda'
import WeeklyGrid from './components/WeeklyGrid'
import SearchResults from './components/SearchResults'
import ErrorBoundary, { InlineError } from './components/ErrorState'
import { BannerSkeleton, AgendaSkeleton } from './components/Skeletons'

const VIEWS = [
  { id: 'today', label: 'Today', icon: Sun },
  { id: 'day', label: 'Day', icon: CalendarRange },
  { id: 'week', label: 'Week', icon: LayoutGrid },
]

function AppInner() {
  const now = useNow()
  const [activeYear, setActiveYear] = useState('y2')
  const [view, setView] = useState('today')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [failed, setFailed] = useState(false)

  const todayCode = jsDayToCode(now.getDay())
  const [activeDay, setActiveDay] = useState(todayCode || 'MON')

  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 650)
    return () => clearTimeout(t)
  }, [])

  useEffect(() => {
    if (todayCode) setActiveDay(todayCode)
  }, [todayCode])

  const year = YEARS[activeYear]
  const nowMinutes = now.getHours() * 60 + now.getMinutes()

  const { current, next } = useMemo(() => {
    if (!todayCode) return { current: null, next: null }
    const entries = year.schedule[todayCode] || []
    return findCurrentAndNext(entries, nowMinutes)
  }, [year, todayCode, nowMinutes])

  const isSearching = search.trim().length > 0

  const retry = () => {
    setFailed(false)
    setLoading(true)
    setTimeout(() => setLoading(false), 500)
  }

  return (
    <div className="min-h-screen bg-canvas-light text-ink-light dark:bg-canvas-dark dark:text-ink-dark">
      <Header search={search} onSearch={setSearch} />

      <main className="mx-auto max-w-6xl px-4 pb-24 pt-6 sm:px-6">
        <AnimatePresence mode="wait">
          {isSearching ? (
            <motion.div
              key="search"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.2 }}
            >
              <SearchResults query={search} />
            </motion.div>
          ) : (
            <motion.div
              key="main"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.2 }}
              className="flex flex-col gap-6"
            >
              {/* Year + view controls */}
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <YearSelector activeYear={activeYear} onChange={setActiveYear} />
                <div className="flex gap-1 self-start rounded-2xl bg-black/5 p-1 dark:bg-white/[0.06] sm:self-auto">
                  {VIEWS.map((v) => {
                    const Icon = v.icon
                    const active = view === v.id
                    return (
                      <button
                        key={v.id}
                        onClick={() => setView(v.id)}
                        className={`focus-ring flex items-center gap-1.5 rounded-xl px-3 py-2 text-[12.5px] font-medium transition-colors ${
                          active
                            ? 'bg-white text-ink-light shadow-soft dark:bg-[#3A3A3C] dark:text-ink-dark'
                            : 'text-muted-light dark:text-muted-dark'
                        }`}
                      >
                        <Icon size={13.5} /> {v.label}
                      </button>
                    )
                  })}
                </div>
              </div>

              <div>
                <h1 className="text-[22px] font-bold tracking-tight sm:text-[26px]">{year.sem}</h1>
                <p className="mt-0.5 text-[13px] text-muted-light dark:text-muted-dark">
                  Class incharge: {year.incharge}
                </p>
              </div>

              {failed ? (
                <InlineError onRetry={retry} />
              ) : loading ? (
                <>
                  <BannerSkeleton />
                  <AgendaSkeleton />
                </>
              ) : (
                <>
                  {(view === 'today' || view === 'day') && (
                    <StatusBanner
                      dayCode={view === 'today' ? todayCode : activeDay}
                      year={year}
                      current={view === 'today' ? current : null}
                      next={view === 'today' ? next : null}
                      nowMinutes={nowMinutes}
                    />
                  )}

                  {view === 'today' && <StatsRow year={year} todayCode={todayCode || 'MON'} />}

                  {(view === 'today' || view === 'day') && (
                    <div className="flex flex-col gap-4">
                      {view === 'day' && (
                        <DayTabs activeDay={activeDay} onChange={setActiveDay} todayCode={todayCode} />
                      )}
                      <AnimatePresence mode="wait">
                        <motion.div
                          key={view === 'today' ? todayCode || 'none' : activeDay}
                          initial={{ opacity: 0, y: 6 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -6 }}
                          transition={{ duration: 0.18 }}
                        >
                          {view === 'today' && !todayCode ? (
                            <div className="rounded-3xl border border-dashed border-line-light py-14 text-center text-[13px] text-muted-light dark:border-line-dark dark:text-muted-dark">
                              It's Sunday — no classes scheduled.
                            </div>
                          ) : (
                            <DayAgenda
                              year={year}
                              dayCode={view === 'today' ? todayCode : activeDay}
                              isToday={(view === 'today' ? todayCode : activeDay) === todayCode}
                              nowMinutes={nowMinutes}
                            />
                          )}
                        </motion.div>
                      </AnimatePresence>
                    </div>
                  )}

                  {view === 'week' && (
                    <WeeklyGrid year={year} todayCode={todayCode} nowMinutes={nowMinutes} />
                  )}
                </>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <ErrorBoundary>
      <AppInner />
    </ErrorBoundary>
  )
}
