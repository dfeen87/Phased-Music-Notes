"""
HarmonicBlender
---------------
Final stage of the Phased-Music-Notes DSP pipeline.

Responsibilities:
    - Smooth harmonic content after phase-aligned transitions
    - Reduce harsh overtones introduced by boundary blending
    - Apply spectral softening (mode-dependent)
    - Preserve timbre while reducing transient spikes

Techniques:
    - Short-time FFT
    - Harmonic envelope smoothing
    - Spectral tilt
    - Soft lowpass blending

This module is intentionally simple and deterministic so Jules
can extend it with more advanced DSP later.
"""

from __future__ import annotations
import numpy as np
from typing import Optional


class HarmonicBlender:
    """
    Harmonic blending engine.

    Parameters
    ----------
    strength : float
        Amount of harmonic smoothing (0.0 - 1.0).
    window_ms : int
        FFT window size in milliseconds.
    """

    def __init__(self,
                 strength: float = 0.4,
                 window_ms: int = 40):

        self.strength = float(np.clip(strength, 0.0, 1.0))
        self.window_ms = window_ms

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------
    def blend(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Apply harmonic blending to mono or stereo audio.

        Parameters
        ----------
        audio : np.ndarray
            Mono or stereo audio buffer.
        sr : int
            Sample rate.

        Returns
        -------
        np.ndarray
            Harmonic-blended audio buffer.
        """

        if audio.ndim == 1:
            return self._blend_mono(audio, sr)
        elif audio.ndim == 2:
            return self._blend_stereo(audio, sr)
        else:
            raise ValueError("Audio must be mono or stereo.")

    # -------------------------------------------------------------
    # Mono processing
    # -------------------------------------------------------------
    def _blend_mono(self, audio: np.ndarray, sr: int) -> np.ndarray:
        win = self._hann_window(sr)
        hop = win.size // 2

        # STFT
        frames = self._frame_audio(audio, hop, win.size)
        spectrum = np.fft.rfft(frames * win, axis=1)
        mag = np.abs(spectrum)
        phase = np.angle(spectrum)

        # Harmonic smoothing
        mag_smooth = self._smooth_harmonics(mag)

        # Reconstruct spectrum
        spectrum_blended = mag_smooth * np.exp(1j * phase)

        # ISTFT
        frames_out = np.fft.irfft(spectrum_blended, axis=1)
        audio_out = self._overlap_add(frames_out, hop)

        # Pad or truncate to match original length exactly
        if len(audio_out) < len(audio):
            pad_len = len(audio) - len(audio_out)
            audio_out = np.pad(audio_out, (0, pad_len))
        return audio_out[: len(audio)]

    # -------------------------------------------------------------
    # Stereo processing
    # -------------------------------------------------------------
    def _blend_stereo(self, audio: np.ndarray, sr: int) -> np.ndarray:
        out = np.zeros_like(audio)
        for ch in range(audio.shape[1]):
            out[:, ch] = self._blend_mono(audio[:, ch], sr)
        return out

    # -------------------------------------------------------------
    # Harmonic smoothing core
    # -------------------------------------------------------------
    def _smooth_harmonics(self, mag: np.ndarray) -> np.ndarray:
        """
        Smooth harmonic magnitudes across frequency bins.

        This reduces harsh overtones and creates a soft timbre.
        """

        # Simple spectral smoothing kernel
        kernel = np.array([0.25, 0.5, 0.25])
        mag_smooth = np.copy(mag)

        for i in range(mag.shape[0]):
            mag_smooth[i] = np.convolve(mag[i], kernel, mode="same")

        # Apply strength
        return (1 - self.strength) * mag + self.strength * mag_smooth

    # -------------------------------------------------------------
    # Framing utilities
    # -------------------------------------------------------------
    @staticmethod
    def _frame_audio(audio: np.ndarray, hop: int, win: int) -> np.ndarray:
        num_frames = 1 + (len(audio) - win) // hop
        frames = np.zeros((num_frames, win), dtype=np.float32)

        for i in range(num_frames):
            start = i * hop
            end = start + win
            frames[i] = audio[start:end]

        return frames

    @staticmethod
    def _overlap_add(frames: np.ndarray, hop: int) -> np.ndarray:
        win = frames.shape[1]
        out_len = hop * (frames.shape[0] + 1)
        out = np.zeros(out_len, dtype=np.float32)

        for i, frame in enumerate(frames):
            start = i * hop
            out[start:start + win] += frame

        return out

    # -------------------------------------------------------------
    # Window generator
    # -------------------------------------------------------------
    def _hann_window(self, sr: int) -> np.ndarray:
        win_samples = self._ms_to_samples(self.window_ms, sr)
        return np.hanning(win_samples)

    # -------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------
    @staticmethod
    def _ms_to_samples(ms: float, sr: int) -> int:
        return int((ms / 1000.0) * sr)
