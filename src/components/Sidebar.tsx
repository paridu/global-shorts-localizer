import React from 'react';
import Link from 'next/link';
import { 
  LayoutDashboard, 
  Video, 
  Mic2, 
  Globe2, 
  BarChart3, 
  Settings,
  PlusCircle
} from 'lucide-react';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', href: '/' },
  { icon: Video, label: 'My Projects', href: '/projects' },
  { icon: Mic2, label: 'Voice Library', href: '/voices' },
  { icon: Globe2, label: 'Translations', href: '/translations' },
  { icon: BarChart3, label: 'Analytics', href: '/analytics' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-6">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center">
            <Globe2 className="text-white w-5 h-5" />
          </div>
          <span className="font-bold text-xl tracking-tight text-brand-900">GlobalVoice</span>
        </div>

        <Link 
          href="/projects/new"
          className="flex items-center justify-center gap-2 w-full py-3 bg-brand-600 text-white rounded-gv font-medium hover:bg-brand-700 transition-colors shadow-sm mb-8"
        >
          <PlusCircle size={18} />
          New Project
        </Link>

        <nav className="space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.label}
              href={item.href}
              className="flex items-center gap-3 px-3 py-2.5 text-gray-600 hover:bg-gray-50 hover:text-brand-600 rounded-lg transition-all group"
            >
              <item.icon size={20} className="group-hover:scale-110 transition-transform" />
              <span className="font-medium">{item.label}</span>
            </Link>
          ))}
        </nav>
      </div>

      <div className="mt-auto p-6 border-t border-gray-100">
        <Link
          href="/settings"
          className="flex items-center gap-3 px-3 py-2 text-gray-500 hover:text-gray-900"
        >
          <Settings size={20} />
          <span className="font-medium">Settings</span>
        </Link>
      </div>
    </aside>
  );
}