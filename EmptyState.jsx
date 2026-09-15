import { CalendarDays } from 'lucide-react'

export default function EmptyState({ title = 'Nothing here', subtitle = '', icon: Icon = CalendarDays }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-3xl border border-dashed border-line-light py-14 text-center dark:border-line-dark">
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-black/5 dark:bg-white/10">
        <Icon size={20} className="text-muted-light dark:text-muted-dark" />
      </div>
      <div>
        <p className="text-[14px] font-semibold text-ink-light dark:text-ink-dark">{title}</p>
        {subtitle && <p className="mt-0.5 text-[13px] text-muted-light dark:text-muted-dark">{subtitle}</p>}
      </div>
    </div>
  )
}
