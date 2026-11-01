import React, { useState, useEffect } from 'react';
import { useCourse } from '../context/CourseContext';
import { api } from '../services/api';
import {
  Terminal,
  CheckCircle2,
  AlertTriangle,
  Compass,
  CheckSquare,
  ShieldAlert,
  HelpCircle,
  Clock,
  Sparkles,
  ArrowRight,
  Upload,
  Cpu,
  Layers,
  ChevronRight
} from 'lucide-react';
import { LabDetail, UserLabProgress } from '../types';

export const LabAssistant: React.FC = () => {
  const { selectedLabId, setSelectedLabId } = useCourse();
  const [labs, setLabs] = useState<LabDetail[]>([]);
  const [activeLab, setActiveLab] = useState<LabDetail | null>(null);
  const [labProgress, setLabProgress] = useState<UserLabProgress | null>(null);
  const [activeStepIdx, setActiveStepIdx] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Troubleshooter State
  const [errorInput, setErrorInput] = useState<string>('');
  const [userDescInput, setUserDescInput] = useState<string>('');
  const [isDiagnosing, setIsDiagnosing] = useState<boolean>(false);
  const [diagnosisResult, setDiagnosisResult] = useState<any | null>(null);

  useEffect(() => {
    loadAllLabs();
  }, []);

  useEffect(() => {
    if (labs.length > 0) {
      const targetId = selectedLabId || 'lab_1';
      const found = labs.find(l => l.lab_id === targetId) || labs[0];
      selectLab(found);
    }
  }, [selectedLabId, labs]);

  const loadAllLabs = async () => {
    setIsLoading(true);
    try {
      const allLabs = await api.getLabs();
      setLabs(allLabs);
    } catch (err) {
      console.error('Failed to load labs:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const selectLab = async (lab: LabDetail) => {
    setActiveLab(lab);
    setSelectedLabId(lab.lab_id);
    setActiveStepIdx(0);
    setDiagnosisResult(null);
    try {
      const prog = await api.getLabProgress(lab.lab_id);
      setLabProgress(prog);
      if (prog.current_step && prog.current_step <= lab.steps.length) {
        setActiveStepIdx(prog.current_step - 1);
      }
    } catch (err) {
      console.error('Failed to load lab progress:', err);
    }
  };

  const handleConfirmStep = async (stepNumber: number, confirmed: boolean) => {
    if (!activeLab) return;
    try {
      const updated = await api.confirmLabStep(activeLab.lab_id, stepNumber, confirmed);
      setLabProgress(updated);
      if (confirmed && stepNumber < activeLab.steps.length) {
        setActiveStepIdx(stepNumber); // Advance to next step index
      }
    } catch (err) {
      console.error('Failed to confirm step:', err);
    }
  };

  const handleTroubleshoot = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeLab || (!errorInput.trim() && !userDescInput.trim())) return;

    setIsDiagnosing(true);
    try {
      const result = await api.troubleshootLab({
        lab_id: activeLab.lab_id,
        step_number: activeStepIdx + 1,
        error_message: errorInput,
        user_description: userDescInput || 'Encountered error during console step execution.'
      });
      setDiagnosisResult(result);
    } catch (err) {
      console.error('Troubleshoot error:', err);
    } finally {
      setIsDiagnosing(false);
    }
  };

  if (isLoading || !activeLab) {
    return (
      <div className="bg-white p-12 rounded-2xl border border-slate-200/80 text-center space-y-3">
        <Sparkles className="w-6 h-6 animate-spin text-[#FF9900] mx-auto" />
        <p className="text-sm font-semibold text-slate-600">Loading AWS Academy Laboratory Guides...</p>
      </div>
    );
  }

  const currentStep = activeLab.steps[activeStepIdx] || activeLab.steps[0];
  const isStepConfirmed = labProgress?.completed_steps?.includes(currentStep.step_number);

  return (
    <div className="space-y-6">
      
      {/* Top Banner & Safety Enforcement (Requirement 7) */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-slate-900 bg-amber-400 px-2.5 py-0.5 rounded-md shadow-2xs">
                AWS Lab Assistant
              </span>
              <span className="text-xs text-slate-500 font-semibold">• 6 Guided Practical Labs</span>
            </div>
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
              {activeLab.title}
            </h1>
            <p className="text-xs text-slate-600 max-w-3xl">
              {activeLab.objective}
            </p>
          </div>

          <div className="flex items-center space-x-3 shrink-0">
            <div className="text-right">
              <div className="text-[11px] text-slate-400 font-medium">Estimated Duration</div>
              <div className="text-xs font-bold text-slate-800 flex items-center justify-end space-x-1">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                <span>{activeLab.duration_mins} Minutes</span>
              </div>
            </div>
          </div>
        </div>

        {/* Safety Rule Card */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex items-start space-x-2.5 text-xs text-slate-700">
          <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <span className="font-bold text-slate-900">Safety Guardrail:</span> The Lab Assistant provides step-by-step navigation, verification checklists, and troubleshooting guidance. It will never independently modify, create, or terminate AWS resources in your personal account or learner lab sandbox.
          </div>
        </div>

        {/* Lab Selection Tabs */}
        <div className="flex items-center space-x-2 overflow-x-auto pt-2 border-t border-slate-100">
          {labs.map((l) => (
            <button
              key={l.lab_id}
              onClick={() => selectLab(l)}
              className={`px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                activeLab.lab_id === l.lab_id
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200/80 hover:text-slate-900'
              }`}
            >
              Lab {l.lab_number}: {l.title.replace('Introduction to ', '').replace('Build your ', '')}
            </button>
          ))}
        </div>
      </div>

      {/* Main Lab Layout: Steps Stepper + Detail Pane + Troubleshooter */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column (4 cols): Sequential Steps Stepper */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center space-x-1.5">
              <Layers className="w-3.5 h-3.5 text-[#FF9900]" />
              <span>Lab Stages ({activeLab.steps.length} Steps)</span>
            </h3>

            <div className="space-y-2">
              {activeLab.steps.map((step, idx) => {
                const isSelected = activeStepIdx === idx;
                const isDone = labProgress?.completed_steps?.includes(step.step_number);

                return (
                  <div
                    key={step.step_number}
                    onClick={() => setActiveStepIdx(idx)}
                    className={`p-3 rounded-xl border cursor-pointer transition-all flex items-start space-x-3 text-xs ${
                      isSelected
                        ? 'bg-amber-50/60 border-[#FF9900] ring-1 ring-[#FF9900]'
                        : isDone
                        ? 'bg-emerald-50/40 border-emerald-200'
                        : 'bg-white border-slate-200/70 hover:border-slate-300'
                    }`}
                  >
                    <div className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5 ${
                      isDone
                        ? 'bg-emerald-600 text-white'
                        : isSelected
                        ? 'bg-[#FF9900] text-slate-950'
                        : 'bg-slate-200 text-slate-600'
                    }`}>
                      {isDone ? '✓' : step.step_number}
                    </div>

                    <div className="min-w-0 flex-1">
                      <div className={`font-bold truncate ${
                        isSelected ? 'text-slate-900' : 'text-slate-700'
                      }`}>
                        {step.title}
                      </div>
                      <div className="text-[11px] text-slate-400 line-clamp-1">
                        {step.objective}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Involved AWS Services */}
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-2.5">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              AWS Services Configured:
            </h4>
            <div className="flex flex-wrap gap-1.5">
              {activeLab.aws_services.map((svc, i) => (
                <span
                  key={i}
                  className="text-xs font-semibold bg-slate-100 text-slate-800 px-2.5 py-1 rounded-lg border border-slate-200"
                >
                  {svc}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column (8 cols): Step Guidance & Console Walkthrough */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Active Step Details */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-5">
            <div className="flex items-start justify-between border-b border-slate-100 pb-4 gap-3">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#FF9900]">
                  Step {currentStep.step_number} of {activeLab.steps.length}
                </span>
                <h2 className="text-lg font-bold text-slate-900 mt-0.5">
                  {currentStep.title}
                </h2>
                <p className="text-xs text-slate-600 mt-1">
                  {currentStep.objective}
                </p>
              </div>

              <span className={`text-[11px] font-bold px-2.5 py-1 rounded-full shrink-0 ${
                isStepConfirmed
                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                  : 'bg-slate-100 text-slate-600 border border-slate-200'
              }`}>
                {isStepConfirmed ? 'Verified Completed' : 'Pending Confirmation'}
              </span>
            </div>

            {/* AWS Console Navigation Path */}
            <div className="bg-slate-900 text-slate-100 p-3.5 rounded-xl text-xs space-y-1">
              <div className="text-[10px] uppercase font-bold text-amber-400 flex items-center space-x-1.5">
                <Compass className="w-3.5 h-3.5" />
                <span>AWS Management Console Navigation:</span>
              </div>
              <div className="font-mono text-xs text-slate-200">
                {currentStep.console_navigation}
              </div>
            </div>

            {/* Step-by-Step Instructions */}
            <div className="space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Sequential Instructions:
              </h3>

              <div className="space-y-2">
                {currentStep.instructions.map((inst, idx) => (
                  <div
                    key={idx}
                    className="flex items-start space-x-3 text-xs text-slate-700 bg-slate-50/70 p-3 rounded-xl border border-slate-200/60"
                  >
                    <span className="w-5 h-5 rounded-full bg-white border border-slate-300 flex items-center justify-center font-bold text-slate-600 shrink-0 text-[11px]">
                      {idx + 1}
                    </span>
                    <span className="leading-relaxed whitespace-pre-line font-medium">
                      {inst}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Expected Result Box */}
            <div className="bg-emerald-50/60 border border-emerald-200/80 rounded-xl p-3.5 text-xs text-emerald-900 space-y-1">
              <span className="font-bold flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Expected Result:</span>
              </span>
              <p className="leading-relaxed">{currentStep.expected_result}</p>
            </div>

            {/* Common Pitfalls Box */}
            {currentStep.common_pitfalls?.length > 0 && (
              <div className="bg-amber-50/60 border border-amber-200/80 rounded-xl p-3.5 text-xs text-amber-900 space-y-1">
                <span className="font-bold flex items-center space-x-1.5">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  <span>Common Student Pitfalls:</span>
                </span>
                <ul className="list-disc list-inside space-y-0.5 text-amber-800">
                  {currentStep.common_pitfalls.map((pit, pIdx) => (
                    <li key={pIdx}>{pit}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Step Confirmation Action (Requirement 7: User confirms completed stage) */}
            <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={!!isStepConfirmed}
                  onChange={(e) => handleConfirmStep(currentStep.step_number, e.target.checked)}
                  className="w-5 h-5 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500 cursor-pointer"
                />
                <span className="text-xs font-bold text-slate-800">
                  I have completed & verified this step in the AWS Console
                </span>
              </label>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setActiveStepIdx(prev => Math.max(0, prev - 1))}
                  disabled={activeStepIdx === 0}
                  className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 disabled:opacity-40 text-slate-700 text-xs font-semibold rounded-xl"
                >
                  Previous Step
                </button>
                <button
                  onClick={() => setActiveStepIdx(prev => Math.min(activeLab.steps.length - 1, prev + 1))}
                  disabled={activeStepIdx === activeLab.steps.length - 1}
                  className="px-4 py-1.5 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-white text-xs font-bold rounded-xl flex items-center space-x-1"
                >
                  <span>Next Step</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

          </div>

          {/* Interactive Console Troubleshooter (Requirement 7: Upload screenshot or paste error) */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
                  <Terminal className="w-4 h-4 text-[#FF9900]" />
                  <span>Lab Troubleshooting Assistant</span>
                </h3>
                <p className="text-xs text-slate-500">
                  Stuck or encountered an error in the AWS Management Console? Paste the message or describe your roadblock:
                </p>
              </div>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800">
                Step {currentStep.step_number} Focus
              </span>
            </div>

            <form onSubmit={handleTroubleshoot} className="space-y-3">
              <div>
                <textarea
                  rows={2}
                  placeholder="Paste error text (e.g. UnauthorizedOperation, Timed Out, SecurityGroupNotFound)..."
                  value={errorInput}
                  onChange={(e) => setErrorInput(e.target.value)}
                  className="w-full text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl p-3 focus:ring-2 focus:ring-[#FF9900] focus:outline-none"
                />
              </div>

              <div>
                <input
                  type="text"
                  placeholder="Additional context or what you clicked (e.g. Tried to attach volume but got error)..."
                  value={userDescInput}
                  onChange={(e) => setUserDescInput(e.target.value)}
                  className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-[#FF9900] focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-between pt-1">
                <span className="text-[11px] text-slate-400">
                  AI will suggest console checks and remediation steps.
                </span>

                <button
                  type="submit"
                  disabled={isDiagnosing || (!errorInput.trim() && !userDescInput.trim())}
                  className="px-4 py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-white text-xs font-bold rounded-xl flex items-center space-x-1.5 transition-all shadow-sm"
                >
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  <span>{isDiagnosing ? 'Diagnosing...' : 'Diagnose Console Roadblock'}</span>
                </button>
              </div>
            </form>

            {/* Diagnostic Results Box */}
            {diagnosisResult && (
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3 text-xs">
                <div className="space-y-1">
                  <div className="font-bold text-slate-900 text-xs flex items-center space-x-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                    <span>Diagnosis:</span>
                  </div>
                  <p className="text-slate-800 font-medium">
                    {diagnosisResult.diagnosis}
                  </p>
                </div>

                <div className="space-y-1">
                  <span className="font-bold text-slate-700">Recommended Steps to Fix:</span>
                  <ul className="list-disc list-inside space-y-1 text-slate-600">
                    {diagnosisResult.suggested_fix?.map((fix: string, fIdx: number) => (
                      <li key={fIdx}>{fix}</li>
                    ))}
                  </ul>
                </div>

                <div className="space-y-1">
                  <span className="font-bold text-slate-700">Verification in AWS Console:</span>
                  <ul className="list-disc list-inside space-y-1 text-slate-600">
                    {diagnosisResult.console_steps_to_verify?.map((chk: string, cIdx: number) => (
                      <li key={cIdx}>{chk}</li>
                    ))}
                  </ul>
                </div>

                <div className="text-[10px] text-slate-500 italic pt-1 border-t border-slate-200">
                  {diagnosisResult.safety_reminder}
                </div>
              </div>
            )}
          </div>

        </div>

      </div>

    </div>
  );
};
