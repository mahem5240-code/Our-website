import { BookOpen, FlaskConical, Users } from 'lucide-react'

function Stat({ icon: Icon, label, value, color }) {
  return (
    <div className="flex flex-1 items-center gap-3 rounded-2xl border border-line-light bg-white p-4 dark:border-line-dark dark:bg-surface-dark">
      <div className={`flex h-9 w-9 items-center justify-center rounded-xl ${color}`}>
        <Icon size={16} className="text-white" strokeWidth={2.25} />
      </div>
      <div className="min-w-0">
        <p className="text-[17px] font-bold leading-none text-ink-light dark:text-ink-dark">{value}</p>
        <p className="mt-1 truncate text-[11.5px] text-muted-light dark:text-muted-dark">{label}</p>
      </div>
    </div>
  )
}

export default function StatsRow({ year, todayCode }) {
  const todayEntries = year.schedule[todayCode] || []
  const allEntries = Object.values(year.schedule).flat()
  const labsThisWeek = allEntries.filter(
    (e) => e.type === 'lab' || year.subjects[e.code]?.isLab
  ).length
  const facultyCount = new Set(Object.values(year.subjects).map((s) => s.faculty)).size

  return (
    <div className="flex flex-col gap-3 sm:flex-row">
      <Stat icon={BookOpen} label="Classes today" value={todayEntries.length} color="bg-[#0071E3]" />
      <Stat icon={FlaskConical} label="Lab sessions / week" value={labsThisWeek} color="bg-[#BF5AF2]" />
      <Stat icon={Users} label="Faculty involved" value={facultyCount} color="bg-[#30D158]" />
    </div>
  )
}
