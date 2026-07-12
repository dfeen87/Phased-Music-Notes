"""
PhaseSmoother
-------------
Applies phase‑aligned smoothing across note boundaries.

Modes:
    - velvet : soft transient reduction + gentle interpolation
    - legato : pitch‑aware crossfade for glide‑like transitions
    - melt   : heavy smoothing + spectral softening (pre‑blend)

This module is intentionally simple and deterministic so Jules
can extend the DSP internals without touching the architecture.
"""

from __future__ import annotations
import numpy as np
from typing import List, Tuple


class PhaseSmoother:
    """
    Phase‑aligned smoothing engine.

    Parameters
    ----------
    mode : str
        Smoothing mode preset: velvet, legato, melt.
    """

    def __init__(self, mode: str = "velvet"):
        self.mode = mode.lower()

        # Mode presets (Jules can tune these)
        self.presets = {
            "velvet": {
                "blend_ms": 12,
                "curve": "cosine",
                "strength": 0.35,
            },
            "legato": {
                "blend_ms": 25,
                "curve": "sine",
                "strength": 0.55,
            },
            "melt": {
                "blend_ms": 40,
                "curve": "smoothstep",
                "strength": 0.75,
            },
        }

        if self.mode not in self.presets:
            raise ValueError(f"Unknown smoothing mode: {self.mode}")

        self.cfg = self.presets[self.mode]

    # -------------------------------------------------------------
    # Core smoothing entry point
    # -------------------------------------------------------------
    def apply(self, audio: np.ndarray, boundaries: List[int]) -> np.ndarray:
        """
        Apply smoothing across detected note boundaries.

        Parameters
        ----------
        audio : np.ndarray
            Audio buffer (mono or stereo).
        boundaries : list[int]
            Sample indices where note transitions occur.

        Returns
        -------
        np.ndarray
            Smoothed audio buffer.
        """

        if audio.ndim == 1:
            return self._smooth_mono(audio, boundaries)
        elif audio.ndim == 2:
            return self._smooth_stereo(audio, boundaries)
        else:
            raise ValueError("Audio must be mono or stereo.")

    # -------------------------------------------------------------
    # Mono smoothing
    # -------------------------------------------------------------
    def _smooth_mono(self, audio: np.ndarray, boundaries: List[int]) -> np.ndarray:
        out = audio.copy()
        blend_samples = self._ms_to_samples(self.cfg["blend_ms"])

        for b in boundaries:
            start = max(0, b - blend_samples)
            end = min(len(audio), b + blend_samples)

            left = out[start:b]
            right = out[b:end]

            if len(left) == 0 or len(right) == 0:
                continue

            curve = self._blend_curve(len(left), len(right))
            blended = left * (1 - curve) + right * curve

            out[start:end] = blended

        return out

    # -------------------------------------------------------------
    # Stereo smoothing
    # -------------------------------------------------------------
    def _smooth_stereo(self, audio: np.ndarray, boundaries: List[int]) -> np.ndarray:
        out = audio.copy()
        blend_samples = self._ms_to_samples(self.cfg["blend_ms"])

        for ch in range(audio.shape[1]):
            out[:, ch] = self._smooth_mono(out[:, ch], boundaries)

        return out

    # -------------------------------------------------------------
    # Blend curve generator
    # -------------------------------------------------------------
    def _blend_curve(self, left_len: int, right_len: int) -> np.ndarray:
        n = min(left_len, right_len)

        if self.cfg["curve"] == "cosine":
            t = np.linspace(0, np.pi, n)
            return (1 - np.cos(t)) * 0.5 * self.cfg["strength"]

        elif self.cfg["curve"] == "sine":
            t = np.linspace(0, np.pi / 2, n)
            return np.sin(t) * self.cfg["strength"]

        elif self.cfg["curve"] == "smoothstep":
            t = np.linspace(0, 1, n)
            return (t * t * (3 - 2 * t)) * self.cfg["strength"]

        else:
            return np.linspace(0, 1, n) * self.cfg["strength"]

    # -------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------
    @staticmethod
    def _ms_to_samples(ms: float, sr: int = 44100) -> int:
        return int((ms / 1000.0) * sr)
