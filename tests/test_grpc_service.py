import os
import time
import socket
import threading
import numpy as np
import pytest
import grpc

from drivers import grpc_server
from drivers.grpc_client import smooth_block_grpc, smooth_stream_grpc


def get_free_port():
    """Finds a free port on localhost."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="module")
def grpc_test_server():
    """Fixture to start a test gRPC server in a background thread."""
    port = get_free_port()
    server = grpc_server.serve(port=port)

    # Wait a moment for server to start
    time.sleep(0.1)

    yield "localhost", port

    # Stop server after tests
    server.stop(grace=0)


def test_grpc_smooth_block_stereo(grpc_test_server):
    host, port = grpc_test_server

    # Generate 0.2s of stereo audio (two columns)
    sr = 44100
    audio = np.sin(2 * np.pi * 440 * np.linspace(0, 0.2, int(sr * 0.2))).astype(np.float32)
    stereo = np.column_stack((audio, audio))

    processed = smooth_block_grpc(stereo, mode="velvet", sr=sr, host=host, port=port)

    assert processed.shape == stereo.shape
    assert not np.allclose(processed, stereo)  # Make sure the DSP modified it


def test_grpc_smooth_block_mono(grpc_test_server):
    host, port = grpc_test_server

    # Generate mono audio (1D)
    sr = 44100
    mono = np.sin(2 * np.pi * 440 * np.linspace(0, 0.2, int(sr * 0.2))).astype(np.float32)

    processed = smooth_block_grpc(mono, mode="velvet", sr=sr, host=host, port=port)

    assert processed.ndim == 1
    assert processed.shape == mono.shape
    assert not np.allclose(processed, mono)


def test_grpc_smooth_stream_stereo(grpc_test_server):
    host, port = grpc_test_server

    sr = 44100
    audio = np.sin(2 * np.pi * 440 * np.linspace(0, 0.5, int(sr * 0.5))).astype(np.float32)
    stereo = np.column_stack((audio, audio))

    # Stream using 4096-sample chunks
    stream_generator = smooth_stream_grpc(stereo, chunk_size=4096, mode="velvet", sr=sr, host=host, port=port)

    results = list(stream_generator)
    assert len(results) > 0

    # Concatenate all yielded chunks
    reconstructed = np.concatenate(results, axis=0)
    assert reconstructed.shape == stereo.shape


def test_grpc_smooth_stream_mono(grpc_test_server):
    host, port = grpc_test_server

    sr = 44100
    mono = np.sin(2 * np.pi * 440 * np.linspace(0, 0.5, int(sr * 0.5))).astype(np.float32)

    stream_generator = smooth_stream_grpc(mono, chunk_size=4096, mode="velvet", sr=sr, host=host, port=port)

    results = list(stream_generator)
    assert len(results) > 0

    reconstructed = np.concatenate(results, axis=0)
    assert reconstructed.ndim == 1
    assert reconstructed.shape == mono.shape
