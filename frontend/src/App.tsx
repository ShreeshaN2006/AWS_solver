import { useEffect, useMemo, useState } from 'react'

type Dashboard = {
  course_title: string
  overall_study_progress: number
  total_modules: number
  completed_modules: number
  modules_in_progress: number
  remaining_modules: number
  recent_learning_activity: string[]
  upcoming_tasks: string[]
  weak_topics: string[]
  recommended_next_activity: string
}

type Module = {
  module_id: string
  module_number: number
  title: string
  items: { item_id: string; title: string }[]
}

const pages = [
  'Dashboard',
  'Course Modules',
  'Module Learning Workspace',
  'AI Tutor Chat',
  'Knowledge Check Practice',
  'AWS Lab Assistant',
  'Progress Analytics',
  'Study Planner',
  'Document Library',
  'Settings and Integrations',
]

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')
  const [dashboard, setDashboard] = useState<Dashboard | null>(null)
  const [modules, setModules] = useState<Module[]>([])
  const [question, setQuestion] = useState('Explain shared responsibility model')
  const [answer, setAnswer] = useState('')

  useEffect(() => {
    const load = async () => {
      const [dashboardRes, outlineRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard`),
        fetch(`${API_BASE}/course/outline`),
      ])
      const dashboardPayload = await dashboardRes.json()
      const outlinePayload = await outlineRes.json()
      setDashboard(dashboardPayload)
      setModules(outlinePayload.modules ?? [])
    }
    load().catch(() => undefined)
  }, [])

  const moduleCards = useMemo(
    () =>
      modules.map((module) => (
        <article key={module.module_id} className="rounded-lg border border-slate-700 bg-slate-800/60 p-4">
          <h3 className="font-semibold text-white">Module {module.module_number}: {module.title}</h3>
          <p className="mt-2 text-sm text-slate-300">Learning resources: {module.items.length}</p>
          <p className="text-sm text-slate-300">Knowledge check prep and labs supported in assistant views.</p>
        </article>
      )),
    [modules],
  )

  const askTutor = async () => {
    const res = await fetch(`${API_BASE}/tutor/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    })
    const payload = await res.json()
    setAnswer(payload.answer)
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 px-6 py-4">
        <h1 className="text-2xl font-bold">AWS Academy Course Copilot</h1>
        <p className="text-sm text-slate-300">Course ID 183194 · Canvas-aware learning assistant</p>
      </header>
      <div className="grid gap-4 p-6 lg:grid-cols-[260px_1fr]">
        <nav className="rounded-lg border border-slate-800 bg-slate-900 p-4">
          <ul className="space-y-2">
            {pages.map((page) => (
              <li key={page}>
                <button
                  onClick={() => setActivePage(page)}
                  className={`w-full rounded px-3 py-2 text-left text-sm ${activePage === page ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-200'}`}
                >
                  {page}
                </button>
              </li>
            ))}
          </ul>
        </nav>

        <main className="space-y-4">
          {activePage === 'Dashboard' && dashboard && (
            <section className="grid gap-4 md:grid-cols-3">
              {[
                ['Overall Study Progress', `${dashboard.overall_study_progress.toFixed(0)}%`],
                ['Total Modules', dashboard.total_modules],
                ['Completed Modules', dashboard.completed_modules],
                ['Modules In Progress', dashboard.modules_in_progress],
                ['Remaining Modules', dashboard.remaining_modules],
                ['Recommended Next Activity', dashboard.recommended_next_activity],
              ].map(([label, value]) => (
                <article key={String(label)} className="rounded-lg border border-slate-800 bg-slate-900 p-4">
                  <h2 className="text-sm text-slate-400">{label}</h2>
                  <p className="mt-2 font-semibold text-white">{value}</p>
                </article>
              ))}
              <article className="rounded-lg border border-slate-800 bg-slate-900 p-4 md:col-span-3">
                <h2 className="font-semibold">All 10 Modules</h2>
                <div className="mt-3 grid gap-3 md:grid-cols-2">{moduleCards}</div>
              </article>
            </section>
          )}

          {activePage === 'AI Tutor Chat' && (
            <section className="rounded-lg border border-slate-800 bg-slate-900 p-4">
              <h2 className="font-semibold">Course-aware Tutor</h2>
              <p className="mt-1 text-sm text-slate-300">Answers cite indexed course sources when available.</p>
              <textarea value={question} onChange={(e) => setQuestion(e.target.value)} className="mt-3 h-24 w-full rounded bg-slate-800 p-2" />
              <button onClick={askTutor} className="mt-3 rounded bg-blue-600 px-4 py-2">Ask Tutor</button>
              {answer && <pre className="mt-3 whitespace-pre-wrap rounded bg-slate-800 p-3 text-sm">{answer}</pre>}
            </section>
          )}

          {activePage !== 'Dashboard' && activePage !== 'AI Tutor Chat' && (
            <section className="rounded-lg border border-slate-800 bg-slate-900 p-4">
              <h2 className="font-semibold">{activePage}</h2>
              <p className="mt-2 text-slate-300">This workspace is available in the MVP and wired to backend endpoints for phased expansion.</p>
            </section>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
