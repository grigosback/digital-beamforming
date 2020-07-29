#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 gr-beamforming author.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy
from gnuradio import gr
from random import sample


class randomsampler_py_cc(gr.decim_block):
    """
    This block receives N vector of complex numbers and outputs N/Decimation
    vector of complexs by random choice.
    """

    def __init__(self, vlen, decimation):
        gr.decim_block.__init__(
            self,
            name="randomsampler_py_cc",
            in_sig=[(numpy.complex64, vlen)],
            out_sig=[(numpy.complex64, vlen)],
            decim=decimation,
        )
        self.vlen = vlen  # Number of elements in input vectors.
        self.decimation = decimation  # Decimation factor
        self.set_relative_rate(1.0 / decimation)  # Set output rate

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        idx = sample(range(in0.shape[0]), out.shape[0])  # Generates random indexes
        idx.sort()  # Sorts indexes from least to greatest
        # print("in0=", in0)
        # print("idx=", idx)

        out[:] = in0[idx]
        # print("out=", out)

        return len(output_items[0])
