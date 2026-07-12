# **PHASED‑MUSIC‑NOTES — Architecture & DSP Design Overview**  
*A production‑grade audio engine designed by Don Feeney, in collaboration with Microsoft Copilot.*

---

## **1. Introduction**

Phased‑Music‑Notes is a deterministic, buffer‑based DSP engine designed to smooth, blend, and harmonically stabilize musical notes in both offline and real‑time contexts.  
It is built for production use, with a focus on:

- deterministic DSP  
- phase‑preserving transformations  
- harmonic blending  
- smoothing modes for musical continuity  
- cross‑language integration (Python DSP + C++ JUCE plugin)  
- CI‑verified correctness  
- reproducible behavior across platforms  

The conceptual breakthrough — the smoothing architecture, harmonic blending pipeline, and deterministic DSP flow — was created by **Don Feeney**, in collaboration with **Microsoft Copilot**.

The scaffolding of the test and example suites was contributed by **Jules**, using patterns derived from the AeroCam repository (synthetic signals, deterministic math, FFT/STFT validation).

---

## **2. High‑Level Architecture**

Phased‑Music‑Notes consists of three major layers:

### **2.1 DSP Core (Python)**  
Implements:

- **Analyzer** — detects note boundaries, transitions, and transient events  
- **Smoother** — applies velvet, legato, or melt smoothing to transitions  
- **HarmonicBlender** — blends harmonic content while preserving phase  
- **Utils** — windowing, framing, overlap‑add, normalization, interpolation  

All DSP is deterministic, vectorized, and CI‑safe.

### **2.2 Buffer Engine (Python)**  
`PhasedNotesBuffer` is the canonical DSP entry point.

It accepts planar stereo arrays shaped `(numSamples, 2)` and applies:

1. Analyzer  
2. Smoother  
3. Harmonic blending  
4. Reconstruction  

This engine is used by both Python examples and the C++ plugin.

### **2.3 VST/AU Plugin (C++ / JUCE)**  
The plugin is a thin wrapper around the buffer engine:

- Converts JUCE audio buffers → planar stereo NumPy arrays  
- Calls the Python DSP pipeline  
- Converts output back to JUCE buffers  

This ensures identical behavior between offline Python processing and real‑time plugin processing.

---

## **3. DSP Pipeline Overview**

### **3.1 Analyzer**  
The analyzer identifies:

- note boundaries  
- silence regions  
- transient spikes  
- envelope changes  
- harmonic transitions  

It uses:

- short‑time energy  
- derivative thresholds  
- spectral flux  
- envelope tracking  

Output: a list of boundary indices.

---

### **3.2 Smoother**  
Three smoothing modes:

#### **Velvet**  
Softens transitions using cosine interpolation.  
Preserves energy and avoids clicks.

#### **Legato**  
Extends note tails and blends transitions.  
Useful for vocal and instrumental continuity.

#### **Melt**  
Aggressive smoothing that melts boundaries into each other.  
Useful for pads, ambient textures, and cinematic sound design.

All smoothing is:

- deterministic  
- vectorized  
- phase‑preserving  
- shape‑invariant  

---

### **3.3 HarmonicBlender**

The harmonic blender:

- computes STFT  
- preserves original phase angles  
- smooths magnitude envelopes  
- blends harmonics to reduce harshness  
- reconstructs using overlap‑add  

This ensures:

- phase continuity  
- harmonic stability  
- spectral smoothness  
- musical coherence  

---

## **4. Stereo Shape Invariant**

All stereo audio must be shaped:

```
(numSamples, 2)
```

This invariant is enforced across:

- Python DSP  
- buffer engine  
- VST/AU plugin  
- tests  
- examples  

It ensures deterministic behavior and prevents shape mismatches.

---

## **5. Determinism & CI Guarantees**

Phased‑Music‑Notes is designed for production reliability:

- deterministic DSP  
- seeded randomness (if used)  
- no dynamic allocation inside DSP loops  
- NumPy vectorization  
- CI runs on Ubuntu, macOS, Windows  
- plugin artifacts uploaded on every build  
- tests run under 100ms  
- synthetic audio only  
- no disk I/O in tests  

This ensures reproducible behavior across all environments.

---

## **6. AeroCam Pattern Influence**

The AeroCam repository provided patterns for:

- synthetic signal generation  
- deterministic test scaffolding  
- FFT/STFT comparison  
- phase‑preservation validation  
- round‑trip DSP tests  
- shape invariants  
- CI‑friendly math  

No camera‑stabilization math (Kalman filters, quaternions, IMU fusion, optical flow) is used.

AeroCam is a **pattern reference**, not a **code source**.

---

## **7. Tests & Examples**

### **Tests**  
Cover:

- analyzer  
- smoother  
- harmonics  
- utils  
- full pipeline  

All tests use synthetic audio and validate:

- phase preservation  
- shape invariants  
- deterministic output  
- smoothing correctness  
- harmonic blending stability  

### **Examples**  
Demonstrate:

- buffer‑based DSP  
- smoothing modes  
- harmonic blending  
- spectral centroid comparison  
- synthetic stereo processing  

Examples are dependency‑minimal (NumPy only).

---

## **8. Production Status**

Phased‑Music‑Notes is **production software**, validated through:

- multi‑OS CI  
- deterministic DSP  
- plugin builds  
- test coverage  
- architectural invariants  
- cross‑language consistency  

---

## **9. Acknowledgements**

- **Don Feeney** — conceptual breakthrough, architecture, DSP design  
- **Microsoft Copilot** — Python logic, architectural guidance, DSP reasoning  
- **Jules** — scaffolding of tests/examples, AeroCam pattern integration  

This project reflects a team‑oriented engineering mindset:  
human creativity, AI‑accelerated development, and shared momentum.

---

## **10. Closing**

Phased‑Music‑Notes is a deterministic, phase‑preserving, production‑grade DSP engine designed for musicians, producers, and developers who need smooth, stable, expressive audio transformations.

This document serves as the architectural foundation for the entire repository.

Just tell me the direction you want to go next.
