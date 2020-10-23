/* -*- c++ -*- */

#define BEAMFORMING_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "beamforming_swig_doc.i"

%{
#include "beamforming/beamformer.h"
#include "beamforming/phasedarray.h"
#include "beamforming/doaesprit.h"
#include "beamforming/randomsampler.h"
%}

%include "beamforming/beamformer.h"
GR_SWIG_BLOCK_MAGIC2(beamforming, beamformer);
%include "beamforming/phasedarray.h"
GR_SWIG_BLOCK_MAGIC2(beamforming, phasedarray);
%include "beamforming/doaesprit.h"
GR_SWIG_BLOCK_MAGIC2(beamforming, doaesprit);
%include "beamforming/randomsampler.h"
GR_SWIG_BLOCK_MAGIC2(beamforming, randomsampler);
