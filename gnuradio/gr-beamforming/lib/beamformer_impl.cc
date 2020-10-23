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
#include "beamformer_impl.h"
//#include <iostream>

namespace gr
{
  namespace beamforming
  {

    beamformer::sptr
    beamformer::make(unsigned int mx, unsigned int my, unsigned int idx)
    {
      return gnuradio::get_initial_sptr(new beamformer_impl(mx, my, idx));
    }

    /*
     * The private constructor
     */
    beamformer_impl::beamformer_impl(unsigned int mx, unsigned int my, unsigned int idx)
        : gr::sync_block("beamformer",
                         gr::io_signature::make(1, 1, sizeof(gr_complex) * mx * my),
                         gr::io_signature::make(1, 1, sizeof(gr_complex))),
          d_mx(mx), d_my(my), d_vlen(mx * my), d_idx(idx)
    {
      //std::cout << "Init started\n";
      d_alignment = volk_get_alignment();
      d_aux = (lv_32fc_t *)volk_malloc(sizeof(lv_32fc_t) * d_vlen, d_alignment);
      d_a = (lv_32fc_t *)volk_malloc(sizeof(lv_32fc_t) * d_vlen, d_alignment);
      d_ones = (float *)volk_malloc(sizeof(float) * d_vlen, d_alignment);
      //td::cout << "Init ones\n";
      for (unsigned int i = 0; i < (d_vlen); ++i)
      {
        d_ones[i] = 1.f;
      }
      //std::cout << "Ones initiated\n";
      //      d_c = 299792458;
      //      d_lambda = d_c / d_fc;
      //      d_k = (2 * M_PI) / d_lambda;
      //      d_distance = d_lambda / 2;
      set_doa(M_PI / 2, 0);
      message_port_register_in(pmt::mp("doa_port"));
      set_msg_handler(pmt::mp("doa_port"), [this](pmt::pmt_t msg) { this->set_doa_msg(msg); });
      //std::cout << "Init finished\n";
    }

    void beamformer_impl::set_doa_msg(pmt::pmt_t msg)
    {
      if (pmt::is_pair(msg))
      {
        pmt::pmt_t key = pmt::car(msg);
        pmt::pmt_t val = pmt::cdr(msg);
        if (pmt::eq(key, pmt::string_to_symbol("doa_msg")))
        {
          if (pmt::is_f32vector(val))
          {
            d_doa = pmt::f32vector_elements(val);
            if (d_doa.size() == 3)
            {
              if (int(d_doa[2]) == d_idx)
              {
                set_doa(d_doa[0], d_doa[1]);
                //std::cout << "theta = " << d_doa[0] << ", phi = " << d_doa[1] << "";
              }
            }
            else
            {
              printf("Beamformer: Vector length different than 3");
            }
          }
          else
          {
            printf("Beamformer: Not a f32vector");
          }
        }
        else
        {
          printf("Beamformer: Key not 'doa_msg'");
        }
      }
      else
      {
        printf("Beamformer: Not a tuple\n");
      }
    }

    void beamformer_impl::set_stearing_vector()
    {
      //std::cout << "Updating stearing vector\n";
      for (int i = 0; i < d_mx; i++)
      {
        for (int j = 0; j < d_my; j++)
        {
          d_a_k.real(cos(M_PI * cos(d_theta) * (i * cos(d_phi) + j * sin(d_phi)))); // acá hay que cambiar si se quiere usar para separaciones de elementos distintas a lambda/2
          d_a_k.imag(sin(M_PI * cos(d_theta) * (i * cos(d_phi) + j * sin(d_phi))));
          d_a[i * d_mx + j] = d_a_k;
          //std::cout << "a[" << (i * 4 + j) << "] = " << d_a_k.real() << " + j " << d_a_k.imag() << "\n";
          //printf("a[%d] = %lf + j %lf\n", (i * 4 + j), d_a_k.real(), d_a_k.imag());
        }
      }
      //std::cout << "Stearing vector updated with last element = " << d_a[15] << "\n";
    }

    void beamformer_impl::set_doa(float theta, float phi)
    {
      d_theta = theta;
      d_phi = phi;
      set_stearing_vector();
      //printf("theta = %lf, phi = %lf\n", d_theta, d_phi);
    }

    /*
     * Our virtual destructor.
     */
    beamformer_impl::~beamformer_impl()
    {
    }

    int
    beamformer_impl::work(int noutput_items,
                          gr_vector_const_void_star &input_items,
                          gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *)input_items[0];
      gr_complex *out = (gr_complex *)output_items[0];
      //std::cout << "Entering for\n";
      for (int i = 0; i < noutput_items; i++)
      {
        volk_32fc_x2_multiply_32fc(&d_aux[0], &in[i * d_vlen], &d_a[0], d_vlen);
        volk_32fc_32f_dot_prod_32fc(&out[i], &d_aux[0], &d_ones[0], d_vlen);
        out[i].real(out[i].real() / d_vlen);
        out[i].imag(out[i].imag() / d_vlen);
        //std::cout << "out[i] = " << out[i] << "\n";
      }

      // Do <+signal processing+>

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace beamforming */
} // namespace gr
