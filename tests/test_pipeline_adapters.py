import os
import tempfile
import numpy as np
import soundfile as sf
import pytest

from phased_music_notes.pipeline_adapters import (
    PhasedNotesBeamDoFn,
    PhasedNotesAirflowOperator,
    PhasedNotesLuigiTask
)


def test_beam_do_fn():
    # Test numpy array element processing
    do_fn = PhasedNotesBeamDoFn(mode="velvet", sr=44100)
    do_fn.setup()

    # Generate synthetic stereo audio
    audio_in = np.sin(2 * np.pi * 440 * np.linspace(0, 0.1, 4410)).astype(np.float32)
    audio_stereo = np.column_stack((audio_in, audio_in))

    # Process via Beam DoFn
    results = list(do_fn.process(audio_stereo))
    assert len(results) == 1
    processed = results[0]
    assert processed.shape == audio_stereo.shape


def test_beam_do_fn_dict():
    # Test dict element processing
    do_fn = PhasedNotesBeamDoFn(mode="velvet", sr=44100)
    do_fn.setup()

    audio_in = np.sin(2 * np.pi * 440 * np.linspace(0, 0.1, 4410)).astype(np.float32)
    audio_stereo = np.column_stack((audio_in, audio_in))
    element = {"audio": audio_stereo, "track_id": "spotify_test"}

    results = list(do_fn.process(element))
    assert len(results) == 1
    processed_elem = results[0]
    assert processed_elem["track_id"] == "spotify_test"
    assert processed_elem["audio"].shape == audio_stereo.shape


def test_airflow_operator():
    # Create temp input & output paths
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "in.wav")
        output_path = os.path.join(tmpdir, "out.wav")

        # Generate synthetic audio file
        audio = np.sin(2 * np.pi * 440 * np.linspace(0, 0.5, 22050)).astype(np.float32)
        stereo = np.column_stack((audio, audio))
        sf.write(input_path, stereo, 44100)

        # Run Airflow Operator
        operator = PhasedNotesAirflowOperator(
            task_id="test_smooth",
            input_path=input_path,
            output_path=output_path,
            mode="velvet"
        )
        result_path = operator.execute(context=None)

        assert os.path.exists(output_path)
        assert result_path == output_path

        # Verify output exists and is stereo
        out_audio, sr = sf.read(output_path)
        assert sr == 44100
        assert out_audio.shape[1] == 2


class MockTarget:
    def __init__(self, path):
        self.path = path


def test_luigi_task():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "in.wav")
        output_path = os.path.join(tmpdir, "out.wav")

        audio = np.sin(2 * np.pi * 440 * np.linspace(0, 0.5, 22050)).astype(np.float32)
        stereo = np.column_stack((audio, audio))
        sf.write(input_path, stereo, 44100)

        # Instantiate Task
        task = PhasedNotesLuigiTask()
        task.input = lambda: MockTarget(input_path)
        task.output = lambda: MockTarget(output_path)

        task.run()

        assert os.path.exists(output_path)
        out_audio, sr = sf.read(output_path)
        assert sr == 44100
        assert out_audio.shape[1] == 2
