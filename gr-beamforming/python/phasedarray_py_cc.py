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


class phasedarray_py_cc(gr.sync_block):
    """
    
    """

    def __init__(self, mx, my, theta, phi, fc):
        gr.sync_block.__init__(
            self,
            name="phasedarray_py_cc",
            in_sig=[np.complex64],
            out_sig=[(np.complex64, mx * my)],
        )
        c = 299792458  # c_0 [m/s]
        self.mx = mx  # Number of elements in direction x
        self.my = my  # Number of elements in direction y
        self.m = mx * my  # Number of elements in array
        self.theta = np.radians(theta)  # Elevation angle
        self.phi = np.radians(phi)  # Azimut angle
        self.fc = fc  # Carrier frequency
        self.lambdac = c / fc  # Carrier wavelength
        self.k = 2 * np.pi / self.lambdac  # Wavenumber
        self.d = self.lambdac / 2  # Separation distance between elements

        self.a = np.empty((self.m, 1), dtype=np.complex64)

        self.beta = np.empty((self.mx, 1), dtype=np.complex64)
        self.gamma = np.empty((self.my, 1), dtype=np.complex64)

        beta_k = np.e ** (1j * self.k * self.d * np.cos(self.theta) * np.cos(self.phi))
        gamma_k = np.e ** (1j * self.k * self.d * np.cos(self.theta) * np.sin(self.phi))
        for i in range(self.mx):
            self.beta[i] = beta_k ** (-i)

        for i in range(self.my):
            self.gamma[i] = gamma_k ** (-i)

        self.a = np.kron(self.beta, self.gamma).ravel()

    def set_elevation(self, theta):
        self.theta = np.radians(theta)  # Elevation angle

        self.beta = np.empty((self.mx, 1), dtype=np.complex64)
        self.gamma = np.empty((self.my, 1), dtype=np.complex64)

        beta_k = np.e ** (1j * self.k * self.d * np.cos(self.theta) * np.cos(self.phi))
        gamma_k = np.e ** (1j * self.k * self.d * np.cos(self.theta) * np.sin(self.phi))
        for i in range(self.mx):
            self.beta[i] = beta_k ** (-i)

        for i in range(self.my):
            self.gamma[i] = gamma_k ** (-i)

        self.a = np.kron(self.beta, self.gamma).ravel()

    def set_azimut(self, phi):
        self.phi = np.radians(phi)  # Azimut angle

        self.beta = np.empty((self.mx, 1), dtype=np.complex64)
        self.gamma = np.empty((self.my, 1), dtype=np.complex64)

        beta_k = np.e ** (1j * self.k * self.d * np.cos(self.theta) * np.cos(self.phi))
        gamma_k = np.e ** (1j * self.k * self.d * np.cos(self.theta) * np.sin(self.phi))
        for i in range(self.mx):
            self.beta[i] = beta_k ** (-i)

        for i in range(self.my):
            self.gamma[i] = gamma_k ** (-i)

        self.a = np.kron(self.beta, self.gamma).ravel()

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        n = in0.shape[0]  # Number of input samples

        for i in range(n):
            out[i] = self.a * in0[i]
            # print("out[", i, "]=", out[i])

        return len(output_items[0])

