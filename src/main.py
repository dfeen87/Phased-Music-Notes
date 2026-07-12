"""
Phased-Music-Notes
Smooth Audio Notes with phase-aligned transitions.

This engine mirrors the deterministic architecture of AeroCam:
Analyzer → Smoother → Harmonic Blender → Output.

MIT License
"""

import soundfile as sf
from phased_music_notes.analyzer import NoteAnalyzer
from phased_music_notes.smoother import PhaseSmoother
from phased_music_notes.harmonics import HarmonicBlender


class PhasedMusicEngine:
    """
    Static-style engine inspired by AeroCam's main.cpp.
    Modules are initialized once, mirroring embedded-style determinism.
    """

    def __init__(self, mode="velvet"):
        self.mode = mode
        self.analyzer = NoteAnalyzer()
        self.smoother = PhaseSmoother(mode=mode)
        self.harmonics = HarmonicBlender()

    def smooth_file(self, input_path: str, output_path: str):
        # Load audio
        audio, sr = sf.read(input_path)

        # Step 1: Detect note boundaries
        boundaries = self.analyzer.detect_boundaries(audio, sr)

        # Step 2: Apply smoothing per boundary region
        softened = self.smoother.apply(audio, boundaries)

        # Step 3: Blend harmonics for gradual transitions
        final_output = self.harmonics.blend(softened, sr)

        # Step 4: Save output
        sf.write(output_path, final_output, sr)

        print(f"[Phased-Music-Notes] Mode '{self.mode}' applied.")
        print(f"Output saved to {output_path}")


if __name__ == "__main__":
    engine = PhasedMusicEngine(mode="velvet")
    engine.smooth_file("input.wav", "output_smooth.wav")
