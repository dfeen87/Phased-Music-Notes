import numpy as np
import pytest
from phased_music_notes.analyzer import NoteAnalyzer

def generate_test_signal(sr=44100):
    # sine -> silence -> sine with transient spikes
    t1 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine1 = np.sin(2 * np.pi * 440 * t1)

    t2 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine2 = np.sin(2 * np.pi * 880 * t2)

    silence = np.zeros(sr // 4)

    signal = np.concatenate([sine1, silence, sine2])

    # Add transient spikes at boundaries
    spike1_idx = len(sine1)
    spike2_idx = len(sine1) + len(silence)

    signal[spike1_idx:spike1_idx+10] = 1.0
    signal[spike2_idx:spike2_idx+10] = 1.0

    return signal, [spike1_idx, spike2_idx]

def test_detect_boundaries_mono():
    sr = 44100
    signal, expected_boundaries = generate_test_signal(sr)

    analyzer = NoteAnalyzer(frame_ms=10, hop_ms=5, sensitivity=1.5)
    boundaries = analyzer.detect_boundaries(signal, sr)

    # We expect the detected boundaries to be near the spikes
    tolerance = analyzer._ms_to_samples(20, sr) # 20ms tolerance

    for expected in expected_boundaries:
        # Check if any detected boundary is within tolerance
        assert any(abs(b - expected) <= tolerance for b in boundaries), \
            f"Expected boundary at {expected} not found within {tolerance} samples. Detected: {boundaries}"

def test_detect_boundaries_stereo():
    sr = 44100
    signal_mono, expected_boundaries = generate_test_signal(sr)

    # planar stereo
    signal_stereo = np.column_stack((signal_mono, signal_mono))

    analyzer = NoteAnalyzer(frame_ms=10, hop_ms=5, sensitivity=1.5)
    boundaries = analyzer.detect_boundaries(signal_stereo, sr)

    tolerance = analyzer._ms_to_samples(20, sr)

    for expected in expected_boundaries:
        assert any(abs(b - expected) <= tolerance for b in boundaries), \
            f"Expected boundary at {expected} not found within {tolerance} samples in stereo. Detected: {boundaries}"


def test_detect_boundaries_handles_empty_and_short_audio():
    analyzer = NoteAnalyzer()

    assert analyzer.detect_boundaries(np.array([]), 44100) == []
    assert analyzer.detect_boundaries(np.ones(32), 44100) == []
