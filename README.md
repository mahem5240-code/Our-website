# AIML Timetable — Trinity College of Engineering & Technology, Peddapalli

A premium, Apple-inspired timetable app for the AIML department (2nd, 3rd & 4th Year),
built with React, Vite, Tailwind CSS, Framer Motion and Lucide icons.

## Setup

```bash
npm install
npm run dev
```

Then open the printed local URL (typically http://localhost:5173).

## Build

```bash
npm run build
npm run preview
```

## Structure

```
src/
  data/timetableData.js     Source-of-truth schedule for all 3 years
  utils/                    time helpers, color tokens, day-row builder
  hooks/useNow.js           live clock (updates every 30s)
  context/ThemeContext.jsx  dark/light mode with persistence
  components/               Header, YearSelector, DayTabs, StatusBanner,
                             SubjectCard, WeeklyGrid, DayAgenda, SearchResults,
                             StatsRow, Skeletons, EmptyState, ErrorState
  App.jsx                   app shell — Today / Day / Week views
```

## Notes on the data

The schedule in `src/data/timetableData.js` was transcribed from the official
department timetable (W.E.F. 06-JULY-2026). Lab sessions that visually span a
break period in the printed sheet are represented as a single merged time
block. If you spot a mismatch against the original notice board copy, it's a
one-file edit — everything else (UI, current/next detection, search) derives
from this file automatically.
