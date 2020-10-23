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

#ifndef INCLUDED_ANALOG_VECTORNOISE_SOURCE_IMPL_H
#define INCLUDED_ANALOG_VECTORNOISE_SOURCE_IMPL_H

#include <analog/vectornoise_source.h>
#include <gnuradio/random.h>

namespace gr
{
  namespace analog
  {

    class vectornoise_source_impl : public vectornoise_source
    {
    private:
      float d_ampl;
      unsigned int d_vlen;
      gr::random d_rng;

    public:
      vectornoise_source_impl(float ampl, unsigned int vlen);
      ~vectornoise_source_impl();
      void set_ampl(float ampl);

      // Where all the action really happens
      int work(
          int noutput_items,
          gr_vector_const_void_star &input_items,
          gr_vector_void_star &output_items);
    };

  } // namespace analog
} // namespace gr

#endif /* INCLUDED_ANALOG_VECTORNOISE_SOURCE_IMPL_H */
