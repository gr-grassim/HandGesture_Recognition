import { expect, test } from 'vitest';
import { extractFeatures } from './landmarkProcessor';
import fixtureData from '../../../ml/fixtures/landmark_fixture.json';
import expectedData from '../../../ml/fixtures/expected_features.json';

test('JS feature extraction exactly matches Python output', () => {
  const landmarks = fixtureData.landmarks;
  const jsFeatures = extractFeatures(landmarks);
  const pyFeatures = expectedData.features;

  expect(jsFeatures.length).toBe(63);
  expect(jsFeatures.length).toBe(pyFeatures.length);

  for (let i = 0; i < jsFeatures.length; i++) {
    // Assert floating point parity with a very tight tolerance
    expect(jsFeatures[i]).toBeCloseTo(pyFeatures[i], 5);
  }
});
