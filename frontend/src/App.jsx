import React, { useEffect, useState } from 'react';
import { Header } from './components/Header';
import { CameraView } from './components/CameraView';
import { ControlButtons } from './components/ControlButtons';
import { GestureResult } from './components/GestureResult';
import { ConfidenceBar } from './components/ConfidenceBar';
import { StatusIndicator } from './components/StatusIndicator';
import { ModelInfo } from './components/ModelInfo';
import { useCamera } from './hooks/useCamera';
import { useGestureRecognition } from './hooks/useGestureRecognition';
import { config } from './config';

function App() {
  const [modelInfo, setModelInfo] = useState(null);
  
  const { videoRef, cameraStatus, startCamera, stopCamera } = useCamera();
  
  const {
    gesture,
    confidence,
    handDetected,
    apiStatus,
    startLoop,
    stopLoop,
    landmarkerRef
  } = useGestureRecognition(videoRef);

  // Fetch model info on mount
  useEffect(() => {
    fetch(`${config.apiBaseUrl}/api/model-info`)
      .then(res => res.json())
      .then(data => setModelInfo(data))
      .catch(err => console.error("Failed to fetch model info", err));
  }, []);

  // Sync recognition loop with camera
  useEffect(() => {
    if (cameraStatus === 'Active') {
      startLoop();
    } else {
      stopLoop();
    }
  }, [cameraStatus, startLoop, stopLoop]);

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-gray-100 font-sans p-4 md:p-8 selection:bg-indigo-500/30">
      <div className="max-w-6xl mx-auto">
        <Header />
        
        <main className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Camera */}
          <div className="space-y-6 flex flex-col h-full">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest">Camera Feed</h2>
            <CameraView 
              videoRef={videoRef} 
              cameraStatus={cameraStatus} 
              landmarkerRef={landmarkerRef}
            />
            
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-gray-900/50 p-4 rounded-xl border border-gray-800">
              <ControlButtons 
                cameraStatus={cameraStatus} 
                onStart={startCamera} 
                onStop={stopCamera} 
              />
              <div className="flex flex-col gap-2">
                <StatusIndicator label="Camera" status={cameraStatus} />
                <StatusIndicator label="Backend" status={apiStatus} />
              </div>
            </div>
          </div>

          {/* Right Column: Prediction */}
          <div className="space-y-6 flex flex-col h-full">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest">Current Gesture</h2>
            
            <div className="flex-1 min-h-[300px]">
              <GestureResult 
                gesture={gesture} 
                handDetected={handDetected} 
                apiStatus={apiStatus} 
              />
            </div>
            
            <ConfidenceBar 
              confidence={confidence} 
              visible={handDetected && apiStatus === 'Connected'} 
            />
          </div>
        </main>

        <ModelInfo modelInfo={modelInfo} />
      </div>
    </div>
  );
}

export default App;
