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

#ifndef INCLUDED_BEAMFORMING_VECTORNOISE_SOURCE_IMPL_H
#define INCLUDED_BEAMFORMING_VECTORNOISE_SOURCE_IMPL_H

#include <beamforming/vectornoise_source.h>
#include <gnuradio/random.h>
#include <vector>

namespace gr
{
  namespace beamforming
  {
    template <class T>
    class vectornoise_source_impl : public vectornoise_source
    {
    private:
      float d_ampl;
      int d_vlen;
      gr::random d_rng;
      std::vector<T> d_samples;
      uint64_t d_state[2];

    public:
      vectornoise_source_impl(float ampl, long seed, long samples, int vlen);
      ~vectornoise_source_impl();

      T sample();
      T sample_unbiased();
      const std::vector<T> &samples() const;

      void set_amplitude(float ampl);
      void generate();

      float amplitude() const { return d_ampl; }

      int work(
          int noutput_items,
          gr_vector_const_void_star &input_items,
          gr_vector_void_star &output_items);
    };

  } // namespace beamforming
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_VECTORNOISE_SOURCE_IMPL_H */
