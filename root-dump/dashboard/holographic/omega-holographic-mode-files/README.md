# OMEGA Holographic Mode (MVP)

This folder contains a drop-in MVP for **gesture-driven UI** using MediaPipe Tasks Vision.

## Install

```bash
npm i @mediapipe/tasks-vision framer-motion lucide-react
```

## Files

```
components/HolographicController.tsx
hooks/useHandDetector.ts
lib/gesture/types.ts
lib/gesture/geometry.ts
lib/gesture/recognizers.ts
lib/gesture/gestureBus.ts
examples/command-center-page.tsx
```

## Usage

1) Wire the controller on your Command Center page (see `examples/command-center-page.tsx`).  
2) Inside your `OmegaCommandCenter2`, listen to the `omega-ui` events to open/toggle menu and switch sections.  
3) Toggle **Holographic** (top-right) to enable the webcam and gestures.

## Privacy

All processing is done **locally** in-browser. No frames are sent to a server. Toggle OFF immediately stops the camera tracks.

## Roadmap

- Two-hand zoom/rotate
- r3f constellation map control
- Calibration overlay & per-user thresholds
- Voice + gesture fusion
