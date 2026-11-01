import React, { useState, useEffect } from 'react';
import { useCourse } from '../context/CourseContext';
import { api } from '../services/api';
import {
  BookOpen,
  CheckCircle2,
  Sparkles,
  Send,
  HelpCircle,
  Terminal,
  ExternalLink,
  Bot,
  User,
  Quote,
  Clock,
  Layers,
  ChevronRight
} from 'lucide-react';
import { CourseModule, ChatMessage, Citation } from '../types';

export const LearningWorkspace: React.FC = () => {
  const { modules, selectedModuleId, setSelectedModuleId, navigateTo, refreshProgress } = useCourse();
  const [activeModule, setActiveModule] = useState<CourseModule | null>(null);
  const [completedItems, setCompletedItems] = useState<Record<string, boolean>>({});
  
  // Embedded Tutor Chat State
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; text: string; citations?: Citation[] }>>([
    {
      role: 'assistant',
      text: "👋 Welcome to your Module Learning Workspace! I am your course-aware AI tutor. As you read your student guides and watch lectures, ask me any questions about concepts, compare AWS services, or ask for real-world enterprise examples."
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [isSending, setIsSending] = useState(false);

  // Set active module based on selectedModuleId
  useEffect(() => {
    const targetId = selectedModuleId || '10101';
    const found = modules.find(m => m.module_id === targetId) || modules[0];
    if (found) {
      setActiveModule(found);
      // Initialize completed map
      const initialMap: Record<string, boolean> = {};
      found.items.forEach(it => {
        initialMap[it.item_id] = it.is_completed;
      });
      setCompletedItems(initialMap);
    }
  }, [selectedModuleId, modules]);

  const toggleItemCompletion = async (itemId: string) => {
    if (!activeModule) return;
    const currentVal = !!completedItems[itemId];
    const newVal = !currentVal;
    
    setCompletedItems(prev => ({ ...prev, [itemId]: newVal }));
    try {
      await api.updateItemProgress({
        module_id: activeModule.module_id,
        item_id: itemId,
        completed: newVal,
        time_spent_mins: 15
      });
      await refreshProgress();
    } catch (err) {
      console.error('Failed to update item completion:', err);
    }
  };

  const handleSendMessage = async (customPrompt?: string) => {
    const textToSend = customPrompt || chatInput;
    if (!textToSend.trim() || isSending || !activeModule) return;

    const userMsg = textToSend.trim();
    if (!customPrompt) setChatInput('');
    setIsSending(true);

    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);

    try {
      const response = await api.sendChatMessage({
        message: userMsg,
        module_id: activeModule.module_id,
      });

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          text: response.message,
          citations: response.citations
        }
      ]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          text: "I encountered an issue connecting to the AI agent service. Please verify backend is running on port 8000."
        }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  if (!activeModule) {
    return <div className="p-8 text-center text-slate-500">Loading module workspace...</div>;
  }

  return (
    <div className="h-[calc(100vh-6rem)] flex flex-col space-y-4">
      
      {/* Top Workspace Header Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3 shrink-0">
        <div className="flex items-center space-x-3">
          <span className="text-xs font-bold bg-[#FF9900]/15 text-amber-800 border border-amber-300 px-2.5 py-1 rounded-lg">
            {activeModule.is_core_module ? `Module ${activeModule.module_number}` : 'Section'}
          </span>

          <select
            value={activeModule.module_id}
            onChange={(e) => {
              setSelectedModuleId(e.target.value);
            }}
            className="text-sm font-bold text-slate-900 bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-[#FF9900] cursor-pointer"
          >
            {modules.map((m) => (
              <option key={m.module_id} value={m.module_id}>
                {m.is_core_module ? `Module ${m.module_number}: ` : ''}{m.title}
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center space-x-2">
          {activeModule.has_lab && (
            <button
              onClick={() => navigateTo('labs', activeModule.module_id, activeModule.lab_id)}
              className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-xl flex items-center space-x-1.5 transition-all shadow-sm"
            >
              <Terminal className="w-3.5 h-3.5 text-amber-400" />
              <span>Lab Assistant</span>
            </button>
          )}

          <button
            onClick={() => navigateTo('practice', activeModule.module_id)}
            className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-xl flex items-center space-x-1.5 transition-colors"
          >
            <HelpCircle className="w-3.5 h-3.5 text-slate-600" />
            <span>Practice Knowledge Check</span>
          </button>
        </div>
      </div>

      {/* Split Workspace Body: Left (Notes & Resources) + Right (Embedded Tutor) */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-4 min-h-0 overflow-hidden">
        
        {/* LEFT PANE (7 Cols): Module Content & Checklist */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 overflow-y-auto space-y-6">
          
          <div className="space-y-2 border-b border-slate-100 pb-4">
            <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">
              {activeModule.title}
            </h2>
            <p className="text-xs text-slate-600 leading-relaxed">
              {activeModule.description}
            </p>

            {/* Key Services Badges */}
            <div className="flex flex-wrap items-center gap-1.5 pt-2">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                Exam Objectives & Services:
              </span>
              {activeModule.key_aws_services.map((svc, i) => (
                <span
                  key={i}
                  onClick={() => handleSendMessage(`Explain ${svc} and its main purpose in ${activeModule.title}`)}
                  className="cursor-pointer text-[11px] font-medium bg-amber-50 hover:bg-amber-100 text-amber-900 px-2.5 py-0.5 rounded-full border border-amber-200 transition-colors"
                  title="Click to ask AI Tutor about this service"
                >
                  {svc}
                </span>
              ))}
            </div>
          </div>

          {/* Module Topics / Syllabus breakdown */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
              <BookOpen className="w-3.5 h-3.5" />
              <span>Core Learning Topics in this Module</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {(activeModule.topics || []).map((topic, i) => (
                <div
                  key={i}
                  onClick={() => handleSendMessage(`Explain the topic: "${topic}" from ${activeModule.title} with practical examples.`)}
                  className="cursor-pointer p-3 rounded-xl bg-slate-50 hover:bg-slate-100/80 border border-slate-200/60 text-xs font-semibold text-slate-800 transition-all flex items-center justify-between group"
                >
                  <span>{topic}</span>
                  <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-amber-500 transition-colors" />
                </div>
              ))}
            </div>
          </div>

          {/* Interactive Checklist of Learning Items */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Learning Resources & Activity Checklist</span>
              </h3>
              <span className="text-[11px] text-slate-400">Locally Tracked Progress</span>
            </div>

            <div className="space-y-2">
              {activeModule.items.map((item) => {
                const isChecked = !!completedItems[item.item_id];

                return (
                  <div
                    key={item.item_id}
                    className={`flex items-center justify-between p-3 rounded-xl border transition-all ${
                      isChecked 
                        ? 'bg-emerald-50/50 border-emerald-200' 
                        : 'bg-white border-slate-200/80 hover:border-slate-300'
                    }`}
                  >
                    <div className="flex items-center space-x-3 min-w-0">
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => toggleItemCompletion(item.item_id)}
                        className="w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500 cursor-pointer"
                      />
                      <div className="truncate">
                        <div className={`text-xs font-semibold truncate ${
                          isChecked ? 'line-through text-slate-400' : 'text-slate-800'
                        }`}>
                          {item.title}
                        </div>
                        <div className="text-[10px] text-slate-400 flex items-center space-x-2">
                          <span className="uppercase">{item.type}</span>
                          <span>•</span>
                          <span>~{item.time_estimate_mins} mins</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 ml-3 shrink-0">
                      <button
                        onClick={() => handleSendMessage(`Summarise the lesson: "${item.title}" from ${activeModule.title}`)}
                        className="px-2 py-1 text-[11px] font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors flex items-center space-x-1"
                      >
                        <Sparkles className="w-3 h-3 text-amber-500" />
                        <span>Summarise</span>
                      </button>

                      {item.url && (
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noreferrer"
                          className="p-1 text-slate-400 hover:text-slate-600"
                          title="Open official resource in Canvas"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </div>

        {/* RIGHT PANE (5 Cols): Embedded Interactive AI Tutor Copilot */}
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200/80 shadow-sm flex flex-col min-h-0 overflow-hidden">
          
          {/* Tutor Chat Header */}
          <div className="p-3.5 border-b border-slate-100 bg-slate-50 flex items-center justify-between shrink-0">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded-lg bg-amber-500 flex items-center justify-center text-slate-950 font-bold shadow-xs">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <h3 className="font-bold text-xs text-slate-900">AI Module Copilot</h3>
                <p className="text-[10px] text-slate-500">Context: {activeModule.title}</p>
              </div>
            </div>

            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
              RAG Active
            </span>
          </div>

          {/* Chat Messages Log */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 text-xs min-h-0">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex space-x-2.5 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {m.role === 'assistant' && (
                  <div className="w-6 h-6 rounded-md bg-amber-500/20 text-amber-900 flex items-center justify-center shrink-0 mt-0.5 font-bold">
                    <Bot className="w-3.5 h-3.5 text-amber-700" />
                  </div>
                )}

                <div
                  className={`max-w-[85%] rounded-2xl p-3 shadow-2xs space-y-2 ${
                    m.role === 'user'
                      ? 'bg-slate-900 text-white rounded-tr-none'
                      : 'bg-slate-50 text-slate-800 border border-slate-200/70 rounded-tl-none'
                  }`}
                >
                  <div className="whitespace-pre-line leading-relaxed">
                    {m.text}
                  </div>

                  {/* Citations Box */}
                  {m.citations && m.citations.length > 0 && (
                    <div className="pt-2 border-t border-slate-200/60 space-y-1">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider flex items-center space-x-1">
                        <Quote className="w-3 h-3 text-amber-600" />
                        <span>Verified Course Source</span>
                      </div>
                      <div className="text-[10px] text-slate-600 bg-white/80 p-1.5 rounded-lg border border-slate-200/60">
                        <div><strong>Doc:</strong> {m.citations[0].document_name}</div>
                        {m.citations[0].page_number && <div><strong>Page:</strong> {m.citations[0].page_number}</div>}
                        <p className="italic text-slate-500 line-clamp-2 mt-0.5">"{m.citations[0].snippet}"</p>
                      </div>
                    </div>
                  )}
                </div>

                {m.role === 'user' && (
                  <div className="w-6 h-6 rounded-md bg-slate-900 text-white flex items-center justify-center shrink-0 mt-0.5 font-bold">
                    <User className="w-3.5 h-3.5 text-amber-400" />
                  </div>
                )}
              </div>
            ))}

            {isSending && (
              <div className="flex items-center space-x-2 text-slate-400 text-xs py-2">
                <Sparkles className="w-3.5 h-3.5 animate-spin text-amber-500" />
                <span>Searching course materials and reasoning...</span>
              </div>
            )}
          </div>

          {/* Quick Prompts Bar */}
          <div className="p-2 bg-slate-50 border-t border-slate-100 flex items-center space-x-1 overflow-x-auto shrink-0">
            <button
              onClick={() => handleSendMessage(`Summarise the main exam concepts in ${activeModule.title}`)}
              className="px-2 py-1 bg-white hover:bg-slate-100 border border-slate-200 rounded-lg text-[10px] font-semibold text-slate-700 whitespace-nowrap"
            >
              📝 Key Takeaways
            </button>
            <button
              onClick={() => handleSendMessage(`What are the most common exam traps or mistakes students make in ${activeModule.title}?`)}
              className="px-2 py-1 bg-white hover:bg-slate-100 border border-slate-200 rounded-lg text-[10px] font-semibold text-slate-700 whitespace-nowrap"
            >
              ⚠️ Exam Pitfalls
            </button>
            <button
              onClick={() => handleSendMessage(`Give me a beginner-friendly analogy to remember ${activeModule.key_aws_services[0] || 'this concept'}`)}
              className="px-2 py-1 bg-white hover:bg-slate-100 border border-slate-200 rounded-lg text-[10px] font-semibold text-slate-700 whitespace-nowrap"
            >
              💡 Real-World Metaphor
            </button>
          </div>

          {/* Input Chat Box */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="p-3 border-t border-slate-200 bg-white flex items-center space-x-2 shrink-0"
          >
            <input
              type="text"
              placeholder={`Ask a question about ${activeModule.title}...`}
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              disabled={isSending}
              className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#FF9900]"
            />
            <button
              type="submit"
              disabled={!chatInput.trim() || isSending}
              className="p-2 bg-[#FF9900] hover:bg-[#e68a00] disabled:opacity-40 text-slate-950 rounded-xl transition-colors shadow-sm"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

        </div>

      </div>

    </div>
  );
};
