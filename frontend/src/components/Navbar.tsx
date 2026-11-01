import React from 'react';
import { useCourse } from '../context/CourseContext';
import { 
  Cloud, 
  ExternalLink, 
  Cpu, 
  Sparkles, 
  CheckCircle2, 
  MessageSquare, 
  Settings as SettingsIcon 
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const { course, settings, navigateTo, progress } = useCourse();

  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-200/80 shadow-sm backdrop-blur-sm bg-white/95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          
          {/* Left: Brand & Course Header */}
          <div className="flex items-center space-x-3">
            <div 
              onClick={() => navigateTo('dashboard')}
              className="flex items-center space-x-2.5 cursor-pointer group"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#232F3E] to-[#131921] flex items-center justify-center shadow-md group-hover:scale-105 transition-transform">
                <Cloud className="w-6 h-6 text-[#FF9900]" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-extrabold text-slate-900 tracking-tight text-lg">
                    AWS Academy
                  </span>
                  <span className="bg-[#FF9900]/15 text-[#D97706] text-xs font-semibold px-2 py-0.5 rounded-full border border-[#FF9900]/30">
                    Course Copilot
                  </span>
                </div>
                <p className="text-xs text-slate-500 font-medium">
                  {course?.name || 'Cloud Foundations (ID: 183194)'}
                </p>
              </div>
            </div>
          </div>

          {/* Right: Status Pills & Action buttons */}
          <div className="flex items-center space-x-3">
            {/* Canvas LMS Link */}
            <a 
              href="https://awsacademy.instructure.com/courses/183194/modules" 
              target="_blank" 
              rel="noreferrer"
              className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 hover:bg-slate-200/80 rounded-lg transition-colors border border-slate-200"
            >
              <span>Canvas Modules</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
            </a>

            {/* AI Provider Status Pill */}
            <div 
              onClick={() => navigateTo('settings')}
              className="cursor-pointer flex items-center space-x-1.5 px-2.5 py-1 text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200/60 rounded-lg hover:bg-emerald-100/60 transition-colors"
              title="Click to view or switch AI provider in Settings"
            >
              <Cpu className="w-3.5 h-3.5 text-emerald-600" />
              <span className="capitalize">{settings?.llm_provider || 'Local AI'}</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            </div>

            {/* Quick Ask Tutor Button */}
            <button
              onClick={() => navigateTo('chat')}
              className="flex items-center space-x-1.5 bg-[#FF9900] hover:bg-[#e68a00] text-slate-950 font-semibold px-3.5 py-1.5 rounded-lg text-xs shadow-sm transition-all hover:shadow"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Ask Tutor</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
