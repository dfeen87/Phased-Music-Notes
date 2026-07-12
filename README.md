# Phased‑Music‑Notes  
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)
![Status](https://img.shields.io/badge/Status-Hardened-success)
![Status](https://img.shields.io/badge/Status-DSP--Optimized-green)
[![CI](https://github.com/dfeen87/Phased-Music-Notes/actions/workflows/ci.yml/badge.svg)](https://github.com/dfeen87/Phased-Music-Notes/actions/workflows/ci.yml)


---

## 🎧 Smooth Audio Notes  
Phased‑Music‑Notes is a lightweight Python DSP engine that creates **phase‑aligned, gradual transitions between musical notes**. It analyzes note boundaries, blends harmonic structure, and softens abrupt changes to produce smoother, more expressive continuity in any audio track.

This project is MIT‑licensed, clone‑friendly, and designed for producers, sound designers, and developers who want a simple, innovative tool for **gentle note transitions** and **soft harmonic movement**.

---

## ✨ Features  
- **Phase‑Aligned Note Smoothing** — reduces harsh jumps between notes  
- **Harmonic Blending** — softens overtones for a warm, gradual sound  
- **Boundary Detection** — identifies note transitions in audio  
- **Soft DSP Modes** — customizable smoothing profiles  
- **Python DSL** — expressive commands for musical shaping  
- **Plugin‑Ready Architecture** — can be wrapped into VST/AU later  
- **Minimal Codebase** — easy to fork, extend, and integrate  

---

## 🧠 Why This Exists  
Slowed audio often reveals harsh discontinuities in acoustic instruments—especially piano—where note transitions become abrupt, metallic, or overly resonant. Phased‑Music‑Notes introduces a **continuity layer** that gently smooths these transitions without altering tempo or performance feel.

This project explores a new idea:  
> *What if musical notes could transition with engineered softness, even in instruments that don’t naturally provide it?*

---

## 📦 Installation  
```bash
pip install phased-music-notes
```

(Placeholder — update once published.)

---

## 🐍 Example Usage  
A simple Python DSL for soft note transitions:

```python
from phased_music_notes import SmoothPhase

engine = SmoothPhase(mode="velvet")

output = engine.smooth("input.wav")
output.save("output_smooth.wav")
```

Modes you might implement:

- `"velvet"` — softens transients  
- `"legato"` — glides pitch transitions  
- `"melt"` — blends harmonic overtones  

---

## 📁 Project Structure  
```
Phased-Music-Notes/
│
├── src/
│   └── main.py              ← core engine (AeroCam-style)
│
├── phased_music_notes/
│   ├── analyzer.py
│   ├── smoother.py
│   ├── harmonics.py
│   ├── dsl.py
│   └── utils.py
│
├── drivers/
│   ├── cli.py
│   ├── api.py
│   └── vst/
│       ├── CMakeLists.txt
│       ├── PluginProcessor.cpp
│       ├── PluginEditor.cpp
│       ├── python_bridge.cpp
│       └── python_bridge.hpp
│ 
├── examples/
│       ├── smooth_file.py
│       ├── smooth_buffer.py
│       ├── compare_modes.py
│       └── vst_debug_roundtrip.py
│
├──tests/
│    │
│    ├── test_analyzer.py
│    ├── test_smoother.py
│    ├── test_harmonics.py
│    ├── test_engine_integration.py
│    └── test_utils.py
│
├── requirements.txt
├── LICENSE
└── README.md

```

---

## 🧪 Roadmap  
- **Add more smoothing modes**  
- **Implement real‑time processing**  
- **Create a VST/AU wrapper**  
- **Add visualization tools**  
- **Publish pip package**  

---

## 🤝 Contributing  
Contributions are welcome.  
Feel free to open issues, submit PRs, or propose new smoothing modes.

---

## 📜 License  
MIT License — free to use, modify, and integrate into commercial or personal projects.

---

## 🙏 Acknowledgements

The development of this codebase reflects a collaborative effort across contributors and tools.

Google Jules provided essential scaffolding for the tests/ and examples/ directories, ensuring the DSP engine is thoroughly validated and easy to adopt.

Microsoft Copilot contributed Python logic, architectural guidance, and iterative refinement throughout the design of the DSP modules, the buffer‑based engine, and the cross‑language integration.

The core conceptual breakthrough — the Phased‑Music‑Notes architecture, smoothing modes, harmonic blending pipeline, and deterministic DSP design — was developed by Don Feeney, working in collaboration with Copilot.

This project embodies team‑oriented engineering: human insight, AI‑accelerated development, and a shared commitment to building robust, expressive audio software.
