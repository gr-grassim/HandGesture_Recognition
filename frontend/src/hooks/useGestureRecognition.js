import { useState, useRef, useCallback, useEffect } from 'react';
import { FilesetResolver, HandLandmarker } from '@mediapipe/tasks-vision';
import { extractFeatures } from '../utils/landmarkProcessor';
import { config } from '../config';

export function useGestureRecognition(videoRef) {
  const [gesture, setGesture] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [handDetected, setHandDetected] = useState(false);
  const [apiStatus, setApiStatus] = useState('Disconnected'); // Connected, Disconnected, Unavailable
  
  const landmarkerRef = useRef(null);
  const requestAnimationFrameRef = useRef(null);
  const isPredictingRef = useRef(false);
  const lastPredictionTimeRef = useRef(0);

  // Check health on mount
  useEffect(() => {
    fetch(`${config.apiBaseUrl}/health`)
      .then(res => {
        if (res.ok) setApiStatus('Connected');
      })
      .catch(() => setApiStatus('Disconnected'));
  }, []);

  // Initialize HandLandmarker
  useEffect(() => {
    let active = true;
    const initLandmarker = async () => {
      try {
        const vision = await FilesetResolver.forVisionTasks(
          "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm"
        );
        const landmarker = await HandLandmarker.createFromOptions(vision, {
          baseOptions: {
            modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
            delegate: "GPU"
          },
          runningMode: "VIDEO",
          numHands: 1
        });
        if (active) {
          landmarkerRef.current = landmarker;
        }
      } catch (err) {
        console.error("Failed to initialize MediaPipe HandLandmarker:", err);
      }
    };
    initLandmarker();
    
    return () => {
      active = false;
      if (landmarkerRef.current) {
        landmarkerRef.current.close();
      }
    };
  }, []);

  const predictFrame = useCallback(async () => {
    if (!videoRef.current || videoRef.current.readyState < 2 || !landmarkerRef.current) {
      return;
    }

    const video = videoRef.current;
    const startTimeMs = performance.now();

    // Run MediaPipe detection
    const results = landmarkerRef.current.detectForVideo(video, startTimeMs);

    if (results.landmarks && results.landmarks.length > 0) {
      setHandDetected(true);
      const rawLandmarks = results.landmarks[0]; // First hand

      // Rate limit API calls
      const now = Date.now();
      if (!isPredictingRef.current && (now - lastPredictionTimeRef.current > config.inferenceIntervalMs)) {
        isPredictingRef.current = true;
        lastPredictionTimeRef.current = now;

        try {
          // Extract features exactly as defined in canonical logic
          const features = extractFeatures(rawLandmarks);

          const response = await fetch(`${config.apiBaseUrl}/api/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features: features })
          });

          if (!response.ok) {
            throw new Error(`API returned status ${response.status}`);
          }

          const data = await response.json();
          setApiStatus('Connected');
          
          if (data.hand_detected) {
            setGesture(data.gesture);
            setConfidence(data.confidence);
          } else {
             // API explicitly rejected it
             setGesture(null);
             setConfidence(0);
          }
        } catch (err) {
          console.error("Prediction API Error:", err);
          setApiStatus('Unavailable');
        } finally {
          isPredictingRef.current = false;
        }
      }
    } else {
      setHandDetected(false);
      // Reset confidence if no hand
      setGesture(null);
      setConfidence(0);
    }
  }, [videoRef]);

  // Main render loop
  const tick = useCallback(() => {
    predictFrame();
    requestAnimationFrameRef.current = requestAnimationFrame(tick);
  }, [predictFrame]);

  // Start/Stop loop based on camera activity
  const startLoop = useCallback(() => {
    if (!requestAnimationFrameRef.current) {
      requestAnimationFrameRef.current = requestAnimationFrame(tick);
    }
  }, [tick]);

  const stopLoop = useCallback(() => {
    if (requestAnimationFrameRef.current) {
      cancelAnimationFrame(requestAnimationFrameRef.current);
      requestAnimationFrameRef.current = null;
    }
    setHandDetected(false);
    setGesture(null);
    setConfidence(0);
  }, []);

  return {
    gesture,
    confidence,
    handDetected,
    apiStatus,
    startLoop,
    stopLoop,
    landmarkerRef
  };
}
