cmake_minimum_required(VERSION 3.15)

project(PhasedNotes VERSION 1.0.0)

# ======================================================================
# JUCE setup
# ======================================================================
# JUCE should be added as a submodule:
#   git submodule add https://github.com/juce-framework/JUCE.git
#   add_subdirectory(JUCE)
add_subdirectory(JUCE)

# ======================================================================
# pybind11 setup
# ======================================================================
# If pybind11 is a submodule:
#   git submodule add https://github.com/pybind/pybind11.git
#   add_subdirectory(pybind11)
add_subdirectory(pybind11)

# ======================================================================
# Plugin target
# ======================================================================
juce_add_plugin(PhasedNotes
    COMPANY_NAME "PhasedMusic"
    BUNDLE_ID    "com.phasedmusic.notes"
    PLUGIN_MANUFACTURER_CODE PMus
    PLUGIN_CODE PNts
    FORMATS VST3 AU
    PRODUCT_NAME "PhasedNotes"
)

# ======================================================================
# Source files
# ======================================================================
target_sources(PhasedNotes PRIVATE
    PluginProcessor.cpp
    PluginEditor.cpp
    python_bridge.cpp
)

# ======================================================================
# Include directories
# ======================================================================
target_include_directories(PhasedNotes PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../..
)

# ======================================================================
# Link libraries
# ======================================================================
target_link_libraries(PhasedNotes PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_dsp
    pybind11::embed
)

# ======================================================================
# C++ standard
# ======================================================================
target_compile_features(PhasedNotes PRIVATE cxx_std_17)

# ======================================================================
# macOS bundle settings (for AU)
# ======================================================================
if(APPLE)
    set_target_properties(PhasedNotes PROPERTIES
        MACOSX_BUNDLE TRUE
        MACOSX_BUNDLE_INFO_PLIST ${CMAKE_CURRENT_SOURCE_DIR}/Info.plist
    )
endif()
