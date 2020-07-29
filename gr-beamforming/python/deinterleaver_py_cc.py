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


class deinterleaver_py_cc(gr.sync_block):
    """
    docstring for block deinterleaver_py_cc
    """

    def __init__(self, sequence):
        gr.sync_block.__init__(
            self,
            name="deinterleaver_py_cc",
            in_sig=[(numpy.complex64, len(sequence))],
            out_sig=[(numpy.complex64, len(sequence))],
        )
        self.sequence = sequence
        self.size = len(sequence)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        for i, j in enumerate(self.sequence):
            out[:, j] = in0[:, i]
        print("out=", out)

        return len(output_items[0])
