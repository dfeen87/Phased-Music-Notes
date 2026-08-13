# Phased‑Music‑Notes Repository for ISLA
## ISLA Audio Engineering focus is to Smooth Audio Notes with phase‑aligned transitions for cleaner, more natural musical flow.
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Production--Ready-white)
![Status](https://img.shields.io/badge/Status-Hardened-success)
![Status](https://img.shields.io/badge/Status-DSP--Optimized-purple)
[![CI](https://github.com/dfeen87/Phased-Music-Notes/actions/workflows/ci.yml/badge.svg)](https://github.com/dfeen87/Phased-Music-Notes/actions/workflows/ci.yml)


---

## 🎧 Smooth Audio Notes  
Phased‑Music‑Notes is a lightweight Python DSP engine that creates **phase‑aligned, gradual transitions between musical notes**. It analyzes note boundaries, blends harmonic structure, and softens abrupt changes to produce smoother, more expressive continuity in any audio track.

This project is MIT‑licensed, clone‑friendly, and designed for producers, sound designers, and developers who want a simple, innovative tool for **gentle note transitions** and **soft harmonic movement**.

ISLA is a baby girl recently born in Los Angeles. Don Feeney creator of this Repo is now an Uncle. For all that want to contribute meaningfully to dedicate this specific sound engineering to be called: ISLA

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
pip install -e .
```

This installs the Python DSP utilities and the pybind11 bridge directly from the repository.

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

## 🤝 Contributing  
Contributions are welcome.  
Feel free to open issues, submit PRs, or propose new smoothing modes.

---

## 📜 License  
MIT License — free to use, modify, and integrate into commercial or personal projects.

---

## 🙏 Acknowledgements

The development of this codebase reflects a collaborative effort across contributors and tools.

Special thanks to Google Jules for delivering the foundational scaffolding for the tests and examples directories. This contribution strengthened the project’s validation layer, improved developer onboarding, and ensured the DSP engine can be exercised deterministically across multiple modes and workflows.

Microsoft Copilot contributed Python logic, architectural guidance, and iterative refinement throughout the design of the DSP modules, the buffer‑based engine, and the cross‑language integration. Its involvement strengthened the determinism of the system, clarified the DSP flow, and accelerated the development of a clean, reproducible, multi‑language architecture.

The core conceptual breakthrough — the Phased‑Music‑Notes architecture, smoothing modes, harmonic blending pipeline, and deterministic DSP design — was developed by Don Feeney, building on the architectural patterns he previously orchestrated in the AeroCam repository. His work established the system’s foundational invariants, cross‑language design, and buffer‑based DSP flow, forming the backbone of the entire engine.

This project embodies team‑oriented engineering: human insight, AI‑accelerated development, and a shared commitment to building robust, expressive audio software.

Last acknowledgment goes to Carmen, Act I: Habanera — the soundtrack that carried the final battle with Windows CI. Fate is a rebellious bird, but deterministic builds win.
