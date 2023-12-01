cmake_minimum_required(VERSION 3.26)
project(aoc_2023)

set(CMAKE_CXX_STANDARD 20)

add_executable(aoc_2023 main.cpp)

find_package(Catch2 3 REQUIRED)
add_executable(tests test_day1.cpp
        test_day1.cpp)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
