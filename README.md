# AI-Based Smart Traffic Management System (Pygame demo)

This repository contains a Pygame-based traffic intersection simulator with an AI-driven adaptive signal controller.

## Quick start
1. Create virtualenv, install requirements:
   ```
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run:
   ```
   python src/simulation.py
   ```

## Images
The `images/` directory contains extracted assets from uploaded example projects when available.
If you replace images, ensure the following structure:
```
images/
  intersection.png
  signals/
    red.png
    yellow.png
    green.png
  right/
  left/
  up/
  down/
```

## AI Controller
`src/ai_controller.py` implements a lightweight, queue-based adaptive controller.

## License
MIT