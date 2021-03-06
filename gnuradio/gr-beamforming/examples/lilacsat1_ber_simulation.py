#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BER Simulation
# GNU Radio version: 3.8.1.0

import os
import sys

sys.path.append(os.environ.get("GRC_HIER_PATH", os.path.expanduser("~/.grc_gnuradio")))

from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from lilacsat1_ber_bpsk import lilacsat1_ber_bpsk  # grc-generated hier_block
from scipy.special import erfc
import analog
import beamforming
import math
import numpy
import pylab
import matplotlib.pyplot as plt


class lilacsat1_ber_simulation(gr.top_block):
    def __init__(
        self,
        EbN0=0,
        element_error=0,
        esprit_decimation=128,
        fc=436e6,
        mx=4,
        my=4,
        n=1,
        phi=50,
        rs_decimation=8,
        theta=30,
    ):
        gr.top_block.__init__(self, "BER Simulation")

        ##################################################
        # Parameters
        ##################################################
        self.EbN0 = EbN0
        self.element_error = element_error
        self.esprit_decimation = esprit_decimation
        self.fc = fc
        self.mx = mx
        self.my = my
        self.n = n
        self.phi = phi
        self.rs_decimation = rs_decimation
        self.theta = theta

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 5
        self.N_BITS = N_BITS = 1e5
        self.samp_rate = samp_rate = 32000
        self.noise_voltage = noise_voltage = 1.0 / math.sqrt(
            1 / float(sps) * 10 ** (float(EbN0) / 10)
        )
        self.intdump_decim = intdump_decim = min(int(N_BITS / 10), 100000)
        self.const = const = digital.constellation_bpsk().base()
        self.alpha = alpha = 0.35
        self.SKIP = SKIP = 1000
        self.RAND_SEED = RAND_SEED = 42

        ##################################################
        # Blocks
        ##################################################
        self.lilacsat1_ber_bpsk_0 = lilacsat1_ber_bpsk(
            bfo=12000,
            callsign="",
            ip="::",
            latitude=0,
            longitude=0,
            port=7355,
            recstart="",
        )
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(
            1, (0, 0, (1 + 1j) / numpy.sqrt(2),)
        )
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x0, 16)
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(2)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0x00, 16)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=const,
            differential=False,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=alpha,
            verbose=False,
            log=False,
        )
        self.blocks_vector_source_x_0 = blocks.vector_source_b([1], True, 1, [])
        self.blocks_vector_sink_x_0 = blocks.vector_sink_f(1, 1024)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_char * 1, SKIP)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_not_xx_0 = blocks.not_bb()
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(0.1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1.0 / intdump_decim)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(intdump_decim, 1)
        self.blocks_head_0 = blocks.head(gr.sizeof_char * 1, int(N_BITS))
        self.blocks_and_const_xx_0 = blocks.and_const_bb(1)
        self.blocks_add_xx_0 = blocks.add_vcc(mx * my)
        self.beamforming_randomsampler_0 = beamforming.randomsampler(
            mx * my, rs_decimation
        )
        self.beamforming_phasedarray_0 = beamforming.phasedarray(
            mx, my, theta, phi, fc, (299792458 / (2 * fc)), element_error
        )
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(
            mx, my, fc, (299792458 / (2 * fc)), n, 128
        )
        self.beamforming_beamformer_0 = beamforming.beamformer(mx, my)
        self.analog_vectornoise_source_0 = analog.vectornoise_source(
            noise_voltage, mx * my
        )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect(
            (self.beamforming_doaesprit_py_cf_0, "doa_port"),
            (self.beamforming_beamformer_0, "doa_port"),
        )
        self.connect((self.analog_vectornoise_source_0, 0), (self.blocks_add_xx_0, 1))
        self.connect(
            (self.beamforming_beamformer_0, 0), (self.blocks_multiply_const_vxx_1, 0)
        )
        self.connect((self.beamforming_phasedarray_0, 0), (self.blocks_add_xx_0, 0))
        self.connect(
            (self.beamforming_randomsampler_0, 0),
            (self.beamforming_doaesprit_py_cf_0, 0),
        )
        self.connect((self.blocks_add_xx_0, 0), (self.beamforming_beamformer_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.beamforming_randomsampler_0, 0))
        self.connect((self.blocks_and_const_xx_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_head_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect(
            (self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0)
        )
        self.connect(
            (self.blocks_multiply_const_vxx_0, 0), (self.blocks_vector_sink_x_0, 0)
        )
        self.connect(
            (self.blocks_multiply_const_vxx_1, 0), (self.lilacsat1_ber_bpsk_0, 0)
        )
        self.connect((self.blocks_not_xx_0, 0), (self.blocks_and_const_xx_0, 0))
        self.connect(
            (self.blocks_pack_k_bits_bb_0, 0),
            (self.digital_constellation_modulator_0, 0),
        )
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_not_xx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_head_0, 0))
        self.connect(
            (self.digital_constellation_modulator_0, 0), (self.fir_filter_xxx_0, 0)
        )
        self.connect((self.digital_descrambler_bb_0, 0), (self.blocks_skiphead_0, 0))
        self.connect(
            (self.digital_diff_decoder_bb_0, 0), (self.digital_descrambler_bb_0, 0)
        )
        self.connect(
            (self.digital_diff_encoder_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0)
        )
        self.connect(
            (self.digital_scrambler_bb_0, 0), (self.digital_diff_encoder_bb_0, 0)
        )
        self.connect((self.fir_filter_xxx_0, 0), (self.beamforming_phasedarray_0, 0))
        self.connect(
            (self.lilacsat1_ber_bpsk_0, 0), (self.digital_diff_decoder_bb_0, 0)
        )

    def get_EbN0(self):
        return self.EbN0

    def set_EbN0(self, EbN0):
        self.EbN0 = EbN0
        self.set_noise_voltage(
            1.0 / math.sqrt(1 / float(self.sps) * 10 ** (float(self.EbN0) / 10))
        )

    def get_element_error(self):
        return self.element_error

    def set_element_error(self, element_error):
        self.element_error = element_error
        self.beamforming_phasedarray_0.set_element_error(self.element_error)

    def get_esprit_decimation(self):
        return self.esprit_decimation

    def set_esprit_decimation(self, esprit_decimation):
        self.esprit_decimation = esprit_decimation

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

    def get_phi(self):
        return self.phi

    def set_phi(self, phi):
        self.phi = phi
        self.beamforming_phasedarray_0.set_azimuth(self.phi)

    def get_rs_decimation(self):
        return self.rs_decimation

    def set_rs_decimation(self, rs_decimation):
        self.rs_decimation = rs_decimation

    def get_theta(self):
        return self.theta

    def set_theta(self, theta):
        self.theta = theta
        self.beamforming_phasedarray_0.set_elevation(self.theta)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_noise_voltage(
            1.0 / math.sqrt(1 / float(self.sps) * 10 ** (float(self.EbN0) / 10))
        )

    def get_N_BITS(self):
        return self.N_BITS

    def set_N_BITS(self, N_BITS):
        self.N_BITS = N_BITS
        self.set_intdump_decim(min(int(self.N_BITS / 10), 100000))
        self.blocks_head_0.set_length(int(self.N_BITS))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.analog_vectornoise_source_0.set_ampl(self.noise_voltage)

    def get_intdump_decim(self):
        return self.intdump_decim

    def set_intdump_decim(self, intdump_decim):
        self.intdump_decim = intdump_decim
        self.blocks_multiply_const_vxx_0.set_k(1.0 / self.intdump_decim)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_SKIP(self):
        return self.SKIP

    def set_SKIP(self, SKIP):
        self.SKIP = SKIP

    def get_RAND_SEED(self):
        return self.RAND_SEED

    def set_RAND_SEED(self, RAND_SEED):
        self.RAND_SEED = RAND_SEED


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--esprit-decimation",
        dest="esprit_decimation",
        type=intx,
        default=128,
        help="Set ESPRIT decimation factor [default=%(default)r]",
    )
    parser.add_argument(
        "--fc",
        dest="fc",
        type=eng_float,
        default="436.0M",
        help="Set Carrier frequency [default=%(default)r]",
    )
    parser.add_argument(
        "--mx",
        dest="mx",
        type=intx,
        default=4,
        help="Set # elements in x [default=%(default)r]",
    )
    parser.add_argument(
        "--my",
        dest="my",
        type=intx,
        default=4,
        help="Set # elements in y [default=%(default)r]",
    )
    parser.add_argument(
        "--n",
        dest="n",
        type=intx,
        default=1,
        help="Set # impinging signals [default=%(default)r]",
    )
    parser.add_argument(
        "--phi",
        dest="phi",
        type=eng_float,
        default="50.0",
        help="Set Azimut angle [default=%(default)r]",
    )
    parser.add_argument(
        "--rs-decimation",
        dest="rs_decimation",
        type=intx,
        default=8,
        help="Set Random sampler decimation factor [default=%(default)r]",
    )
    parser.add_argument(
        "--theta",
        dest="theta",
        type=eng_float,
        default="30.0",
        help="Set Elevation angle [default=%(default)r]",
    )
    return parser


def main(top_block_cls=lilacsat1_ber_simulation, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(
        esprit_decimation=options.esprit_decimation,
        fc=options.fc,
        mx=options.mx,
        my=options.my,
        n=options.n,
        phi=options.phi,
        rs_decimation=options.rs_decimation,
        theta=options.theta,
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


def berawgn(EbN0):
    """ Calculates theoretical bit error rate in AWGN (for BPSK and given Eb/N0) """
    return 0.5 * erfc(math.sqrt(10 ** (float(EbN0) / 10)))


def simulate_ber(EbN0, element_error):
    """ All the work's done here: create flow graph, run, read out BER """
    print("Eb/N0 = %d dB" % EbN0)
    print("element error = ", element_error, "%")
    fg = lilacsat1_ber_simulation(EbN0, element_error)
    fg.run()
    data = fg.blocks_vector_sink_x_0.data()
    print("noise=", fg.noise_voltage)
    print(data)
    factor = 6.0  # each bit error produces 6 errors, taking into account differential coding and scrambler
    return numpy.sum(data) / (factor * len(data))


if __name__ == "__main__":
    EbN0_min = -10
    EbN0_max = 1
    EbN0_range = range(EbN0_min, EbN0_max + 1)
    element_error_range = [0, 1, 5, 10, 15, 20]
    ber_theory = [berawgn(x) for x in EbN0_range]
    print("Simulating uncoded BPSK...")
    ber_simu_bpsk = numpy.empty((len(EbN0_range), len(element_error_range)))
    for i in range(len(element_error_range)):
        ber_simu_bpsk[:, i] = [
            simulate_ber(x, element_error_range[i]) for x in EbN0_range
        ]

    plt.figure(figsize=(16, 9), dpi=100)
    plt.grid()
    for i in range(len(element_error_range)):
        plt.plot(EbN0_range, ber_simu_bpsk[:, i])
    plt.title("BER Simulation")
    plt.xlabel(r"$\frac{E_b}{N_0}$ [dB]")
    plt.ylabel(r"BER")
    plt.legend(
        [
            r"$\sigma^2_d=0\%$",
            r"$\sigma^2_d=1\%$",
            r"$\sigma^2_d=5\%$",
            r"$\sigma^2_d=10\%$",
            r"$\sigma^2_d=15\%$",
            r"$\sigma^2_d=20\%$",
        ]
    )
    plt.yscale("log")
    plt.savefig("ber_simulation.png", dpi=200, bbox_inches="tight")
    plt.show()

    """
    f = pylab.figure()
    s = f.add_subplot(1, 1, 1)
    # s.semilogy(EbN0_range, ber_theory, "g-.")
    # s.semilogy(EbN0_range, ber_simu_bpsk, "b-o", label="Simulated uncoded BPSK")
    for i in range(len(element_error_range)):
        s.semilogy(EbN0_range, ber_simu_bpsk[:, i])
    s.set_title("BER Simulation")
    s.set_xlabel("Eb/N0 [dB]")
    s.set_ylabel("BER")
    s.legend(
        [
            r"$\sigma^2_d=0\%$",
            r"$\sigma^2_d=1\%$",
            r"$\sigma^2_d=5\%$",
            r"$\sigma^2_d=10\%$",
            r"$\sigma^2_d=15\%$",
            r"$\sigma^2_d=20\%$",
        ]
    )
    s.grid()
    pylab.show()"""

