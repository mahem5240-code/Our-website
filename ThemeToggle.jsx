import { motion } from 'framer-motion'
import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'

export default function ThemeToggle() {
  const { theme, toggle } = useTheme()
  const isDark = theme === 'dark'

  return (
    <button
      onClick={toggle}
      aria-label="Toggle dark mode"
      aria-pressed={isDark}
      className="focus-ring relative flex h-9 w-16 items-center rounded-full bg-black/5 p-1 transition-colors dark:bg-white/10"
    >
      <motion.div
        layout
        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        className="flex h-7 w-7 items-center justify-center rounded-full bg-white shadow-soft dark:bg-[#3A3A3C]"
        style={{ marginLeft: isDark ? 'auto' : 0 }}
      >
        {isDark ? (
          <Moon size={14} className="text-indigo-300" strokeWidth={2.25} />
        ) : (
          <Sun size={14} className="text-orange-400" strokeWidth={2.25} />
        )}
      </motion.div>
    </button>
  )
}
