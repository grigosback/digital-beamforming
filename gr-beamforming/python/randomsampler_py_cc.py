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
            in_sig=[(numpy.complex64, int(vlen))],
            out_sig=[(numpy.complex64, int(vlen))],
            decim=int(decimation),
        )
        self.vlen = int(vlen)  # Number of elements in array
        self.decimation = int(decimation)  # Decimation factor
        self.set_relative_rate(1.0 / decimation)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        # print("in0 shape=", len(in0), ",", len(in0[0]))
        # print("out shape=", len(out), ",", len(out[0]))

        idx = sample(range(len(in0)), len(out))
        idx.sort()
        print("in0=", in0)
        print("idx=", idx)

        out = in0[idx]
        print("out", out)

        return len(output_items[0])
