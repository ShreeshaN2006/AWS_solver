import React, { useState, useEffect } from 'react';
import { useCourse } from '../context/CourseContext';
import { api } from '../services/api';
import {
  FolderArchive,
  Upload,
  FileText,
  CheckCircle2,
  Sparkles,
  Layers,
  Database,
  ExternalLink,
  Search,
  Filter
} from 'lucide-react';
import { LearningDocument, DocumentChunk } from '../types';

export const DocumentLibrary: React.FC = () => {
  const { modules, refreshCourse } = useCourse();
  const [documents, setDocuments] = useState<LearningDocument[]>([]);
  const [chunks, setChunks] = useState<DocumentChunk[]>([]);
  const [activeTab, setActiveTab] = useState<'documents' | 'chunks'>('documents');
  const [selectedModuleFilter, setSelectedModuleFilter] = useState<string>('all');
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  // Form State for uploading PDF / Transcript
  const [uploadModuleId, setUploadModuleId] = useState<string>('10101');
  const [uploadDocType, setUploadDocType] = useState<string>('pdf');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Canvas HTML Form
  const [canvasHtmlFile, setCanvasHtmlFile] = useState<File | null>(null);
  const [isImportingHtml, setIsImportingHtml] = useState<boolean>(false);

  useEffect(() => {
    loadDocs();
    loadChunks();
  }, [selectedModuleFilter]);

  const loadDocs = async () => {
    try {
      const docs = await api.getDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to load documents:', err);
    }
  };

  const loadChunks = async () => {
    try {
      const chks = await api.getChunks(selectedModuleFilter !== 'all' ? selectedModuleFilter : undefined, 40);
      setChunks(chks);
    } catch (err) {
      console.error('Failed to load chunks:', err);
    }
  };

  const handleImportCanvasHtml = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canvasHtmlFile) return;

    setIsImportingHtml(true);
    setUploadMessage(null);
    try {
      const res = await api.importCanvasHtml(canvasHtmlFile);
      setUploadMessage(`Success: Imported ${res.details?.modules_imported || 0} modules and ${res.details?.total_items || 0} items from Canvas HTML.`);
      await refreshCourse();
      setCanvasHtmlFile(null);
    } catch (err: any) {
      setUploadMessage(`Error parsing HTML: ${err.message}`);
    } finally {
      setIsImportingHtml(false);
    }
  };

  const handleUploadDocument = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setIsUploading(true);
    setUploadMessage(null);
    try {
      const targetMod = modules.find(m => m.module_id === uploadModuleId);
      const modTitle = targetMod?.title || `Module ${uploadModuleId}`;

      const res = await api.uploadDocument(
        selectedFile,
        uploadModuleId,
        modTitle,
        uploadDocType
      );
      setUploadMessage(`Success: ${res.message}`);
      await loadDocs();
      await loadChunks();
      setSelectedFile(null);
    } catch (err: any) {
      setUploadMessage(`Error uploading document: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
            Course Document Library & RAG Ingestion Pipeline
          </h1>
          <p className="text-xs text-slate-500">
            Ingest Canvas LMS course exports, PyMuPDF-parsed student guides, and video transcripts into vector memory
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-semibold">
          <span className="bg-emerald-50 text-emerald-800 border border-emerald-200 px-3 py-1.5 rounded-xl flex items-center space-x-1.5">
            <Database className="w-3.5 h-3.5 text-emerald-600" />
            <span>{chunks.length}+ Vector Chunks Indexed</span>
          </span>
        </div>
      </div>

      {uploadMessage && (
        <div className="p-3.5 bg-amber-50 text-amber-900 border border-amber-200 rounded-xl text-xs font-medium flex items-center justify-between">
          <span>{uploadMessage}</span>
          <button onClick={() => setUploadMessage(null)} className="font-bold ml-2">✕</button>
        </div>
      )}

      {/* Two Upload Ingestion Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Card 1: Canvas Course HTML Export Import */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-4">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-xl bg-amber-500/15 flex items-center justify-center text-[#FF9900]">
              <Upload className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900">
                1. Import Canvas HTML Modules Export
              </h2>
              <p className="text-[11px] text-slate-500">
                Parses course modules, module IDs, items, and external tools
              </p>
            </div>
          </div>

          <form onSubmit={handleImportCanvasHtml} className="space-y-3">
            <div className="border-2 border-dashed border-slate-200 rounded-xl p-4 text-center hover:border-slate-300 transition-colors">
              <input
                type="file"
                accept=".html,.htm"
                onChange={(e) => setCanvasHtmlFile(e.target.files?.[0] || null)}
                className="text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-slate-100 file:text-slate-800 hover:file:bg-slate-200 cursor-pointer"
              />
              <p className="text-[11px] text-slate-400 mt-1">
                Accepts official Instructure Canvas HTML module snapshot
              </p>
            </div>

            <button
              type="submit"
              disabled={!canvasHtmlFile || isImportingHtml}
              className="w-full py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center justify-center space-x-1.5"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>{isImportingHtml ? 'Parsing Canvas Export...' : 'Import Canvas Course Outline'}</span>
            </button>
          </form>
        </div>

        {/* Card 2: PDF / Transcript Ingestion */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm space-y-4">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-xl bg-blue-500/15 flex items-center justify-center text-blue-600">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900">
                2. Ingest Student Guide or Transcript
              </h2>
              <p className="text-[11px] text-slate-500">
                Extracts text with PyMuPDF, chunks, embeds, and indexes for RAG
              </p>
            </div>
          </div>

          <form onSubmit={handleUploadDocument} className="space-y-3 text-xs">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Target Module</label>
                <select
                  value={uploadModuleId}
                  onChange={(e) => setUploadModuleId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-semibold"
                >
                  {modules.filter(m => m.is_core_module).map((m) => (
                    <option key={m.module_id} value={m.module_id}>
                      Module {m.module_number}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">File Format</label>
                <select
                  value={uploadDocType}
                  onChange={(e) => setUploadDocType(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 font-semibold"
                >
                  <option value="pdf">PDF Guide (PyMuPDF)</option>
                  <option value="transcript">Video Transcript (.txt)</option>
                  <option value="text">Notes / Markdown (.txt)</option>
                </select>
              </div>
            </div>

            <div className="border-2 border-dashed border-slate-200 rounded-xl p-3 text-center hover:border-slate-300">
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                className="text-xs text-slate-500 file:mr-3 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-slate-100 file:text-slate-800 hover:file:bg-slate-200 cursor-pointer"
              />
            </div>

            <button
              type="submit"
              disabled={!selectedFile || isUploading}
              className="w-full py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center justify-center space-x-1.5"
            >
              <Database className="w-3.5 h-3.5 text-amber-400" />
              <span>{isUploading ? 'Extracting & Generating Embeddings...' : 'Extract, Chunk & Embed'}</span>
            </button>
          </form>
        </div>

      </div>

      {/* Tabs & Content Inspector */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-5 space-y-4">
        
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setActiveTab('documents')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'documents'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              Indexed Documents ({documents.length})
            </button>
            <button
              onClick={() => setActiveTab('chunks')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'chunks'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              Vector Chunks Inspector ({chunks.length})
            </button>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400 font-medium">Filter by Module:</span>
            <select
              value={selectedModuleFilter}
              onChange={(e) => setSelectedModuleFilter(e.target.value)}
              className="text-xs font-semibold bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-1 focus:ring-2 focus:ring-[#FF9900]"
            >
              <option value="all">All Modules</option>
              {modules.filter(m => m.is_core_module).map((m) => (
                <option key={m.module_id} value={m.module_id}>
                  Module {m.module_number}
                </option>
              ))}
            </select>
          </div>
        </div>

        {activeTab === 'documents' ? (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 uppercase text-[10px]">
                  <th className="py-2.5">Document Name</th>
                  <th className="py-2.5">Module</th>
                  <th className="py-2.5">Type</th>
                  <th className="py-2.5">Chunks</th>
                  <th className="py-2.5">Size</th>
                  <th className="py-2.5">Indexed Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {documents.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-slate-400">
                      No documents manually uploaded yet. Pre-seeded core curriculum textbook chunks are active.
                    </td>
                  </tr>
                ) : (
                  documents.map((doc) => (
                    <tr key={doc.doc_id} className="hover:bg-slate-50">
                      <td className="py-3 font-bold text-slate-800">
                        {doc.title || doc.original_filename}
                      </td>
                      <td className="py-3 text-slate-600">
                        {doc.module_title}
                      </td>
                      <td className="py-3 font-semibold uppercase text-[10px] text-slate-500">
                        {doc.file_type}
                      </td>
                      <td className="py-3 font-bold text-[#0073bb]">
                        {doc.chunk_count}
                      </td>
                      <td className="py-3 text-slate-500">
                        {Math.round(doc.file_size_bytes / 1024)} KB
                      </td>
                      <td className="py-3">
                        <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
                          Vectorized ✓
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="space-y-3">
            {chunks.map((chk) => (
              <div
                key={chk.chunk_id}
                className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs space-y-1.5"
              >
                <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-500 font-semibold gap-2">
                  <div className="flex items-center space-x-2">
                    <span className="bg-amber-100 text-amber-900 px-2 py-0.5 rounded font-bold">
                      {chk.module_title || 'Module'}
                    </span>
                    <span className="text-slate-800">{chk.document_name}</span>
                    {chk.page_number && <span>(Page {chk.page_number})</span>}
                    {chk.timestamp && <span>(Time {chk.timestamp})</span>}
                  </div>
                  <span className="font-mono text-[10px] text-slate-400">ID: {chk.chunk_id}</span>
                </div>

                <p className="text-slate-800 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/60">
                  {chk.content}
                </p>
              </div>
            ))}
          </div>
        )}

      </div>

    </div>
  );
};
