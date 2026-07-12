import numpy as np
import soundfile as sf
import time
from drivers.api import PhasedNotesBuffer

def main():
    print("--- Smooth Buffer Example ---")
    sr = 44100

    # 1. Simulate loaded audio via a NumPy array (instead of librosa)
    # Generate synthetic stereo signal directly
    t1 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine1 = np.sin(2 * np.pi * 440 * t1)

    t2 = np.linspace(0, 0.5, sr // 2, endpoint=False)
    sine2 = np.sin(2 * np.pi * 880 * t2)

    mono_signal = np.concatenate([sine1, sine2])

    # Simulate a loader that returns (2, numSamples) like librosa does for stereo
    loaded_audio = np.stack([mono_signal, mono_signal])

    print(f"Simulated loaded audio shape: {loaded_audio.shape}")

    # 2. Convert to planar stereo (numSamples, 2)
    if loaded_audio.ndim == 2 and loaded_audio.shape[0] == 2:
        planar_stereo = loaded_audio.T
    else:
        planar_stereo = loaded_audio

    print(f"Converted to planar stereo shape: {planar_stereo.shape}")

    # 3. Use PhasedNotesBuffer
    start_time = time.time()

    pnb = PhasedNotesBuffer(mode="velvet", sr=sr)
    output_buffer = pnb.process_buffer(planar_stereo)

    end_time = time.time()

    output_path = "buffer_output.wav"
    sf.write(output_path, output_buffer, sr)

    print(f"Processed output shape: {output_buffer.shape}")
    print(f"Output saved to: {output_path}")
    print(f"Buffer processing time: {(end_time - start_time) * 1000:.2f} ms")

if __name__ == "__main__":
    main()
