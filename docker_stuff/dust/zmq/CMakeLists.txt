cmake_minimum_required(VERSION 3.10)
project(zmq_module VERSION 0.2.0)

set(CMAKE_CXX_STANDARD 17)

option(WITH_EXAMPLES "build with examples" ON)

if (WITH_EXAMPLES)
    add_definitions(-DWITH_EXAMPLES)
endif ()

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/version.txt "${PROJECT_VERSION}")

# set(WITH_DUST_STATIC ON)
find_package(dust 2 REQUIRED)
find_package(ZeroMQ 4.3 REQUIRED)
if (NOT ZeroMQ_FOUND)
    message(FATAL_ERROR "Cannot find ZeroMQ")
endif ()

message("DUST Include Path: ${DUST_INCLUDE_DIR}")
message("DUST Library Path: ${DUST_LIBRARIES}")
message("ZeroMQ Include Path: ${ZeroMQ_INCLUDE_DIR}")
message("ZeroMQ Library Path: ${ZeroMQ_LIBRARY}")

add_library(zmq_module SHARED
        src/zmq_module.h src/zmq_module.cpp
        src/zmq_transport.h src/zmq_transport.cpp
        src/zmq_factory.h src/zmq_factory.cpp)

target_include_directories(${PROJECT_NAME} PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
        ${DUST_INCLUDE_DIR}
        ${ZeroMQ_INCLUDE_DIR}
        PRIVATE ${PROJECT_NAME}
        )

target_link_libraries(${PROJECT_NAME}
        ${DUST_LIBRARIES}
        libzmq-static)

# Strip binary for release builds
if (CMAKE_BUILD_TYPE STREQUAL Release AND CMAKE_STRIP)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_STRIP} $<TARGET_FILE:${PROJECT_NAME}>)
endif ()

if (WITH_EXAMPLES)
    configure_file(example/resources/configuration.json configuration.json COPYONLY)

    add_executable(simplePublisher example/simple_publisher.cpp)

    target_include_directories(simplePublisher PUBLIC
            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
            $<INSTALL_INTERFACE:include>
            ${DUST_INCLUDE_DIR}
            )
    target_link_libraries(simplePublisher ${DUST_LIBRARIES})

    add_executable(simpleSubscriber example/simple_subscriber.cpp)

    target_include_directories(simpleSubscriber PUBLIC
            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
            $<INSTALL_INTERFACE:include>
            ${DUST_INCLUDE_DIR}
            )
    target_link_libraries(simpleSubscriber ${DUST_LIBRARIES})
endif ()