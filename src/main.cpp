#include <iostream>
#include <cstdlib>
#include <bits/stdc++.h> 
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#define infinity 9999
#include <algorithm>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace std;

void interface(){

	cout<<"Inside pybind module";
}

PYBIND11_MODULE(_core, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: python_example
        .. autosummary::
           :toctree: _generate
           DFS
           BFS
           Dijkstra
    )pbdoc";

    m.def("interface", &interface);

}
