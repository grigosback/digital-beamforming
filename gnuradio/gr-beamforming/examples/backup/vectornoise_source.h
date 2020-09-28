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

#ifndef INCLUDED_BEAMFORMING_VECTORNOISE_SOURCE_H
#define INCLUDED_BEAMFORMING_VECTORNOISE_SOURCE_H

#include <beamforming/api.h>
#include <gnuradio/sync_block.h>
#include <cstdint>
#include <vector>

namespace gr
{
  namespace beamforming
  {

    /*!
     * \brief <+description of block+>
     * \ingroup beamforming
     * \details
     */
    template <class T>
    class BEAMFORMING_API vectornoise_source : virtual public gr::sync_block
    {
    public:
      typedef boost::shared_ptr<vectornoise_source> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of      
     * \param type the random distribution to use (see
     *        gnuradio/analog/noise_type.h)
     * \param ampl the standard deviation of a 1-d noise process. If
     *        this is the complex source, this parameter is split
     *        among the real and imaginary parts:
     *        <pre>(ampl/sqrt(2))x + j(ampl/sqrt(2))y</pre>
     * \param seed seed for random generators. Note that for uniform
     *        and Gaussian distributions, this should be a negative
     *        number.
     * \param samples Number of samples to pre-generate
     */
      static sptr make(float ampl, long seed = 0, long samples = 1024 * 16, int vlen);
      virtual T sample() = 0;
      virtual T sample_unbiased() = 0;
      virtual const std::vector<T> &samples() const = 0;

      /*!
     * Set the standard deviation (amplitude) of the 1-d noise
     * process.
     */
      virtual void set_amplitude(float ampl) = 0;
      virtual float amplitude() const = 0;
    };

    typedef vectornoise_source<gr_complex> vectornoise_source_c;

  } // namespace beamforming
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_VECTORNOISE_SOURCE_H */
