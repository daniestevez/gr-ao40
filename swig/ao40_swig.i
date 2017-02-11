/* -*- c++ -*- */

#define AO40_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "ao40_swig_doc.i"

%{
#include "ao40/syncframe.h"
#include "ao40/deinterleaver.h"
#include "ao40/rs_decoder.h"
%}


%include "ao40/syncframe.h"
GR_SWIG_BLOCK_MAGIC2(ao40, syncframe);
%include "ao40/deinterleaver.h"
GR_SWIG_BLOCK_MAGIC2(ao40, deinterleaver);
%include "ao40/rs_decoder.h"
GR_SWIG_BLOCK_MAGIC2(ao40, rs_decoder);
