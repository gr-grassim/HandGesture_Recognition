/**
 * Extracts normalized features from 21 MediaPipe hand landmarks.
 * Must produce the exact same output as the Python backend logic.
 * 
 * @param {Array} landmarks Array of 21 objects with {x, y, z}
 * @returns {Array} 1D array of 63 normalized float features
 */
export function extractFeatures(landmarks) {
  if (!landmarks || landmarks.length !== 21) {
    throw new Error("Expected exactly 21 landmarks.");
  }

  // Translate relative to wrist (landmark 0)
  const wristX = landmarks[0].x || 0.0;
  const wristY = landmarks[0].y || 0.0;
  const wristZ = landmarks[0].z || 0.0;

  const translated = [];
  let maxVal = 0.0;

  for (let i = 0; i < landmarks.length; i++) {
    const lm = landmarks[i];
    const dx = (lm.x || 0.0) - wristX;
    const dy = (lm.y || 0.0) - wristY;
    const dz = (lm.z || 0.0) - wristZ;

    translated.push([dx, dy, dz]);
    maxVal = Math.max(maxVal, Math.abs(dx), Math.abs(dy), Math.abs(dz));
  }

  if (maxVal === 0.0) {
    maxVal = 1.0;
  }

  const features = [];
  for (let i = 0; i < translated.length; i++) {
    const [dx, dy, dz] = translated[i];
    features.push(dx / maxVal, dy / maxVal, dz / maxVal);
  }

  return features;
}
