"""
SmoothPhase DSL
---------------
A musical, expressive interface for Phased-Music-Notes.

Goals:
    - Provide a soft, human-friendly API
    - Wrap the engine with simple commands
    - Expose smoothing modes (velvet, legato, melt)
    - Allow future expansion (glide, halo, ghost, bloom)

This DSL is intentionally minimal and expressive so Jules
can extend it with more advanced musical constructs later.
"""

from __future__ import annotations
from pathlib import Path
from typing import Union

from src.main import PhasedMusicEngine


class SmoothPhase:
    """
    SmoothPhase DSL entry point.

    Example:
        sp = SmoothPhase(mode="velvet")
        sp.smooth_file("input.wav", "output.wav")

    Modes:
        velvet : soft transient smoothing
        legato : glide-like transitions
        melt   : heavy smoothing + spectral softening
    """

    VALID_MODES = {"velvet", "legato", "melt"}

    def __init__(self, mode: str = "velvet"):
        mode = mode.lower()
        if mode not in self.VALID_MODES:
            raise ValueError(f"Unknown SmoothPhase mode: {mode}")

        self.mode = mode
        self.engine = PhasedMusicEngine(mode=mode)

    # -------------------------------------------------------------
    # File-based smoothing
    # -------------------------------------------------------------
    def smooth_file(self,
                    input_path: Union[str, Path],
                    output_path: Union[str, Path]) -> None:
        """
        Smooth an audio file using the selected DSL mode.
        """

        input_path = Path(input_path)
        output_path = Path(output_path)

        self.engine.smooth_file(str(input_path), str(output_path))

    # -------------------------------------------------------------
    # Mode switching
    # -------------------------------------------------------------
    def set_mode(self, mode: str) -> None:
        """
        Change smoothing mode dynamically.
        """
        mode = mode.lower()
        if mode not in self.VALID_MODES:
            raise ValueError(f"Unknown SmoothPhase mode: {mode}")

        self.mode = mode
        self.engine = PhasedMusicEngine(mode=mode)

    # -------------------------------------------------------------
    # Future DSL expansion hooks
    # -------------------------------------------------------------
    def velvet(self):
        """Switch to velvet mode."""
        self.set_mode("velvet")

    def legato(self):
        """Switch to legato mode."""
        self.set_mode("legato")

    def melt(self):
        """Switch to melt mode."""
        self.set_mode("melt")
