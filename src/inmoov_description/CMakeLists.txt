cmake_minimum_required(VERSION 3.5)
project(inmoov_description)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)


if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
endif()

## INSTALL
install(
  DIRECTORY robots urdf config launch/
  DESTINATION share/${PROJECT_NAME}
)

## EXPORTS
ament_package()