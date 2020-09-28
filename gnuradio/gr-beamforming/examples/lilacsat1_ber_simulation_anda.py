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
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from lilacsat1_ber_bpsk import lilacsat1_ber_bpsk  # grc-generated hier_block
from scipy.special import erfc
import math
import numpy
import pylab


class lilacsat1_ber_simulation(gr.top_block):
    def __init__(self, EbN0):
        gr.top_block.__init__(self, "BER Simulation")

        ##################################################
        # Variables
        ##################################################
        self.N_BITS = N_BITS = 1e5
        self.EbN0 = EbN0
        self.sps = sps = 5
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
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_voltage,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=(0, 0, (1 + 1j) / numpy.sqrt(2),),
            noise_seed=RAND_SEED,
            block_tags=False,
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

        ##################################################
        # Connections
        ##################################################
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
            (self.channels_channel_model_0, 0), (self.blocks_multiply_const_vxx_1, 0)
        )
        self.connect(
            (self.digital_constellation_modulator_0, 0),
            (self.channels_channel_model_0, 0),
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
        self.connect(
            (self.lilacsat1_ber_bpsk_0, 0), (self.digital_diff_decoder_bb_0, 0)
        )

    def get_N_BITS(self):
        return self.N_BITS

    def set_N_BITS(self, N_BITS):
        self.N_BITS = N_BITS
        self.set_intdump_decim(min(int(self.N_BITS / 10), 100000))
        self.blocks_head_0.set_length(int(self.N_BITS))

    def get_EbN0(self):
        return self.EbN0

    def set_EbN0(self, EbN0):
        self.EbN0 = EbN0
        self.set_noise_voltage(0.5 * erfc(math.sqrt(10 ** (float(self.EbN0) / 10))))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.channels_channel_model_0.set_noise_voltage(self.noise_voltage)

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


"""def main(top_block_cls=lilacsat1_ber_simulation, options=None):
    tb = top_block_cls()

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
    tb.wait()"""


def berawgn(EbN0):
    """ Calculates theoretical bit error rate in AWGN (for BPSK and given Eb/N0) """
    return 0.5 * erfc(math.sqrt(10 ** (float(EbN0) / 10)))


def simulate_ber(EbN0):
    """ All the work's done here: create flow graph, run, read out BER """
    print("Eb/N0 = %d dB" % EbN0)
    fg = lilacsat1_ber_simulation(EbN0)
    fg.run()
    data = fg.blocks_vector_sink_x_0.data()
    print("noise=", fg.noise_voltage)
    print(data)
    factor = 6.0  # each bit error produces 6 errors, taking into account differential coding and scrambler
    return numpy.sum(data) / (factor * len(data))


if __name__ == "__main__":
    EbN0_min = 0
    EbN0_max = 12
    EbN0_range = range(EbN0_min, EbN0_max + 1)
    ber_theory = [berawgn(x) for x in EbN0_range]
    print("Simulating uncoded BPSK...")
    ber_simu_bpsk = [simulate_ber(x) for x in EbN0_range]

    f = pylab.figure()
    s = f.add_subplot(1, 1, 1)
    s.semilogy(EbN0_range, ber_theory, "g-.", label="Theoretical uncoded BPSK")
    s.semilogy(EbN0_range, ber_simu_bpsk, "b-o", label="Simulated uncoded BPSK")
    s.set_title("BER Simulation")
    s.set_xlabel("Eb/N0 (dB)")
    s.set_ylabel("BER")
    s.legend()
    s.grid()
    pylab.show()
