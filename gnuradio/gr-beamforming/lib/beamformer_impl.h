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

#ifndef INCLUDED_BEAMFORMING_BEAMFORMER_IMPL_H
#define INCLUDED_BEAMFORMING_BEAMFORMER_IMPL_H

#include <beamforming/beamformer.h>
#include <volk/volk.h>

namespace gr
{
  namespace beamforming
  {

    class beamformer_impl : public beamformer
    {
    private:
      unsigned int d_mx;
      unsigned int d_my;
      unsigned int d_vlen;
      //      unsigned int d_c;
      //      float d_lambda;
      //      float d_distance;
      //      float d_k;
      //float d_fc;
      float d_theta;
      float d_phi;
      gr_complex d_a_k;
      lv_32fc_t *d_a;
      lv_32fc_t *d_aux;
      float *d_ones;
      unsigned int d_alignment;

      gr_vector_float d_doa;

    public:
      beamformer_impl(unsigned int mx, unsigned int my);
      ~beamformer_impl();

      // Where all the action really happens
      int work(
          int noutput_items,
          gr_vector_const_void_star &input_items,
          gr_vector_void_star &output_items);

      void set_doa(float theta, float phi);
      void set_doa_msg(pmt::pmt_t msg);
      void set_stearing_vector();
    };

  } // namespace beamforming
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_BEAMFORMER_IMPL_H */
