"""
Phased-Music-Notes
Smooth Audio Notes with phase-aligned transitions.

This main file initializes the smoothing engine, loads audio,
detects note boundaries, applies harmonic blending, and outputs
a softened, gradual version of the track.

MIT License
"""

from phased_music_notes.analyzer import NoteAnalyzer
from phased_music_notes.smoother import PhaseSmoother
from phased_music_notes.harmonics import HarmonicBlender
from phased_music_notes.dsl import SmoothPhase
import soundfile as sf


def process_audio(input_path: str, output_path: str, mode: str = "velvet"):
    """
    Core processing pipeline:
    1. Load audio
    2. Analyze note boundaries
    3. Apply smoothing + harmonic blending
    4. Save softened output
    """

    # Load audio
    audio, sr = sf.read(input_path)

    # Initialize components
    analyzer = NoteAnalyzer(sr=sr)
    smoother = PhaseSmoother(mode=mode)
    harmonics = HarmonicBlender()

    # Detect note boundaries
    boundaries = analyzer.detect_boundaries(audio)

    # Apply smoothing
    softened = smoother.apply(audio, boundaries)

    # Blend harmonics for gradual transitions
    final_output = harmonics.blend(softened)

    # Save result
    sf.write(output_path, final_output, sr)

    print(f"Phased-Music-Notes: '{mode}' smoothing applied.")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    # Example usage of the DSL-style interface
    engine = SmoothPhase(mode="velvet")
    engine.smooth_file("input.wav", "output_smooth.wav")
