import React from 'react';
import { Play, Globe, MoreVertical, CheckCircle2, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ProjectCardProps {
  title: string;
  originalLanguage: string;
  targetLanguages: string[];
  status: 'processing' | 'completed' | 'failed';
  thumbnailUrl?: string;
  timestamp: string;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  title,
  originalLanguage,
  targetLanguages,
  status,
  thumbnailUrl,
  timestamp
}) => {
  return (
    <div className="group relative overflow-hidden rounded-xl border bg-card p-4 transition-all hover:shadow-md">
      <div className="relative aspect-video w-full overflow-hidden rounded-lg bg-muted">
        {thumbnailUrl ? (
          <img src={thumbnailUrl} alt={title} className="object-cover transition-transform group-hover:scale-105" />
        ) : (
          <div className="flex h-full items-center justify-center">
            <Play className="h-10 w-10 text-muted-foreground/40" />
          </div>
        )}
        <div className="absolute bottom-2 right-2">
          {status === 'completed' ? (
            <span className="flex items-center gap-1 rounded-full bg-green-500/90 px-2 py-1 text-[10px] font-bold text-white uppercase">
              <CheckCircle2 size={12} /> Ready
            </span>
          ) : (
            <span className="flex items-center gap-1 rounded-full bg-amber-500/90 px-2 py-1 text-[10px] font-bold text-white uppercase">
              <Clock size={12} /> Processing
            </span>
          )}
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-foreground line-clamp-1">{title}</h3>
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <MoreVertical size={16} />
          </Button>
        </div>
        
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="font-medium text-primary uppercase">{originalLanguage}</span>
          <span>→</span>
          <div className="flex gap-1">
            {targetLanguages.map((lang) => (
              <span key={lang} className="flex items-center gap-1 rounded bg-secondary/10 px-1.5 py-0.5 text-secondary">
                <Globe size={10} /> {lang}
              </span>
            ))}
          </div>
        </div>
        
        <p className="mt-2 text-[10px] text-muted-foreground">
          Updated {timestamp}
        </p>
      </div>
    </div>
  );
};