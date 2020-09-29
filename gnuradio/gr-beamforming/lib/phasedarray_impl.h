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

#ifndef INCLUDED_BEAMFORMING_PHASEDARRAY_IMPL_H
#define INCLUDED_BEAMFORMING_PHASEDARRAY_IMPL_H

#include <beamforming/phasedarray.h>
#include <volk/volk.h>
#include <math.h>

namespace gr
{
  namespace beamforming
  {

    class phasedarray_impl : public phasedarray
    {
    private:
      unsigned int d_mx;
      unsigned int d_my;
      unsigned int d_vlen;
      float d_theta;
      float d_phi;
      float d_fc;
      float d_element_separation;
      float d_element_error;
      float d_c;
      float d_k;
      unsigned int d_alignment;
      gr_complex d_a_k;
      lv_32fc_t *d_a;

    public:
      phasedarray_impl(unsigned int mx, unsigned int my, float theta, float phi, float fc, float element_separation, float element_error);
      ~phasedarray_impl();

      // Where all the action really happens
      int work(
          int noutput_items,
          gr_vector_const_void_star &input_items,
          gr_vector_void_star &output_items);
      float deg2radians(float angle);
      void set_stearing_vector();
      void set_elevation(float theta);
      void set_azimuth(float phi);
    };

  } // namespace beamforming
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_PHASEDARRAY_IMPL_H */
