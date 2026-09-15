# ML Pipeline Architecture

## Feature Specification

Both the Python backend (during training) and the JavaScript frontend (during production inference) must implement the exact same feature extraction logic to prevent training-serving skew.

### Input
21 3D landmarks from MediaPipe Hands. Each landmark has `x, y, z` coordinates.

### Normalization Process
1. **Translation**: Make all coordinates relative to the wrist (landmark 0).
   - `dx_i = x_i - x_0`
   - `dy_i = y_i - y_0`
   - `dz_i = z_i - z_0`
2. **Scaling**: Find the maximum absolute value among all `dx_i, dy_i, dz_i` across all 21 landmarks.
   - `max_val = max(abs(d)) for all d in dx, dy, dz`
   - If `max_val` is 0 (extremely unlikely), set it to 1 to avoid division by zero.
3. **Normalization**: Divide all translated coordinates by `max_val`.
   - `nx_i = dx_i / max_val`
   - `ny_i = dy_i / max_val`
   - `nz_i = dz_i / max_val`

### Feature Vector Output
A 1D array of 63 floats (21 landmarks * 3 coordinates), flattened in the following order:
`[nx_0, ny_0, nz_0, nx_1, ny_1, nz_1, ..., nx_20, ny_20, nz_20]`

Since `nx_0, ny_0, nz_0` will always be `0.0, 0.0, 0.0`, they could be omitted, but they are retained for indexing simplicity and consistency.
