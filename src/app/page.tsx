import React from 'react';
import { 
  TrendingUp, 
  Clock, 
  Languages, 
  PlayCircle,
  MoreVertical
} from 'lucide-react';

const stats = [
  { label: 'Total Dubbed Minutes', value: '1,240', icon: Clock, color: 'text-blue-600' },
  { label: 'Global Reach Est.', value: '+450%', icon: TrendingUp, color: 'text-green-600' },
  { label: 'Active Languages', value: '12', icon: Languages, color: 'text-purple-600' },
];

const recentProjects = [
  { id: '1', title: 'Cooking Masterclass - Ep 04', status: 'Processing', progress: 65, language: 'Spanish' },
  { id: '2', title: 'Tech Review: iPhone 15 Pro', status: 'Completed', progress: 100, language: 'Thai' },
  { id: '3', title: 'Startup Pitch Deck V2', status: 'Draft', progress: 0, language: 'Japanese' },
];

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold text-gray-900">Creator Studio</h1>
        <p className="text-gray-500 mt-1">Welcome back. Your global audience is waiting.</p>
      </header>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white p-6 rounded-gv border border-gray-100 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <stat.icon className={`${stat.color} w-6 h-6`} />
            </div>
            <p className="text-gray-500 text-sm font-medium">{stat.label}</p>
            <h3 className="text-2xl font-bold mt-1">{stat.value}</h3>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <section className="bg-white rounded-gv border border-gray-100 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="font-semibold text-lg">Recent Projects</h2>
          <button className="text-brand-600 text-sm font-medium hover:underline">View All</button>
        </div>
        <div className="divide-y divide-gray-100">
          {recentProjects.map((project) => (
            <div key={project.id} className="p-6 flex items-center gap-4 hover:bg-gray-50 transition-colors">
              <div className="w-16 h-10 bg-gray-100 rounded flex items-center justify-center">
                <PlayCircle className="text-gray-400" />
              </div>
              <div className="flex-1">
                <h4 className="font-medium text-gray-900">{project.title}</h4>
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-blue-50 text-blue-700">
                    {project.language}
                  </span>
                  <span className="text-xs text-gray-400">ID: {project.id}</span>
                </div>
              </div>
              <div className="text-right flex items-center gap-6">
                <div className="w-32 hidden md:block">
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-gray-500">{project.status}</span>
                    <span className="font-semibold">{project.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden">
                    <div 
                      className="bg-brand-600 h-full transition-all duration-500" 
                      style={{ width: `${project.progress}%` }}
                    />
                  </div>
                </div>
                <button className="p-2 hover:bg-gray-100 rounded-full">
                  <MoreVertical size={18} className="text-gray-400" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}