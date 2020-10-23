#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Eigenvalues Grabber
# Author: grigosback
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import analog
import beamforming
import random


class eigenvalues_grabber(gr.top_block):
    def __init__(
        self,
        const_1_name="BPSK",
        const_2_name="QPSK",
        element_separation=0,
        file_name="eigenvalues5.csv",
        noise_voltage_1=0,
        noise_voltage_2=0,
        phi_1=70,
        phi_2=41,
        theta_1=45,
        theta_2=75,
    ):
        gr.top_block.__init__(self, "Eigenvalues Grabber")

        ##################################################
        # Parameters
        ##################################################
        self.const_1_name = const_1_name
        self.const_2_name = const_2_name
        self.element_separation = element_separation
        self.file_name = file_name
        self.noise_voltage_1 = noise_voltage_1
        self.noise_voltage_2 = noise_voltage_2
        self.phi_1 = phi_1
        self.phi_2 = phi_2
        self.theta_1 = theta_1
        self.theta_2 = theta_2

        ##################################################
        # Variables
        ##################################################
        if const_1_name == "bpsk":
            self.const_1 = const_1 = digital.constellation_bpsk().base()
        elif const_1_name == "qpsk":
            self.const_1 = const_1 = digital.constellation_qpsk().base()
        elif const_1_name == "dqpsk":
            self.const_1 = const_1 = digital.constellation_dqpsk().base()
        elif const_1_name == "8psk":
            self.const_1 = const_1 = digital.constellation_8psk().base()
        elif const_1_name == "16qam":
            self.const_1 = const_1 = digital.constellation_16qam().base()

        if const_2_name == "bpsk":
            self.const_2 = const_2 = digital.constellation_bpsk().base()
        elif const_2_name == "qpsk":
            self.const_2 = const_2 = digital.constellation_qpsk().base()
        elif const_2_name == "dqpsk":
            self.const_2 = const_2 = digital.constellation_dqpsk().base()
        elif const_2_name == "8psk":
            self.const_2 = const_2 = digital.constellation_8psk().base()
        elif const_2_name == "16qam":
            self.const_2 = const_2 = digital.constellation_16qam().base()

        self.samp_rate = samp_rate = 150000
        self.n = n = 2
        self.my = my = 4
        self.mx = mx = 4
        self.fc = fc = 436e6
        self.bps_2 = bps_2 = const_2.bits_per_symbol()
        self.bps_1 = bps_1 = const_1.bits_per_symbol()

        ##################################################
        # Blocks
        ##################################################
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(
            const_2.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(
            const_1.points(), 1
        )
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_char * 1, samp_rate, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char * 1, samp_rate, True)
        self.blocks_packed_to_unpacked_xx_0_0 = blocks.packed_to_unpacked_bb(
            bps_2, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(
            bps_1, gr.GR_MSB_FIRST
        )
        self.blocks_add_xx_1 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0 = blocks.add_vcc(mx * my)
        self.beamforming_randomsampler_0 = beamforming.randomsampler(mx * my, 8)
        self.beamforming_phasedarray_0_0 = beamforming.phasedarray(
            mx, my, theta_2, phi_2, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0 = beamforming.phasedarray(
            mx, my, theta_1, phi_1, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(
            mx, my, fc, (299792458 / (2 * fc)), n, 128, file_name
        )
        self.analog_vectornoise_source_0_0 = analog.vectornoise_source(
            noise_voltage_2, mx * my
        )
        self.analog_vectornoise_source_0 = analog.vectornoise_source(
            noise_voltage_1, mx * my
        )
        self.analog_random_source_x_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 1000))), False
        )
        self.analog_random_source_x_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 1000))), False
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect(
            (self.analog_random_source_x_0_0, 0), (self.blocks_throttle_0_0, 0)
        )
        self.connect((self.analog_vectornoise_source_0, 0), (self.blocks_add_xx_0, 1))
        self.connect(
            (self.analog_vectornoise_source_0_0, 0), (self.blocks_add_xx_0_0, 1)
        )
        self.connect((self.beamforming_phasedarray_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.beamforming_phasedarray_0_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect(
            (self.beamforming_randomsampler_0, 0),
            (self.beamforming_doaesprit_py_cf_0, 0),
        )
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_add_xx_1, 0), (self.beamforming_randomsampler_0, 0))
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0, 0),
            (self.digital_chunks_to_symbols_xx_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0, 0),
        )
        self.connect(
            (self.blocks_throttle_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0)
        )
        self.connect(
            (self.blocks_throttle_0_0, 0), (self.blocks_packed_to_unpacked_xx_0_0, 0)
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0, 0),
            (self.beamforming_phasedarray_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0, 0),
            (self.beamforming_phasedarray_0_0, 0),
        )

    def get_const_1_name(self):
        return self.const_1_name

    def set_const_1_name(self, const_1_name):
        self.const_1_name = const_1_name

    def get_const_2_name(self):
        return self.const_2_name

    def set_const_2_name(self, const_2_name):
        self.const_2_name = const_2_name

    def get_element_separation(self):
        return self.element_separation

    def set_element_separation(self, element_separation):
        self.element_separation = element_separation
        self.beamforming_phasedarray_0.set_element_error(self.element_separation)
        self.beamforming_phasedarray_0_0.set_element_error(self.element_separation)

    def get_file_name(self):
        return self.file_name

    def set_file_name(self, file_name):
        self.file_name = file_name

    def get_noise_voltage_1(self):
        return self.noise_voltage_1

    def set_noise_voltage_1(self, noise_voltage_1):
        self.noise_voltage_1 = noise_voltage_1
        self.analog_vectornoise_source_0.set_ampl(self.noise_voltage_1)

    def get_noise_voltage_2(self):
        return self.noise_voltage_2

    def set_noise_voltage_2(self, noise_voltage_2):
        self.noise_voltage_2 = noise_voltage_2
        self.analog_vectornoise_source_0_0.set_ampl(self.noise_voltage_2)

    def get_phi_1(self):
        return self.phi_1

    def set_phi_1(self, phi_1):
        self.phi_1 = phi_1
        self.beamforming_phasedarray_0.set_azimuth(self.phi_1)

    def get_phi_2(self):
        return self.phi_2

    def set_phi_2(self, phi_2):
        self.phi_2 = phi_2
        self.beamforming_phasedarray_0_0.set_azimuth(self.phi_2)

    def get_theta_1(self):
        return self.theta_1

    def set_theta_1(self, theta_1):
        self.theta_1 = theta_1
        self.beamforming_phasedarray_0.set_elevation(self.theta_1)

    def get_theta_2(self):
        return self.theta_2

    def set_theta_2(self, theta_2):
        self.theta_2 = theta_2
        self.beamforming_phasedarray_0_0.set_elevation(self.theta_2)

    def get_const_2(self):
        return self.const_2

    def set_const_2(self, const_2):
        self.const_2 = const_2

    def get_const_1(self):
        return self.const_1

    def set_const_1(self, const_1):
        self.const_1 = const_1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n

    def get_my(self):
        return self.my

    def set_my(self, my):
        self.my = my

    def get_mx(self):
        return self.mx

    def set_mx(self, mx):
        self.mx = mx

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc

    def get_bps_2(self):
        return self.bps_2

    def set_bps_2(self, bps_2):
        self.bps_2 = bps_2

    def get_bps_1(self):
        return self.bps_1

    def set_bps_1(self, bps_1):
        self.bps_1 = bps_1


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--const-1-name",
        dest="const_1_name",
        type=str,
        default="BPSK",
        help="Set const_1_name [default=%(default)r]",
    )
    parser.add_argument(
        "--const-2-name",
        dest="const_2_name",
        type=str,
        default="QPSK",
        help="Set const_2_name [default=%(default)r]",
    )
    parser.add_argument(
        "--file-name",
        dest="file_name",
        type=str,
        default="eigenvalues5.csv",
        help="Set file_name [default=%(default)r]",
    )
    parser.add_argument(
        "--phi-1",
        dest="phi_1",
        type=eng_float,
        default="70.0",
        help="Set Azimut Angle 1 [default=%(default)r]",
    )
    parser.add_argument(
        "--phi-2",
        dest="phi_2",
        type=eng_float,
        default="41.0",
        help="Set Azimut Angle 2 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-1",
        dest="theta_1",
        type=eng_float,
        default="45.0",
        help="Set Elevation Angle 1 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-2",
        dest="theta_2",
        type=eng_float,
        default="75.0",
        help="Set Elevation Angle 1 [default=%(default)r]",
    )
    return parser


def main(top_block_cls=eigenvalues_grabber, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(
        const_1_name=options.const_1_name,
        const_2_name=options.const_2_name,
        file_name=options.file_name,
        phi_1=options.phi_1,
        phi_2=options.phi_2,
        theta_1=options.theta_1,
        theta_2=options.theta_2,
    )

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        input("Press Enter to quit: ")
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == "__main__":
    element_separation_min = 0
    element_separation_max = 5
    noise_voltage_min = 0.001
    noise_voltage_max = 2
    phi_min = -180
    phi_max = 180
    theta_min = 0
    theta_max = 90
    file_name = "eigenvalues6.csv"
    const = numpy.array(["bpsk", "qpsk", "dqpsk", "8psk"])
    for i in range(1000):
        element_separation = random.uniform(
            element_separation_min, element_separation_max
        )
        noise_voltage_1 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_2 = random.uniform(noise_voltage_min, noise_voltage_max)
        phi_1 = random.uniform(phi_min, phi_max)
        phi_2 = random.uniform(phi_min, phi_max)
        theta_1 = random.uniform(theta_min, theta_max)
        theta_2 = random.uniform(theta_min, theta_max)
        const_1 = numpy.random.choice(const)
        const_2 = numpy.random.choice(const)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Iteration " + str(i) + ":")
        print("const_1 = " + const_1)
        print("const_2 = " + const_2)
        print("element_separation = %2lf" % element_separation)
        print("noise_voltage_1 = %.2lf" % noise_voltage_1)
        print("noise_voltage_2 = %.2lf" % noise_voltage_2)
        print("phi_1 = %.2lf" % phi_1)
        print("phi_2 = %.2lf" % phi_2)
        print("theta_1 = %.2lf" % theta_1)
        print("theta_2 = %.2lf" % theta_2)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        fg = eigenvalues_grabber(
            const_1,
            const_2,
            element_separation,
            file_name,
            noise_voltage_1,
            noise_voltage_2,
            phi_1,
            phi_2,
            theta_1,
            theta_2,
        )

        fg.run()
