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

#ifndef INCLUDED_BEAMFORMING_RANDOMSAMPLER_IMPL_H
#define INCLUDED_BEAMFORMING_RANDOMSAMPLER_IMPL_H

#include <beamforming/randomsampler.h>
#include <iostream>  // std::cout
#include <algorithm> // std::shuffle
#include <array>     // std::array
#include <random>    // std::default_random_engine
#include <chrono>    // std::chrono::system_clock

namespace gr
{
  namespace beamforming
  {

    class randomsampler_impl : public randomsampler
    {
    private:
      unsigned int d_vlen;
      unsigned int d_decimation;
      unsigned int d_ninput_items;
      std::vector<int> d_idx;
      unsigned d_seed;

    public:
      randomsampler_impl(unsigned int vlen, unsigned int decimation);
      ~randomsampler_impl();

      // Where all the action really happens
      int work(
          int noutput_items,
          gr_vector_const_void_star &input_items,
          gr_vector_void_star &output_items);
    };

  } // namespace beamforming
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_RANDOMSAMPLER_IMPL_H */
