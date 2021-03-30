
cmake_minimum_required(VERSION 3.1...3.16)
project(fastjet LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
add_subdirectory(pybind11)
set(FASTJET "${CMAKE_CURRENT_SOURCE_DIR}/cgal/buildf_dir/include/fastjet")
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_EXE_LINKER_FLAGS "-static")
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

include_directories("${CMAKE_CURRENT_SOURCE_DIR}/fastjet/fastjet")
include_directories(/${CMAKE_CURRENT_SOURCE_DIR}/cgal/buildf_dir/bin)
find_package(FASTJET REQUIRED)


message(STATUS "Fastjet libs: ${FASTJET_LIBS}, dirs: ${FASTJET_LIBS_DIR}")


link_directories(${FASTJET_LIBS_DIR})
add_definitions(${FASTJET_DEFINITIONS})

pybind11_add_module(_core src/main.cpp SHARED)
set_target_properties(_core PROPERTIES CXX_VISIBILITY_PRESET hidden POSITION_INDEPENDENT_CODE TRUE)
