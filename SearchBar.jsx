import { Search, X } from 'lucide-react'

export default function SearchBar({ value, onChange, placeholder = 'Search subjects or faculty' }) {
  return (
    <div className="relative w-full">
      <Search
        size={16}
        strokeWidth={2.25}
        className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-light dark:text-muted-dark"
      />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="focus-ring w-full rounded-xl border border-line-light bg-white py-2.5 pl-10 pr-9 text-sm text-ink-light placeholder:text-muted-light/70 transition-shadow dark:border-line-dark dark:bg-surface-dark dark:text-ink-dark dark:placeholder:text-muted-dark/60"
      />
      {value && (
        <button
          onClick={() => onChange('')}
          aria-label="Clear search"
          className="focus-ring absolute right-3 top-1/2 -translate-y-1/2 text-muted-light hover:text-ink-light dark:text-muted-dark dark:hover:text-ink-dark"
        >
          <X size={15} />
        </button>
      )}
    </div>
  )
}
