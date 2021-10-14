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
import pmt


class doaesprit_py_cf(gr.basic_block):
    """
    docstring for block doaesprit_py_cf
    """

    def __init__(
        self, mx, my, fc, element_separation, n=1, spd=128,
    ):
        gr.basic_block.__init__(
            self, name="doaesprit_py_cf", in_sig=[(np.complex64, mx * my)], out_sig=[],
        )
        c = 299792458  # c_0 [m/s]
        self.mx = mx  # Number of elements in direction x
        self.my = my  # Number of elements in direction y
        self.m = mx * my  # Number of elements in array
        self.fc = fc  # Carrier frequency
        self.k = 2 * np.pi * fc / c  # Wavenumber
        self.d = element_separation  # Separation distance between elements
        self.n = n  # Number of receive signals
        self.spd = spd  # Snapshots per DoA
        # self.file_name = file_name  # File output name
        self.theta = np.pi / 2
        self.phi = 0
        self.u1_x = np.empty(((mx - 1) * my, n), dtype=np.complex64)
        self.u2_x = np.empty(((mx - 1) * my, n), dtype=np.complex64)
        self.u1_y = np.empty(((my - 1) * mx, n), dtype=np.complex64)
        self.u2_y = np.empty(((my - 1) * mx, n), dtype=np.complex64)
        self.message_port_register_in(pmt.intern("signal_number_port"))
        self.message_port_register_out(pmt.intern("doa_port"))
        self.set_msg_handler(
            pmt.intern("signal_number_port"), self.set_signal_number_msg
        )

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        ninput_items_required[0] = self.spd

    def set_signal_number_msg(self, msg):
        if pmt.is_pair(msg):
            key = pmt.car(msg)
            val = pmt.cdr(msg)
            if pmt.eq(key, pmt.string_to_symbol("signal_number_msg")):
                if pmt.is_integer(val):
                    self.n = pmt.to_long(val)
                else:
                    print("DoA Esprit: Not an integer")
            else:
                print("DoA Esprit: Key not 'signal_number_msg'")
        else:
            print("DoA Esprit: Not a tuple")

    def general_work(self, input_items, output_items):
        in0 = input_items[0]

        # Singular value decomposition of matrix "X"
        [u, _, _] = np.linalg.svd(in0.T)
        us = u[:, 0 : self.n]

        # Eigenvalue classification
        #       s = abs(s)
        #       snr_aval = 10 * np.log10((s[0] - s[-1]) / (self.m * s[-1]))
        #       data = np.zeros((self.m, 3))

        #        with open(
        #            "/mnt/d/Users/grigo/Google Drive/Facultad/Balseiro/PI Lucas/git-repository/digital-beamforming/machine_learning/"
        #            + self.file_name,
        #            "a",
        #        ) as fd:
        #            for i in range(self.m):
        #                if i < self.n:
        #                    fd.write(str(s[i]) + ", " + str(snr_aval) + ", 1\n")
        #                else:
        #                    fd.write(str(s[i]) + ", " + str(snr_aval) + ", 0\n")

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

        [_, _, vv_x] = np.linalg.svd(np.append(self.u1_x, self.u2_x, axis=1))
        vv_x = vv_x.T

        vv12_x = vv_x[0 : self.n, self.n : 2 * self.n]
        vv22_x = vv_x[self.n : 2 * self.n, self.n : 2 * self.n]

        # Calculate the engenvalues of Psi
        psi_x = -vv12_x @ np.linalg.inv(vv22_x)
        [phi_x, _] = np.linalg.eig(psi_x)

        [_, _, vv_y] = np.linalg.svd(
            np.append(self.u1_y, self.u2_y, axis=1), full_matrices=False
        )
        vv_y = vv_y.T

        vv12_y = vv_y[0 : self.n, self.n : 2 * self.n]
        vv22_y = vv_y[self.n : 2 * self.n, self.n : 2 * self.n]

        # Calculate the engenvalues of Psi
        psi_y = -vv12_y @ np.linalg.inv(vv22_y)
        [phi_y, _] = np.linalg.eig(psi_y)

        for i in range(self.n):
            arg = (np.angle(phi_x[i]) ** 2 + np.angle(phi_y[i]) ** 2) / (
                (self.k * self.d) ** 2
            )
            # if abs(arg) > 1:
            # print("DoA Esprit: Arg in arccos greater than 1 for i=%.2lf" % i)
            # CAMBIAR ESTO Y HACER QUE IF < 1
            # if i == (self.n - 1):
            #    self.consume(0, self.spd)
            #    return 0
            # else:
            # DOA estimation
            if abs(arg) <= 1:
                self.phi = np.arctan2(np.angle(phi_y[i]), np.angle(phi_x[i]))
                self.theta = np.arccos(np.sqrt(arg))
                doa = pmt.make_f32vector(3, 0.0)
                # print("doa=(", theta, ",", phi, ")")
                pmt.f32vector_set(doa, 0, float(self.theta))
                # print("doa_msg=", doa)
                pmt.f32vector_set(doa, 1, float(self.phi))
                pmt.f32vector_set(doa, 2, float(i))
                doa_msg = pmt.cons(pmt.to_pmt("doa_msg"), doa)
                self.message_port_pub(pmt.intern("doa_port"), doa_msg)
        self.consume(0, self.spd)
        return 0
