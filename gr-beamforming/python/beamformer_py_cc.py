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


class beamformer_py_cc(gr.basic_block):
    """
    docstring for block beamformer_py_cc
    """

    def __init__(self, mx, my, fc, theta_start, phi_start, inputs_per_angle):
        gr.basic_block.__init__(
            self,
            name="beamformer_py_cc",
            in_sig=[(np.complex64, mx * my), np.float32, np.float32],
            out_sig=[np.complex64],
        )
        c = 299792458  # c_0 [m/s]
        self.mx = mx  # Number of elements in direction x
        self.my = my  # Number of elements in direction y
        self.m = mx * my  # Number of elements in array
        self.fc = fc  # Carrier frequency
        self.inputs_per_angle = (
            inputs_per_angle  # Number of inputs required to make a DoA estimation
        )
        self.lambdac = c / fc  # Carrier wavelength
        self.k = 2 * np.pi / self.lambdac  # Wavenumber
        self.d = self.lambdac / 2  # Separation distance between elements
        self.beta = np.empty((self.mx, 1), dtype=np.complex64)
        self.gamma = np.empty((self.my, 1), dtype=np.complex64)
        self.theta_start = np.radians(theta_start)
        self.phi_start = np.radians(phi_start)

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        ninput_items_required[0] = noutput_items
        ninput_items_required[1] = int(noutput_items / self.inputs_per_angle)
        ninput_items_required[2] = int(noutput_items / self.inputs_per_angle)

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        if input_items[1] != 0:
            theta = np.radians(input_items[1])
            self.theta_start = theta
        else:
            theta = self.theta_start
        if input_items[2] != 0:
            phi = np.radians(input_items[2])
            self.phi_start = phi
        else:
            phi = self.phi_start
        out = output_items[0]
        n = out.size

        # print("n=", n)
        # print("in0.shape=", in0.shape)
        # print("out.shape=", out.shape)
        # print("phi=", phi)
        # print("theta=", theta)

        for i in range(n):
            beta_k = np.e ** (1j * self.k * self.d * np.cos(theta) * np.cos(phi))
            gamma_k = np.e ** (1j * self.k * self.d * np.cos(theta) * np.sin(phi))

            for j in range(self.mx):
                self.beta[j] = beta_k ** (-j)

            for j in range(self.my):
                self.gamma[j] = gamma_k ** (-j)

            a = np.kron(self.beta, self.gamma).ravel()

            x_n = in0[i] * a.conj()
            out[i] = np.average(x_n)

        self.consume(0, n)  # Consume port 0 input
        self.consume(1, len(input_items[1]))  # Consume port 1 input
        self.consume(2, len(input_items[2]))  # Consume port 2 input
        return len(output_items[0])
