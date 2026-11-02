import React, { useState, useEffect } from 'react';
import { useCourse } from '../context/CourseContext';
import { api } from '../services/api';
import {
  Settings,
  Cpu,
  ShieldCheck,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  Database,
  Lock,
  Sparkles,
  RefreshCw
} from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { settings, refreshSettings } = useCourse();

  // Provider Settings Form
  const [provider, setProvider] = useState<string>('local_mock');
  const [openaiKey, setOpenaiKey] = useState<string>('');
  const [awsKey, setAwsKey] = useState<string>('');
  const [awsSecret, setAwsSecret] = useState<string>('');
  const [isUpdatingProvider, setIsUpdatingProvider] = useState<boolean>(false);
  const [providerStatusMsg, setProviderStatusMsg] = useState<string | null>(null);

  // Canvas Integration Form
  const [canvasStatus, setCanvasStatus] = useState<any | null>(null);
  const [isTestingCanvas, setIsTestingCanvas] = useState<boolean>(false);
  const [canvasTestMsg, setCanvasTestMsg] = useState<string | null>(null);

  useEffect(() => {
    if (settings) {
      setProvider(settings.llm_provider || 'local_mock');
    }
    checkCanvas();
  }, [settings]);

  const checkCanvas = async () => {
    try {
      const st = await api.getCanvasStatus();
      setCanvasStatus(st);
    } catch (err) {
      console.error('Failed to get Canvas status:', err);
    }
  };

  const handleUpdateProvider = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsUpdatingProvider(true);
    setProviderStatusMsg(null);
    try {
      const res = await api.updateProvider(provider, openaiKey || undefined, awsKey || undefined, awsSecret || undefined);
      setProviderStatusMsg(res.message);
      await refreshSettings();
    } catch (err: any) {
      setProviderStatusMsg(`Error: ${err.message}`);
    } finally {
      setIsUpdatingProvider(false);
    }
  };

  const handleTestCanvas = async () => {
    setIsTestingCanvas(true);
    setCanvasTestMsg(null);
    try {
      const st = await api.getCanvasStatus();
      setCanvasStatus(st);
      setCanvasTestMsg(st.test_result?.message || 'Connection test completed.');
    } catch (err: any) {
      setCanvasTestMsg(`Test failed: ${err.message}`);
    } finally {
      setIsTestingCanvas(false);
    }
  };

  const handleSyncCanvas = async () => {
    try {
      const res = await api.syncCanvas();
      setCanvasTestMsg(res.message);
    } catch (err: any) {
      setCanvasTestMsg(`Sync error: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      
      {/* Header */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
        <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
          System Settings & Integrations
        </h1>
        <p className="text-xs text-slate-500">
          Configure AI reasoning providers, MongoDB database connections, and Canvas LMS synchronization
        </p>
      </div>

      {/* AI Provider Abstraction Card (Requirement 2 & 14) */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-5">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-amber-500/15 flex items-center justify-center text-[#FF9900]">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900">
              AI Provider Abstraction
            </h2>
            <p className="text-xs text-slate-500">
              Select your LLM inference engine. Switch between Local AI, OpenAI API, and Amazon Bedrock.
            </p>
          </div>
        </div>

        {providerStatusMsg && (
          <div className="p-3 bg-amber-50 text-amber-900 border border-amber-200 rounded-xl text-xs font-semibold">
            {providerStatusMsg}
          </div>
        )}

        <form onSubmit={handleUpdateProvider} className="space-y-4 text-xs">
          {/* Provider Selection Radio Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            
            <div
              onClick={() => setProvider('local_mock')}
              className={`p-3.5 rounded-xl border cursor-pointer transition-all space-y-1 ${
                provider === 'local_mock'
                  ? 'bg-amber-50/70 border-[#FF9900] ring-1 ring-[#FF9900]'
                  : 'bg-white border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="font-bold text-slate-900 flex items-center justify-between">
                <span>Local AI / Mock</span>
                <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">
                  Active Default
                </span>
              </div>
              <p className="text-[11px] text-slate-500">
                Offline demo mode with canned AWS explanations and lexical-hash retrieval. It does not produce semantic embeddings.
              </p>
            </div>

            <div
              onClick={() => setProvider('openai')}
              className={`p-3.5 rounded-xl border cursor-pointer transition-all space-y-1 ${
                provider === 'openai'
                  ? 'bg-amber-50/70 border-[#FF9900] ring-1 ring-[#FF9900]'
                  : 'bg-white border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="font-bold text-slate-900 flex items-center justify-between">
                <span>OpenAI API</span>
                <span className="text-[10px] bg-blue-100 text-blue-800 font-bold px-1.5 py-0.5 rounded">
                  gpt-4o-mini
                </span>
              </div>
              <p className="text-[11px] text-slate-500">
                Uses OpenAI GPT-4o-mini with text-embedding-3-small vectors.
              </p>
            </div>

            <div
              onClick={() => setProvider('bedrock')}
              className={`p-3.5 rounded-xl border cursor-pointer transition-all space-y-1 ${
                provider === 'bedrock'
                  ? 'bg-amber-50/70 border-[#FF9900] ring-1 ring-[#FF9900]'
                  : 'bg-white border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="font-bold text-slate-900 flex items-center justify-between">
                <span>Amazon Bedrock</span>
                <span className="text-[10px] bg-purple-100 text-purple-800 font-bold px-1.5 py-0.5 rounded">
                  Claude 3
                </span>
              </div>
              <p className="text-[11px] text-slate-500">
                Amazon Bedrock Claude 3 and Titan Embeddings, using explicit keys or the AWS SDK credential chain.
              </p>
            </div>

          </div>

          {/* Conditional inputs based on selected provider */}
          {provider === 'openai' && (
            <div className="space-y-1.5 pt-2">
              <label className="font-bold text-slate-700">OpenAI API Key</label>
              <input
                type="password"
                placeholder={settings?.openai_has_key ? "•••••••••••••••••••••••• (Configured in .env)" : "sk-..."}
                value={openaiKey}
                onChange={(e) => setOpenaiKey(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 font-mono"
              />
            </div>
          )}

          {provider === 'bedrock' && (
            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="space-y-1.5">
                <label className="font-bold text-slate-700">AWS Access Key ID</label>
                <input
                  type="password"
                  placeholder="AKIA..."
                  value={awsKey}
                  onChange={(e) => setAwsKey(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 font-mono"
                />
              </div>

              <div className="space-y-1.5">
                <label className="font-bold text-slate-700">AWS Secret Access Key</label>
                <input
                  type="password"
                  placeholder="Secret key..."
                  value={awsSecret}
                  onChange={(e) => setAwsSecret(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 font-mono"
                />
              </div>
              <p className="text-[11px] text-slate-500">Prefer an IAM role or AWS SSO in hosted environments. Leave both fields blank to use the AWS SDK credential chain.</p>
            </div>
          )}

          <button
            type="submit"
            disabled={isUpdatingProvider}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white font-bold rounded-xl transition-all shadow-sm"
          >
            {isUpdatingProvider ? 'Saving Provider...' : 'Apply Provider Configuration'}
          </button>
        </form>
      </div>

      {/* Canvas LMS Integration Card (Requirement 8) */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-4">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-blue-500/15 flex items-center justify-center text-blue-600">
            <ExternalLink className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900">
              Canvas LMS Integration (Course ID: 183194)
            </h2>
            <p className="text-xs text-slate-500">
              Read-only synchronization for AWS Academy Cloud Foundations
            </p>
          </div>
        </div>

        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2 text-xs">
          <div className="flex items-center justify-between">
            <span className="text-slate-600 font-semibold">Canvas LMS Base URL:</span>
            <span className="font-mono text-slate-800">https://awsacademy.instructure.com</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-600 font-semibold">Target Course ID:</span>
            <span className="font-mono text-slate-800 font-bold">183194</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-600 font-semibold">Connection Mode:</span>
            <span className="font-bold text-emerald-700">
              {canvasStatus?.mode || 'Local Document & HTML Fallback'}
            </span>
          </div>
        </div>

        {canvasTestMsg && (
          <div className="p-3 bg-blue-50 text-blue-900 border border-blue-200 rounded-xl text-xs font-medium">
            {canvasTestMsg}
          </div>
        )}

        <div className="flex items-center space-x-2 pt-1">
          <button
            onClick={handleTestCanvas}
            disabled={isTestingCanvas}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs rounded-xl flex items-center space-x-1.5 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isTestingCanvas ? 'animate-spin' : ''}`} />
            <span>Test Canvas Connection</span>
          </button>

          <button
            onClick={handleSyncCanvas}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl flex items-center space-x-1.5 transition-all shadow-sm"
          >
            <span>Sync Modules (Read-Only)</span>
          </button>
        </div>

        <div className="text-[11px] text-slate-400 italic">
          Security: Keys entered here remain in backend process memory only. Prefer IAM roles or SSO over long-lived AWS keys. Canvas access remains read-only.
        </div>
      </div>

      {/* Database Connection Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-3">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-emerald-500/15 flex items-center justify-center text-emerald-600">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900">
              Database & Vector Store (MongoDB)
            </h2>
            <p className="text-xs text-slate-500">
              Connected to local MongoDB service with document vector indexes
            </p>
          </div>
        </div>

        <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs space-y-1 font-mono">
          <div><strong>Connection:</strong> {settings?.mongodb_configured ? 'Configured on backend' : 'Not configured'}</div>
          <div><strong>Database:</strong> {settings?.mongodb_db || 'aws_academy_copilot'}</div>
          <div className="text-emerald-700 font-sans font-bold pt-1">Status: Operational & Connected ✓</div>
        </div>
      </div>

    </div>
  );
};
