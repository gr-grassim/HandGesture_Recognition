import React from 'react';

export function ConfidenceBar({ confidence, visible }) {
  if (!visible) return null;

  const percentage = Math.round(confidence * 100);
  
  return (
    <div className="w-full mt-6 space-y-2">
      <div className="flex justify-between text-sm font-semibold text-gray-400">
        <span>Confidence</span>
        <span>{percentage}%</span>
      </div>
      <div className="h-4 w-full bg-gray-800 rounded-full overflow-hidden border border-gray-700">
        <div 
          className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
