import numpy as np
import pytest
from phased_music_notes.harmonics import HarmonicBlender

def generate_harmonic_signal(sr=44100):
    t = np.linspace(0, 1.0, sr, endpoint=False)

    # Fundamental + several harmonics
    freqs = [440, 880, 1320, 1760, 2200, 4400, 8800]
    amps = [1.0, 0.5, 0.3, 0.2, 0.1, 0.05, 0.02]

    signal = np.zeros(sr)
    for f, a in zip(freqs, amps):
        signal += a * np.sin(2 * np.pi * f * t)

    # Normalize
    signal /= np.max(np.abs(signal))

    return signal

def test_harmonic_blender_mono():
    sr = 44100
    signal = generate_harmonic_signal(sr)

    blender = HarmonicBlender(strength=1.0, window_ms=40)
    blended = blender.blend(signal, sr)

    assert signal.shape == blended.shape

    # Extract STFT using internal method to test exactly what the DSP engine saw
    win_samples = blender._ms_to_samples(blender.window_ms, sr)
    hop = win_samples // 2

    # Analyze input
    frames_in = blender._frame_audio(signal, hop, win_samples)
    win = blender._hann_window(sr)
    spec_in = np.fft.rfft(frames_in * win, axis=1)
    mag_in = np.abs(spec_in)
    phase_in = np.angle(spec_in)

    # Analyze output
    frames_out = blender._frame_audio(blended, hop, win_samples)
    spec_out = np.fft.rfft(frames_out * win, axis=1)
    mag_out = np.abs(spec_out)
    phase_out = np.angle(spec_out)

    # Assert magnitude smoothing reduced high-frequency energy
    assert np.sum(mag_out[:, 50:]) < np.sum(mag_in[:, 50:])

    # Ensure phase is preserved inside the prominent bins
    # Because of overlap-add and windowing the phase of the final reconstructed audio won't be perfectly identical to the theoretical STFT bins
    # However, for bins with actual harmonic content, the phase will be largely preserved.
    # Let's filter to just the prominent bins
    peak_mag = np.max(mag_in)
    mask = mag_in > (peak_mag * 0.1) # top 10% of bins

    phase_diff = np.abs(np.angle(np.exp(1j * (phase_in[mask] - phase_out[mask]))))
    assert np.max(phase_diff) < 0.25

def test_harmonic_blender_stereo():
    sr = 44100
    signal = generate_harmonic_signal(sr)
    signal_stereo = np.column_stack((signal, signal))

    blender = HarmonicBlender(strength=0.5, window_ms=40)
    blended = blender.blend(signal_stereo, sr)

    assert signal_stereo.shape == blended.shape

    win_samples = blender._ms_to_samples(blender.window_ms, sr)
    hop = win_samples // 2
    win = blender._hann_window(sr)

    frames_in = blender._frame_audio(signal_stereo[:, 0], hop, win_samples)
    spec_in = np.fft.rfft(frames_in * win, axis=1)
    mag_in = np.abs(spec_in)
    phase_in = np.angle(spec_in)

    frames_out = blender._frame_audio(blended[:, 0], hop, win_samples)
    spec_out = np.fft.rfft(frames_out * win, axis=1)
    mag_out = np.abs(spec_out)
    phase_out = np.angle(spec_out)

    peak_mag = np.max(mag_in)
    mask = mag_in > (peak_mag * 0.1)
    phase_diff = np.abs(np.angle(np.exp(1j * (phase_in[mask] - phase_out[mask]))))
    assert np.max(phase_diff) < 0.25
