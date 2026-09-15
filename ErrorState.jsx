import { Component } from 'react'
import { AlertTriangle, RotateCcw } from 'lucide-react'

export function InlineError({ message = 'Something went wrong loading the timetable.', onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-3xl border border-line-light bg-white py-14 text-center dark:border-line-dark dark:bg-surface-dark">
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#FF375F]/10">
        <AlertTriangle size={20} className="text-[#FF375F]" />
      </div>
      <div>
        <p className="text-[14px] font-semibold text-ink-light dark:text-ink-dark">{message}</p>
        <p className="mt-0.5 text-[13px] text-muted-light dark:text-muted-dark">
          Try again, or switch to a different year.
        </p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="focus-ring mt-1 flex items-center gap-1.5 rounded-full bg-black/5 px-4 py-2 text-[13px] font-medium text-ink-light hover:bg-black/10 dark:bg-white/10 dark:text-ink-dark dark:hover:bg-white/15"
        >
          <RotateCcw size={13} /> Retry
        </button>
      )}
    </div>
  )
}

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }
  static getDerivedStateFromError() {
    return { hasError: true }
  }
  componentDidCatch(error) {
    console.error('AIML Timetable crashed:', error)
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-canvas-light p-6 dark:bg-canvas-dark">
          <InlineError
            message="The app hit an unexpected error."
            onRetry={() => this.setState({ hasError: false })}
          />
        </div>
      )
    }
    return this.props.children
  }
}
