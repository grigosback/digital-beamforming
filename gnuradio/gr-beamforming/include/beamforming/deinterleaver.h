/* -*- c++ -*- */
/*
 * Copyright 2020 gr-taller author.
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

#ifndef INCLUDED_TALLER_DEINTERLEAVER_H
#define INCLUDED_TALLER_DEINTERLEAVER_H

#include <taller/api.h>
#include <gnuradio/sync_block.h>

namespace gr
{
  namespace taller
  {

    /*!
     * \brief This block receives a vector of integers that refers to the order of the interleaving sequence and a vector of complex samples and de-interleaves them.
     * \ingroup taller
     *
     */
    class TALLER_API deinterleaver : virtual public gr::sync_block
    {
    public:
      typedef boost::shared_ptr<deinterleaver> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of taller::deinterleaver.
       *
       * To avoid accidental use of raw pointers, taller::deinterleaver's
       * constructor is in a private implementation
       * class. taller::deinterleaver::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::vector<int> &sequence);
    };

  } // namespace taller
} // namespace gr

#endif /* INCLUDED_TALLER_DEINTERLEAVER_H */
