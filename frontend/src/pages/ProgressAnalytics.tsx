import React from 'react';
import { useCourse } from '../context/CourseContext';
import {
  TrendingUp,
  CheckCircle2,
  Clock,
  Layers,
  AlertTriangle,
  Award,
  BookOpen,
  Terminal,
  ShieldCheck,
  ArrowRight
} from 'lucide-react';

export const ProgressAnalytics: React.FC = () => {
  const { progress, navigateTo } = useCourse();

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Completed':
        return <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-0.5 rounded-full border border-emerald-200">Completed</span>;
      case 'In Progress':
        return <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2.5 py-0.5 rounded-full border border-blue-200">In Progress</span>;
      case 'Needs Revision':
        return <span className="bg-amber-100 text-amber-800 text-xs font-bold px-2.5 py-0.5 rounded-full border border-amber-200">Needs Revision</span>;
      case 'Ready for Assessment':
        return <span className="bg-purple-100 text-purple-800 text-xs font-bold px-2.5 py-0.5 rounded-full border border-purple-200">Ready for Assessment</span>;
      default:
        return <span className="bg-slate-100 text-slate-600 text-xs font-bold px-2.5 py-0.5 rounded-full border border-slate-200">Not Started</span>;
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
            Progress Analytics & Mastery Tracker
          </h1>
          <p className="text-xs text-slate-500">
            Real-time analytics across all 10 modules, 6 labs, and knowledge check evaluations
          </p>
        </div>

        <div className="bg-slate-100 px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-700 flex items-center space-x-1.5 self-start sm:self-auto">
          <Clock className="w-3.5 h-3.5 text-[#FF9900]" />
          <span>Logged Study Time: ~{Math.round((progress?.total_study_time_mins || 340) / 60)} Hours</span>
        </div>
      </div>

      {/* Distinction Callout (Requirement 9: Distinguish local from official Canvas) */}
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex items-start space-x-2.5 text-xs text-slate-700">
        <ShieldCheck className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-slate-900">Progress Tracking Policy:</span> This dashboard tracks your local study preparation, practice quiz attempts, and manual lab confirmations. Official grades and completion credentials remain recorded separately within your AWS Academy Canvas LMS course record.
        </div>
      </div>

      {/* Progress Breakdown Metrics Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 text-center space-y-1">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Total Modules</div>
          <div className="text-2xl font-extrabold text-slate-900">{progress?.total_modules || 10}</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-emerald-200 text-center space-y-1">
          <div className="text-[11px] font-bold uppercase tracking-wider text-emerald-600">Completed</div>
          <div className="text-2xl font-extrabold text-emerald-700">{progress?.completed_modules || 0}</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-blue-200 text-center space-y-1">
          <div className="text-[11px] font-bold uppercase tracking-wider text-blue-600">In Progress</div>
          <div className="text-2xl font-extrabold text-blue-700">{progress?.in_progress_modules || 1}</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-amber-200 text-center space-y-1">
          <div className="text-[11px] font-bold uppercase tracking-wider text-amber-600">Needs Revision</div>
          <div className="text-2xl font-extrabold text-amber-700">
            {progress?.modules_progress?.filter(m => m.status === 'Needs Revision').length || 0}
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-purple-200 text-center space-y-1">
          <div className="text-[11px] font-bold uppercase tracking-wider text-purple-600">Ready for Exam</div>
          <div className="text-2xl font-extrabold text-purple-700">
            {progress?.modules_progress?.filter(m => m.status === 'Ready for Assessment').length || 0}
          </div>
        </div>
      </div>

      {/* Detailed Module Status Table (Requirement 9) */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-4">
        <h2 className="font-bold text-slate-900 text-sm">
          Module-by-Module Progress Breakdown
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead>
              <tr className="border-b border-slate-100 text-slate-400 uppercase text-[10px]">
                <th className="py-2.5">Module</th>
                <th className="py-2.5">Status</th>
                <th className="py-2.5">Progress</th>
                <th className="py-2.5">Items Completed</th>
                <th className="py-2.5">Lab Status</th>
                <th className="py-2.5">Best Quiz</th>
                <th className="py-2.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(progress?.modules_progress || []).map((mod) => (
                <tr key={mod.module_id} className="hover:bg-slate-50/70">
                  <td className="py-3 font-bold text-slate-900 max-w-xs">
                    Module {mod.module_number}: {mod.title.replace(/Module \d+ - /, '')}
                  </td>
                  <td className="py-3">
                    {getStatusBadge(mod.status)}
                  </td>
                  <td className="py-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-20 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                        <div
                          className="bg-amber-500 h-1.5 rounded-full"
                          style={{ width: `${Math.max(4, mod.progress_percentage)}%` }}
                        ></div>
                      </div>
                      <span className="font-semibold text-slate-700">{mod.progress_percentage}%</span>
                    </div>
                  </td>
                  <td className="py-3 text-slate-600">
                    {mod.items_completed}/{mod.total_items} resources
                  </td>
                  <td className="py-3">
                    {mod.has_lab ? (
                      mod.lab_completed ? (
                        <span className="text-emerald-700 font-semibold flex items-center space-x-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>Verified</span>
                        </span>
                      ) : (
                        <span className="text-amber-700 font-semibold flex items-center space-x-1">
                          <Clock className="w-3.5 h-3.5" />
                          <span>Incomplete</span>
                        </span>
                      )
                    ) : (
                      <span className="text-slate-400">N/A</span>
                    )}
                  </td>
                  <td className="py-3 font-semibold text-slate-700">
                    {mod.practice_best_score ? `${mod.practice_best_score}%` : 'Not attempted'}
                  </td>
                  <td className="py-3 text-right">
                    <button
                      onClick={() => navigateTo('workspace', mod.module_id)}
                      className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg font-semibold"
                    >
                      Study
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Concepts Mastery Cloud */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Understood Topics */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-3">
          <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Understood Topics ({progress?.understood_topics?.length || 0})</span>
          </h3>
          <div className="flex flex-wrap gap-2">
            {(progress?.understood_topics || []).map((topic, i) => (
              <span
                key={i}
                className="text-xs font-semibold bg-emerald-50 text-emerald-900 border border-emerald-200 px-3 py-1 rounded-xl"
              >
                ✓ {topic}
              </span>
            ))}
          </div>
        </div>

        {/* Topics Requiring Revision */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-3">
          <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            <span>Topics Requiring Revision ({progress?.weak_topics?.length || 0})</span>
          </h3>
          <div className="flex flex-wrap gap-2">
            {(progress?.weak_topics || []).map((topic, i) => (
              <span
                key={i}
                className="text-xs font-semibold bg-amber-50 text-amber-900 border border-amber-200 px-3 py-1 rounded-xl"
              >
                ⚠️ {topic}
              </span>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
