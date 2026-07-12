"""
Python API driver for Phased-Music-Notes.

This module provides a clean, producer-friendly interface:
    from phased_music_notes import smooth
    smooth("input.wav", "output.wav", mode="velvet")

It wraps the core engine in src/main.py so users never need
to touch internal DSP modules directly.
"""

from pathlib import Path
from src.main import PhasedMusicEngine


def smooth(input_path: str, output_path: str, mode: str = "velvet") -> None:
    """
    Smooth Audio Notes with a single function call.

    Parameters
    ----------
    input_path : str
        Path to the input audio file.
    output_path : str
        Path where the smoothed audio will be saved.
    mode : str
        Smoothing mode (e.g., velvet, legato, melt).
    """

    engine = PhasedMusicEngine(mode=mode)
    engine.smooth_file(input_path, output_path)


class PhasedNotes:
    """
    Object-oriented API wrapper for more advanced users.

    Example:
        pn = PhasedNotes(mode="melt")
        pn.process("piano.wav", "piano_soft.wav")
    """

    def __init__(self, mode: str = "velvet"):
        self.engine = PhasedMusicEngine(mode=mode)

    def process(self, input_path: str, output_path: str) -> None:
        self.engine.smooth_file(input_path, output_path)
