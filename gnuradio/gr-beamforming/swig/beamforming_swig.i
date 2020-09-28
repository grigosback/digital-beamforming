/* -*- c++ -*- */

#define BEAMFORMING_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "beamforming_swig_doc.i"

%{
#include "beamforming/beamformer.h"
%}

%include "beamforming/beamformer.h"
GR_SWIG_BLOCK_MAGIC2(beamforming, beamformer);
