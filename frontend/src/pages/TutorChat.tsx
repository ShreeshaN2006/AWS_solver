import React, { useState, useEffect, useRef } from 'react';
import { useCourse } from '../context/CourseContext';
import { api } from '../services/api';
import {
  Bot,
  User,
  Send,
  Sparkles,
  Quote,
  ExternalLink,
  PlusCircle,
  MessageSquare,
  Filter,
  CheckCircle2,
  AlertCircle,
  Wrench,
  Clock
} from 'lucide-react';
import { ChatMessage, ChatSession, Citation } from '../types';

export const TutorChat: React.FC = () => {
  const { modules, selectedModuleId } = useCourse();
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedModuleContext, setSelectedModuleContext] = useState<string>(selectedModuleId || 'all');
  const [isSending, setIsSending] = useState(false);
  const [suggestedFollowups, setSuggestedFollowups] = useState<string[]>([
    "Compare Amazon S3, EBS, and EFS storage with use cases",
    "Explain the AWS Shared Responsibility Model with examples",
    "What are the 6 Pillars of the AWS Well-Architected Framework?",
    "How do I configure route tables for public vs private subnets?"
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadSessions = async () => {
    try {
      const sessList = await api.getChatSessions();
      setSessions(sessList);
      if (sessList.length > 0) {
        loadSessionMessages(sessList[0].session_id);
      } else {
        // Initial greeting
        setMessages([
          {
            message_id: 'init',
            session_id: 'default',
            role: 'assistant',
            content: "Hello! I am your **AWS Academy Course Copilot**. I have indexed the entire AWS Academy Cloud Foundations course materials, including all 10 modules, lecture notes, and lab guides.\n\nAsk me anything! For example, you can ask me to:\n- Explain complex topics in beginner-friendly terms with practical AWS examples.\n- Compare related AWS services (e.g. S3 vs EBS vs EFS, or RDS vs DynamoDB).\n- Guide you through console steps for our 6 labs.\n- Generate structured revision notes.",
            citations: [],
            created_at: new Date().toISOString()
          }
        ]);
      }
    } catch (err) {
      console.error('Failed to load chat sessions:', err);
    }
  };

  const loadSessionMessages = async (sessionId: string) => {
    setActiveSessionId(sessionId);
    try {
      const history = await api.getSessionMessages(sessionId);
      if (history.length > 0) {
        setMessages(history);
      }
    } catch (err) {
      console.error('Failed to load messages for session:', err);
    }
  };

  const handleStartNewSession = () => {
    setActiveSessionId(null);
    setMessages([
      {
        message_id: 'new',
        session_id: 'new',
        role: 'assistant',
        content: "New study session started! What topic from AWS Academy Cloud Foundations would you like to explore?",
        citations: [],
        created_at: new Date().toISOString()
      }
    ]);
  };

  const handleSendMessage = async (promptOverride?: string) => {
    const textToSend = promptOverride || inputMessage;
    if (!textToSend.trim() || isSending) return;

    if (!promptOverride) setInputMessage('');
    setIsSending(true);

    const tempUserMsg: ChatMessage = {
      message_id: `temp_${Date.now()}`,
      session_id: activeSessionId || 'pending',
      role: 'user',
      content: textToSend,
      module_context: selectedModuleContext !== 'all' ? selectedModuleContext : undefined,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);

    try {
      const response = await api.sendChatMessage({
        message: textToSend,
        session_id: activeSessionId || undefined,
        module_id: selectedModuleContext !== 'all' ? selectedModuleContext : undefined
      });

      if (!activeSessionId) {
        setActiveSessionId(response.session_id);
        loadSessions();
      }

      const tempAssistantMsg: ChatMessage = {
        message_id: `temp_resp_${Date.now()}`,
        session_id: response.session_id,
        role: 'assistant',
        content: response.message,
        citations: response.citations,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, tempAssistantMsg]);
      if (response.suggested_followups && response.suggested_followups.length > 0) {
        setSuggestedFollowups(response.suggested_followups);
      }
    } catch (err) {
      console.error('Failed to send message:', err);
      setMessages(prev => [
        ...prev,
        {
          message_id: `err_${Date.now()}`,
          session_id: activeSessionId || 'err',
          role: 'assistant',
          content: "Sorry, I encountered an error communicating with the agent server. Please make sure the backend is active.",
          created_at: new Date().toISOString()
        }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="h-[calc(100vh-6rem)] flex gap-4 overflow-hidden">
      
      {/* Left Sidebar: Study Sessions History (Hidden on mobile) */}
      <div className="hidden md:flex w-64 bg-white rounded-2xl border border-slate-200/80 shadow-sm flex-col overflow-hidden shrink-0">
        <div className="p-3.5 border-b border-slate-100 flex items-center justify-between">
          <div className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
            <MessageSquare className="w-4 h-4 text-[#FF9900]" />
            <span>Study Sessions</span>
          </div>
          <button
            onClick={handleStartNewSession}
            className="p-1 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
            title="Start new study session"
          >
            <PlusCircle className="w-4 h-4" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {sessions.length === 0 ? (
            <div className="p-4 text-center text-xs text-slate-400">
              No previous study chats found.
            </div>
          ) : (
            sessions.map((s) => (
              <button
                key={s.session_id}
                onClick={() => loadSessionMessages(s.session_id)}
                className={`w-full text-left p-2.5 rounded-xl text-xs font-semibold truncate transition-colors ${
                  activeSessionId === s.session_id
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'text-slate-700 hover:bg-slate-100'
                }`}
              >
                <div className="truncate">{s.title || 'AWS Study Session'}</div>
                <div className="text-[10px] text-slate-400 font-normal">
                  {new Date(s.updated_at || s.created_at).toLocaleDateString()}
                </div>
              </button>
            ))
          )}
        </div>
      </div>

      {/* Main Chat Conversation Container */}
      <div className="flex-1 bg-white rounded-2xl border border-slate-200/80 shadow-sm flex flex-col min-h-0 overflow-hidden">
        
        {/* Top Chat Bar: Module Context Selector */}
        <div className="p-4 border-b border-slate-100 bg-slate-50/50 flex flex-wrap items-center justify-between gap-3 shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#232F3E] to-[#131921] flex items-center justify-center text-white shadow-sm">
              <Bot className="w-5 h-5 text-[#FF9900]" />
            </div>
            <div>
              <h2 className="text-sm font-extrabold text-slate-900">
                AWS Academy AI Learning Tutor
              </h2>
              <p className="text-[11px] text-slate-500">
                Course-aware agent with verified textbook citations & RAG retrieval
              </p>
            </div>
          </div>

          {/* Module Filter Context */}
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-slate-500 flex items-center space-x-1">
              <Filter className="w-3.5 h-3.5" />
              <span>Context:</span>
            </span>
            <select
              value={selectedModuleContext}
              onChange={(e) => setSelectedModuleContext(e.target.value)}
              className="text-xs font-bold text-slate-800 bg-white border border-slate-200 rounded-xl px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-[#FF9900]"
            >
              <option value="all">Entire Course (All 10 Modules)</option>
              {modules.filter(m => m.is_core_module).map((m) => (
                <option key={m.module_id} value={m.module_id}>
                  Module {m.module_number}: {m.title}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Chat Messages Log */}
        <div className="flex-1 p-5 overflow-y-auto space-y-4 min-h-0">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex space-x-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {m.role === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-[#232F3E] flex items-center justify-center text-[#FF9900] shrink-0 mt-0.5 shadow-xs">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-[80%] rounded-2xl p-4 space-y-3 shadow-xs ${
                  m.role === 'user'
                    ? 'bg-slate-900 text-white rounded-tr-none'
                    : 'bg-slate-50 text-slate-900 border border-slate-200/80 rounded-tl-none'
                }`}
              >
                <div className="whitespace-pre-line text-xs sm:text-sm leading-relaxed">
                  {m.content}
                </div>

                {/* Citations Box (Requirement 4: Source citations) */}
                {m.citations && m.citations.length > 0 && (
                  <div className="pt-3 border-t border-slate-200/70 space-y-2">
                    <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center space-x-1.5">
                      <Quote className="w-3.5 h-3.5 text-[#FF9900]" />
                      <span>Verified Course Materials Grounding:</span>
                    </div>

                    <div className="space-y-1.5">
                      {m.citations.map((c, cIdx) => (
                        <div
                          key={cIdx}
                          className="bg-white p-2.5 rounded-xl border border-slate-200 text-xs space-y-1 shadow-2xs"
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-bold text-slate-800">
                              {c.document_name}
                            </span>
                            {c.page_number && (
                              <span className="text-[11px] bg-slate-100 font-semibold px-2 py-0.5 rounded text-slate-600">
                                Page {c.page_number}
                              </span>
                            )}
                            {c.timestamp && (
                              <span className="text-[11px] bg-slate-100 font-semibold px-2 py-0.5 rounded text-slate-600">
                                Time: {c.timestamp}
                              </span>
                            )}
                          </div>
                          <div className="text-[11px] text-slate-500 italic">
                            "{c.snippet}"
                          </div>
                          {c.module_title && (
                            <div className="text-[10px] text-amber-700 font-semibold">
                              {c.module_title}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {m.role === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-slate-900 flex items-center justify-center text-amber-400 shrink-0 mt-0.5 shadow-xs">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {isSending && (
            <div className="flex items-center space-x-2 text-slate-400 text-xs py-2 pl-11">
              <Sparkles className="w-4 h-4 animate-spin text-[#FF9900]" />
              <span>Consulting official AWS Academy course index...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Prompts Carousel */}
        {suggestedFollowups.length > 0 && (
          <div className="p-2.5 bg-slate-50 border-t border-slate-100 flex items-center space-x-2 overflow-x-auto shrink-0">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider shrink-0 pl-2">
              Suggested:
            </span>
            {suggestedFollowups.map((q, i) => (
              <button
                key={i}
                onClick={() => handleSendMessage(q)}
                className="px-3 py-1.5 bg-white hover:bg-slate-100 border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 whitespace-nowrap transition-colors shadow-2xs hover:border-slate-300"
              >
                {q}
              </button>
            ))}
          </div>
        )}

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="p-4 border-t border-slate-200 bg-white flex items-center space-x-3 shrink-0"
        >
          <input
            type="text"
            placeholder="Ask any question about AWS Cloud Foundations, services, architectures, or labs..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={isSending}
            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-[#FF9900] transition-all"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isSending}
            className="p-2.5 bg-[#FF9900] hover:bg-[#e68a00] disabled:opacity-40 text-slate-950 rounded-xl font-bold transition-all shadow-sm"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>

      </div>

    </div>
  );
};
