import React from 'react';
import { AlertTriangle } from 'lucide-react';

export function ModelInfo({ modelInfo }) {
  if (!modelInfo) return null;

  const isSynthetic = modelInfo.training_data_type === 'synthetic_fixture';
  const notProduction = modelInfo.is_production_model === false || modelInfo.is_production_ready === false;

  return (
    <div className="w-full mt-8 p-4 bg-gray-900 border border-gray-800 rounded-xl">
      {(isSynthetic || notProduction) && (
        <div className="flex items-start gap-3 p-3 mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-500">
          <AlertTriangle className="shrink-0 mt-0.5" size={18} />
          <div className="text-sm">
            <p className="font-bold uppercase tracking-wide">⚠ Development Model</p>
            <p className="mt-1 text-amber-500/80">
              {modelInfo.dataset_warning || (isSynthetic ? "Synthetic Fixture Model. Not trained on real gesture data." : "This model is not yet production ready.")}
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
        <div>
          <span className="block text-gray-500 text-xs uppercase tracking-wider mb-1">Model</span>
          <span className="font-medium text-gray-300">{modelInfo.model_type}</span>
        </div>
        <div>
          <span className="block text-gray-500 text-xs uppercase tracking-wider mb-1">Version</span>
          <span className="font-medium text-gray-300">v{modelInfo.model_version}</span>
        </div>
        <div>
          <span className="block text-gray-500 text-xs uppercase tracking-wider mb-1">Feature Spec</span>
          <span className="font-medium text-gray-300">v{modelInfo.feature_spec_version} • 63 dims</span>
        </div>
        <div>
          <span className="block text-gray-500 text-xs uppercase tracking-wider mb-1">Training Data</span>
          <span className="font-medium text-gray-300 capitalize">{modelInfo.training_data_type?.replace('_', ' ') || 'Unknown'}</span>
        </div>
      </div>
    </div>
  );
}
