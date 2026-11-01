import React from 'react';
import { useCourse } from '../context/CourseContext';
import { PageView } from '../types';
import {
  LayoutDashboard,
  Layers,
  BookOpen,
  Bot,
  CheckSquare,
  Terminal,
  TrendingUp,
  Calendar,
  FolderArchive,
  Settings,
  ChevronRight,
  GraduationCap
} from 'lucide-react';

interface NavItem {
  id: PageView;
  label: string;
  icon: React.ElementType;
  badge?: string;
}

export const Sidebar: React.FC = () => {
  const { activePage, navigateTo, progress } = useCourse();

  const navItems: NavItem[] = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'modules', label: 'Course Modules', icon: Layers, badge: '10' },
    { id: 'workspace', label: 'Learning Workspace', icon: BookOpen },
    { id: 'chat', label: 'AI Tutor Chat', icon: Bot, badge: 'RAG' },
    { id: 'practice', label: 'Knowledge Check', icon: CheckSquare },
    { id: 'labs', label: 'AWS Lab Assistant', icon: Terminal, badge: '6 Labs' },
    { id: 'progress', label: 'Progress Analytics', icon: TrendingUp },
    { id: 'planner', label: 'Study Planner', icon: Calendar },
    { id: 'documents', label: 'Document Library', icon: FolderArchive },
    { id: 'settings', label: 'Settings & Integrations', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200/80 min-h-[calc(100vh-4rem)] flex flex-col justify-between shrink-0">
      <div className="p-4 space-y-1">
        <div className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Navigation
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.id;

          return (
            <button
              key={item.id}
              onClick={() => navigateTo(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? 'bg-slate-900 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon
                  className={`w-4 h-4 ${
                    isActive ? 'text-[#FF9900]' : 'text-slate-400'
                  }`}
                />
                <span className="truncate">{item.label}</span>
              </div>

              {item.badge && (
                <span
                  className={`text-[10px] font-bold px-1.5 py-0.5 rounded-md ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'bg-slate-100 text-slate-500'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Progress Footer Card in Sidebar */}
      <div className="p-4 border-t border-slate-100">
        <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200/60 space-y-2.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-slate-700 flex items-center space-x-1.5">
              <GraduationCap className="w-4 h-4 text-[#FF9900]" />
              <span>Course Progress</span>
            </span>
            <span className="font-bold text-slate-900">
              {progress?.overall_progress_percentage || 0}%
            </span>
          </div>

          <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-[#FF9900] to-amber-500 h-2 rounded-full transition-all duration-500"
              style={{
                width: `${Math.min(100, Math.max(5, progress?.overall_progress_percentage || 0))}%`,
              }}
            ></div>
          </div>

          <div className="flex justify-between text-[11px] text-slate-500 font-medium">
            <span>{progress?.completed_modules || 0}/10 Modules Completed</span>
            <span 
              onClick={() => navigateTo('progress')}
              className="text-[#0073bb] hover:underline cursor-pointer flex items-center"
            >
              Details
              <ChevronRight className="w-3 h-3 ml-0.5" />
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
};
