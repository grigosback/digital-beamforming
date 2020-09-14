#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BER Curve Generator
# Author: grigosback
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import beamforming

class bercurve_generator(gr.top_block):

    def __init__(self, fc=436e6, mx=4, my=4, n=1, noise=0, phi=50, theta=45):
        gr.top_block.__init__(self, "BER Curve Generator")

        ##################################################
        # Parameters
        ##################################################
        self.fc = fc
        self.mx = mx
        self.my = my
        self.n = n
        self.noise = noise
        self.phi = phi
        self.theta = theta

        ##################################################
        # Variables
        ##################################################
        self.const = const = digital.constellation_bpsk().base()
        self.samp_rate = samp_rate = 32000
        self.packet_len = packet_len = 1
        self.bps = bps = const.bits_per_symbol()

        ##################################################
        # Blocks
        ##################################################
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const.base())
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(const.points(), 1)
        self.blocks_vector_sink_x_0_1 = blocks.vector_sink_f(1, 128)
        self.blocks_vector_sink_x_0_0 = blocks.vector_sink_b(1, 128)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_b(1, 128)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(bps, gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bps, gr.GR_MSB_FIRST)
        self.beamforming_randomsampler_py_cc_0_0 = beamforming.randomsampler_py_cc(mx*my,8)
        self.beamforming_phasedarray_py_cc_0 = beamforming.phasedarray_py_cc(mx, my, theta, phi, fc, noise)
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(128, mx, my, fc, n)
        self.beamforming_beamformer_py_cc_0 = beamforming.beamformer_py_cc(mx, my, fc, 0, 0, 8*128)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, const.arity(), int(1e2)))), False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_vector_sink_x_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.beamforming_beamformer_py_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.beamforming_doaesprit_py_cf_0, 1), (self.beamforming_beamformer_py_cc_0, 2))
        self.connect((self.beamforming_doaesprit_py_cf_0, 0), (self.beamforming_beamformer_py_cc_0, 1))
        self.connect((self.beamforming_phasedarray_py_cc_0, 0), (self.beamforming_beamformer_py_cc_0, 0))
        self.connect((self.beamforming_phasedarray_py_cc_0, 0), (self.beamforming_randomsampler_py_cc_0_0, 0))
        self.connect((self.beamforming_randomsampler_py_cc_0_0, 0), (self.beamforming_doaesprit_py_cf_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.beamforming_phasedarray_py_cc_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.blocks_vector_sink_x_0_1, 0))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc

    def get_mx(self):
        return self.mx

    def set_mx(self, mx):
        self.mx = mx

    def get_my(self):
        return self.my

    def set_my(self, my):
        self.my = my

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.beamforming_phasedarray_py_cc_0.set_noise(self.noise)

    def get_phi(self):
        return self.phi

    def set_phi(self, phi):
        self.phi = phi
        self.beamforming_phasedarray_py_cc_0.set_azimut(self.phi)

    def get_theta(self):
        return self.theta

    def set_theta(self, theta):
        self.theta = theta
        self.beamforming_phasedarray_py_cc_0.set_elevation(self.theta)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--fc", dest="fc", type=eng_float, default="436.0M",
        help="Set Carrier frequency [default=%(default)r]")
    parser.add_argument(
        "--mx", dest="mx", type=intx, default=4,
        help="Set # elements in x [default=%(default)r]")
    parser.add_argument(
        "--my", dest="my", type=intx, default=4,
        help="Set # elements in y [default=%(default)r]")
    parser.add_argument(
        "--n", dest="n", type=intx, default=1,
        help="Set # impinging signals [default=%(default)r]")
    return parser


def main(top_block_cls=bercurve_generator, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(fc=options.fc, mx=options.mx, my=options.my, n=options.n)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
