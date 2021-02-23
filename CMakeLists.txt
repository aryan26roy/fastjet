
cmake_minimum_required(VERSION 3.1...3.16)
project(Pathfinders LANGUAGES CXX)


add_subdirectory(pybind11)


pybind11_add_module(_core src/main.cpp)
set_target_properties(_core PROPERTIES CXX_VISIBILITY_PRESET hidden)

