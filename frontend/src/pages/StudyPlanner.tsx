import React, { useState, useEffect } from 'react';
import { useCourse } from '../context/CourseContext';
import { api } from '../services/api';
import {
  Calendar,
  Clock,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  BookOpen,
  Terminal,
  HelpCircle,
  Sliders,
  ChevronRight,
  TrendingUp
} from 'lucide-react';
import { StudyPlan, StudyTask } from '../types';

export const StudyPlanner: React.FC = () => {
  const { progress, refreshProgress } = useCourse();
  const [studyPlan, setStudyPlan] = useState<StudyPlan | null>(null);
  const [weeklyHours, setWeeklyHours] = useState<number>(7);
  const [dailyMins, setDailyMins] = useState<number>(60);
  const [targetDate, setTargetDate] = useState<string>('2026-11-20');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    loadPlan();
  }, []);

  const loadPlan = async () => {
    setIsLoading(true);
    try {
      const plan = await api.getCurrentPlan();
      setStudyPlan(plan);
      if (plan) {
        setWeeklyHours(plan.weekly_hours_available || 7);
        setDailyMins(plan.daily_available_mins || 60);
        setTargetDate(plan.target_completion_date || '2026-11-20');
      }
    } catch (err) {
      console.error('Failed to load study plan:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGeneratePlan = async () => {
    setIsGenerating(true);
    try {
      const newPlan = await api.generateStudyPlan({
        target_completion_date: targetDate,
        weekly_hours: Number(weeklyHours),
        daily_study_mins: Number(dailyMins),
        prioritize_weak_topics: true,
        include_all_labs: true
      });
      setStudyPlan(newPlan);
      await refreshProgress();
    } catch (err) {
      console.error('Failed to generate study plan:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleToggleTask = async (taskId: string, currentStatus: boolean) => {
    if (!studyPlan) return;
    const newStatus = !currentStatus;

    // Optimistically update local UI
    const updatedSchedules = studyPlan.schedules.map(day => ({
      ...day,
      tasks: day.tasks.map(t => t.task_id === taskId ? { ...t, is_completed: newStatus } : t)
    }));
    setStudyPlan({ ...studyPlan, schedules: updatedSchedules });

    try {
      await api.toggleStudyTask(taskId, newStatus);
      await refreshProgress();
    } catch (err) {
      console.error('Failed to toggle task completion:', err);
    }
  };

  const getTaskIcon = (type: string) => {
    switch (type) {
      case 'lab':
        return <Terminal className="w-3.5 h-3.5 text-emerald-600" />;
      case 'practice_quiz':
        return <HelpCircle className="w-3.5 h-3.5 text-purple-600" />;
      case 'revision':
        return <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />;
      default:
        return <BookOpen className="w-3.5 h-3.5 text-blue-600" />;
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Top Banner & Generation Parameters */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-5">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-slate-900 bg-[#FF9900] px-2.5 py-0.5 rounded-md shadow-2xs">
                Intelligent Study Planner
              </span>
              <span className="text-xs text-slate-500 font-semibold">• Adaptive Daily Scheduling</span>
            </div>
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight mt-1">
              Personalized Course Schedule
            </h1>
            <p className="text-xs text-slate-500">
              Adapts dynamically to prioritize weak topics, unfinished labs, and remaining curriculum modules.
            </p>
          </div>

          <button
            onClick={handleGeneratePlan}
            disabled={isGenerating}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white font-bold text-xs rounded-xl flex items-center space-x-2 shadow-sm transition-all self-start md:self-auto"
          >
            <Sparkles className="w-4 h-4 text-[#FF9900]" />
            <span>{isGenerating ? 'Recalculating Plan...' : 'Regenerate Adaptive Plan'}</span>
          </button>
        </div>

        {/* Configuration Sliders & Target Inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-slate-100">
          
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700 flex items-center justify-between">
              <span>Weekly Available Time</span>
              <span className="text-[#0073bb] font-extrabold">{weeklyHours} Hours/week</span>
            </label>
            <input
              type="range"
              min="3"
              max="25"
              step="1"
              value={weeklyHours}
              onChange={(e) => setWeeklyHours(Number(e.target.value))}
              className="w-full accent-[#FF9900] cursor-pointer"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700 flex items-center justify-between">
              <span>Daily Study Target</span>
              <span className="text-[#0073bb] font-extrabold">{dailyMins} Mins/day</span>
            </label>
            <select
              value={dailyMins}
              onChange={(e) => setDailyMins(Number(e.target.value))}
              className="w-full text-xs font-semibold bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 focus:ring-2 focus:ring-[#FF9900]"
            >
              <option value="30">30 minutes / day</option>
              <option value="45">45 minutes / day</option>
              <option value="60">60 minutes (Recommended)</option>
              <option value="90">90 minutes / day (Intensive)</option>
              <option value="120">120 minutes / day</option>
            </select>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700">
              Target Completion Date
            </label>
            <input
              type="date"
              value={targetDate}
              onChange={(e) => setTargetDate(e.target.value)}
              className="w-full text-xs font-semibold bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 focus:ring-2 focus:ring-[#FF9900]"
            />
          </div>

        </div>
      </div>

      {/* Focus Areas Pill Bar */}
      {studyPlan?.focus_areas && studyPlan.focus_areas.length > 0 && (
        <div className="bg-amber-50/70 border border-amber-200/80 rounded-2xl p-4 flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider text-amber-900 flex items-center space-x-1.5 mr-2">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            <span>Active Priority Focus Areas:</span>
          </span>
          {studyPlan.focus_areas.map((fa, i) => (
            <span
              key={i}
              className="text-xs font-semibold bg-white text-amber-900 px-3 py-1 rounded-xl border border-amber-200 shadow-2xs"
            >
              🎯 {fa}
            </span>
          ))}
        </div>
      )}

      {/* Day by Day Schedule Timeline */}
      {isLoading ? (
        <div className="bg-white p-12 rounded-2xl border border-slate-200 text-center">
          <Sparkles className="w-6 h-6 animate-spin text-[#FF9900] mx-auto" />
          <p className="text-xs font-semibold text-slate-600 mt-2">Loading study schedule...</p>
        </div>
      ) : (
        <div className="space-y-4">
          <h2 className="font-bold text-slate-900 text-sm">
            Daily Study Schedule (Next 7 Days)
          </h2>

          <div className="space-y-4">
            {(studyPlan?.schedules || []).map((day) => (
              <div
                key={day.day_number}
                className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden"
              >
                {/* Day Header */}
                <div className="p-4 bg-slate-50/70 border-b border-slate-100 flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center space-x-3">
                    <span className="w-8 h-8 rounded-xl bg-slate-900 text-amber-400 font-extrabold text-xs flex items-center justify-center shadow-2xs">
                      D{day.day_number}
                    </span>
                    <div>
                      <div className="font-bold text-slate-900 text-xs sm:text-sm">
                        {day.focus_topic}
                      </div>
                      <div className="text-[11px] text-slate-400">
                        Date: {day.date}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    <span className="text-xs font-semibold text-slate-600 flex items-center space-x-1">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      <span>{day.target_study_mins} mins target</span>
                    </span>
                    <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-slate-200/70 text-slate-700">
                      {day.tasks.filter(t => t.is_completed).length}/{day.tasks.length} Completed
                    </span>
                  </div>
                </div>

                {/* Day Tasks List */}
                <div className="p-4 space-y-2">
                  {day.tasks.map((task) => (
                    <div
                      key={task.task_id}
                      className={`p-3 rounded-xl border flex items-start justify-between gap-3 text-xs transition-all ${
                        task.is_completed
                          ? 'bg-emerald-50/40 border-emerald-200'
                          : 'bg-white border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <div className="flex items-start space-x-3 min-w-0 flex-1">
                        <input
                          type="checkbox"
                          checked={task.is_completed}
                          onChange={() => handleToggleTask(task.task_id, task.is_completed)}
                          className="w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500 cursor-pointer mt-0.5"
                        />

                        <div className="space-y-0.5 min-w-0">
                          <div className="flex items-center space-x-2">
                            {getTaskIcon(task.task_type)}
                            <span className={`font-bold truncate ${
                              task.is_completed ? 'line-through text-slate-400' : 'text-slate-900'
                            }`}>
                              {task.title}
                            </span>
                          </div>

                          {task.reason && (
                            <p className="text-[11px] text-slate-500 italic pl-5.5">
                              "{task.reason}"
                            </p>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center space-x-2 shrink-0">
                        <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                          {task.task_type.replace('_', ' ')}
                        </span>
                        <span className="text-[11px] font-semibold text-slate-500">
                          {task.duration_mins}m
                        </span>
                        {task.priority === 'high' && (
                          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800">
                            High Priority
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
};
