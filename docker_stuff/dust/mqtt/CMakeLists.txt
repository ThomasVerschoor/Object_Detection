cmake_minimum_required(VERSION 3.10)
project(mqtt_module VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)

option(WITH_EXAMPLES "build with examples" ON)
if (NOT WIN32)
    option(STATIC_MOSQUITTO "link libmosquitto statically" ON)
else ()
    option(STATIC_MOSQUITTO "link libmosquitto statically" OFF)
endif ()

if (WITH_EXAMPLES)
    add_definitions(-DWITH_EXAMPLES)
endif ()

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/version.txt "${PROJECT_VERSION}")

find_package(dust 2 REQUIRED)
find_path(MOSQUITTO_INCLUDE_DIR mosquitto.h)
if (STATIC_MOSQUITTO)
    find_library(MOSQUITTO_LIBRARY NAMES mosquitto_static)
    find_package(OpenSSL)
else ()
    find_library(MOSQUITTO_LIBRARY NAMES mosquitto)
endif ()

message("DUST Include Path: ${DUST_INCLUDE_DIR}")
message("DUST Library Path: ${DUST_LIBRARIES}")
message("Mosquitto Include Path: ${MOSQUITTO_INCLUDE_DIR}")
message("Mosquitto Library Path: ${MOSQUITTO_LIBRARY}")

add_library(mqtt_module SHARED
        src/mqtt_module.cpp
        src/mqtt_module.h
        src/mqtt_factory.cpp
        src/mqtt_factory.h
        src/mqtt_transport.cpp
        src/mqtt_transport.h)

target_include_directories(mqtt_module PUBLIC ${MOSQUITTO_INCLUDE_DIR} ${DUST_INCLUDE_DIR} PRIVATE src)
target_link_libraries(mqtt_module ${DUST_LIBRARIES} ${MOSQUITTO_LIBRARY})

if (STATIC_MOSQUITTO AND OPENSSL_FOUND)
    target_link_libraries(mqtt_module OpenSSL::SSL)
endif ()

# Strip binary for release builds
if (CMAKE_BUILD_TYPE STREQUAL Release AND CMAKE_STRIP)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_STRIP} $<TARGET_FILE:${PROJECT_NAME}>)
endif ()

if (WITH_EXAMPLES)
    add_executable(simplePublisher example/simple_publisher.cpp)
    target_include_directories(simplePublisher PUBLIC ${DUST_INCLUDE_DIR})
    target_link_libraries(simplePublisher ${DUST_LIBRARIES})

    add_executable(simpleSubscriber example/simple_subscriber.cpp)
    target_include_directories(simpleSubscriber PUBLIC ${DUST_INCLUDE_DIR})
    target_link_libraries(simpleSubscriber ${DUST_LIBRARIES})
endif ()
