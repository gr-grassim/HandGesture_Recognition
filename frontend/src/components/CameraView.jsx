import React, { useRef, useEffect } from 'react';
import { HandLandmarker } from '@mediapipe/tasks-vision';

export function CameraView({ videoRef, cameraStatus, landmarkerRef }) {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    let animationFrameId;
    
    const drawLandmarks = () => {
      if (!videoRef.current || !canvasRef.current || !landmarkerRef.current) {
        animationFrameId = requestAnimationFrame(drawLandmarks);
        return;
      }
      
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      
      if (video.videoWidth > 0 && video.videoHeight > 0) {
        if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
        }
        
        ctx.save();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Mirror the canvas because the video is mirrored (user facing camera)
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        
        // Detect and draw
        const results = landmarkerRef.current.detectForVideo(video, performance.now());
        
        if (results.landmarks) {
          for (const landmarks of results.landmarks) {
            // Draw connections
            ctx.strokeStyle = '#00FF00';
            ctx.lineWidth = 2;
            
            for (const connection of HandLandmarker.HAND_CONNECTIONS) {
              const start = landmarks[connection.start];
              const end = landmarks[connection.end];
              ctx.beginPath();
              ctx.moveTo(start.x * canvas.width, start.y * canvas.height);
              ctx.lineTo(end.x * canvas.width, end.y * canvas.height);
              ctx.stroke();
            }
            
            // Draw points
            ctx.fillStyle = '#FF0000';
            for (const pt of landmarks) {
              ctx.beginPath();
              ctx.arc(pt.x * canvas.width, pt.y * canvas.height, 3, 0, 2 * Math.PI);
              ctx.fill();
            }
          }
        }
        ctx.restore();
      }
      
      animationFrameId = requestAnimationFrame(drawLandmarks);
    };
    
    if (cameraStatus === 'Active') {
      drawLandmarks();
    }
    
    return () => {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    };
  }, [cameraStatus, videoRef, landmarkerRef]);

  return (
    <div className="relative w-full max-w-[640px] aspect-video bg-gray-900 rounded-lg overflow-hidden border border-gray-700 shadow-xl">
      {cameraStatus !== 'Active' && (
        <div className="absolute inset-0 flex items-center justify-center text-gray-500">
          <p>{cameraStatus === 'Ready' ? 'Camera is off' : cameraStatus}</p>
        </div>
      )}
      
      <video 
        ref={videoRef}
        className="absolute inset-0 w-full h-full object-cover -scale-x-100" 
        playsInline 
        muted 
      />
      
      <canvas 
        ref={canvasRef}
        className="absolute inset-0 w-full h-full object-cover pointer-events-none"
      />
    </div>
  );
}
