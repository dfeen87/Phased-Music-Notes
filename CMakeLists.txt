cmake_minimum_required(VERSION 3.15)

project(PhasedNotes VERSION 1.0.0)

# JUCE
add_subdirectory(drivers/JUCE)

# pybind11
add_subdirectory(drivers/pybind11)

# Plugin target
juce_add_plugin(PhasedNotes
    COMPANY_NAME "PhasedMusic"
    BUNDLE_ID    "com.phasedmusic.notes"
    PLUGIN_MANUFACTURER_CODE PMus
    PLUGIN_CODE PNts
    FORMATS VST3 AU
    PRODUCT_NAME "PhasedNotes"
)

target_sources(PhasedNotes PRIVATE
    drivers/vst/PluginProcessor.cpp
    drivers/vst/PluginEditor.cpp
    drivers/vst/python_bridge.cpp
)

target_include_directories(PhasedNotes PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/drivers/vst
    ${CMAKE_CURRENT_SOURCE_DIR}/drivers
)

target_link_libraries(PhasedNotes PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_dsp
    pybind11::embed
)

target_compile_features(PhasedNotes PRIVATE cxx_std_17)
