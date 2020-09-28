/* -*- c++ -*- */
/*
 * Copyright 2020 gr-taller author.
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
#include "deinterleaver_impl.h"

namespace gr
{
  namespace taller
  {

    deinterleaver::sptr
    deinterleaver::make(const std::vector<int> &sequence)
    {
      return gnuradio::get_initial_sptr(new deinterleaver_impl(sequence));
    }

    /*
     * The private constructor
     */
    deinterleaver_impl::deinterleaver_impl(const std::vector<int> &sequence)
        : gr::sync_block("deinterleaver",
                         gr::io_signature::make(1, 1, sequence.size() * sizeof(gr_complex)),
                         gr::io_signature::make(1, 1, sequence.size() * sizeof(gr_complex))),
          d_sequence(sequence)
    // si necesito más de una salida de distintos tipos?
    {
      d_nsamples = (int)d_sequence.size();
    }

    /*
     * Our virtual destructor.
     */
    deinterleaver_impl::~deinterleaver_impl()
    {
    }

    int
    deinterleaver_impl::work(int noutput_items,
                             gr_vector_const_void_star &input_items,
                             gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *)input_items[0];
      gr_complex *out = (gr_complex *)output_items[0];

      // Do <+signal processing+>
      for (int i = 0; i < noutput_items; i++)
      {
        for (int j = 0; j < d_nsamples; j++)
        {
          out[i * d_nsamples + d_sequence[j]] = in[i * d_nsamples + j];
        }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace taller */
} /* namespace gr */