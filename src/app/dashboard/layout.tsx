import React from 'react';
import { 
  LayoutDashboard, 
  Video, 
  Languages, 
  Settings, 
  BarChart3, 
  PlusCircle,
  LogOut
} from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen w-full bg-background">
      {/* Sidebar */}
      <aside className="flex w-64 flex-col border-r bg-muted/30 p-4">
        <div className="mb-8 flex items-center gap-2 px-2">
          <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
            <Languages className="text-primary-foreground" size={20} />
          </div>
          <span className="text-xl font-bold tracking-tight">GlobalVoice</span>
        </div>

        <nav className="flex-1 space-y-1">
          <SidebarItem icon={<LayoutDashboard size={18} />} label="Overview" active />
          <SidebarItem icon={<Video size={18} />} label="My Projects" />
          <SidebarItem icon={<BarChart3 size={18} />} label="Analytics" />
          <SidebarItem icon={<Settings size={18} />} label="Settings" />
        </nav>

        <div className="mt-auto border-t pt-4">
          <Button variant="ghost" className="w-full justify-start gap-2 text-muted-foreground">
            <LogOut size={18} />
            Logout
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="flex h-16 items-center justify-between border-b px-8 bg-background/80 backdrop-blur-md sticky top-0 z-10">
          <h1 className="text-lg font-semibold">Creator Studio</h1>
          <Button className="gap-2">
            <PlusCircle size={18} />
            New Translation
          </Button>
        </header>
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}

function SidebarItem({ icon, label, active = false }: { icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <button className={`
      flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
      ${active ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-accent hover:text-foreground'}
    `}>
      {icon}
      {label}
    </button>
  );
}