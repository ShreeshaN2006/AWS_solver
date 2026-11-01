import React, { createContext, useContext, useState, useEffect } from 'react';
import { Course, CourseModule, UserOverallProgress, PageView, SystemSettings } from '../types';
import { api } from '../services/api';

interface CourseContextType {
  activePage: PageView;
  setActivePage: (page: PageView) => void;
  selectedModuleId: string | null;
  setSelectedModuleId: (id: string | null) => void;
  selectedLabId: string | null;
  setSelectedLabId: (id: string | null) => void;
  course: Course | null;
  modules: CourseModule[];
  progress: UserOverallProgress | null;
  settings: SystemSettings | null;
  isLoading: boolean;
  navigateTo: (page: PageView, moduleId?: string, labId?: string) => void;
  refreshProgress: () => Promise<void>;
  refreshCourse: () => Promise<void>;
  refreshSettings: () => Promise<void>;
}

const CourseContext = createContext<CourseContextType | undefined>(undefined);

export const CourseProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activePage, setActivePage] = useState<PageView>('dashboard');
  const [selectedModuleId, setSelectedModuleId] = useState<string | null>('10101');
  const [selectedLabId, setSelectedLabId] = useState<string | null>('lab_1');
  const [course, setCourse] = useState<Course | null>(null);
  const [modules, setModules] = useState<CourseModule[]>([]);
  const [progress, setProgress] = useState<UserOverallProgress | null>(null);
  const [settings, setSettings] = useState<SystemSettings | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshCourse = async () => {
    try {
      const courseData = await api.getCourse();
      setCourse(courseData);
      setModules(courseData.modules || []);
    } catch (err) {
      console.error('Error fetching course:', err);
    }
  };

  const refreshProgress = async () => {
    try {
      const prog = await api.getProgressAnalytics();
      setProgress(prog);
    } catch (err) {
      console.error('Error fetching progress:', err);
    }
  };

  const refreshSettings = async () => {
    try {
      const sett = await api.getSettings();
      setSettings(sett);
    } catch (err) {
      console.error('Error fetching settings:', err);
    }
  };

  useEffect(() => {
    const init = async () => {
      setIsLoading(true);
      await Promise.all([refreshCourse(), refreshProgress(), refreshSettings()]);
      setIsLoading(false);
    };
    init();
  }, []);

  const navigateTo = (page: PageView, moduleId?: string, labId?: string) => {
    if (moduleId) setSelectedModuleId(moduleId);
    if (labId) setSelectedLabId(labId);
    setActivePage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <CourseContext.Provider
      value={{
        activePage,
        setActivePage,
        selectedModuleId,
        setSelectedModuleId,
        selectedLabId,
        setSelectedLabId,
        course,
        modules,
        progress,
        settings,
        isLoading,
        navigateTo,
        refreshProgress,
        refreshCourse,
        refreshSettings,
      }}
    >
      {children}
    </CourseContext.Provider>
  );
};

export const useCourse = () => {
  const context = useContext(CourseContext);
  if (!context) {
    throw new Error('useCourse must be used within a CourseProvider');
  }
  return context;
};
