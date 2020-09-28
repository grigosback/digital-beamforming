/* -*- c++ -*- */

#define ANALOG_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "analog_swig_doc.i"

%{
#include "analog/vectornoise_source.h"
%}

%include "analog/vectornoise_source.h"
GR_SWIG_BLOCK_MAGIC2(analog, vectornoise_source);
