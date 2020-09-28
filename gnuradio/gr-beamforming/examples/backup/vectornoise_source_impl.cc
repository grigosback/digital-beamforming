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
#include "vectornoise_source_impl.h"
#include <gnuradio/io_signature.h>
#include <gnuradio/xoroshiro128p.h>
#include <stdexcept>
#include <vector>

namespace gr
{
  namespace beamforming
  {
    template <class T>
    typename vectornoise_source::sptr
    vectornoise_source<T>::make(float ampl, long seed, long samples, int vlen)
    {
      return gnuradio::make_block_sptr<vectornoise_source_impl<T>>(ampl, seed, samples, vlen);
    }

    void vectornoise_source_impl<gr_complex>::generate()
    {
      int noutput_items = d_samples.size();
      for (int i = 0; i < noutput_items; i++)
        d_samples[i] = d_ampl * d_rng.rayleigh_complex();
    }
  } // namespace beamforming

  template <class T>
  vectornoise_source_impl::vectornoise_source_impl(float ampl, long seed, long samples, int vlen)
      : gr::sync_block("vectornoise_source",
                       gr::io_signature::make(0, 0, 0),
                       gr::io_signature::make(1, 1, sizeof(gr_complex) * vlen)),
        d_ampl(ampl), d_rng(seed), d_vlen(vlen)
  {
    d_samples.resize(samples);
    xoroshiro128p_seed(d_state, (uint64_t)seed);
    generate();
  }

  template <>
  vectornoise_source_impl<gr_complex>::vectornoise_source_impl(
      float ampl,
      long seed,
      long samples, int vlen)
      : sync_block("vectornoise_source",
                   io_signature::make(0, 0, 0),
                   io_signature::make(1, 1, sizeof(gr_complex) * vlen)),
        d_ampl(ampl / sqrtf(2.0f)),
        d_rng(seed), d_vlen(vlen)
  {
    d_samples.resize(samples);
    xoroshiro128p_seed(d_state, (uint64_t)seed);
    generate();
  }

  template <class T>
  vectornoise_source_impl::~vectornoise_source_impl()
  {
  }

  template <class T>
  void vectornoise_source_impl<T>::set_amplitude(float ampl)
  {
    gr::thread::scoped_lock l(this->d_setlock);
    d_ampl = ampl;
    generate();
  }

  template <>
  void vectornoise_source_impl<gr_complex>::set_amplitude(float ampl)
  {
    gr::thread::scoped_lock l(this->d_setlock);
    d_ampl = ampl / sqrtf(2.0f);
    generate();
  }

  template <class T>
  void fastnoise_source_impl<T>::generate()
  {
    int noutput_items = d_samples.size();

    for (int i = 0; i < noutput_items; i++)
      d_samples[i] = (T)(d_ampl * d_rng.gasdev());
  }

  int vectornoise_source_impl::work(int noutput_items,
                                    gr_vector_const_void_star &input_items,
                                    gr_vector_void_star &output_items)
  {
    gr_complex *out = (gr_complex *)output_items[0];

    // Do <+signal processing+>

    // Tell runtime system how many output items we produced.
    return noutput_items;
  }
  template class fastnoise_source<gr_complex>;
} // namespace gr
} /* namespace gr */
