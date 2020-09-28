INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_ANALOG analog)

FIND_PATH(
    ANALOG_INCLUDE_DIRS
    NAMES analog/api.h
    HINTS $ENV{ANALOG_DIR}/include
        ${PC_ANALOG_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ANALOG_LIBRARIES
    NAMES gnuradio-analog
    HINTS $ENV{ANALOG_DIR}/lib
        ${PC_ANALOG_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/analogTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ANALOG DEFAULT_MSG ANALOG_LIBRARIES ANALOG_INCLUDE_DIRS)
MARK_AS_ADVANCED(ANALOG_LIBRARIES ANALOG_INCLUDE_DIRS)
