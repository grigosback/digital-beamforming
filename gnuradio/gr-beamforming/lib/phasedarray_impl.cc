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
#include "phasedarray_impl.h"

namespace gr
{
  namespace beamforming
  {

    phasedarray::sptr
    phasedarray::make(unsigned int mx, unsigned int my, float theta, float phi, float fc, float element_separation, float element_error)
    {
      return gnuradio::get_initial_sptr(new phasedarray_impl(mx, my, theta, phi, fc, element_separation, element_error));
    }

    /*
     * The private constructor
     */
    phasedarray_impl::phasedarray_impl(unsigned int mx, unsigned int my, float theta, float phi, float fc, float element_separation, float element_error)
        : gr::sync_block("phasedarray",
                         gr::io_signature::make(1, 1, sizeof(gr_complex)),
                         gr::io_signature::make(1, 1, sizeof(gr_complex) * mx * my)),
          d_mx(mx), d_my(my), d_vlen(mx * my), d_theta(deg2radians(theta)), d_phi(deg2radians(phi)), d_fc(fc), d_element_separation(element_separation), d_element_error(element_error / 100)
    {
      if (d_element_error >= 1)
      {
        d_element_error = 1;
      }
      else if (d_element_error <= 0)
      {
        d_element_error = 0;
      }
      d_c = 299792458;
      d_k = (2 * M_PI * fc) / d_c;
      d_alignment = volk_get_alignment();
      d_a = (lv_32fc_t *)volk_malloc(sizeof(lv_32fc_t) * d_vlen, d_alignment);
      set_stearing_vector();
    }

    /*
     * Our virtual destructor.
     */
    phasedarray_impl::~phasedarray_impl()
    {
    }

    float phasedarray_impl::deg2radians(float angle)
    {
      return ((angle * M_PI) / 180);
    }

    void phasedarray_impl::set_stearing_vector()
    {
      //std::cout << "Updating stearing vector\n";
      for (int i = 0; i < d_mx; i++)
      {
        for (int j = 0; j < d_my; j++)
        {
          d_random_phase_x = d_element_error * d_rng.gasdev();
          d_random_phase_y = d_element_error * d_rng.gasdev();
          d_a_k.real(cos(-1.f * d_k * cos(d_theta) * (d_element_separation * (i * cos(d_phi) + j * sin(d_phi)) + d_random_phase_x * (cos(d_phi) + sin(d_phi)))));
          d_a_k.imag(sin(-1.f * d_k * cos(d_theta) * (d_element_separation * (i * cos(d_phi) + j * sin(d_phi)) + d_random_phase_y * (cos(d_phi) + sin(d_phi)))));
          d_a[i * d_mx + j] = d_a_k;
          //std::cout << "d_random_phase_x[" << (i * d_mx + j) << "] = " << d_random_phase_x << "\n";
          //std::cout << "d_random_phase_y[" << (i * d_mx + j) << "] = " << d_random_phase_y << "\n";
          //std::cout << "a[" << (i * 4 + j) << "] = " << d_a_k.real() << " + j " << d_a_k.imag() << "\n";
          //printf("a[%d] = %lf + j %lf\n", (i * 4 + j), d_a_k.real(), d_a_k.imag());
        }
      }
      //std::cout << "Stearing vector updated with last element = " << d_a[15] << "\n";
    }

    void phasedarray_impl::set_elevation(float theta)
    {
      d_theta = deg2radians(theta);
      set_stearing_vector();
    }
    void phasedarray_impl::set_azimuth(float phi)
    {
      d_phi = deg2radians(phi);
      set_stearing_vector();
    }
    void phasedarray_impl::set_element_error(float element_error)
    {
      d_element_error = element_error / 100;
      if (d_element_error >= 1)
      {
        d_element_error = 1;
      }
      else if (d_element_error <= 0)
      {
        d_element_error = 0;
      }
      //std::cout << "element error = " << d_element_error << "\n";
      set_stearing_vector();
    }

    int
    phasedarray_impl::work(int noutput_items,
                           gr_vector_const_void_star &input_items,
                           gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *)input_items[0];
      gr_complex *out = (gr_complex *)output_items[0];

      for (int i = 0; i < noutput_items; i++)
      {
        volk_32fc_s32fc_multiply_32fc(&out[i * d_vlen], &d_a[0], lv_cmake(in[i].real(), in[i].imag()), d_vlen);
      }
      //printf("a[0] = %lf + j%lf\n", d_a[0].real(), d_a[0].imag());
      // Tell runtime system how many output items we produced.
      return noutput_items;
    }
  } /* namespace beamforming */
} /* namespace gr */
