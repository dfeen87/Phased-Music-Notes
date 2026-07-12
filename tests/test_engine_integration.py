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

    # Assert determinism
    output2 = engine.process_buffer(signal)
    np.testing.assert_array_equal(output1, output2)

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
