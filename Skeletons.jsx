export function BannerSkeleton() {
  return (
    <div className="shimmer-bg h-[148px] w-full rounded-3xl bg-black/[0.04] dark:bg-white/[0.06]" />
  )
}

export function CardSkeleton() {
  return (
    <div className="shimmer-bg min-h-[104px] w-full rounded-2xl border border-line-light bg-black/[0.03] dark:border-line-dark dark:bg-white/[0.04]" />
  )
}

export function AgendaSkeleton() {
  return (
    <div className="flex flex-col gap-2.5">
      {Array.from({ length: 5 }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  )
}

export function GridSkeleton() {
  return (
    <div className="shimmer-bg h-[560px] w-full rounded-3xl border border-line-light bg-black/[0.03] dark:border-line-dark dark:bg-white/[0.04]" />
  )
}
