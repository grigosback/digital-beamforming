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
        const_3_name="BPSK",
        const_4_name="QPSK",
        const_5_name="BPSK",
        const_6_name="QPSK",
        const_7_name="BPSK",
        const_8_name="QPSK",
        element_separation=0,
        file_name="eigenvalues5.csv",
        noise_voltage_1=0,
        noise_voltage_2=0,
        noise_voltage_3=0,
        noise_voltage_4=0,
        noise_voltage_5=0,
        noise_voltage_6=0,
        noise_voltage_7=0,
        noise_voltage_8=0,
        phi_1=70,
        phi_2=41,
        phi_3=70,
        phi_4=41,
        phi_5=70,
        phi_6=41,
        phi_7=70,
        phi_8=41,
        theta_1=45,
        theta_2=75,
        theta_3=45,
        theta_4=75,
        theta_5=45,
        theta_6=75,
        theta_7=45,
        theta_8=75,
    ):
        gr.top_block.__init__(self, "Eigenvalues Grabber")

        ##################################################
        # Parameters
        ##################################################
        self.const_1_name = const_1_name
        self.const_2_name = const_2_name
        self.const_3_name = const_3_name
        self.const_4_name = const_4_name
        self.const_5_name = const_5_name
        self.const_6_name = const_6_name
        self.const_7_name = const_7_name
        self.const_8_name = const_8_name
        self.element_separation = element_separation
        self.file_name = file_name
        self.noise_voltage_1 = noise_voltage_1
        self.noise_voltage_2 = noise_voltage_2
        self.noise_voltage_3 = noise_voltage_3
        self.noise_voltage_4 = noise_voltage_4
        self.noise_voltage_5 = noise_voltage_5
        self.noise_voltage_6 = noise_voltage_6
        self.noise_voltage_7 = noise_voltage_7
        self.noise_voltage_8 = noise_voltage_8
        self.phi_1 = phi_1
        self.phi_2 = phi_2
        self.phi_3 = phi_3
        self.phi_4 = phi_4
        self.phi_5 = phi_5
        self.phi_6 = phi_6
        self.phi_7 = phi_7
        self.phi_8 = phi_8
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.theta_3 = theta_3
        self.theta_4 = theta_4
        self.theta_5 = theta_5
        self.theta_6 = theta_6
        self.theta_7 = theta_7
        self.theta_8 = theta_8

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

        if const_3_name == "bpsk":
            self.const_3 = const_3 = digital.constellation_bpsk().base()
        elif const_3_name == "qpsk":
            self.const_3 = const_3 = digital.constellation_qpsk().base()
        elif const_3_name == "dqpsk":
            self.const_3 = const_3 = digital.constellation_dqpsk().base()
        elif const_3_name == "8psk":
            self.const_3 = const_3 = digital.constellation_8psk().base()
        elif const_3_name == "16qam":
            self.const_3 = const_3 = digital.constellation_16qam().base()

        if const_4_name == "bpsk":
            self.const_4 = const_4 = digital.constellation_bpsk().base()
        elif const_4_name == "qpsk":
            self.const_4 = const_4 = digital.constellation_qpsk().base()
        elif const_4_name == "dqpsk":
            self.const_4 = const_4 = digital.constellation_dqpsk().base()
        elif const_4_name == "8psk":
            self.const_4 = const_4 = digital.constellation_8psk().base()
        elif const_4_name == "16qam":
            self.const_4 = const_4 = digital.constellation_16qam().base()

        if const_5_name == "bpsk":
            self.const_5 = const_5 = digital.constellation_bpsk().base()
        elif const_5_name == "qpsk":
            self.const_5 = const_5 = digital.constellation_qpsk().base()
        elif const_5_name == "dqpsk":
            self.const_5 = const_5 = digital.constellation_dqpsk().base()
        elif const_5_name == "8psk":
            self.const_5 = const_5 = digital.constellation_8psk().base()
        elif const_5_name == "16qam":
            self.const_5 = const_5 = digital.constellation_16qam().base()

        if const_6_name == "bpsk":
            self.const_6 = const_6 = digital.constellation_bpsk().base()
        elif const_6_name == "qpsk":
            self.const_6 = const_6 = digital.constellation_qpsk().base()
        elif const_6_name == "dqpsk":
            self.const_6 = const_6 = digital.constellation_dqpsk().base()
        elif const_6_name == "8psk":
            self.const_6 = const_6 = digital.constellation_8psk().base()
        elif const_6_name == "16qam":
            self.const_6 = const_6 = digital.constellation_16qam().base()

        if const_7_name == "bpsk":
            self.const_7 = const_7 = digital.constellation_bpsk().base()
        elif const_7_name == "qpsk":
            self.const_7 = const_7 = digital.constellation_qpsk().base()
        elif const_7_name == "dqpsk":
            self.const_7 = const_7 = digital.constellation_dqpsk().base()
        elif const_7_name == "8psk":
            self.const_7 = const_7 = digital.constellation_8psk().base()
        elif const_7_name == "16qam":
            self.const_7 = const_7 = digital.constellation_16qam().base()

        if const_8_name == "bpsk":
            self.const_8 = const_8 = digital.constellation_bpsk().base()
        elif const_8_name == "qpsk":
            self.const_8 = const_8 = digital.constellation_qpsk().base()
        elif const_8_name == "dqpsk":
            self.const_8 = const_8 = digital.constellation_dqpsk().base()
        elif const_8_name == "8psk":
            self.const_8 = const_8 = digital.constellation_8psk().base()
        elif const_8_name == "16qam":
            self.const_8 = const_8 = digital.constellation_16qam().base()
        self.samp_rate = samp_rate = 150000
        self.n = n = 2
        self.my = my = 4
        self.mx = mx = 4
        self.fc = fc = 436e6
        self.bps_8 = bps_8 = const_8.bits_per_symbol()
        self.bps_7 = bps_7 = const_7.bits_per_symbol()
        self.bps_6 = bps_6 = const_6.bits_per_symbol()
        self.bps_5 = bps_5 = const_5.bits_per_symbol()
        self.bps_4 = bps_4 = const_4.bits_per_symbol()
        self.bps_3 = bps_3 = const_3.bits_per_symbol()
        self.bps_2 = bps_2 = const_2.bits_per_symbol()
        self.bps_1 = bps_1 = const_1.bits_per_symbol()

        ##################################################
        # Blocks
        ##################################################
        self.digital_chunks_to_symbols_xx_0_0_0_0_0_0_0_0 = digital.chunks_to_symbols_bc(
            const_8.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0_0_0_0_0_0_0 = digital.chunks_to_symbols_bc(
            const_7.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0_0_0_0_0_0 = digital.chunks_to_symbols_bc(
            const_6.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0_0_0_0_0 = digital.chunks_to_symbols_bc(
            const_5.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0_0_0_0 = digital.chunks_to_symbols_bc(
            const_4.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bc(
            const_3.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(
            const_2.points(), 1
        )
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(
            const_1.points(), 1
        )
        self.blocks_throttle_0_0_0_0_0_0_0_0 = blocks.throttle(
            gr.sizeof_char * 1, samp_rate, True
        )
        self.blocks_throttle_0_0_0_0_0_0_0 = blocks.throttle(
            gr.sizeof_char * 1, samp_rate, True
        )
        self.blocks_throttle_0_0_0_0_0_0 = blocks.throttle(
            gr.sizeof_char * 1, samp_rate, True
        )
        self.blocks_throttle_0_0_0_0_0 = blocks.throttle(
            gr.sizeof_char * 1, samp_rate, True
        )
        self.blocks_throttle_0_0_0_0 = blocks.throttle(
            gr.sizeof_char * 1, samp_rate, True
        )
        self.blocks_throttle_0_0_0 = blocks.throttle(
            gr.sizeof_char * 1, samp_rate, True
        )
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_char * 1, samp_rate, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char * 1, samp_rate, True)
        self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0_0_0 = blocks.packed_to_unpacked_bb(
            bps_8, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0_0 = blocks.packed_to_unpacked_bb(
            bps_7, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0 = blocks.packed_to_unpacked_bb(
            bps_6, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0_0_0_0_0 = blocks.packed_to_unpacked_bb(
            bps_5, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0_0_0_0 = blocks.packed_to_unpacked_bb(
            bps_4, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0_0_0 = blocks.packed_to_unpacked_bb(
            bps_3, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0_0 = blocks.packed_to_unpacked_bb(
            bps_2, gr.GR_MSB_FIRST
        )
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(
            bps_1, gr.GR_MSB_FIRST
        )
        self.blocks_add_xx_1_0_0_0_0_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_1_0_0_0_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_1_0_0_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_1_0_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_1_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_1_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_1 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_2 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_1_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_1 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_0_1 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_0_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0_0 = blocks.add_vcc(mx * my)
        self.blocks_add_xx_0 = blocks.add_vcc(mx * my)
        self.beamforming_randomsampler_0 = beamforming.randomsampler(mx * my, 8)
        self.beamforming_phasedarray_0_0_0_0_0_0_0_0 = beamforming.phasedarray(
            mx, my, theta_8, phi_8, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0_0_0_0_0_0_0 = beamforming.phasedarray(
            mx, my, theta_7, phi_7, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0_0_0_0_0_0 = beamforming.phasedarray(
            mx, my, theta_6, phi_6, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0_0_0_0_0 = beamforming.phasedarray(
            mx, my, theta_5, phi_5, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0_0_0_0 = beamforming.phasedarray(
            mx, my, theta_4, phi_4, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0_0_0 = beamforming.phasedarray(
            mx, my, theta_3, phi_3, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0_0 = beamforming.phasedarray(
            mx, my, theta_2, phi_2, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_phasedarray_0 = beamforming.phasedarray(
            mx, my, theta_1, phi_1, 436e6, (299792458 / (2 * fc)), element_separation
        )
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(
            mx, my, fc, (299792458 / (2 * fc)), n, 128, "eigenvalues_4signals"
        )
        self.analog_vectornoise_source_0_2 = analog.vectornoise_source(
            noise_voltage_5, mx * my
        )
        self.analog_vectornoise_source_0_1_0 = analog.vectornoise_source(
            noise_voltage_7, mx * my
        )
        self.analog_vectornoise_source_0_1 = analog.vectornoise_source(
            noise_voltage_3, mx * my
        )
        self.analog_vectornoise_source_0_0_1 = analog.vectornoise_source(
            noise_voltage_6, mx * my
        )
        self.analog_vectornoise_source_0_0_0_0 = analog.vectornoise_source(
            noise_voltage_8, mx * my
        )
        self.analog_vectornoise_source_0_0_0 = analog.vectornoise_source(
            noise_voltage_4, mx * my
        )
        self.analog_vectornoise_source_0_0 = analog.vectornoise_source(
            noise_voltage_2, mx * my
        )
        self.analog_vectornoise_source_0 = analog.vectornoise_source(
            noise_voltage_1, mx * my
        )
        self.analog_random_source_x_0_0_0_0_0_0_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )
        self.analog_random_source_x_0_0_0_0_0_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )
        self.analog_random_source_x_0_0_0_0_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )
        self.analog_random_source_x_0_0_0_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )
        self.analog_random_source_x_0_0_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )
        self.analog_random_source_x_0_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )
        self.analog_random_source_x_0_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )
        self.analog_random_source_x_0 = blocks.vector_source_b(
            list(map(int, numpy.random.randint(0, 256, 10000))), False
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect(
            (self.analog_random_source_x_0_0, 0), (self.blocks_throttle_0_0, 0)
        )
        self.connect(
            (self.analog_random_source_x_0_0_0, 0), (self.blocks_throttle_0_0_0, 0)
        )
        self.connect(
            (self.analog_random_source_x_0_0_0_0, 0), (self.blocks_throttle_0_0_0_0, 0)
        )
        self.connect(
            (self.analog_random_source_x_0_0_0_0_0, 0),
            (self.blocks_throttle_0_0_0_0_0, 0),
        )
        self.connect(
            (self.analog_random_source_x_0_0_0_0_0_0, 0),
            (self.blocks_throttle_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.analog_random_source_x_0_0_0_0_0_0_0, 0),
            (self.blocks_throttle_0_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.analog_random_source_x_0_0_0_0_0_0_0_0, 0),
            (self.blocks_throttle_0_0_0_0_0_0_0_0, 0),
        )
        self.connect((self.analog_vectornoise_source_0, 0), (self.blocks_add_xx_0, 1))
        self.connect(
            (self.analog_vectornoise_source_0_0, 0), (self.blocks_add_xx_0_0, 1)
        )
        self.connect(
            (self.analog_vectornoise_source_0_0_0, 0), (self.blocks_add_xx_0_0_0, 1)
        )
        self.connect(
            (self.analog_vectornoise_source_0_0_0_0, 0), (self.blocks_add_xx_0_0_0_0, 1)
        )
        self.connect(
            (self.analog_vectornoise_source_0_0_1, 0), (self.blocks_add_xx_0_0_1, 1)
        )
        self.connect(
            (self.analog_vectornoise_source_0_1, 0), (self.blocks_add_xx_0_1, 1)
        )
        self.connect(
            (self.analog_vectornoise_source_0_1_0, 0), (self.blocks_add_xx_0_1_0, 1)
        )
        self.connect(
            (self.analog_vectornoise_source_0_2, 0), (self.blocks_add_xx_0_2, 1)
        )
        self.connect((self.beamforming_phasedarray_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.beamforming_phasedarray_0_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect(
            (self.beamforming_phasedarray_0_0_0, 0), (self.blocks_add_xx_0_1, 0)
        )
        self.connect(
            (self.beamforming_phasedarray_0_0_0_0, 0), (self.blocks_add_xx_0_0_0, 0)
        )
        self.connect(
            (self.beamforming_phasedarray_0_0_0_0_0, 0), (self.blocks_add_xx_0_2, 0)
        )
        self.connect(
            (self.beamforming_phasedarray_0_0_0_0_0_0, 0), (self.blocks_add_xx_0_0_1, 0)
        )
        self.connect(
            (self.beamforming_phasedarray_0_0_0_0_0_0_0, 0),
            (self.blocks_add_xx_0_1_0, 0),
        )
        self.connect(
            (self.beamforming_phasedarray_0_0_0_0_0_0_0_0, 0),
            (self.blocks_add_xx_0_0_0_0, 0),
        )
        self.connect(
            (self.beamforming_randomsampler_0, 0),
            (self.beamforming_doaesprit_py_cf_0, 0),
        )
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.blocks_add_xx_1_0, 1))
        self.connect((self.blocks_add_xx_0_0_0_0, 0), (self.blocks_add_xx_1_0_0_0, 1))
        self.connect((self.blocks_add_xx_0_0_1, 0), (self.blocks_add_xx_1_0_0, 1))
        self.connect((self.blocks_add_xx_0_1, 0), (self.blocks_add_xx_1_0, 0))
        self.connect((self.blocks_add_xx_0_1_0, 0), (self.blocks_add_xx_1_0_0_0, 0))
        self.connect((self.blocks_add_xx_0_2, 0), (self.blocks_add_xx_1_0_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_add_xx_1_0_0_0_0_0, 0))
        self.connect((self.blocks_add_xx_1_0, 0), (self.blocks_add_xx_1_0_0_0_0_0, 1))
        self.connect((self.blocks_add_xx_1_0_0, 0), (self.blocks_add_xx_1_0_0_0_0, 0))
        self.connect((self.blocks_add_xx_1_0_0_0, 0), (self.blocks_add_xx_1_0_0_0_0, 1))
        self.connect(
            (self.blocks_add_xx_1_0_0_0_0, 0), (self.blocks_add_xx_1_0_0_0_0_0_0, 1)
        )
        self.connect(
            (self.blocks_add_xx_1_0_0_0_0_0, 0), (self.blocks_add_xx_1_0_0_0_0_0_0, 0)
        )
        self.connect(
            (self.blocks_add_xx_1_0_0_0_0_0_0, 0), (self.beamforming_randomsampler_0, 0)
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0, 0),
            (self.digital_chunks_to_symbols_xx_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0_0_0, 0),
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_throttle_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0)
        )
        self.connect(
            (self.blocks_throttle_0_0, 0), (self.blocks_packed_to_unpacked_xx_0_0, 0)
        )
        self.connect(
            (self.blocks_throttle_0_0_0, 0),
            (self.blocks_packed_to_unpacked_xx_0_0_0, 0),
        )
        self.connect(
            (self.blocks_throttle_0_0_0_0, 0),
            (self.blocks_packed_to_unpacked_xx_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_throttle_0_0_0_0_0, 0),
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_throttle_0_0_0_0_0_0, 0),
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_throttle_0_0_0_0_0_0_0, 0),
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.blocks_throttle_0_0_0_0_0_0_0_0, 0),
            (self.blocks_packed_to_unpacked_xx_0_0_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0, 0),
            (self.beamforming_phasedarray_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0, 0),
            (self.beamforming_phasedarray_0_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0_0, 0),
            (self.beamforming_phasedarray_0_0_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0_0_0, 0),
            (self.beamforming_phasedarray_0_0_0_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0, 0),
            (self.beamforming_phasedarray_0_0_0_0_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0_0, 0),
            (self.beamforming_phasedarray_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0_0_0, 0),
            (self.beamforming_phasedarray_0_0_0_0_0_0_0, 0),
        )
        self.connect(
            (self.digital_chunks_to_symbols_xx_0_0_0_0_0_0_0_0, 0),
            (self.beamforming_phasedarray_0_0_0_0_0_0_0_0, 0),
        )

    def get_const_1_name(self):
        return self.const_1_name

    def set_const_1_name(self, const_1_name):
        self.const_1_name = const_1_name

    def get_const_2_name(self):
        return self.const_2_name

    def set_const_2_name(self, const_2_name):
        self.const_2_name = const_2_name

    def get_const_3_name(self):
        return self.const_3_name

    def set_const_3_name(self, const_3_name):
        self.const_3_name = const_3_name

    def get_const_4_name(self):
        return self.const_4_name

    def set_const_4_name(self, const_4_name):
        self.const_4_name = const_4_name

    def get_const_5_name(self):
        return self.const_5_name

    def set_const_5_name(self, const_5_name):
        self.const_5_name = const_5_name

    def get_const_6_name(self):
        return self.const_6_name

    def set_const_6_name(self, const_6_name):
        self.const_6_name = const_6_name

    def get_const_7_name(self):
        return self.const_7_name

    def set_const_7_name(self, const_7_name):
        self.const_7_name = const_7_name

    def get_const_8_name(self):
        return self.const_8_name

    def set_const_8_name(self, const_8_name):
        self.const_8_name = const_8_name

    def get_element_separation(self):
        return self.element_separation

    def set_element_separation(self, element_separation):
        self.element_separation = element_separation
        self.beamforming_phasedarray_0.set_element_error(self.element_separation)
        self.beamforming_phasedarray_0_0.set_element_error(self.element_separation)
        self.beamforming_phasedarray_0_0_0.set_element_error(self.element_separation)
        self.beamforming_phasedarray_0_0_0_0.set_element_error(self.element_separation)
        self.beamforming_phasedarray_0_0_0_0_0.set_element_error(
            self.element_separation
        )
        self.beamforming_phasedarray_0_0_0_0_0_0.set_element_error(
            self.element_separation
        )
        self.beamforming_phasedarray_0_0_0_0_0_0_0.set_element_error(
            self.element_separation
        )
        self.beamforming_phasedarray_0_0_0_0_0_0_0_0.set_element_error(
            self.element_separation
        )

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

    def get_noise_voltage_3(self):
        return self.noise_voltage_3

    def set_noise_voltage_3(self, noise_voltage_3):
        self.noise_voltage_3 = noise_voltage_3
        self.analog_vectornoise_source_0_1.set_ampl(self.noise_voltage_3)

    def get_noise_voltage_4(self):
        return self.noise_voltage_4

    def set_noise_voltage_4(self, noise_voltage_4):
        self.noise_voltage_4 = noise_voltage_4
        self.analog_vectornoise_source_0_0_0.set_ampl(self.noise_voltage_4)

    def get_noise_voltage_5(self):
        return self.noise_voltage_5

    def set_noise_voltage_5(self, noise_voltage_5):
        self.noise_voltage_5 = noise_voltage_5
        self.analog_vectornoise_source_0_2.set_ampl(self.noise_voltage_5)

    def get_noise_voltage_6(self):
        return self.noise_voltage_6

    def set_noise_voltage_6(self, noise_voltage_6):
        self.noise_voltage_6 = noise_voltage_6
        self.analog_vectornoise_source_0_0_1.set_ampl(self.noise_voltage_6)

    def get_noise_voltage_7(self):
        return self.noise_voltage_7

    def set_noise_voltage_7(self, noise_voltage_7):
        self.noise_voltage_7 = noise_voltage_7
        self.analog_vectornoise_source_0_1_0.set_ampl(self.noise_voltage_7)

    def get_noise_voltage_8(self):
        return self.noise_voltage_8

    def set_noise_voltage_8(self, noise_voltage_8):
        self.noise_voltage_8 = noise_voltage_8
        self.analog_vectornoise_source_0_0_0_0.set_ampl(self.noise_voltage_8)

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

    def get_phi_3(self):
        return self.phi_3

    def set_phi_3(self, phi_3):
        self.phi_3 = phi_3
        self.beamforming_phasedarray_0_0_0.set_azimuth(self.phi_3)

    def get_phi_4(self):
        return self.phi_4

    def set_phi_4(self, phi_4):
        self.phi_4 = phi_4
        self.beamforming_phasedarray_0_0_0_0.set_azimuth(self.phi_4)

    def get_phi_5(self):
        return self.phi_5

    def set_phi_5(self, phi_5):
        self.phi_5 = phi_5
        self.beamforming_phasedarray_0_0_0_0_0.set_azimuth(self.phi_5)

    def get_phi_6(self):
        return self.phi_6

    def set_phi_6(self, phi_6):
        self.phi_6 = phi_6
        self.beamforming_phasedarray_0_0_0_0_0_0.set_azimuth(self.phi_6)

    def get_phi_7(self):
        return self.phi_7

    def set_phi_7(self, phi_7):
        self.phi_7 = phi_7
        self.beamforming_phasedarray_0_0_0_0_0_0_0.set_azimuth(self.phi_7)

    def get_phi_8(self):
        return self.phi_8

    def set_phi_8(self, phi_8):
        self.phi_8 = phi_8
        self.beamforming_phasedarray_0_0_0_0_0_0_0_0.set_azimuth(self.phi_8)

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

    def get_theta_3(self):
        return self.theta_3

    def set_theta_3(self, theta_3):
        self.theta_3 = theta_3
        self.beamforming_phasedarray_0_0_0.set_elevation(self.theta_3)

    def get_theta_4(self):
        return self.theta_4

    def set_theta_4(self, theta_4):
        self.theta_4 = theta_4
        self.beamforming_phasedarray_0_0_0_0.set_elevation(self.theta_4)

    def get_theta_5(self):
        return self.theta_5

    def set_theta_5(self, theta_5):
        self.theta_5 = theta_5
        self.beamforming_phasedarray_0_0_0_0_0.set_elevation(self.theta_5)

    def get_theta_6(self):
        return self.theta_6

    def set_theta_6(self, theta_6):
        self.theta_6 = theta_6
        self.beamforming_phasedarray_0_0_0_0_0_0.set_elevation(self.theta_6)

    def get_theta_7(self):
        return self.theta_7

    def set_theta_7(self, theta_7):
        self.theta_7 = theta_7
        self.beamforming_phasedarray_0_0_0_0_0_0_0.set_elevation(self.theta_7)

    def get_theta_8(self):
        return self.theta_8

    def set_theta_8(self, theta_8):
        self.theta_8 = theta_8
        self.beamforming_phasedarray_0_0_0_0_0_0_0_0.set_elevation(self.theta_8)

    def get_const_8(self):
        return self.const_8

    def set_const_8(self, const_8):
        self.const_8 = const_8

    def get_const_7(self):
        return self.const_7

    def set_const_7(self, const_7):
        self.const_7 = const_7

    def get_const_6(self):
        return self.const_6

    def set_const_6(self, const_6):
        self.const_6 = const_6

    def get_const_5(self):
        return self.const_5

    def set_const_5(self, const_5):
        self.const_5 = const_5

    def get_const_4(self):
        return self.const_4

    def set_const_4(self, const_4):
        self.const_4 = const_4

    def get_const_3(self):
        return self.const_3

    def set_const_3(self, const_3):
        self.const_3 = const_3

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
        self.blocks_throttle_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0_0_0_0_0.set_sample_rate(self.samp_rate)

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

    def get_bps_8(self):
        return self.bps_8

    def set_bps_8(self, bps_8):
        self.bps_8 = bps_8

    def get_bps_7(self):
        return self.bps_7

    def set_bps_7(self, bps_7):
        self.bps_7 = bps_7

    def get_bps_6(self):
        return self.bps_6

    def set_bps_6(self, bps_6):
        self.bps_6 = bps_6

    def get_bps_5(self):
        return self.bps_5

    def set_bps_5(self, bps_5):
        self.bps_5 = bps_5

    def get_bps_4(self):
        return self.bps_4

    def set_bps_4(self, bps_4):
        self.bps_4 = bps_4

    def get_bps_3(self):
        return self.bps_3

    def set_bps_3(self, bps_3):
        self.bps_3 = bps_3

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
        "--const-3-name",
        dest="const_3_name",
        type=str,
        default="BPSK",
        help="Set const_3_name [default=%(default)r]",
    )
    parser.add_argument(
        "--const-4-name",
        dest="const_4_name",
        type=str,
        default="QPSK",
        help="Set const_4_name [default=%(default)r]",
    )
    parser.add_argument(
        "--const-5-name",
        dest="const_5_name",
        type=str,
        default="BPSK",
        help="Set const_5_name [default=%(default)r]",
    )
    parser.add_argument(
        "--const-6-name",
        dest="const_6_name",
        type=str,
        default="QPSK",
        help="Set const_6_name [default=%(default)r]",
    )
    parser.add_argument(
        "--const-7-name",
        dest="const_7_name",
        type=str,
        default="BPSK",
        help="Set const_7_name [default=%(default)r]",
    )
    parser.add_argument(
        "--const-8-name",
        dest="const_8_name",
        type=str,
        default="QPSK",
        help="Set const_8_name [default=%(default)r]",
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
        "--phi-3",
        dest="phi_3",
        type=eng_float,
        default="70.0",
        help="Set Azimut Angle 3 [default=%(default)r]",
    )
    parser.add_argument(
        "--phi-4",
        dest="phi_4",
        type=eng_float,
        default="41.0",
        help="Set Azimut Angle 4 [default=%(default)r]",
    )
    parser.add_argument(
        "--phi-5",
        dest="phi_5",
        type=eng_float,
        default="70.0",
        help="Set Azimut Angle 5 [default=%(default)r]",
    )
    parser.add_argument(
        "--phi-6",
        dest="phi_6",
        type=eng_float,
        default="41.0",
        help="Set Azimut Angle 6 [default=%(default)r]",
    )
    parser.add_argument(
        "--phi-7",
        dest="phi_7",
        type=eng_float,
        default="70.0",
        help="Set Azimut Angle 7 [default=%(default)r]",
    )
    parser.add_argument(
        "--phi-8",
        dest="phi_8",
        type=eng_float,
        default="41.0",
        help="Set Azimut Angle 8 [default=%(default)r]",
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
        help="Set Elevation Angle 2 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-3",
        dest="theta_3",
        type=eng_float,
        default="45.0",
        help="Set Elevation Angle 3 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-4",
        dest="theta_4",
        type=eng_float,
        default="75.0",
        help="Set Elevation Angle 4 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-5",
        dest="theta_5",
        type=eng_float,
        default="45.0",
        help="Set Elevation Angle 5 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-6",
        dest="theta_6",
        type=eng_float,
        default="75.0",
        help="Set Elevation Angle 6 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-7",
        dest="theta_7",
        type=eng_float,
        default="45.0",
        help="Set Elevation Angle 7 [default=%(default)r]",
    )
    parser.add_argument(
        "--theta-8",
        dest="theta_8",
        type=eng_float,
        default="75.0",
        help="Set Elevation Angle 8 [default=%(default)r]",
    )
    return parser


def main(top_block_cls=eigenvalues_grabber, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(
        const_1_name=options.const_1_name,
        const_2_name=options.const_2_name,
        const_3_name=options.const_3_name,
        const_4_name=options.const_4_name,
        const_5_name=options.const_5_name,
        const_6_name=options.const_6_name,
        const_7_name=options.const_7_name,
        const_8_name=options.const_8_name,
        file_name=options.file_name,
        phi_1=options.phi_1,
        phi_2=options.phi_2,
        phi_3=options.phi_3,
        phi_4=options.phi_4,
        phi_5=options.phi_5,
        phi_6=options.phi_6,
        phi_7=options.phi_7,
        phi_8=options.phi_8,
        theta_1=options.theta_1,
        theta_2=options.theta_2,
        theta_3=options.theta_3,
        theta_4=options.theta_4,
        theta_5=options.theta_5,
        theta_6=options.theta_6,
        theta_7=options.theta_7,
        theta_8=options.theta_8,
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
    file_name = "eigenvalues_8signals.csv"
    const = numpy.array(["bpsk", "qpsk", "dqpsk", "8psk"])
    for i in range(1000):
        element_separation = random.uniform(
            element_separation_min, element_separation_max
        )
        noise_voltage_1 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_2 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_3 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_4 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_5 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_6 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_7 = random.uniform(noise_voltage_min, noise_voltage_max)
        noise_voltage_8 = random.uniform(noise_voltage_min, noise_voltage_max)
        phi_1 = random.uniform(phi_min, phi_max)
        phi_2 = random.uniform(phi_min, phi_max)
        phi_3 = random.uniform(phi_min, phi_max)
        phi_4 = random.uniform(phi_min, phi_max)
        phi_5 = random.uniform(phi_min, phi_max)
        phi_6 = random.uniform(phi_min, phi_max)
        phi_7 = random.uniform(phi_min, phi_max)
        phi_8 = random.uniform(phi_min, phi_max)
        theta_1 = random.uniform(theta_min, theta_max)
        theta_2 = random.uniform(theta_min, theta_max)
        theta_3 = random.uniform(theta_min, theta_max)
        theta_4 = random.uniform(theta_min, theta_max)
        theta_5 = random.uniform(theta_min, theta_max)
        theta_6 = random.uniform(theta_min, theta_max)
        theta_7 = random.uniform(theta_min, theta_max)
        theta_8 = random.uniform(theta_min, theta_max)
        const_1 = numpy.random.choice(const)
        const_2 = numpy.random.choice(const)
        const_3 = numpy.random.choice(const)
        const_4 = numpy.random.choice(const)
        const_5 = numpy.random.choice(const)
        const_6 = numpy.random.choice(const)
        const_7 = numpy.random.choice(const)
        const_8 = numpy.random.choice(const)

        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Iteration " + str(i) + ":")
        print("const_1 = " + const_1)
        print("const_2 = " + const_2)
        print("const_3 = " + const_3)
        print("const_4 = " + const_4)
        print("const_5 = " + const_5)
        print("const_6 = " + const_6)
        print("const_7 = " + const_7)
        print("const_8 = " + const_8)
        print("element_separation = %2lf" % element_separation)
        print("noise_voltage_1 = %.2lf" % noise_voltage_1)
        print("noise_voltage_2 = %.2lf" % noise_voltage_2)
        print("noise_voltage_3 = %.2lf" % noise_voltage_3)
        print("noise_voltage_4 = %.2lf" % noise_voltage_4)
        print("noise_voltage_5 = %.2lf" % noise_voltage_5)
        print("noise_voltage_6 = %.2lf" % noise_voltage_6)
        print("noise_voltage_7 = %.2lf" % noise_voltage_7)
        print("noise_voltage_8 = %.2lf" % noise_voltage_8)
        print("phi_1 = %.2lf" % phi_1)
        print("phi_2 = %.2lf" % phi_2)
        print("phi_3 = %.2lf" % phi_3)
        print("phi_4 = %.2lf" % phi_4)
        print("phi_5 = %.2lf" % phi_5)
        print("phi_6 = %.2lf" % phi_6)
        print("phi_7 = %.2lf" % phi_7)
        print("phi_8 = %.2lf" % phi_8)
        print("theta_1 = %.2lf" % theta_1)
        print("theta_2 = %.2lf" % theta_2)
        print("theta_3 = %.2lf" % theta_3)
        print("theta_4 = %.2lf" % theta_4)
        print("theta_5 = %.2lf" % theta_5)
        print("theta_6 = %.2lf" % theta_6)
        print("theta_7 = %.2lf" % theta_7)
        print("theta_8 = %.2lf" % theta_8)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        fg = eigenvalues_grabber(
            const_1,
            const_2,
            const_3,
            const_4,
            const_5,
            const_6,
            const_7,
            const_8,
            element_separation,
            file_name,
            noise_voltage_1,
            noise_voltage_2,
            noise_voltage_3,
            noise_voltage_4,
            noise_voltage_5,
            noise_voltage_6,
            noise_voltage_7,
            noise_voltage_8,
            phi_1,
            phi_2,
            phi_3,
            phi_4,
            phi_5,
            phi_6,
            phi_7,
            phi_8,
            theta_1,
            theta_2,
            theta_3,
            theta_4,
            theta_5,
            theta_6,
            theta_7,
            theta_8,
        )

        fg.run()
