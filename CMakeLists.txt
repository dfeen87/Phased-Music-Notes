cmake_minimum_required(VERSION 3.15)
project(PhasedNotes VERSION 1.0.0)

# ================================================================
# Disable VST2 BEFORE JUCE is added
# ================================================================
set(JUCE_BUILD_VST2 OFF CACHE BOOL "" FORCE)
set(JUCE_PLUGINHOST_VST OFF CACHE BOOL "" FORCE)
set(JUCE_PLUGINHOST_VST3 ON CACHE BOOL "" FORCE)

# ================================================================
# JUCE + pybind11
# ================================================================
add_subdirectory(drivers/JUCE)
add_subdirectory(drivers/pybind11)

# ================================================================
# Plugin formats per OS
# ================================================================
if (APPLE)
    set(PLUGIN_FORMATS VST3 AU)
else()
    set(PLUGIN_FORMATS VST3)
endif()

# ================================================================
# Plugin target
# ================================================================
juce_add_plugin(PhasedNotes
    COMPANY_NAME "PhasedMusic"
    BUNDLE_ID    "com.phasedmusic.notes"
    PLUGIN_MANUFACTURER_CODE PMus
    PLUGIN_CODE PNts
    FORMATS ${PLUGIN_FORMATS}
    PRODUCT_NAME "PhasedNotes"
)

# JUCE generates PhasedNotes_VST3 on Linux
set(PLUGIN_TARGET PhasedNotes_VST3)

# ================================================================
# Source files
# ================================================================
target_sources(${PLUGIN_TARGET} PRIVATE
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
target_include_directories(${PLUGIN_TARGET} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/drivers/vst
    ${CMAKE_CURRENT_SOURCE_DIR}/drivers
)

# ================================================================
# Link libraries
# ================================================================
target_link_libraries(${PLUGIN_TARGET} PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_dsp
    pybind11::embed
)

target_compile_features(${PLUGIN_TARGET} PRIVATE cxx_std_17)
