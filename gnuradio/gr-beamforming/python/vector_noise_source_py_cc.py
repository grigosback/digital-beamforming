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


import numpy as np
from gnuradio import gr


class vector_noise_source_py_cc(gr.sync_block):
    """
    docstring for block vector_noise_source_py_cc
    """

    def __init__(self, noise_voltage, noise_seed, vlen):
        gr.sync_block.__init__(
            self,
            name="vector_noise_source_py_cc",
            in_sig=None,
            out_sig=[(np.complex64, vlen)],
        )
        self.noise_voltage = noise_voltage
        self.noise_seed = noise_seed
        self.vlen = vlen
        self.sigma = np.sqrt(noise_voltage / 2)
        np.random.seed(seed=noise_seed)

    def gaussiannoise(self, sigma, vlen):
        w = np.random.normal(0, sigma, vlen) + 1j * np.random.normal(0, sigma, vlen)
        return w

    def work(self, input_items, output_items):
        out = output_items[0]
        n = len(out)
        for i in range(n):
            out[i] = self.gaussiannoise(self.sigma, self.vlen)
            # print("out[", i, "]=", out[i])
        return len(output_items[0])

