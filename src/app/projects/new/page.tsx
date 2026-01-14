'use client';

import React, { useState } from 'react';
import { Upload, Link as LinkIcon, Globe, Sparkles } from 'lucide-react';

export default function NewProject() {
  const [sourceUrl, setSourceUrl] = useState('');

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold">New Dubbing Project</h1>
        <p className="text-gray-500">Translate your content into any language with neural precision.</p>
      </header>

      <div className="grid gap-8">
        {/* Input Methods */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button className="p-8 border-2 border-dashed border-gray-200 rounded-gv hover:border-brand-500 hover:bg-brand-50 transition-all group flex flex-col items-center text-center">
            <Upload className="w-10 h-10 text-gray-400 group-hover:text-brand-600 mb-4" />
            <span className="font-semibold block">Upload Video</span>
            <span className="text-sm text-gray-500 mt-1">MP4, MOV up to 1GB</span>
          </button>
          
          <div className="p-8 border-2 border-gray-100 bg-white rounded-gv shadow-sm">
            <LinkIcon className="w-10 h-10 text-brand-600 mb-4" />
            <span className="font-semibold block">Paste URL</span>
            <input 
              type="text" 
              placeholder="YouTube or TikTok link"
              className="mt-4 w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
              value={sourceUrl}
              onChange={(e) => setSourceUrl(e.target.value)}
            />
          </div>
        </div>

        {/* Configuration */}
        <section className="bg-white p-8 rounded-gv border border-gray-100 shadow-sm space-y-6">
          <div className="flex items-center gap-2 mb-2">
            <Globe className="text-brand-600 w-5 h-5" />
            <h2 className="font-bold text-lg">Target Language</h2>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Primary Dubbing</label>
              <select className="w-full px-4 py-2 border border-gray-200 rounded-lg">
                <option>English (US)</option>
                <option>Spanish (ES)</option>
                <option>Thai (TH)</option>
                <option>Japanese (JP)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Voice Style</label>
              <select className="w-full px-4 py-2 border border-gray-200 rounded-lg">
                <option>Clone Original Voice</option>
                <option>Studio Narrative</option>
                <option>Casual Conversation</option>
              </select>
            </div>
          </div>

          <div className="pt-6 border-t border-gray-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="text-yellow-500 w-4 h-4" />
              <span className="text-sm text-gray-600 italic">Includes AI Lip-Sync & Cultural Adaptation</span>
            </div>
            <button className="px-8 py-3 bg-brand-600 text-white font-bold rounded-gv hover:bg-brand-700 transition-all shadow-lg shadow-brand-100">
              Start Globalizing
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}