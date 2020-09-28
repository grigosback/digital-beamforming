#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Vector Noise Source Test
# Author: grigosback
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class vector_noise_source_test(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Vector Noise Source Test")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1024

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_source_x_0 = blocks.vector_source_c(
            (1, 2, 3, 4), True, 4, []
        )
        self.blocks_vector_sink_x_0 = blocks.vector_sink_c(4, 12)
        self.blocks_throttle_0 = blocks.throttle(
            gr.sizeof_gr_complex * 4, samp_rate, True
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=vector_noise_source_test, options=None):
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
    data = tb.blocks_vector_sink_x_0.data()
    print(data)
    tb.stop()
    tb.wait()


if __name__ == "__main__":
    main()
