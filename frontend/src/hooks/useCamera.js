import { useState, useRef, useCallback, useEffect } from 'react';

export function useCamera() {
  const [cameraStatus, setCameraStatus] = useState('Ready'); // Ready, Active, Permission Required, Error
  const [errorMsg, setErrorMsg] = useState(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const startCamera = useCallback(async () => {
    try {
      setCameraStatus('Permission Required');
      setErrorMsg(null);
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 }, 
          height: { ideal: 480 },
          facingMode: "user"
        } 
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setCameraStatus('Active');
    } catch (err) {
      console.error("Camera error:", err);
      if (err.name === 'NotAllowedError') {
        setCameraStatus('Error');
        setErrorMsg('Camera permission denied.');
      } else if (err.name === 'NotFoundError') {
        setCameraStatus('Error');
        setErrorMsg('No camera found.');
      } else {
        setCameraStatus('Error');
        setErrorMsg('Camera unavailable.');
      }
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setCameraStatus('Ready');
    setErrorMsg(null);
  }, []);

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, [stopCamera]);

  return {
    videoRef,
    cameraStatus,
    errorMsg,
    startCamera,
    stopCamera
  };
}
