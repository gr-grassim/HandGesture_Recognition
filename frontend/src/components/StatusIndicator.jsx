import React from 'react';

export function StatusIndicator({ label, status }) {
  let colorClass = 'bg-gray-500';
  
  if (status === 'Active' || status === 'Connected' || status === 'Ready') {
    colorClass = 'bg-emerald-500';
  } else if (status === 'Error' || status === 'Unavailable' || status === 'Permission Required') {
    colorClass = 'bg-rose-500';
  } else if (status === 'Disconnected') {
    colorClass = 'bg-amber-500';
  }

  return (
    <div className="flex items-center gap-2">
      <div className={`w-2.5 h-2.5 rounded-full ${colorClass} ${colorClass === 'bg-emerald-500' ? 'animate-pulse' : ''}`} />
      <span className="text-sm font-medium text-gray-300 whitespace-nowrap">
        {label}: {status}
      </span>
    </div>
  );
}
