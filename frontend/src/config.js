export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  inferenceIntervalMs: parseInt(import.meta.env.VITE_INFERENCE_INTERVAL_MS || '100', 10),
};
