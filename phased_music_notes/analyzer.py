"""
NoteAnalyzer
------------
Detects note boundaries in audio using lightweight DSP:

Techniques:
    - Short-time energy (STE)
    - Spectral flux (SF)
    - Adaptive thresholding
    - Peak picking

This module is intentionally simple and deterministic so Jules
can extend it with more advanced DSP later (ML onset detection,
harmonic segmentation, multi-band flux, etc.).
"""

from __future__ import annotations
import numpy as np
from typing import List


class NoteAnalyzer:
    """
    Detects note boundaries in audio.

    Parameters
    ----------
    frame_ms : int
        Analysis frame size in milliseconds.
    hop_ms : int
        Hop size between frames.
    sensitivity : float
        Threshold multiplier for onset detection.
    """

    def __init__(self,
                 frame_ms: int = 20,
                 hop_ms: int = 10,
                 sensitivity: float = 1.5):

        self.frame_ms = frame_ms
        self.hop_ms = hop_ms
        self.sensitivity = sensitivity

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------
    def detect_boundaries(self, audio: np.ndarray, sr: int) -> List[int]:
        """
        Detect note boundaries using spectral flux + energy.

        Parameters
        ----------
        audio : np.ndarray
            Mono or stereo audio buffer.
        sr : int
            Sample rate.

        Returns
        -------
        list[int]
            Sample indices where note transitions occur.
        """

        if sr <= 0:
            raise ValueError("Sample rate must be positive.")

        mono = self._to_mono(np.asarray(audio))
        if mono.size == 0:
            return []

        frames = self._frame_audio(mono, sr)
        flux = self._spectral_flux(frames)
        energy = self._short_time_energy(frames)

        onset_curve = self._combine_curves(flux, energy)
        boundaries = self._peak_pick(onset_curve, sr)

        return boundaries

    # -------------------------------------------------------------
    # Mono conversion
    # -------------------------------------------------------------
    @staticmethod
    def _to_mono(audio: np.ndarray) -> np.ndarray:
        if audio.ndim == 1:
            return audio
        if audio.ndim == 2:
            return audio.mean(axis=1)
        raise ValueError("Audio must be mono or stereo.")

    # -------------------------------------------------------------
    # Framing
    # -------------------------------------------------------------
    def _frame_audio(self, audio: np.ndarray, sr: int) -> np.ndarray:
        frame_len = self._ms_to_samples(self.frame_ms, sr)
        hop_len = self._ms_to_samples(self.hop_ms, sr)

        if frame_len <= 0 or hop_len <= 0:
            raise ValueError("Frame and hop sizes must be at least one sample.")

        remaining = max(0, len(audio) - frame_len)
        num_frames = 1 + (remaining + hop_len - 1) // hop_len
        max_frames_with_audio = 1 + (len(audio) - 1) // hop_len
        num_frames = min(num_frames, max_frames_with_audio)
        frames = np.zeros((num_frames, frame_len), dtype=np.float32)

        for i in range(num_frames):
            start = i * hop_len
            end = start + frame_len
            chunk = audio[start:end]
            frames[i, :len(chunk)] = chunk

        return frames

    # -------------------------------------------------------------
    # Short-time energy
    # -------------------------------------------------------------
    @staticmethod
    def _short_time_energy(frames: np.ndarray) -> np.ndarray:
        return np.sum(frames ** 2, axis=1)

    # -------------------------------------------------------------
    # Spectral flux
    # -------------------------------------------------------------
    @staticmethod
    def _spectral_flux(frames: np.ndarray) -> np.ndarray:
        window = np.hanning(frames.shape[1])
        prev_mag = None
        flux = np.zeros(frames.shape[0], dtype=np.float32)

        for i, frame in enumerate(frames):
            spectrum = np.fft.rfft(frame * window)
            mag = np.abs(spectrum)

            if prev_mag is not None:
                diff = mag - prev_mag
                flux[i] = np.sum(diff[diff > 0])

            prev_mag = mag

        return flux

    # -------------------------------------------------------------
    # Combine flux + energy
    # -------------------------------------------------------------
    def _combine_curves(self, flux: np.ndarray, energy: np.ndarray) -> np.ndarray:
        # Normalize
        flux_n = flux / (np.max(flux) + 1e-6)
        energy_n = energy / (np.max(energy) + 1e-6)

        # Weighted combination
        onset_curve = 0.7 * flux_n + 0.3 * energy_n
        return onset_curve

    # -------------------------------------------------------------
    # Peak picking
    # -------------------------------------------------------------
    def _peak_pick(self, onset_curve: np.ndarray, sr: int) -> List[int]:
        threshold = np.mean(onset_curve) * self.sensitivity
        peaks = np.where(onset_curve > threshold)[0]

        hop_len = self._ms_to_samples(self.hop_ms, sr)
        return [int(p * hop_len) for p in peaks]

    # -------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------
    @staticmethod
    def _ms_to_samples(ms: float, sr: int) -> int:
        return int((ms / 1000.0) * sr)
