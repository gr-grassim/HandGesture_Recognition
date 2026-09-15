import React from 'react';

const gestureMap = {
  'open_palm': { icon: '🖐️', label: 'OPEN PALM' },
  'fist': { icon: '✊', label: 'FIST' },
  'thumbs_up': { icon: '👍', label: 'THUMBS UP' },
  'thumbs_down': { icon: '👎', label: 'THUMBS DOWN' },
  'victory': { icon: '✌️', label: 'VICTORY' },
  'okay': { icon: '👌', label: 'OKAY' },
  'pointing': { icon: '🫵', label: 'POINTING' },
  'rock': { icon: '🤘', label: 'ROCK' },
  'UNKNOWN': { icon: '❓', label: 'Unknown Gesture' }
};

export function GestureResult({ gesture, handDetected, apiStatus }) {
  if (apiStatus === 'Unavailable') {
    return (
      <div className="flex flex-col items-center justify-center p-8 bg-gray-900 rounded-xl border border-gray-800 h-full">
        <span className="text-4xl mb-4">🔌</span>
        <h2 className="text-xl font-bold text-gray-400 text-center">Backend Unavailable</h2>
      </div>
    );
  }

  if (!handDetected) {
    return (
      <div className="flex flex-col items-center justify-center p-8 bg-gray-900 rounded-xl border border-gray-800 h-full transition-all">
        <span className="text-4xl mb-4 opacity-50 grayscale">👋</span>
        <h2 className="text-xl font-bold text-gray-500">No Hand Detected</h2>
      </div>
    );
  }

  const { icon, label } = gestureMap[gesture] || gestureMap['UNKNOWN'];
  const isUnknown = gesture === 'UNKNOWN';

  return (
    <div className={`flex flex-col items-center justify-center p-8 rounded-xl border transition-all h-full ${
      isUnknown ? 'bg-orange-500/10 border-orange-500/30' : 'bg-emerald-500/10 border-emerald-500/30'
    }`}>
      <span className="text-6xl mb-6 animate-pulse">{icon}</span>
      <h2 className={`text-2xl font-black tracking-wider ${
        isUnknown ? 'text-orange-400' : 'text-emerald-400'
      }`}>
        {label}
      </h2>
    </div>
  );
}
