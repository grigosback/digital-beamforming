/* -*- c++ -*- */
/*
 * Copyright 2020 gr-analog author.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "vectornoise_source_impl.h"

namespace gr
{
  namespace analog
  {

    vectornoise_source::sptr
    vectornoise_source::make(float ampl, unsigned int vlen)
    {
      return gnuradio::get_initial_sptr(new vectornoise_source_impl(ampl, vlen));
    }

    /*
     * The private constructor
     */
    vectornoise_source_impl::vectornoise_source_impl(float ampl, unsigned int vlen)
        : gr::sync_block("vectornoise_source",
                         gr::io_signature::make(0, 0, 0),
                         gr::io_signature::make(1, 1, sizeof(gr_complex) * vlen)),
          d_ampl(ampl / sqrtf(2.0f)), d_vlen(vlen)
    {
    }

    /*
     * Our virtual destructor.
     */
    vectornoise_source_impl::~vectornoise_source_impl()
    {
    }

    int
    vectornoise_source_impl::work(int noutput_items,
                                  gr_vector_const_void_star &input_items,
                                  gr_vector_void_star &output_items)
    {
      gr_complex *out = (gr_complex *)output_items[0];

      for (int i = 0; i < noutput_items; i++)
      {
        for (int j = 0; j < d_vlen; j++)
        {
          out[i * d_vlen + j] = d_ampl * d_rng.rayleigh_complex();
        }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace analog */
} /* namespace gr */
