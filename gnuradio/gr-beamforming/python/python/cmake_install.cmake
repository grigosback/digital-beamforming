# Install script for directory: /mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/beamforming" TYPE FILE FILES
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/__init__.py"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/deinterleaver_py_cc.py"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/randomsampler_py_cc.py"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/doaesprit_py_cf.py"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/phasedarray_py_cc.py"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/beamformer_py_cc.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/beamforming" TYPE FILE FILES
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/__init__.pyc"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/deinterleaver_py_cc.pyc"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/randomsampler_py_cc.pyc"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/doaesprit_py_cf.pyc"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/phasedarray_py_cc.pyc"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/beamformer_py_cc.pyc"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/__init__.pyo"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/deinterleaver_py_cc.pyo"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/randomsampler_py_cc.pyo"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/doaesprit_py_cf.pyo"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/phasedarray_py_cc.pyo"
    "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/python/beamformer_py_cc.pyo"
    )
endif()

