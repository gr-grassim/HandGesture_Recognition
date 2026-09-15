def extract_features(landmarks):
    """
    Extracts normalized features from 21 MediaPipe hand landmarks.
    Each landmark should be a dict or object with x, y, z attributes.
    """
    if len(landmarks) != 21:
        raise ValueError("Expected exactly 21 landmarks.")
        
    # Handle both dict and object access
    def get_coord(lm, coord):
        if isinstance(lm, dict):
            return lm.get(coord, 0.0)
        return getattr(lm, coord, 0.0)

    # Translate relative to wrist (landmark 0)
    wrist_x = get_coord(landmarks[0], 'x')
    wrist_y = get_coord(landmarks[0], 'y')
    wrist_z = get_coord(landmarks[0], 'z')
    
    translated = []
    max_val = 0.0
    
    for lm in landmarks:
        dx = get_coord(lm, 'x') - wrist_x
        dy = get_coord(lm, 'y') - wrist_y
        dz = get_coord(lm, 'z') - wrist_z
        
        translated.append((dx, dy, dz))
        max_val = max(max_val, abs(dx), abs(dy), abs(dz))
        
    if max_val == 0.0:
        max_val = 1.0
        
    features = []
    for dx, dy, dz in translated:
        features.extend([dx / max_val, dy / max_val, dz / max_val])
        
    return features
