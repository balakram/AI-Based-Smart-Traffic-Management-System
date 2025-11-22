# 🚦 AI-Based Smart Traffic Management System  
### Intelligent Real-Time Traffic Signal Optimization using Python, Pygame & Adaptive Control

This project implements an **AI-driven adaptive traffic signal system** that dynamically adjusts signal timings based on real-time vehicular congestion.  
It includes a fully working **traffic intersection simulator (Pygame)** and an **AI controller** that optimizes green times based on queue lengths.

The project is inspired by the Pygame intersection articles by Mihir Gandhi and extended with a modern adaptive controller.

---

## 🧠 Key Features

### ✅ **AI-Driven Adaptive Signal Timing**
- Monitors queue lengths in real-time  
- Adjusts green signal duration proportionally  
- Reduces congestion & improves traffic flow  
- Uses exponential smoothing to avoid abrupt changes  

### ✅ **Realistic Traffic Simulation**
- Multi-lane intersection  
- Real vehicle images (cars, buses, bikes, trucks)  
- Signal states: Green → Yellow → Red  
- Continuous random vehicle generation  

### ✅ **Modular Architecture**
- `simulation.py` — full traffic simulator  
- `ai_controller.py` — adaptive AI logic  
- Easily replace AI with ML/DQN/RL models  

### ✅ **GitHub & CI Ready**
- MIT license  
- `.gitignore` and clean project structure  
- GitHub Actions workflow for linting/testing  

---

## 📁 Project Structure

ai-traffic-manager/
│
├── images/                     # Extracted assets from uploaded zips
│   ├── intersection.png
│   ├── signals/
│   ├── right/
│   ├── left/
│   ├── up/
│   └── down/
│
├── src/
│   ├── simulation.py           # Main traffic simulation (Pygame)
│   └── ai_controller.py        # AI-based adaptive traffic controller
│
├── .github/workflows/
│   └── python-app.yml          # GitHub CI workflow
│
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md

---

## 🚀 Installation & Setup

### 1️⃣ Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Simulation
python src/simulation.py


🧠 How the AI Works (Adaptive Algorithm)
The AI controller:


Measures queue lengths for all directions


Calculates weight distribution (bigger queues → longer green)


Uses a dynamic cycle budget


Applies exponential smoothing to avoid oscillations


Updates defaultGreen times in real time


This system can later be replaced with:


Reinforcement Learning (DQN, PPO)


Genetic Algorithms


Deep Q-Network traffic agents



🖼 Screenshots (Optional)
You can add your own screenshots here:
![Simulation Screenshot](images/screenshot1.png)
![Adaptive Signal Timing](images/screenshot2.png)


🧪 GitHub Actions CI
The repository includes a CI workflow:


Python setup


Dependency installation


Smoke test import of Pygame & NumPy


Workflow file location:
.github/workflows/python-app.yml


📦 Download Project ZIP
Download the ready-to-run ZIP:
👉 ai-traffic-manager.zip

📝 License
This project is licensed under the MIT License, allowing commercial and academic use.

⭐ Contributing
Pull requests, issue discussions, and feature improvements are welcome!

🙌 Acknowledgements


Tutorial inspiration from Mihir Gandhi


Vehicle/road assets extracted from uploaded references


Thanks to the OpenAI ecosystem


```

