import React from 'react';
import { useCourse } from '../context/CourseContext';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  ArrowRight,
  Sparkles,
  Layers,
  AlertTriangle,
  Calendar,
  Terminal,
  CheckSquare,
  TrendingUp,
  ExternalLink
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { course, modules, progress, navigateTo } = useCourse();

  // Filter core 10 modules
  const coreModules = modules.filter(m => m.is_core_module);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Completed':
        return <span className="bg-emerald-100 text-emerald-800 text-[11px] font-semibold px-2.5 py-0.5 rounded-full border border-emerald-200">Completed</span>;
      case 'In Progress':
        return <span className="bg-blue-100 text-blue-800 text-[11px] font-semibold px-2.5 py-0.5 rounded-full border border-blue-200">In Progress</span>;
      case 'Needs Revision':
        return <span className="bg-amber-100 text-amber-800 text-[11px] font-semibold px-2.5 py-0.5 rounded-full border border-amber-200">Needs Revision</span>;
      case 'Ready for Assessment':
        return <span className="bg-purple-100 text-purple-800 text-[11px] font-semibold px-2.5 py-0.5 rounded-full border border-purple-200">Ready for Assessment</span>;
      default:
        return <span className="bg-slate-100 text-slate-600 text-[11px] font-semibold px-2.5 py-0.5 rounded-full border border-slate-200">Not Started</span>;
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Hero Welcome Banner */}
      <div className="bg-gradient-to-r from-[#232F3E] via-[#1A2433] to-[#131921] rounded-2xl p-6 text-white shadow-md relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-amber-500/20 via-transparent to-transparent pointer-events-none"></div>
        
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/10 text-xs text-amber-300 font-medium">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Course-Aware AI Agent Active</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            AWS Academy Cloud Foundations
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Your personalized course copilot with access to official AWS Academy materials, 
            hands-on lab walkthroughs, knowledge check practice questions, and dynamic progress tracking.
          </p>

          {/* Recommended Next Action Banner */}
          {progress?.recommended_next_activity && (
            <div className="pt-2">
              <div className="bg-white/10 border border-white/15 rounded-xl p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 backdrop-blur-sm">
                <div className="space-y-0.5">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-amber-400 flex items-center space-x-1.5">
                    <Sparkles className="w-3 h-3" />
                    <span>Recommended Next Activity</span>
                  </div>
                  <div className="font-semibold text-white text-sm">
                    {progress.recommended_next_activity.title}
                  </div>
                  <p className="text-xs text-slate-300">
                    {progress.recommended_next_activity.reason}
                  </p>
                </div>

                <button
                  onClick={() => navigateTo('practice', progress.recommended_next_activity?.module_id)}
                  className="bg-[#FF9900] hover:bg-[#e68a00] text-slate-950 font-bold px-4 py-2 rounded-xl text-xs transition-all shadow-sm flex items-center space-x-1.5 self-start sm:self-auto shrink-0"
                >
                  <span>Start Activity</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Primary Metrics Grid (Requirement 3) */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm space-y-1">
          <div className="text-slate-500 text-xs font-medium flex items-center justify-between">
            <span>Overall Progress</span>
            <TrendingUp className="w-4 h-4 text-[#FF9900]" />
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {progress?.overall_progress_percentage || 0}%
          </div>
          <div className="text-[11px] text-slate-400 font-medium">Curriculum studied</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm space-y-1">
          <div className="text-slate-500 text-xs font-medium flex items-center justify-between">
            <span>Total Modules</span>
            <Layers className="w-4 h-4 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {progress?.total_modules || 10}
          </div>
          <div className="text-[11px] text-slate-400 font-medium">Core foundation units</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm space-y-1">
          <div className="text-slate-500 text-xs font-medium flex items-center justify-between">
            <span>Completed</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600">
            {progress?.completed_modules || 0}
          </div>
          <div className="text-[11px] text-slate-400 font-medium">Modules mastered</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm space-y-1">
          <div className="text-slate-500 text-xs font-medium flex items-center justify-between">
            <span>In Progress</span>
            <Clock className="w-4 h-4 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-blue-600">
            {progress?.in_progress_modules || 1}
          </div>
          <div className="text-[11px] text-slate-400 font-medium">Active study units</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm space-y-1">
          <div className="text-slate-500 text-xs font-medium flex items-center justify-between">
            <span>Remaining</span>
            <BookOpen className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-bold text-slate-700">
            {progress?.remaining_modules || 9}
          </div>
          <div className="text-[11px] text-slate-400 font-medium">Pending completion</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm space-y-1">
          <div className="text-slate-500 text-xs font-medium flex items-center justify-between">
            <span>Study Time</span>
            <Clock className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {Math.round((progress?.total_study_time_mins || 340) / 60)} hrs
          </div>
          <div className="text-[11px] text-slate-400 font-medium">Logged study effort</div>
        </div>

      </div>

      {/* Main 2-Column Section: Modules List (Left) + Insights/Tasks (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left 2 Cols: Organised 10 Modules List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Course Modules (1 to 10)</h2>
              <p className="text-xs text-slate-500">Official AWS Academy Cloud Foundations core modules</p>
            </div>
            <button
              onClick={() => navigateTo('modules')}
              className="text-xs font-semibold text-[#0073bb] hover:underline flex items-center space-x-1"
            >
              <span>View All Sections</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-3">
            {coreModules.map((module) => {
              const modProgress = progress?.modules_progress?.find(p => p.module_id === module.module_id);
              const progressPct = modProgress?.progress_percentage || module.progress_percentage || 0;
              const statusStr = modProgress?.status || module.status || 'Not Started';

              return (
                <div
                  key={module.module_id}
                  className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm hover:border-slate-300 transition-all space-y-3"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold text-[#FF9900] bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200">
                          Module {module.module_number}
                        </span>
                        {getStatusBadge(statusStr)}
                        {module.has_lab && (
                          <span className="bg-slate-100 text-slate-700 text-[10px] font-semibold px-2 py-0.5 rounded-md border border-slate-200 flex items-center space-x-1">
                            <Terminal className="w-3 h-3 text-slate-500" />
                            <span>Hands-on Lab</span>
                          </span>
                        )}
                      </div>
                      <h3 className="font-bold text-slate-900 text-sm">
                        {module.title}
                      </h3>
                      <p className="text-xs text-slate-500 line-clamp-1">
                        {module.description}
                      </p>
                    </div>

                    <div className="text-right shrink-0">
                      <span className="text-sm font-bold text-slate-900">{progressPct}%</span>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-amber-500 h-1.5 rounded-full"
                      style={{ width: `${Math.max(3, progressPct)}%` }}
                    ></div>
                  </div>

                  {/* Action Quick Links */}
                  <div className="flex flex-wrap items-center justify-between pt-1 text-xs border-t border-slate-100 gap-2">
                    <div className="flex items-center space-x-4 text-slate-500 font-medium">
                      <span className="flex items-center space-x-1">
                        <BookOpen className="w-3.5 h-3.5" />
                        <span>{module.items.length} Resources</span>
                      </span>
                      {module.has_lab && (
                        <span 
                          onClick={() => navigateTo('labs', module.module_id, module.lab_id)}
                          className="flex items-center space-x-1 text-[#0073bb] hover:underline cursor-pointer"
                        >
                          <Terminal className="w-3.5 h-3.5" />
                          <span>Lab Guidance</span>
                        </span>
                      )}
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => navigateTo('practice', module.module_id)}
                        className="px-2.5 py-1 text-[11px] font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors flex items-center space-x-1"
                      >
                        <CheckSquare className="w-3 h-3" />
                        <span>Practice</span>
                      </button>

                      <button
                        onClick={() => navigateTo('workspace', module.module_id)}
                        className="px-3 py-1 text-[11px] font-semibold text-slate-900 bg-amber-400 hover:bg-amber-500 rounded-lg transition-colors flex items-center space-x-1 shadow-sm"
                      >
                        <span>Study Module</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Weak Topics, Upcoming Tasks & Activity */}
        <div className="space-y-6">
          
          {/* Weak Topics Card */}
          <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4 text-amber-500" />
                <span>Weak Topics Identified</span>
              </h3>
              <span className="text-[11px] text-slate-400 font-medium">From quiz attempts</span>
            </div>

            <p className="text-xs text-slate-500">
              Concepts requiring reinforcement based on practice tests:
            </p>

            <div className="space-y-2">
              {(progress?.weak_topics || [
                'AWS Shared Responsibility Model',
                'VPC Subnet Routing & CIDR',
                'Amazon S3 vs EBS Use Cases'
              ]).map((topic, i) => (
                <div
                  key={i}
                  className="p-2.5 bg-amber-50/60 rounded-lg border border-amber-200/60 flex items-center justify-between text-xs"
                >
                  <span className="font-semibold text-amber-900">{topic}</span>
                  <button
                    onClick={() => navigateTo('chat')}
                    className="text-[#0073bb] hover:underline font-semibold text-[11px]"
                  >
                    Ask Copilot
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Upcoming Tasks Card */}
          <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
                <Calendar className="w-4 h-4 text-blue-500" />
                <span>Upcoming Study Tasks</span>
              </h3>
              <button
                onClick={() => navigateTo('planner')}
                className="text-[11px] font-semibold text-[#0073bb] hover:underline"
              >
                Open Planner
              </button>
            </div>

            <div className="space-y-2">
              {(progress?.upcoming_tasks || []).map((task) => (
                <div
                  key={task.id}
                  className="p-2.5 bg-slate-50 rounded-lg border border-slate-200/60 flex items-start justify-between text-xs gap-2"
                >
                  <div className="space-y-0.5">
                    <div className="font-semibold text-slate-800">{task.title}</div>
                    <div className="text-[11px] text-slate-400">Due: {task.due}</div>
                  </div>
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                    task.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-slate-200 text-slate-700'
                  }`}>
                    {task.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Learning Activity Card */}
          <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-sm space-y-3">
            <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
              <Clock className="w-4 h-4 text-slate-500" />
              <span>Recent Activity</span>
            </h3>

            <div className="space-y-3 divide-y divide-slate-100">
              {(progress?.recent_activities || []).map((act, i) => (
                <div key={i} className="pt-2 first:pt-0 space-y-1">
                  <p className="text-xs font-medium text-slate-800 leading-snug">
                    {act.title}
                  </p>
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span>{act.module}</span>
                    <span>{act.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};
