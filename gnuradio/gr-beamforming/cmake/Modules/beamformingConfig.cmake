INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_BEAMFORMING beamforming)

FIND_PATH(
    BEAMFORMING_INCLUDE_DIRS
    NAMES beamforming/api.h
    HINTS $ENV{BEAMFORMING_DIR}/include
        ${PC_BEAMFORMING_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    BEAMFORMING_LIBRARIES
    NAMES gnuradio-beamforming
    HINTS $ENV{BEAMFORMING_DIR}/lib
        ${PC_BEAMFORMING_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/beamformingTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(BEAMFORMING DEFAULT_MSG BEAMFORMING_LIBRARIES BEAMFORMING_INCLUDE_DIRS)
MARK_AS_ADVANCED(BEAMFORMING_LIBRARIES BEAMFORMING_INCLUDE_DIRS)
