import numpy as np
import pytest
from phased_music_notes.smoother import PhaseSmoother

def generate_discontinuous_signal(sr=44100):
    t1 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    # 440 Hz
    part1 = np.sin(2 * np.pi * 440 * t1)

    t2 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    # Out of phase 880 Hz
    part2 = np.cos(2 * np.pi * 880 * t2)

    # Boundary at index sr // 2
    boundary_idx = len(part1)
    signal = np.concatenate([part1, part2])

    return signal, [boundary_idx]

@pytest.mark.parametrize("mode", ["velvet", "legato", "melt"])
def test_smoother_mono(mode):
    sr = 44100
    signal, boundaries = generate_discontinuous_signal(sr)

    smoother = PhaseSmoother(mode=mode)
    smoothed = smoother.apply(signal, boundaries)

    assert signal.shape == smoothed.shape

    # Calculate difference between adjacent samples (derivative) at the boundary
    b = boundaries[0]

    orig_diff = np.abs(signal[b] - signal[b-1])
    smooth_diff = np.abs(smoothed[b] - smoothed[b-1])

    # Smoothing should reduce the abrupt change
    assert smooth_diff < orig_diff

@pytest.mark.parametrize("mode", ["velvet", "legato", "melt"])
def test_smoother_stereo(mode):
    sr = 44100
    signal_mono, boundaries = generate_discontinuous_signal(sr)
    signal_stereo = np.column_stack((signal_mono, signal_mono))

    smoother = PhaseSmoother(mode=mode)
    smoothed = smoother.apply(signal_stereo, boundaries)

    assert signal_stereo.shape == smoothed.shape

    b = boundaries[0]
    orig_diff = np.abs(signal_stereo[b, 0] - signal_stereo[b-1, 0])
    smooth_diff = np.abs(smoothed[b, 0] - smoothed[b-1, 0])

    assert smooth_diff < orig_diff
