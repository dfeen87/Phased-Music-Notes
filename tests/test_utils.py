import numpy as np
from phased_music_notes.utils import (
    normalize, to_mono, ensure_stereo,
    hann_window, hamming_window, blackman_window,
    cosine_curve, sine_curve, smoothstep_curve,
    frame_audio, overlap_add, smoothing_kernel, ms_to_samples
)

def test_normalization():
    signal = np.array([-2.0, 0.0, 4.0])
    norm = normalize(signal)

    assert np.max(np.abs(norm)) <= 1.0
    assert norm[2] > 0
    assert norm[0] < 0

def test_mono_stereo_conversion():
    # mono -> stereo -> mono
    mono = np.array([0.5, 0.5, -0.5])
    stereo = ensure_stereo(mono)

    assert stereo.shape == (3, 2)
    assert np.all(stereo[:, 0] == mono)
    assert np.all(stereo[:, 1] == mono)

    mono_back = to_mono(stereo)
    assert mono_back.shape == (3,)
    assert np.all(mono_back == mono)

def test_windows():
    size = 1024
    assert hann_window(size).shape == (size,)
    assert hamming_window(size).shape == (size,)
    assert blackman_window(size).shape == (size,)

def test_curves():
    n = 100
    cos_c = cosine_curve(n)
    sin_c = sine_curve(n)
    smooth_c = smoothstep_curve(n)

    for c in [cos_c, sin_c, smooth_c]:
        assert c.shape == (n,)
        assert c[0] == 0.0
        assert c[-1] == 1.0

def test_frame_overlap_add_roundtrip():
    signal = np.random.rand(10000).astype(np.float32)

    frame_size = 512
    hop_size = 256

    # Needs a constant overlap-add window or just sum it without window for testing
    frames = frame_audio(signal, frame_size, hop_size)
    reconstructed = overlap_add(frames, hop_size)

    # Because there is no window, overlap_add with hop=half-frame will just add the regions twice in the middle
    # We should just ensure it runs and outputs expected shape
    # For perfect reconstruction without window, center elements will be 2*signal
    center_idx = 5000
    assert np.isclose(reconstructed[center_idx], signal[center_idx] * 2)

def test_kernels():
    k_soft = smoothing_kernel("soft")
    assert np.sum(k_soft) == 1.0

    k_wide = smoothing_kernel("wide")
    assert np.isclose(np.sum(k_wide), 1.0)

def test_ms_to_samples():
    sr = 44100
    samples = ms_to_samples(1000.0, sr)
    assert samples == 44100

    samples = ms_to_samples(500.0, sr)
    assert samples == 22050
