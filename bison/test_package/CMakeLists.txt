project(test_package)
cmake_minimum_required(VERSION 3.0)

set(CMAKE_CXX_STANDARD 11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(BISON)

set(BISON_VARS
    BISON_FOUND
    BISON_EXECUTABLE
    BISON_VERSION
)

foreach(BISON_VAR ${BISON_VARS})
    message("${BISON_VAR}: ${${BISON_VAR}}")
    if(NOT ${BISON_VAR})
        message(FATAL_ERROR "${BISON_VAR} NOT FOUND")
    endif()
endforeach()

bison_target(Bison_McParser
    mc_parser.yy "${CMAKE_CURRENT_BINARY_DIR}/mc_parser.cpp"
)

add_executable(McParser
    "${CMAKE_CURRENT_BINARY_DIR}/mc_parser.cpp"
    dummy_lex.cpp
)
target_include_directories(McParser
    PRIVATE
        "${CMAKE_CURRENT_BINARY_DIR}"
)
target_link_libraries(McParser
    PRIVATE
        CONAN_PKG::bison
)