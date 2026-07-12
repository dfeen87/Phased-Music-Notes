cmake_minimum_required(VERSION 3.15)

project(PhasedNotes VERSION 1.0.0)

# ================================================================
# Disable VST2 completely (prevents JUCE automation conflict error)
# ================================================================
set(JUCE_BUILD_VST2 OFF)

# ================================================================
# JUCE + pybind11
# ================================================================
add_subdirectory(drivers/JUCE)
add_subdirectory(drivers/pybind11)

# ================================================================
# Plugin target
# ================================================================
juce_add_plugin(PhasedNotes
    COMPANY_NAME "PhasedMusic"
    BUNDLE_ID    "com.phasedmusic.notes"
    PLUGIN_MANUFACTURER_CODE PMus
    PLUGIN_CODE PNts

    # IMPORTANT: VST3 + AU ONLY — NO VST2
    FORMATS VST3 AU

    PRODUCT_NAME "PhasedNotes"
)

# ================================================================
# Source files
# ================================================================
target_sources(PhasedNotes PRIVATE
    drivers/vst/PluginProcessor.cpp
    drivers/vst/PluginProcessor.h
    drivers/vst/PluginEditor.cpp
    drivers/vst/PluginEditor.h
    drivers/vst/python_bridge.cpp
    drivers/vst/python_bridge.hpp
)

# ================================================================
# Include directories
# ================================================================
target_include_directories(PhasedNotes PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/drivers/vst
    ${CMAKE_CURRENT_SOURCE_DIR}/drivers
)

# ================================================================
# Link libraries
# ================================================================
target_link_libraries(PhasedNotes PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_dsp
    pybind11::embed
)

# ================================================================
# C++ standard
# ================================================================
target_compile_features(PhasedNotes PRIVATE cxx_std_17)

# ================================================================
# Post-build properties / specific platforms
# ================================================================
# Avoid AU validation errors on non-macOS systems (JUCE handles most of it, but just in case)
if(NOT APPLE)
    # Remove AU format if not on macOS, though juce_add_plugin gracefully handles it
endif()
