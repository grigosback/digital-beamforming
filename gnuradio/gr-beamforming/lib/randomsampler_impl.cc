/* -*- c++ -*- */
/*
 * Copyright 2020 gr-beamforming author.
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
#include "randomsampler_impl.h"

namespace gr
{
  namespace beamforming
  {

    randomsampler::sptr
    randomsampler::make(unsigned int vlen, unsigned int decimation)
    {
      return gnuradio::get_initial_sptr(new randomsampler_impl(vlen, decimation));
    }

    /*
     * The private constructor
     */
    randomsampler_impl::randomsampler_impl(unsigned int vlen, unsigned int decimation)
        : gr::sync_decimator("randomsampler",
                             gr::io_signature::make(1, 1, sizeof(gr_complex) * vlen),
                             gr::io_signature::make(1, 1, sizeof(gr_complex) * vlen), decimation),
          d_vlen(vlen), d_decimation(decimation)
    {
      // obtain a time-based seed:
      d_seed = std::chrono::system_clock::now().time_since_epoch().count();
    }

    /*
     * Our virtual destructor.
     */
    randomsampler_impl::~randomsampler_impl()
    {
    }

    int
    randomsampler_impl::work(int noutput_items,
                             gr_vector_const_void_star &input_items,
                             gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *)input_items[0];
      gr_complex *out = (gr_complex *)output_items[0];
      d_ninput_items = noutput_items * d_decimation;

      for (int i = 0; i < d_ninput_items; i++)
      {
        d_idx.push_back(i);
      }

      shuffle(d_idx.begin(), d_idx.end(), std::default_random_engine(d_seed));

      //std::cout << "noutput_items=" << noutput_items << "\n";
      for (int i = 0; i < noutput_items; i++)
      {
        for (int j = 0; j < d_vlen; j++)
        {
          out[i * d_vlen + j] = in[d_idx[i] * d_vlen + j];
        }
      }
      d_idx.clear();

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace beamforming */
} /* namespace gr */
