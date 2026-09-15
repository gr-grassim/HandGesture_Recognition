import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GestureResult } from './components/GestureResult';
import { ConfidenceBar } from './components/ConfidenceBar';
import { StatusIndicator } from './components/StatusIndicator';
import { ModelInfo } from './components/ModelInfo';

describe('UI Components', () => {
  it('renders ConfidenceBar with correct width', () => {
    const { container } = render(<ConfidenceBar confidence={0.85} visible={true} />);
    expect(screen.getByText('85%')).toBeDefined();
    // Width should be 85%
    const bar = container.querySelector('.bg-gradient-to-r');
    expect(bar.style.width).toBe('85%');
  });

  it('hides ConfidenceBar when visible is false', () => {
    const { container } = render(<ConfidenceBar confidence={0.85} visible={false} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders UNKNOWN gesture state properly', () => {
    render(<GestureResult gesture="UNKNOWN" handDetected={true} apiStatus="Connected" />);
    expect(screen.getByText('Unknown Gesture')).toBeDefined();
    expect(screen.getByText('❓')).toBeDefined();
  });

  it('renders No Hand Detected state', () => {
    render(<GestureResult gesture="fist" handDetected={false} apiStatus="Connected" />);
    expect(screen.getByText('No Hand Detected')).toBeDefined();
    expect(screen.getByText('👋')).toBeDefined();
  });

  it('renders Backend Unavailable state', () => {
    render(<GestureResult gesture="fist" handDetected={true} apiStatus="Unavailable" />);
    expect(screen.getByText('Backend Unavailable')).toBeDefined();
    expect(screen.getByText('🔌')).toBeDefined();
  });

  it('renders standard known gesture (fist)', () => {
    render(<GestureResult gesture="fist" handDetected={true} apiStatus="Connected" />);
    expect(screen.getByText('FIST')).toBeDefined();
    expect(screen.getByText('✊')).toBeDefined();
  });

  it('renders StatusIndicator colors correctly', () => {
    const { container, rerender } = render(<StatusIndicator label="Test" status="Active" />);
    expect(container.innerHTML).toContain('bg-emerald-500');

    rerender(<StatusIndicator label="Test" status="Error" />);
    expect(container.innerHTML).toContain('bg-rose-500');

    rerender(<StatusIndicator label="Test" status="Disconnected" />);
    expect(container.innerHTML).toContain('bg-amber-500');
  });

  it('renders ModelInfo for synthetic model', () => {
    const info = {
      model_type: 'TestModel',
      model_version: '1.0',
      feature_spec_version: '1.0',
      training_data_type: 'synthetic_fixture',
      is_production_model: false
    };
    render(<ModelInfo modelInfo={info} />);
    expect(screen.getByText('⚠ Development Model')).toBeDefined();
    expect(screen.getByText('synthetic fixture')).toBeDefined();
  });
});
