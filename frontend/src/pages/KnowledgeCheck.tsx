import React, { useState, useEffect } from 'react';
import { useCourse } from '../context/CourseContext';
import { api } from '../services/api';
import {
  CheckSquare,
  HelpCircle,
  Award,
  AlertTriangle,
  RotateCcw,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  XCircle,
  ShieldAlert,
  Clock,
  Layers,
  BookOpen
} from 'lucide-react';
import { PracticeQuestion, PracticeAttempt } from '../types';

export const KnowledgeCheck: React.FC = () => {
  const { modules, selectedModuleId, navigateTo, refreshProgress } = useCourse();

  // Configuration
  const [selectedModule, setSelectedModule] = useState<string>(selectedModuleId || '10101');
  const [isComprehensive, setIsComprehensive] = useState<boolean>(false);
  const [difficultyFilter, setDifficultyFilter] = useState<string>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');

  // Active Quiz State
  const [questions, setQuestions] = useState<PracticeQuestion[]>([]);
  const [currentIdx, setCurrentIdx] = useState<number>(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [showImmediateFeedback, setShowImmediateFeedback] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [attemptResult, setAttemptResult] = useState<PracticeAttempt | null>(null);

  // Prior Attempts
  const [pastAttempts, setPastAttempts] = useState<PracticeAttempt[]>([]);

  useEffect(() => {
    loadQuestions();
    loadPastAttempts();
  }, [selectedModule, isComprehensive, difficultyFilter, typeFilter]);

  const loadQuestions = async () => {
    setIsLoading(true);
    setIsSubmitted(false);
    setAttemptResult(null);
    setCurrentIdx(0);
    setSelectedAnswers({});

    try {
      const qList = await api.getPracticeQuestions({
        module_id: isComprehensive ? undefined : selectedModule,
        difficulty: difficultyFilter !== 'all' ? difficultyFilter : undefined,
        question_type: typeFilter !== 'all' ? typeFilter : undefined,
        limit: isComprehensive ? 15 : 6,
      });
      setQuestions(qList);
    } catch (err) {
      console.error('Failed to load questions:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const loadPastAttempts = async () => {
    try {
      const atts = await api.getPracticeAttempts();
      setPastAttempts(atts);
    } catch (err) {
      console.error('Failed to load past attempts:', err);
    }
  };

  const handleSelectOption = (questionId: string, optionId: string) => {
    if (isSubmitted) return;
    setSelectedAnswers(prev => ({ ...prev, [questionId]: optionId }));
  };

  const handleSubmitQuiz = async () => {
    if (questions.length === 0) return;

    const answersPayload = questions.map(q => ({
      question_id: q.question_id,
      selected_option_id: selectedAnswers[q.question_id] || 'NONE'
    }));

    try {
      const result = await api.submitPracticeSession({
        module_id: isComprehensive ? undefined : selectedModule,
        is_comprehensive_exam: isComprehensive,
        answers: answersPayload,
        time_spent_seconds: 180,
      });

      setAttemptResult(result);
      setIsSubmitted(true);
      await refreshProgress();
      await loadPastAttempts();
    } catch (err) {
      console.error('Submission failed:', err);
    }
  };

  const currentQ = questions[currentIdx];
  const totalQ = questions.length;
  const answeredCount = Object.keys(selectedAnswers).length;

  return (
    <div className="space-y-6">
      
      {/* Header & Modes */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200">
              Assessment Prep Agent
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-500 font-medium">Practice & Knowledge Check</span>
          </div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight mt-1">
            AWS Knowledge Check Practice
          </h1>
        </div>

        {/* Mode Selector */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center bg-slate-100 p-1 rounded-xl text-xs font-medium">
            <button
              onClick={() => setIsComprehensive(false)}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                !isComprehensive
                  ? 'bg-white text-slate-900 font-bold shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Module Knowledge Check
            </button>
            <button
              onClick={() => setIsComprehensive(true)}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                isComprehensive
                  ? 'bg-white text-slate-900 font-bold shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Full Course Mock Exam
            </button>
          </div>

          {!isComprehensive && (
            <select
              value={selectedModule}
              onChange={(e) => setSelectedModule(e.target.value)}
              className="text-xs font-bold text-slate-800 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 focus:ring-2 focus:ring-[#FF9900]"
            >
              {modules.filter(m => m.is_core_module).map((m) => (
                <option key={m.module_id} value={m.module_id}>
                  Module {m.module_number}: {m.title}
                </option>
              ))}
            </select>
          )}
        </div>
      </div>

      {/* Safety Notice Banner (Requirement 6 Compliance) */}
      <div className="bg-amber-50/70 border border-amber-200/80 rounded-xl p-3 flex items-start space-x-2.5 text-xs text-amber-900">
        <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Student Independence Safeguard:</span> All practice questions are originally generated by the AI agent to prepare you for examinations. The copilot does not and will never automatically answer, select, or submit official live graded Canvas LMS quizzes.
        </div>
      </div>

      {/* Main Quiz Area */}
      {isLoading ? (
        <div className="bg-white p-12 rounded-2xl border border-slate-200/80 text-center space-y-3">
          <Sparkles className="w-6 h-6 animate-spin text-[#FF9900] mx-auto" />
          <p className="text-sm font-semibold text-slate-600">Generating practice questions from course material...</p>
        </div>
      ) : questions.length === 0 ? (
        <div className="bg-white p-12 rounded-2xl border border-slate-200/80 text-center space-y-3">
          <HelpCircle className="w-8 h-8 text-slate-300 mx-auto" />
          <h3 className="font-bold text-slate-800 text-sm">No practice questions found for this filter.</h3>
          <p className="text-xs text-slate-500">Try choosing another module or switching filters to All.</p>
        </div>
      ) : isSubmitted && attemptResult ? (
        
        /* Post-Quiz Results Summary (Requirement 6) */
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
              <div className="flex items-center space-x-4">
                <div className={`w-16 h-16 rounded-2xl flex flex-col items-center justify-center font-extrabold ${
                  attemptResult.score_percentage >= 70
                    ? 'bg-emerald-100 text-emerald-800 border-2 border-emerald-300'
                    : 'bg-amber-100 text-amber-800 border-2 border-amber-300'
                }`}>
                  <span className="text-xl">{attemptResult.score_percentage}%</span>
                  <span className="text-[10px] uppercase font-bold">Score</span>
                </div>

                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Assessment Result
                    </span>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                      attemptResult.score_percentage >= 70
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}>
                      {attemptResult.score_percentage >= 70 ? 'Passed (>=70%)' : 'Needs Revision'}
                    </span>
                  </div>
                  <h2 className="text-lg font-bold text-slate-900">
                    {attemptResult.correct_count} of {attemptResult.total_questions} Questions Answered Correctly
                  </h2>
                  <p className="text-xs text-slate-500">
                    Target passing score for AWS Certified Cloud Practitioner is 70%.
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={loadQuestions}
                  className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold rounded-xl flex items-center space-x-1.5 transition-colors"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Retake Practice</span>
                </button>
                <button
                  onClick={() => navigateTo('chat')}
                  className="px-4 py-2 bg-[#FF9900] hover:bg-[#e68a00] text-slate-950 text-xs font-bold rounded-xl flex items-center space-x-1.5 transition-all shadow-sm"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Review Weak Topics with AI</span>
                </button>
              </div>
            </div>

            {/* Weak Concepts & Recommended Revision Topics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-amber-50/60 p-4 rounded-xl border border-amber-200/60 space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-amber-800 flex items-center space-x-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Weak Concepts Detected</span>
                </h3>
                <div className="flex flex-wrap gap-1.5">
                  {attemptResult.weak_concepts.length > 0 ? (
                    attemptResult.weak_concepts.map((c, i) => (
                      <span key={i} className="text-xs font-semibold bg-white text-amber-900 px-2.5 py-1 rounded-lg border border-amber-200 shadow-2xs">
                        {c}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-emerald-700 font-semibold">
                      🎉 Outstanding mastery! No weak concepts identified.
                    </span>
                  )}
                </div>
              </div>

              <div className="bg-blue-50/60 p-4 rounded-xl border border-blue-200/60 space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-blue-800 flex items-center space-x-1.5">
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Recommended Revision Topics</span>
                </h3>
                <div className="space-y-1">
                  {attemptResult.recommended_revision_topics.map((t, i) => (
                    <div key={i} className="text-xs font-medium text-blue-900 flex items-center space-x-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
                      <span>{t}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Detailed Question Review Rubric */}
            <div className="space-y-4 pt-2">
              <h3 className="font-bold text-slate-900 text-sm">
                Question Review & Detailed Explanations
              </h3>

              <div className="space-y-4">
                {attemptResult.results.map((res, i) => (
                  <div
                    key={i}
                    className={`p-4 rounded-xl border space-y-2.5 ${
                      res.is_correct
                        ? 'bg-white border-emerald-200'
                        : 'bg-red-50/20 border-red-200'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-start space-x-2">
                        {res.is_correct ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                        ) : (
                          <XCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                        )}
                        <span className="font-bold text-xs text-slate-900">
                          Question {i + 1}: {res.prompt}
                        </span>
                      </div>
                      <span className={`text-[11px] font-bold px-2 py-0.5 rounded ${
                        res.is_correct ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {res.is_correct ? 'Correct' : 'Incorrect'}
                      </span>
                    </div>

                    <div className="text-xs space-y-1 pl-6">
                      <div className="text-slate-600">
                        <strong>Your Answer:</strong> Option {res.selected_option_id}
                      </div>
                      {!res.is_correct && (
                        <div className="text-emerald-700 font-semibold">
                          <strong>Correct Answer:</strong> Option {res.correct_option_id}
                        </div>
                      )}
                      <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200/60 text-slate-700 text-xs mt-1.5">
                        <strong>Explanation:</strong> {res.explanation}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

      ) : (

        /* Active Question Display */
        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-6">
          
          {/* Progress within current test */}
          <div className="flex items-center justify-between text-xs text-slate-500 font-semibold border-b border-slate-100 pb-3">
            <div className="flex items-center space-x-2">
              <span className="bg-slate-100 px-2.5 py-1 rounded-md text-slate-700">
                Question {currentIdx + 1} of {totalQ}
              </span>
              <span className="capitalize text-slate-400">
                Type: {currentQ.question_type.replace('_', ' ')}
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${
                currentQ.difficulty === 'hard' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
              }`}>
                {currentQ.difficulty}
              </span>
            </div>

            <div className="flex items-center space-x-2">
              <span>{answeredCount}/{totalQ} Answered</span>
            </div>
          </div>

          {/* Scenario Callout if present */}
          {currentQ.scenario && (
            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs text-slate-700 space-y-1">
              <span className="font-bold text-slate-900 uppercase tracking-wider text-[10px] flex items-center space-x-1">
                <BookOpen className="w-3 h-3 text-[#FF9900]" />
                <span>Scenario Context:</span>
              </span>
              <p className="italic">{currentQ.scenario}</p>
            </div>
          )}

          {/* Prompt */}
          <h2 className="text-base font-bold text-slate-900 leading-snug">
            {currentQ.prompt}
          </h2>

          {/* Option Choices */}
          <div className="space-y-2.5">
            {currentQ.options.map((opt) => {
              const isSelected = selectedAnswers[currentQ.question_id] === opt.id;

              return (
                <div
                  key={opt.id}
                  onClick={() => handleSelectOption(currentQ.question_id, opt.id)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all flex items-start space-x-3 text-xs ${
                    isSelected
                      ? 'bg-amber-50/70 border-[#FF9900] ring-1 ring-[#FF9900] text-slate-900'
                      : 'bg-white border-slate-200 hover:border-slate-300 text-slate-700'
                  }`}
                >
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                    isSelected
                      ? 'bg-[#FF9900] text-slate-950 font-extrabold'
                      : 'bg-slate-100 text-slate-600'
                  }`}>
                    {opt.id}
                  </div>
                  <span className="font-medium text-xs sm:text-sm leading-relaxed">
                    {opt.text}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Immediate Feedback if enabled and option chosen */}
          {showImmediateFeedback && selectedAnswers[currentQ.question_id] && (
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5 text-xs">
              <div className="font-bold text-slate-800 flex items-center space-x-1.5">
                <HelpCircle className="w-3.5 h-3.5 text-[#FF9900]" />
                <span>Curriculum Explanation:</span>
              </div>
              <p className="text-slate-600 leading-relaxed">
                {currentQ.explanation}
              </p>
              {currentQ.source_reference && (
                <div className="text-[10px] text-slate-400 font-semibold pt-1">
                  Source: {currentQ.source_reference}
                </div>
              )}
            </div>
          )}

          {/* Footer Controls */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-100">
            <button
              onClick={() => setCurrentIdx(prev => Math.max(0, prev - 1))}
              disabled={currentIdx === 0}
              className="px-4 py-2 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 disabled:opacity-40 rounded-xl transition-colors"
            >
              Previous
            </button>

            <div className="flex items-center space-x-2">
              {currentIdx < totalQ - 1 ? (
                <button
                  onClick={() => setCurrentIdx(prev => Math.min(totalQ - 1, prev + 1))}
                  className="px-4 py-2 text-xs font-bold text-slate-900 bg-amber-400 hover:bg-amber-500 rounded-xl transition-all shadow-sm flex items-center space-x-1"
                >
                  <span>Next Question</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              ) : (
                <button
                  onClick={handleSubmitQuiz}
                  className="px-5 py-2 text-xs font-bold text-white bg-slate-900 hover:bg-slate-800 rounded-xl transition-all shadow-sm flex items-center space-x-1.5"
                >
                  <Award className="w-4 h-4 text-amber-400" />
                  <span>Submit Practice Session</span>
                </button>
              )}
            </div>
          </div>

        </div>
      )}

      {/* Past Attempts Table */}
      {pastAttempts.length > 0 && (
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-3">
          <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
            <Award className="w-4 h-4 text-[#FF9900]" />
            <span>Practice Attempt History</span>
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 uppercase text-[10px]">
                  <th className="py-2">Session</th>
                  <th className="py-2">Date</th>
                  <th className="py-2">Score</th>
                  <th className="py-2">Correct</th>
                  <th className="py-2">Weak Concepts</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {pastAttempts.slice(0, 5).map((att) => (
                  <tr key={att.attempt_id} className="hover:bg-slate-50">
                    <td className="py-2.5 font-semibold text-slate-800">
                      {att.module_title}
                    </td>
                    <td className="py-2.5 text-slate-500">
                      {new Date(att.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-2.5 font-bold">
                      <span className={`px-2 py-0.5 rounded-full ${
                        att.score_percentage >= 70 ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {att.score_percentage}%
                      </span>
                    </td>
                    <td className="py-2.5 text-slate-600">
                      {att.correct_count}/{att.total_questions}
                    </td>
                    <td className="py-2.5 text-slate-500">
                      {att.weak_concepts?.join(', ') || 'None'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
};
