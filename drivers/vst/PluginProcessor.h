#pragma once

#include <juce_audio_processors/juce_audio_processors.h>
#include <string>

// Forward declaration of your Python bridge
void init_python(int sampleRate, const std::string& mode = "velvet");
void shutdown_python();
void process_audio(float* audioData, int numSamples, int numChannels);

class PhasedNotesAudioProcessor : public juce::AudioProcessor
{
public:
    PhasedNotesAudioProcessor();
    ~PhasedNotesAudioProcessor() override;

    //==============================================================================
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

    bool isBusesLayoutSupported(const BusesLayout& layouts) const override;

    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    //==============================================================================
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    //==============================================================================
    const juce::String getName() const override { return "PhasedNotes"; }

    bool acceptsMidi() const override { return false; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }

    double getTailLengthSeconds() const override { return 0.0; }

    //==============================================================================
    int getNumPrograms() override { return 1; }
    int getCurrentProgram() override { return 0; }
    void setCurrentProgram(int) override {}
    const juce::String getProgramName(int) override { return {}; }
    void changeProgramName(int, const juce::String&) override {}

    //==============================================================================
    void getStateInformation(juce::MemoryBlock&) override {}
    void setStateInformation(const void*, int) override {}

    //==============================================================================
    // Called by PluginEditor to switch DSP modes
    void setMode(const std::string& mode);

private:
    std::string currentMode = "velvet";

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PhasedNotesAudioProcessor)
};
