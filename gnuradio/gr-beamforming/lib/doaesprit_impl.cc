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
#include "doaesprit_impl.h"

namespace gr
{
  namespace beamforming
  {

    doaesprit::sptr
    doaesprit::make(unsigned int mx, unsigned int my, float fc, float element_separation, unsigned int spa)
    {
      return gnuradio::get_initial_sptr(new doaesprit_impl(mx, my, fc, element_separation, spa));
    }

    /*
     * The private constructor
     */
    doaesprit_impl::doaesprit_impl(unsigned int mx, unsigned int my, float fc, float element_separation, unsigned int spa)
        : gr::sync_block("doaesprit",
                         gr::io_signature::make(1, 1, sizeof(gr_complex) * mx * my),
                         gr::io_signature::make(0, 0, 0)),
          d_mx(mx), d_my(my), d_vlen(mx * my), d_fc(fc), d_spa(spa)
    {
      d_c = 299792458;
      d_k = (2 * M_PI * fc) / d_c;
    }

    /*
     * Our virtual destructor.
     */
    doaesprit_impl::~doaesprit_impl()
    {
    }

    int
    doaesprit_impl::work(int noutput_items,
                         gr_vector_const_void_star &input_items,
                         gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *)input_items[0];

      // Do <+signal processing+>

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace beamforming */
} /* namespace gr */
