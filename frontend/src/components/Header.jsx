import React from 'react';
import { Hand } from 'lucide-react';

export function Header() {
  return (
    <header className="w-full pb-6 mb-6 border-b border-gray-800">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-indigo-500/10 rounded-xl text-indigo-400">
          <Hand size={32} />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Hand Gesture Recognition</h1>
          <p className="text-gray-400 text-sm mt-1">Real-time computer vision demo</p>
        </div>
      </div>
    </header>
  );
}
