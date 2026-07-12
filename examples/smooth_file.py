import numpy as np
import soundfile as sf
import time
from phased_music_notes import SmoothPhase

def main():
    # 1. Generate synthetic WAV
    sr = 44100
    t1 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine1 = np.sin(2 * np.pi * 440 * t1)
    t2 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine2 = np.sin(2 * np.pi * 880 * t2)

    signal = np.concatenate([sine1, sine2])

    input_wav = "synthetic_input.wav"
    output_wav = "synthetic_output_smooth.wav"

    sf.write(input_wav, signal, sr)

    print("--- SmoothPhase DSL Example ---")
    print(f"Generated synthetic input: {input_wav}")

    # 2. Use SmoothPhase DSL
    start_time = time.time()

    sp = SmoothPhase(mode="velvet")
    sp.smooth_file(input_wav, output_wav)

    end_time = time.time()

    print(f"Mode applied: {sp.mode}")
    print(f"Output saved to: {output_wav}")
    print(f"Processing time: {(end_time - start_time) * 1000:.2f} ms")

if __name__ == "__main__":
    main()
