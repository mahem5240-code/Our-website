import { motion } from 'framer-motion'
import { GraduationCap } from 'lucide-react'
import ThemeToggle from './ThemeToggle'
import SearchBar from './SearchBar'

export default function Header({ search, onSearch }) {
  return (
    <header className="glass sticky top-0 z-30 border-b border-line-light/70 bg-white/70 dark:border-line-dark/70 dark:bg-black/60">
      <div className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3 sm:px-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-[#0071E3] to-[#5E5CE6] text-white shadow-soft"
        >
          <GraduationCap size={18} strokeWidth={2.25} />
        </motion.div>
        <div className="hidden min-w-0 sm:block">
          <p className="truncate text-[13.5px] font-semibold leading-tight text-ink-light dark:text-ink-dark">
            AIML Timetable
          </p>
          <p className="truncate text-[11px] leading-tight text-muted-light dark:text-muted-dark">
            Trinity College of Engineering &amp; Technology, Peddapalli
          </p>
        </div>
        <div className="ml-auto flex flex-1 items-center justify-end gap-3 sm:flex-none sm:w-80">
          <SearchBar value={search} onChange={onSearch} />
        </div>
        <ThemeToggle />
      </div>
    </header>
  )
}
