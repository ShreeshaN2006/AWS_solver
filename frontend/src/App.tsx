import React from 'react';
import { CourseProvider, useCourse } from './context/CourseContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

// Pages
import { Dashboard } from './pages/Dashboard';
import { CourseModules } from './pages/CourseModules';
import { LearningWorkspace } from './pages/LearningWorkspace';
import { TutorChat } from './pages/TutorChat';
import { KnowledgeCheck } from './pages/KnowledgeCheck';
import { LabAssistant } from './pages/LabAssistant';
import { ProgressAnalytics } from './pages/ProgressAnalytics';
import { StudyPlanner } from './pages/StudyPlanner';
import { DocumentLibrary } from './pages/DocumentLibrary';
import { SettingsPage } from './pages/SettingsPage';

const AppContent: React.FC = () => {
  const { activePage, isLoading } = useCourse();

  const renderActivePage = () => {
    switch (activePage) {
      case 'dashboard':
        return <Dashboard />;
      case 'modules':
        return <CourseModules />;
      case 'workspace':
        return <LearningWorkspace />;
      case 'chat':
        return <TutorChat />;
      case 'practice':
        return <KnowledgeCheck />;
      case 'labs':
        return <LabAssistant />;
      case 'progress':
        return <ProgressAnalytics />;
      case 'planner':
        return <StudyPlanner />;
      case 'documents':
        return <DocumentLibrary />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />
      
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <Sidebar />
        
        <main className="flex-1 p-4 sm:p-6 lg:p-8 min-w-0 overflow-y-auto">
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <CourseProvider>
      <AppContent />
    </CourseProvider>
  );
};

export default App;
