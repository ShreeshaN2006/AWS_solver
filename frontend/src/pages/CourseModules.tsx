import React, { useState } from 'react';
import { useCourse } from '../context/CourseContext';
import {
  BookOpen,
  Search,
  Filter,
  CheckCircle2,
  Terminal,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  FileText,
  PlayCircle,
  HelpCircle,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export const CourseModules: React.FC = () => {
  const { modules, navigateTo } = useCourse();
  const [filterType, setFilterType] = useState<'all' | 'core' | 'additional' | 'labs'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedModules, setExpandedModules] = useState<Record<string, boolean>>({
    '10101': true,
    '10401': true
  });

  const toggleExpand = (modId: string) => {
    setExpandedModules(prev => ({ ...prev, [modId]: !prev[modId] }));
  };

  const filteredModules = modules.filter(m => {
    // Filter type
    if (filterType === 'core' && !m.is_core_module) return false;
    if (filterType === 'additional' && m.is_core_module) return false;
    if (filterType === 'labs' && !m.has_lab) return false;

    // Search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const inTitle = m.title.toLowerCase().includes(q);
      const inServices = (m.key_aws_services || []).some(s => s.toLowerCase().includes(q));
      const inTopics = (m.topics || []).some(t => t.toLowerCase().includes(q));
      return inTitle || inServices || inTopics;
    }
    return true;
  });

  const getItemIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'file':
        return <FileText className="w-4 h-4 text-blue-500" />;
      case 'externaltool':
      case 'video':
        return <PlayCircle className="w-4 h-4 text-amber-500" />;
      case 'quiz':
        return <HelpCircle className="w-4 h-4 text-purple-500" />;
      default:
        return <BookOpen className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
            Course Curriculum & Modules
          </h1>
          <p className="text-xs text-slate-500">
            AWS Academy Cloud Foundations (ID: 183194) — All 10 Modules & Course Sections
          </p>
        </div>

        {/* Search & Filters */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search services or topics..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-4 py-2 rounded-xl text-xs bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-[#FF9900] w-56 transition-all"
            />
          </div>

          <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl text-xs font-medium">
            <button
              onClick={() => setFilterType('all')}
              className={`px-3 py-1 rounded-lg transition-all ${
                filterType === 'all' ? 'bg-white text-slate-900 shadow-xs font-bold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilterType('core')}
              className={`px-3 py-1 rounded-lg transition-all ${
                filterType === 'core' ? 'bg-white text-slate-900 shadow-xs font-bold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              10 Core Modules
            </button>
            <button
              onClick={() => setFilterType('labs')}
              className={`px-3 py-1 rounded-lg transition-all ${
                filterType === 'labs' ? 'bg-white text-slate-900 shadow-xs font-bold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Hands-on Labs (6)
            </button>
            <button
              onClick={() => setFilterType('additional')}
              className={`px-3 py-1 rounded-lg transition-all ${
                filterType === 'additional' ? 'bg-white text-slate-900 shadow-xs font-bold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Extra Sections
            </button>
          </div>
        </div>
      </div>

      {/* Modules List */}
      <div className="space-y-4">
        {filteredModules.map((module) => {
          const isExpanded = !!expandedModules[module.module_id];

          return (
            <div
              key={module.module_id}
              className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden transition-all"
            >
              {/* Header row */}
              <div
                onClick={() => toggleExpand(module.module_id)}
                className="p-5 flex items-center justify-between cursor-pointer hover:bg-slate-50/70 transition-colors"
              >
                <div className="flex items-center space-x-3.5 flex-1 min-w-0">
                  <span className={`text-xs font-extrabold px-2.5 py-1 rounded-lg shrink-0 ${
                    module.is_core_module 
                      ? 'bg-amber-100 text-amber-900 border border-amber-300' 
                      : 'bg-slate-100 text-slate-700 border border-slate-200'
                  }`}>
                    {module.is_core_module ? `Module ${module.module_number}` : 'Section'}
                  </span>

                  <div className="truncate">
                    <h3 className="font-bold text-slate-900 text-sm truncate">
                      {module.title}
                    </h3>
                    <p className="text-xs text-slate-500 truncate">
                      {module.description}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3 ml-4 shrink-0">
                  {module.has_lab && (
                    <span className="hidden sm:inline-flex items-center space-x-1 px-2.5 py-1 rounded-md text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      <Terminal className="w-3.5 h-3.5" />
                      <span>Lab Available</span>
                    </span>
                  )}

                  <span className="text-xs font-semibold text-slate-500">
                    {module.items.length} items
                  </span>

                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400" />
                  )}
                </div>
              </div>

              {/* Collapsible Content */}
              {isExpanded && (
                <div className="px-5 pb-5 pt-2 border-t border-slate-100 space-y-4 bg-slate-50/30">
                  
                  {/* Key Services & Topics Tags */}
                  {(module.key_aws_services?.length > 0 || module.topics?.length > 0) && (
                    <div className="flex flex-wrap items-center gap-1.5 pt-1">
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1">
                        Key AWS Services:
                      </span>
                      {module.key_aws_services?.map((svc, i) => (
                        <span key={i} className="text-[11px] font-medium bg-white px-2.5 py-0.5 rounded-full border border-slate-200 text-slate-700 shadow-2xs">
                          {svc}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Items List */}
                  <div className="space-y-2">
                    <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                      Module Learning Resources & Activities:
                    </div>

                    <div className="space-y-1.5 bg-white rounded-xl border border-slate-200 p-2.5">
                      {module.items.map((item) => (
                        <div
                          key={item.item_id}
                          className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 text-xs transition-colors"
                        >
                          <div className="flex items-center space-x-2.5 min-w-0">
                            {getItemIcon(item.type)}
                            <span className="font-semibold text-slate-800 truncate">
                              {item.title}
                            </span>
                          </div>

                          <div className="flex items-center space-x-3 shrink-0 ml-3">
                            <span className="text-[11px] text-slate-400 font-medium">
                              {item.time_estimate_mins} mins
                            </span>
                            <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                              {item.type}
                            </span>
                            {item.url && (
                              <a
                                href={item.url}
                                target="_blank"
                                rel="noreferrer"
                                className="text-slate-400 hover:text-slate-600"
                                title="Open in Canvas LMS"
                              >
                                <ExternalLink className="w-3.5 h-3.5" />
                              </a>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Actions for this module */}
                  <div className="flex items-center justify-between pt-2">
                    <div className="text-xs text-slate-500">
                      Module ID: <code className="bg-slate-100 px-1 py-0.5 rounded text-[11px] font-mono">{module.module_id}</code>
                    </div>

                    <div className="flex items-center space-x-2">
                      {module.has_lab && (
                        <button
                          onClick={() => navigateTo('labs', module.module_id, module.lab_id)}
                          className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition-all shadow-sm"
                        >
                          <Terminal className="w-3.5 h-3.5 text-amber-400" />
                          <span>Open Lab Assistant</span>
                        </button>
                      )}

                      <button
                        onClick={() => navigateTo('practice', module.module_id)}
                        className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                      >
                        <HelpCircle className="w-3.5 h-3.5" />
                        <span>Practice Questions</span>
                      </button>

                      <button
                        onClick={() => navigateTo('workspace', module.module_id)}
                        className="px-3.5 py-1.5 bg-[#FF9900] hover:bg-[#e68a00] text-slate-950 font-bold rounded-xl text-xs flex items-center space-x-1.5 transition-all shadow-sm"
                      >
                        <BookOpen className="w-3.5 h-3.5" />
                        <span>Study in Workspace</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                </div>
              )}
            </div>
          );
        })}
      </div>

    </div>
  );
};
