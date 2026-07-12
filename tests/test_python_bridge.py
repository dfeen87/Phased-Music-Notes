import numpy as np
import pytest
from drivers.api import PhasedNotesBuffer

def test_bridge_init():
    """Validate that PhasedNotesBuffer initializes without errors."""
    bridge = PhasedNotesBuffer(mode="velvet", sr=44100)
    assert bridge.mode == "velvet"
    assert bridge.sr == 44100
    assert bridge.engine is not None

def test_bridge_process_mono():
    """Validate processing on a small, deterministic mono audio buffer."""
    bridge = PhasedNotesBuffer(mode="velvet", sr=44100)

    # Generate larger buffer (1 second) to avoid empty flux arrays in detect_boundaries
    num_samples = 44100
    audio = np.zeros(num_samples, dtype=np.float32)

    output = bridge.process_buffer(audio)

    # Check that output shape and type match input
    assert output.shape == audio.shape
    assert output.dtype == audio.dtype

def test_bridge_process_stereo():
    """Validate processing on a small, deterministic stereo audio buffer."""
    bridge = PhasedNotesBuffer(mode="velvet", sr=44100)

    # 1 second of a simple sine wave in stereo
    num_samples = 44100
    t = np.arange(num_samples) / 44100.0
    sine = np.sin(2 * np.pi * 440.0 * t).astype(np.float32)

    # stereo is stored as [num_samples, 2] in PhasedNotes
    audio = np.stack((sine, sine), axis=1)

    output = bridge.process_buffer(audio)

    # Check that output shape and type match input
    assert output.shape == audio.shape
    assert output.shape == (44100, 2)

def test_bridge_modes():
    """Validate that the bridge supports different modes."""
    bridge = PhasedNotesBuffer(mode="melt", sr=44100)
    assert bridge.mode == "melt"
    assert bridge.engine.mode == "melt"

def test_bridge_shutdown():
    """Validate the bridge shutdown mechanism."""
    # Since shutdown_python is a C++ call, we just ensure our API handles cleanup safely
    # For PhasedNotesBuffer, we simulate teardown.
    bridge = PhasedNotesBuffer(mode="velvet", sr=44100)
    assert bridge.engine is not None
    # Assuming standard teardown doesn't throw
    del bridge
