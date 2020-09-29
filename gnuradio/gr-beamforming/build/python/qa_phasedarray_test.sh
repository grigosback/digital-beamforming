#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir="/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python"
export GR_CONF_CONTROLPORT_ON=False
export PATH="/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/build/python":$PATH
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/mnt/d/Users/grigo/Google\ Drive/Facultad/Balseiro/PI\ Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/build/swig:$PYTHONPATH
/usr/bin/python3 /mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/gnuradio/gr-beamforming/python/qa_phasedarray.py 
