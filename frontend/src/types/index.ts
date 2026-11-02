export type PageView = 
  | 'dashboard'
  | 'modules'
  | 'workspace'
  | 'chat'
  | 'practice'
  | 'labs'
  | 'progress'
  | 'planner'
  | 'documents'
  | 'settings';

export interface ModuleItem {
  item_id: string;
  module_id: string;
  title: string;
  type: string;
  url?: string;
  position: number;
  description?: string;
  is_completed: boolean;
  time_estimate_mins: number;
}

export interface CourseModule {
  module_id: string;
  course_id: string;
  module_number: number;
  title: string;
  description?: string;
  is_core_module: boolean;
  order: number;
  items: ModuleItem[];
  progress_percentage: number;
  status: 'Not Started' | 'In Progress' | 'Needs Revision' | 'Ready for Assessment' | 'Completed';
  has_lab: boolean;
  lab_id?: string;
  key_aws_services: string[];
  topics: string[];
}

export interface Course {
  course_id: string;
  name: string;
  code: string;
  canvas_url: string;
  total_modules: number;
  modules: CourseModule[];
}

export interface Citation {
  module_id?: string;
  module_title?: string;
  document_name: string;
  page_number?: number;
  timestamp?: string;
  source_url?: string;
  snippet: string;
  confidence: number;
}

export interface ChatMessage {
  message_id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  citations?: Citation[];
  tool_calls?: any[];
  module_context?: string;
  lesson_context?: string;
  created_at: string;
}

export interface ChatSession {
  session_id: string;
  user_id: string;
  title: string;
  current_module_id?: string;
  current_lesson_id?: string;
  created_at: string;
  updated_at: string;
}

export interface QuestionOption {
  id: string;
  text: string;
}

export interface PracticeQuestion {
  question_id: string;
  module_id: string;
  module_title: string;
  question_type: 'multiple_choice' | 'true_false' | 'scenario' | 'conceptual' | 'difficult';
  difficulty: 'easy' | 'medium' | 'hard';
  prompt: string;
  scenario?: string;
  options: QuestionOption[];
  correct_option_id: string;
  explanation: string;
  concept_tags: string[];
  aws_services: string[];
  source_reference?: string;
}

export interface QuestionResult {
  question_id: string;
  prompt: string;
  selected_option_id: string;
  correct_option_id: string;
  is_correct: boolean;
  explanation: string;
  concept_tags: string[];
  aws_services: string[];
}

export interface PracticeAttempt {
  attempt_id: string;
  user_id: string;
  module_id?: string;
  module_title?: string;
  is_comprehensive_exam: boolean;
  total_questions: number;
  correct_count: number;
  score_percentage: number;
  time_spent_seconds: number;
  results: QuestionResult[];
  weak_concepts: string[];
  recommended_revision_topics: string[];
  created_at: string;
}

export interface LabStep {
  step_number: number;
  title: string;
  objective: string;
  console_navigation: string;
  instructions: string[];
  expected_result: string;
  common_pitfalls: string[];
  verification_check: string;
}

export interface LabDetail {
  lab_id: string;
  lab_number: number;
  title: string;
  duration_mins: number;
  module_id: string;
  module_title: string;
  objective: string;
  aws_services: string[];
  architecture_summary: string;
  steps: LabStep[];
  final_summary: string;
}

export interface UserLabProgress {
  user_id: string;
  lab_id: string;
  current_step: number;
  total_steps: number;
  completed_steps: number[];
  is_completed: boolean;
  started_at: string;
}

export interface UserModuleProgress {
  module_id: string;
  module_number: number;
  title: string;
  status: 'Not Started' | 'In Progress' | 'Needs Revision' | 'Ready for Assessment' | 'Completed';
  progress_percentage: number;
  items_completed: number;
  total_items: number;
  lab_completed: boolean;
  practice_best_score?: number;
  has_lab: boolean;
  lab_id?: string;
}

export interface UserOverallProgress {
  user_id: string;
  course_id: string;
  total_study_time_mins: number;
  overall_progress_percentage: number;
  total_modules: number;
  completed_modules: number;
  in_progress_modules: number;
  remaining_modules: number;
  modules_progress: UserModuleProgress[];
  understood_topics: string[];
  weak_topics: string[];
  recent_activities: Array<{ type: string; title: string; time: string; module: string }>;
  upcoming_tasks: Array<{ id: string; title: string; due: string; priority: string; type: string }>;
  recommended_next_activity?: {
    title: string;
    type: string;
    module_id: string;
    module_title: string;
    action_url: string;
    reason: string;
  };
}

export interface StudyTask {
  task_id: string;
  title: string;
  module_id?: string;
  module_title?: string;
  task_type: 'reading' | 'video' | 'lab' | 'practice_quiz' | 'revision';
  duration_mins: number;
  is_completed: boolean;
  priority: 'high' | 'medium' | 'low';
  reason?: string;
}

export interface DailySchedule {
  day_number: number;
  date: string;
  focus_topic: string;
  target_study_mins: number;
  tasks: StudyTask[];
  is_rest_day: boolean;
}

export interface StudyPlan {
  plan_id: string;
  user_id: string;
  course_id: string;
  target_completion_date: string;
  weekly_hours_available: number;
  daily_available_mins: number;
  learning_pace: string;
  schedules: DailySchedule[];
  total_estimated_hours: number;
  focus_areas: string[];
}

export interface LearningDocument {
  doc_id: string;
  course_id: string;
  module_id: string;
  module_title: string;
  title: string;
  file_type: string;
  original_filename: string;
  file_size_bytes: number;
  chunk_count: number;
  source_url?: string;
  uploaded_at: string;
  processed: boolean;
}

export interface DocumentChunk {
  chunk_id: string;
  doc_id: string;
  course_id: string;
  module_id: string;
  module_title: string;
  document_name: string;
  page_number?: number;
  timestamp?: string;
  content: string;
  source_url?: string;
  score?: number;
}

export interface SystemSettings {
  llm_provider: string;
  openai_model: string;
  openai_has_key: boolean;
  bedrock_model_id: string;
  bedrock_region: string;
  bedrock_has_credentials: boolean;
  bedrock_uses_default_credential_chain: boolean;
  canvas_base_url: string;
  canvas_course_id: string;
  canvas_has_token: boolean;
  mongodb_configured: boolean;
  mongodb_db: string;
}
