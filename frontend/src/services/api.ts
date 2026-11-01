import {
  Course,
  CourseModule,
  ChatMessage,
  ChatSession,
  PracticeQuestion,
  PracticeAttempt,
  LabDetail,
  UserLabProgress,
  UserOverallProgress,
  StudyPlan,
  LearningDocument,
  DocumentChunk,
  SystemSettings
} from '../types';

const API_BASE = '/api';

export const api = {
  // Courses
  async getCourse(): Promise<Course> {
    const res = await fetch(`${API_BASE}/courses/183194`);
    if (!res.ok) throw new Error('Failed to fetch course details');
    return res.json();
  },

  async getModules(coreOnly: boolean = false): Promise<CourseModule[]> {
    const res = await fetch(`${API_BASE}/courses/183194/modules?core_only=${coreOnly}`);
    if (!res.ok) throw new Error('Failed to fetch modules');
    return res.json();
  },

  async getModule(moduleId: string): Promise<CourseModule> {
    const res = await fetch(`${API_BASE}/courses/183194/modules/${moduleId}`);
    if (!res.ok) throw new Error('Failed to fetch module details');
    return res.json();
  },

  // Chat / AI Tutor
  async sendChatMessage(params: {
    message: string;
    session_id?: string;
    module_id?: string;
    lesson_id?: string;
  }): Promise<{
    session_id: string;
    message: string;
    citations: any[];
    suggested_followups: string[];
    used_tools: string[];
  }> {
    const res = await fetch(`${API_BASE}/chat/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Chat request failed');
    return res.json();
  },

  async getChatSessions(): Promise<ChatSession[]> {
    const res = await fetch(`${API_BASE}/chat/sessions`);
    if (!res.ok) throw new Error('Failed to fetch chat sessions');
    return res.json();
  },

  async getSessionMessages(sessionId: string): Promise<ChatMessage[]> {
    const res = await fetch(`${API_BASE}/chat/sessions/${sessionId}/messages`);
    if (!res.ok) throw new Error('Failed to fetch session messages');
    return res.json();
  },

  // Practice & Knowledge Check
  async getPracticeQuestions(params?: {
    module_id?: string;
    difficulty?: string;
    question_type?: string;
    limit?: number;
  }): Promise<PracticeQuestion[]> {
    const searchParams = new URLSearchParams();
    if (params?.module_id) searchParams.append('module_id', params.module_id);
    if (params?.difficulty) searchParams.append('difficulty', params.difficulty);
    if (params?.question_type) searchParams.append('question_type', params.question_type);
    if (params?.limit) searchParams.append('limit', params.limit.toString());

    const res = await fetch(`${API_BASE}/practice/questions?${searchParams.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch questions');
    return res.json();
  },

  async submitPracticeSession(body: {
    module_id?: string;
    is_comprehensive_exam: boolean;
    answers: Array<{ question_id: string; selected_option_id: string }>;
    time_spent_seconds: number;
  }): Promise<PracticeAttempt> {
    const res = await fetch(`${API_BASE}/practice/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error('Failed to submit practice answers');
    return res.json();
  },

  async getPracticeAttempts(): Promise<PracticeAttempt[]> {
    const res = await fetch(`${API_BASE}/practice/attempts`);
    if (!res.ok) throw new Error('Failed to fetch practice attempts');
    return res.json();
  },

  // Labs
  async getLabs(): Promise<LabDetail[]> {
    const res = await fetch(`${API_BASE}/labs`);
    if (!res.ok) throw new Error('Failed to fetch labs');
    return res.json();
  },

  async getLab(labId: string): Promise<LabDetail> {
    const res = await fetch(`${API_BASE}/labs/${labId}`);
    if (!res.ok) throw new Error('Failed to fetch lab');
    return res.json();
  },

  async getLabProgress(labId: string): Promise<UserLabProgress> {
    const res = await fetch(`${API_BASE}/labs/${labId}/progress`);
    if (!res.ok) throw new Error('Failed to fetch lab progress');
    return res.json();
  },

  async confirmLabStep(labId: string, stepNumber: number, confirmed: boolean): Promise<any> {
    const res = await fetch(`${API_BASE}/labs/${labId}/steps/${stepNumber}/confirm`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ confirmed }),
    });
    if (!res.ok) throw new Error('Failed to confirm step');
    return res.json();
  },

  async troubleshootLab(params: {
    lab_id: string;
    step_number: number;
    error_message?: string;
    screenshot_base64?: string;
    user_description: string;
  }): Promise<any> {
    const res = await fetch(`${API_BASE}/labs/troubleshoot`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Failed to diagnose lab error');
    return res.json();
  },

  // Progress & Analytics
  async getProgressAnalytics(): Promise<UserOverallProgress> {
    const res = await fetch(`${API_BASE}/progress/analytics`);
    if (!res.ok) throw new Error('Failed to fetch progress analytics');
    return res.json();
  },

  async updateItemProgress(params: {
    module_id: string;
    item_id: string;
    completed: boolean;
    time_spent_mins?: number;
  }): Promise<any> {
    const res = await fetch(`${API_BASE}/progress/item`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Failed to update item progress');
    return res.json();
  },

  // Study Planner
  async getCurrentPlan(): Promise<StudyPlan> {
    const res = await fetch(`${API_BASE}/planner/current`);
    if (!res.ok) throw new Error('Failed to fetch current plan');
    return res.json();
  },

  async generateStudyPlan(params: {
    target_completion_date?: string;
    weekly_hours: number;
    daily_study_mins: number;
    prioritize_weak_topics: boolean;
    include_all_labs: boolean;
  }): Promise<StudyPlan> {
    const res = await fetch(`${API_BASE}/planner/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error('Failed to generate study plan');
    return res.json();
  },

  async toggleStudyTask(taskId: string, completed: boolean): Promise<any> {
    const res = await fetch(`${API_BASE}/planner/task/${taskId}/toggle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed }),
    });
    if (!res.ok) throw new Error('Failed to toggle task');
    return res.json();
  },

  // Documents & RAG
  async getDocuments(): Promise<LearningDocument[]> {
    const res = await fetch(`${API_BASE}/documents`);
    if (!res.ok) throw new Error('Failed to fetch documents');
    return res.json();
  },

  async getChunks(moduleId?: string, limit: number = 30): Promise<DocumentChunk[]> {
    const url = moduleId && moduleId !== 'all'
      ? `${API_BASE}/documents/chunks?module_id=${moduleId}&limit=${limit}`
      : `${API_BASE}/documents/chunks?limit=${limit}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch document chunks');
    return res.json();
  },

  async importCanvasHtml(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/documents/import-canvas-html`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to parse Canvas HTML export');
    return res.json();
  },

  async uploadDocument(file: File, moduleId: string, moduleTitle: string, docType: string): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('module_id', moduleId);
    formData.append('module_title', moduleTitle);
    formData.append('doc_type', docType);

    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to upload document');
    return res.json();
  },

  // Canvas LMS & Settings
  async getCanvasStatus(): Promise<any> {
    const res = await fetch(`${API_BASE}/canvas/status`);
    if (!res.ok) throw new Error('Failed to fetch Canvas status');
    return res.json();
  },

  async syncCanvas(): Promise<any> {
    const res = await fetch(`${API_BASE}/canvas/sync`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to sync with Canvas LMS');
    return res.json();
  },

  async getSettings(): Promise<SystemSettings> {
    const res = await fetch(`${API_BASE}/settings`);
    if (!res.ok) throw new Error('Failed to fetch settings');
    return res.json();
  },

  async updateProvider(provider: string, openaiKey?: string, awsKey?: string, awsSecret?: string): Promise<any> {
    const res = await fetch(`${API_BASE}/settings/provider`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider,
        openai_key: openaiKey,
        aws_key: awsKey,
        aws_secret: awsSecret,
      }),
    });
    if (!res.ok) throw new Error('Failed to update provider');
    return res.json();
  },
};
