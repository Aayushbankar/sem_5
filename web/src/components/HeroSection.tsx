import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, Cpu, Shield, Brain, Network, ArrowRight } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const SUBJECTS = [
  {
    id: 'CDCT',
    title: 'Cloud & Data Center',
    icon: Network,
    color: 'from-blue-500 to-cyan-500',
    description: 'Virtualization, Cloud Storage, and Security.',
  },
  {
    id: 'FOB',
    title: 'Foundation of Blockchain',
    icon: Shield,
    color: 'from-amber-500 to-orange-600',
    description: 'Decentralization, Crypto, and Smart Contracts.',
  },
  {
    id: 'IOT',
    title: 'Hands on IoT',
    icon: Cpu,
    color: 'from-emerald-400 to-teal-500',
    description: 'Sensors, Actuators, and Cloud Platforms.',
  },
  {
    id: 'AIPD',
    title: 'AI Product Design',
    icon: Brain,
    color: 'from-purple-500 to-pink-500',
    description: 'Human-Centered AI and Strategy.',
  },
  {
    id: 'AIPE',
    title: 'AI Prompt Engineering',
    icon: BookOpen,
    color: 'from-indigo-400 to-violet-600',
    description: 'LLMs, RAG, and Agentic AI.',
  }
];

export const HeroSection = () => {
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  return (
    <div className="relative z-10 max-w-7xl mx-auto w-full px-6 py-20 flex flex-col items-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="text-center mb-16"
      >
        <div className="inline-block mb-4 px-3 py-1 rounded-full border border-white/10 bg-white/5 backdrop-blur-md text-sm text-gray-300 font-medium">
          Igloo.inc Academy
        </div>
        <h1 className="text-5xl md:text-7xl font-display font-bold tracking-tight mb-6">
          Semester 5 <br />
          <span className="text-gradient">Premium Archive</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto font-sans">
          Elevate your engineering knowledge. Explore curated textbook notes, practicals, and deep dives.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
        {SUBJECTS.map((subject, idx) => {
          const Icon = subject.icon;
          const isHovered = hoveredId === subject.id;
          
          return (
            <motion.a
              key={subject.id}
              href={`/sem_5/docs/${subject.id}/notes`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              onMouseEnter={() => setHoveredId(subject.id)}
              onMouseLeave={() => setHoveredId(null)}
              className={cn(
                "group relative p-6 rounded-2xl border transition-all duration-300 overflow-hidden",
                "bg-white/[0.02] border-white/10 backdrop-blur-md",
                "hover:bg-white/[0.04] hover:border-white/20 hover:shadow-2xl hover:-translate-y-1"
              )}
            >
              <div className={cn(
                "absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-500 bg-gradient-to-br",
                subject.color
              )} />
              
              <div className="relative z-10">
                <div className={cn(
                  "w-12 h-12 rounded-xl flex items-center justify-center mb-4 text-white bg-gradient-to-br shadow-lg",
                  subject.color
                )}>
                  <Icon size={24} />
                </div>
                
                <h3 className="text-xl font-display font-semibold text-white mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-400 transition-all duration-300">
                  {subject.title}
                </h3>
                
                <p className="text-sm text-gray-400 mb-6">
                  {subject.description}
                </p>

                <div className="flex items-center text-sm font-medium text-white/60 group-hover:text-white transition-colors">
                  Explore Module <ArrowRight size={16} className="ml-2 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </motion.a>
          );
        })}
      </div>
    </div>
  );
};
