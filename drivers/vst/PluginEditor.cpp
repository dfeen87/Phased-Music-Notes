#include "PluginProcessor.h"
#include "PluginEditor.h"

// ==============================================================================
// Constructor
// ==============================================================================
PhasedNotesAudioProcessorEditor::PhasedNotesAudioProcessorEditor(PhasedNotesAudioProcessor& p)
    : AudioProcessorEditor(&p), processorRef(p)
{
    // Mode selector
    modeBox.addItem("Velvet", 1);
    modeBox.addItem("Legato", 2);
    modeBox.addItem("Melt",   3);

    modeBox.onChange = [this]()
    {
        const int id = modeBox.getSelectedId();
        std::string mode = "velvet";

        if (id == 2) mode = "legato";
        if (id == 3) mode = "melt";

        processorRef.setMode(mode);
    };

    modeBox.setSelectedId(1);
    addAndMakeVisible(modeBox);

    setSize(300, 120);
}

// ==============================================================================
PhasedNotesAudioProcessorEditor::~PhasedNotesAudioProcessorEditor() {}

// ==============================================================================
void PhasedNotesAudioProcessorEditor::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::black);

    g.setColour(juce::Colours::white);
    g.setFont(18.0f);
    g.drawText("Phased Notes", getLocalBounds(), juce::Justification::centredTop);
}

// ==============================================================================
void PhasedNotesAudioProcessorEditor::resized()
{
    modeBox.setBounds(50, 50, 200, 30);
}
