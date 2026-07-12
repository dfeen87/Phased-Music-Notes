#pragma once

// python_bridge.hpp
// Header for Python DSP bridge

// Initialize Python + PhasedNotesBuffer
void init_python(int sampleRate, const std::string& mode = "velvet");

// Process audio buffer (mono or stereo)
void process_audio(float* audioData,
                   int numSamples,
                   int numChannels);

// Shutdown Python interpreter
void shutdown_python();
