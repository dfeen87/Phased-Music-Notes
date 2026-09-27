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

    # Phase-preservation validation
    # Check that regions far away from the boundary are completely unaffected
    # The smoother acts only on a window around the boundary
    blend_samples = smoother._ms_to_samples(smoother.cfg["blend_ms"])

    # Safe margin outside the blend window
    safe_margin = blend_samples + 10

    # Check frequency domain (phase angle) preservation
    from phased_music_notes.utils import hann_window, frame_audio

    # Frame un-modified regions and compare STFT phase angles
    if b > safe_margin:
        # Check a frame entirely to the left of the boundary
        left_frame_len = min(512, b - safe_margin)
        if left_frame_len >= 128:
            left_orig = signal[0:left_frame_len]
            left_smooth = smoothed[0:left_frame_len]

            win = hann_window(left_frame_len)
            phase_orig = np.angle(np.fft.rfft(left_orig * win))
            phase_smooth = np.angle(np.fft.rfft(left_smooth * win))

            # Phases should be perfectly preserved where DSP hasn't touched the signal
            np.testing.assert_allclose(
                phase_orig, phase_smooth,
                atol=1e-5,
                err_msg="Phase angle corrupted in untouched left region"
            )

    if len(signal) - b > safe_margin:
        # Check a frame entirely to the right of the boundary
        right_frame_len = min(512, len(signal) - b - safe_margin)
        if right_frame_len >= 128:
            right_orig = signal[-right_frame_len:]
            right_smooth = smoothed[-right_frame_len:]

            win = hann_window(right_frame_len)
            phase_orig = np.angle(np.fft.rfft(right_orig * win))
            phase_smooth = np.angle(np.fft.rfft(right_smooth * win))

            np.testing.assert_allclose(
                phase_orig, phase_smooth,
                atol=1e-5,
                err_msg="Phase angle corrupted in untouched right region"
            )

@pytest.mark.parametrize("mode", ["velvet", "legato", "melt"])
def test_smoother_stereo(mode):
    sr = 44100
    signal_mono, boundaries = generate_discontinuous_signal(sr)
    signal_stereo = np.column_stack((signal_mono, signal_mono))

    smoother = PhaseSmoother(mode=mode)
    smoothed = smoother.apply(signal_stereo, boundaries)

    assert signal_stereo.shape == smoothed.shape
    assert smoothed.shape[1] == 2, "Stereo array must have shape (numSamples, 2)"

    b = boundaries[0]
    orig_diff = np.abs(signal_stereo[b, 0] - signal_stereo[b-1, 0])
    smooth_diff = np.abs(smoothed[b, 0] - smoothed[b-1, 0])

    assert smooth_diff < orig_diff

    # Phase-preservation validation for stereo
    blend_samples = smoother._ms_to_samples(smoother.cfg["blend_ms"])
    safe_margin = blend_samples + 10

    from phased_music_notes.utils import hann_window, frame_audio

    if b > safe_margin:
        left_frame_len = min(512, b - safe_margin)
        if left_frame_len >= 128:
            win = hann_window(left_frame_len)

            for ch in range(2):
                phase_orig = np.angle(np.fft.rfft(signal_stereo[0:left_frame_len, ch] * win))
                phase_smooth = np.angle(np.fft.rfft(smoothed[0:left_frame_len, ch] * win))

                np.testing.assert_allclose(
                    phase_orig, phase_smooth,
                    atol=1e-5,
                    err_msg=f"Phase angle corrupted in untouched left region for channel {ch}"
                )

    if len(signal_stereo) - b > safe_margin:
        right_frame_len = min(512, len(signal_stereo) - b - safe_margin)
        if right_frame_len >= 128:
            win = hann_window(right_frame_len)

            for ch in range(2):
                phase_orig = np.angle(np.fft.rfft(signal_stereo[-right_frame_len:, ch] * win))
                phase_smooth = np.angle(np.fft.rfft(smoothed[-right_frame_len:, ch] * win))

            np.testing.assert_allclose(
                phase_orig, phase_smooth,
                atol=1e-5,
                err_msg=f"Phase angle corrupted in untouched right region for channel {ch}"
            )


def test_smoother_uses_requested_sample_rate_and_ignores_invalid_boundaries():
    smoother = PhaseSmoother(mode="velvet")
    signal = np.concatenate((np.zeros(1000), np.ones(1000)))

    smoothed = smoother.apply(signal, [-1, 1000, len(signal)], sr=1000)

    expected_width = smoother._ms_to_samples(smoother.cfg["blend_ms"], 1000)
    changed = np.flatnonzero(smoothed != signal)
    # The zero-valued first point of the curve leaves the outermost sample intact.
    assert changed[0] == 1000 - expected_width + 1
    assert changed[-1] == 1000 + expected_width - 1
