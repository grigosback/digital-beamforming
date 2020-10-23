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


class doaesprit_py_cf(gr.decim_block):
    """
    docstring for block doaesprit_py_cf
    """

    def __init__(self, decimation, mx, my, fc, n=1):
        gr.decim_block.__init__(
            self,
            name="doaesprit_py_cf",
            in_sig=[(np.complex64, mx * my)],
            out_sig=[np.float32, np.float32],
            decim=decimation,
        )
        c = 299792458  # c_0 [m/s]
        self.decimation = decimation  # Decimation factor
        self.set_relative_rate(1.0 / decimation)  # Set output rate
        self.mx = mx  # Number of elements in direction x
        self.my = my  # Number of elements in direction y
        self.m = mx * my  # Number of elements in array
        self.fc = fc  # Carrier frequency
        self.lambdac = c / fc  # Carrier wavelength
        self.k = 2 * np.pi / self.lambdac  # Wavenumber
        self.d = self.lambdac / 2  # Separation distance between elements
        self.n = n  # Number of receive signals
        self.u1_x = np.zeros(((mx - 1) * my, n), dtype=np.complex64)
        self.u2_x = np.zeros(((mx - 1) * my, n), dtype=np.complex64)
        self.u1_y = np.zeros(((my - 1) * mx, n), dtype=np.complex64)
        self.u2_y = np.zeros(((my - 1) * mx, n), dtype=np.complex64)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]
        print(in0.shape)
        # Singular value decomposition of matrix "X"
        [u, s, v] = np.linalg.svd(in0.T)
        us = u[:, 0 : self.n]

        for i in range(self.n):
            us_aux = us[:, i].reshape(self.mx, self.my)
            self.u1_x[:, i] = us_aux[0 : self.mx - 1, :].reshape(
                (self.mx - 1) * self.my
            )
            self.u2_x[:, i] = us_aux[1 : self.mx, :].reshape((self.mx - 1) * self.my)
            self.u1_y[:, i] = us_aux[:, 0 : self.my - 1].reshape(
                (self.my - 1) * self.mx
            )
            self.u2_y[:, i] = us_aux[:, 1 : self.my].reshape((self.my - 1) * self.mx)

        [uu_x, ss_x, vv_x] = np.linalg.svd(
            np.append(self.u1_x, self.u2_x, axis=1), full_matrices=False
        )
        vv_x = vv_x.T

        vv12_x = vv_x[0 : self.n, self.n : 2 * self.n]
        vv22_x = vv_x[self.n : 2 * self.n, self.n : 2 * self.n]

        # Calculate the engenvalues of Psi
        psi_x = -vv12_x @ np.linalg.inv(vv22_x)
        [phi_x, psi_avec] = np.linalg.eig(psi_x)

        [uu_y, ss_y, vv_y] = np.linalg.svd(
            np.append(self.u1_y, self.u2_y, axis=1), full_matrices=False
        )
        vv_y = vv_y.T

        vv12_y = vv_y[0 : self.n, self.n : 2 * self.n]
        vv22_y = vv_y[self.n : 2 * self.n, self.n : 2 * self.n]

        # Calculate the engenvalues of Psi
        psi_y = -vv12_y @ np.linalg.inv(vv22_y)
        [phi_y, psi_avec] = np.linalg.eig(psi_y)

        # DOA estimation
        phi = np.degrees(np.arctan2(np.angle(phi_y), np.angle(phi_x)))

        theta = np.degrees(
            np.arccos(
                np.sqrt(
                    (np.angle(phi_x) ** 2 + np.angle(phi_y) ** 2)
                    / ((self.k * self.d) ** 2)
                )
            )
        )
        # print("theta=", theta)
        # print("phi=", phi)
        # print("out.shape=", out0.shape)
        out0[:] = theta
        out1[:] = phi
        return len(output_items[0])
