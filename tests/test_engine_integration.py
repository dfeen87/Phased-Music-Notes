import numpy as np
import pytest
from drivers.api import PhasedNotesBuffer

def generate_test_signal(sr=44100, stereo=False):
    t1 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine1 = np.sin(2 * np.pi * 440 * t1)

    t2 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine2 = np.sin(2 * np.pi * 880 * t2)

    silence = np.zeros(sr // 4)

    signal = np.concatenate([sine1, silence, sine2])

    if stereo:
        return np.column_stack((signal, signal))
    return signal

@pytest.mark.parametrize("mode", ["velvet", "legato", "melt"])
def test_engine_integration_mono(mode):
    sr = 44100
    signal = generate_test_signal(sr, stereo=False)

    engine = PhasedNotesBuffer(mode=mode, sr=sr)
    output1 = engine.process_buffer(signal)

    # Assert shape
    assert signal.shape == output1.shape
    assert output1.ndim == 1, "Mono arrays must be 1D"

    # Assert determinism
    output2 = engine.process_buffer(signal)
    np.testing.assert_array_equal(output1, output2)

def test_dsp_roundtrip_fft():
    """
    Test STFT/FFT comparison pattern for deterministic testing.
    Validates magnitude continuity and energy preservation after DSP pipeline processing.
    """
    sr = 44100
    # Create simple synthetic test tone
    signal = generate_test_signal(sr, stereo=False)

    engine = PhasedNotesBuffer(mode="velvet", sr=sr)
    output = engine.process_buffer(signal)

    # Calculate STFT representation for input
    n_fft = 2048
    hop_length = 512

    # Ensure shape is equal
    assert signal.shape == output.shape

    # Simple STFT extraction for input and output to check magnitude continuity
    from phased_music_notes.utils import hann_window, frame_audio

    win = hann_window(n_fft)

    frames_in = frame_audio(signal, n_fft, hop_length)
    spec_in = np.fft.rfft(frames_in * win, axis=1)
    mag_in = np.abs(spec_in)

    frames_out = frame_audio(output, n_fft, hop_length)
    spec_out = np.fft.rfft(frames_out * win, axis=1)
    mag_out = np.abs(spec_out)

    # Total energy should be somewhat preserved
    energy_in = np.sum(mag_in**2)
    energy_out = np.sum(mag_out**2)

    # Energy preservation (should not diverge wildly)
    ratio = energy_out / (energy_in + 1e-9)
    assert 0.75 <= ratio <= 1.25, f"Energy preservation failed, ratio was {ratio}"

    # Magnitude continuity check - check that most bins are structurally similar
    # Allow some deviation because the DSP is meant to smooth transients and harmonics
    corr = np.corrcoef(mag_in.flatten(), mag_out.flatten())[0, 1]
    assert corr > 0.9, f"Magnitude continuity failed, correlation {corr} is too low"

    # Phase continuity check
    # We allow some phase deviation because NoteAnalyzer uses hop lengths and windows that
    # are slightly different than what HarmonicBlender does. Still, phases should
    # be loosely correlated. Let's make sure the phase delta is not uniformly random.
    peak_mag = np.max(mag_in)
    mask = mag_in > (peak_mag * 0.1)  # only look at significant bins
    phase_diff = np.abs(np.angle(np.exp(1j * (np.angle(spec_in)[mask] - np.angle(spec_out)[mask]))))
    # Check that average phase difference across significant bins is small
    mean_phase_diff = np.mean(phase_diff)
    assert mean_phase_diff < 1.0, f"Phase continuity failed, mean diff was {mean_phase_diff}"

    # Harmonic stability check
    # Check that prominent peaks remain in the same locations for each frame
    peaks_in = np.argmax(mag_in, axis=1)
    peaks_out = np.argmax(mag_out, axis=1)

    # We only care about frames where there is significant signal energy
    frame_energy = np.sum(mag_in**2, axis=1)
    sig_frames = frame_energy > (np.max(frame_energy) * 0.1)

    peak_diff = np.abs(peaks_in[sig_frames] - peaks_out[sig_frames])
    assert np.max(peak_diff) <= 2, f"Harmonic stability failed, peaks shifted significantly"

@pytest.mark.parametrize("mode", ["velvet", "legato", "melt"])
def test_engine_integration_stereo(mode):
    sr = 44100
    signal = generate_test_signal(sr, stereo=True)

    engine = PhasedNotesBuffer(mode=mode, sr=sr)
    output1 = engine.process_buffer(signal)

    # Assert shape
    assert signal.shape == output1.shape

    # Assert determinism
    output2 = engine.process_buffer(signal)
    np.testing.assert_array_equal(output1, output2)
