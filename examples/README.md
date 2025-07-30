# XBot Model Example

This directory contains an example XBot model from Mixamo for testing the fbx2glb conversion process.

## Contents

- `XBot.fbx` - The original FBX model from Mixamo
- `XBot.glb` - The converted GLB model (created by running the conversion tools)
- `XBotModel.tsx` - A React/Three.js component generated from the model

## Usage

### Converting the model

From the project root, run:

```bash
# Using the Python module
fbx2glb examples/XBot/XBot.fbx

# Using the CLI in development
python -m fbx2glb.cli examples/XBot/XBot.fbx

# Generating a React component
fbx2glb-component examples/XBot/XBot.fbx
```

### Using the model in a React/Three.js application

```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { XBotModel } from './XBotModel';

function Scene() {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <XBotModel position={[0, 0, 0]} animation="Idle" />
      <OrbitControls />
    </Canvas>
  );
}
```

## Model Information

The XBot model is a standard humanoid character commonly used for testing and development purposes. It has a full skeleton rig and includes several animations.

### Animations

- Idle
- Walk
- Run
- Jump
- Dance

## License

The XBot model is part of the Mixamo library by Adobe and is subject to [Adobe's licensing terms](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html).
