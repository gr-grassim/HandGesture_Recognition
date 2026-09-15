import React from 'react';
import { Camera, CameraOff, AlertCircle } from 'lucide-react';

export function ControlButtons({ cameraStatus, onStart, onStop }) {
  const isError = cameraStatus === 'Error';
  const isActive = cameraStatus === 'Active';

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <button
        onClick={onStart}
        disabled={isActive || isError}
        className={`flex items-center gap-2 px-6 py-3 rounded-full font-semibold transition-all ${
          isActive || isError
            ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
            : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg hover:shadow-indigo-500/25'
        }`}
      >
        <Camera size={20} />
        Start Camera
      </button>

      <button
        onClick={onStop}
        disabled={!isActive}
        className={`flex items-center gap-2 px-6 py-3 rounded-full font-semibold transition-all ${
          !isActive
            ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
            : 'bg-rose-600 hover:bg-rose-500 text-white shadow-lg hover:shadow-rose-500/25'
        }`}
      >
        <CameraOff size={20} />
        Stop Camera
      </button>
      
      {isError && (
        <div className="flex items-center gap-2 text-rose-500 bg-rose-500/10 px-4 py-2 rounded-full text-sm font-medium">
          <AlertCircle size={16} />
          <span>Please check camera permissions</span>
        </div>
      )}
    </div>
  );
}
