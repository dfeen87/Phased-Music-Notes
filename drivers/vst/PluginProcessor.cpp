void PhasedNotesAudioProcessor::processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    auto* left  = buffer.getWritePointer(0);
    auto* right = buffer.getWritePointer(1);

    py::array audio = py::array({buffer.getNumSamples(), 2}, buffer.getArrayOfWritePointers());

    py::array result = process_audio(audio);

    // Copy result back into buffer
    memcpy(left,  result.data(0), buffer.getNumSamples() * sizeof(float));
    memcpy(right, result.data(1), buffer.getNumSamples() * sizeof(float));
}
