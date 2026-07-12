#pragma once

#include <juce_gui_basics/juce_gui_basics.h>
#include "PluginProcessor.h"

class PhasedNotesAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:
    explicit PhasedNotesAudioProcessorEditor (PhasedNotesAudioProcessor&);
    ~PhasedNotesAudioProcessorEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    PhasedNotesAudioProcessor& processorRef;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (PhasedNotesAudioProcessorEditor)
};
