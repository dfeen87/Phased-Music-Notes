#include <pybind11/embed.h>
namespace py = pybind11;

static py::object engine;

void init_python() {
    py::initialize_interpreter();
    py::module pmn = py::module::import("phased_music_notes");
    engine = pmn.attr("PhasedNotes")("velvet");
}

py::array process_audio(py::array audio) {
    return engine.attr("process_buffer")(audio);
}
