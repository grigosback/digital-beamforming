#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BER Curve Generator
# Author: grigosback
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import beamforming
from gnuradio import qtgui

class bercurve_test(gr.top_block, Qt.QWidget):

    def __init__(self, fc=436e6, mx=4, my=4, n=1, noise=0, phi=50, theta=45):
        gr.top_block.__init__(self, "BER Curve Generator")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BER Curve Generator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "bercurve_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

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
        self.const = const = digital.constellation_qpsk().base()
        self.samp_rate = samp_rate = 32000
        self.bps = bps = const.bits_per_symbol()

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            512, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const.base())
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(const.points(), 1)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(bps, gr.GR_MSB_FIRST)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bps, gr.GR_MSB_FIRST)
        self.beamforming_randomsampler_py_cc_0_0 = beamforming.randomsampler_py_cc(mx*my,8)
        self.beamforming_phasedarray_py_cc_0 = beamforming.phasedarray_py_cc(mx, my, theta, phi, fc, noise)
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(128, mx, my, fc, n)
        self.beamforming_beamformer_py_cc_0 = beamforming.beamformer_py_cc(mx, my, fc, 0, 0, 8*128)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, const.arity(), int(1e6)))), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.beamforming_beamformer_py_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.beamforming_doaesprit_py_cf_0, 1), (self.beamforming_beamformer_py_cc_0, 2))
        self.connect((self.beamforming_doaesprit_py_cf_0, 0), (self.beamforming_beamformer_py_cc_0, 1))
        self.connect((self.beamforming_phasedarray_py_cc_0, 0), (self.beamforming_beamformer_py_cc_0, 0))
        self.connect((self.beamforming_phasedarray_py_cc_0, 0), (self.beamforming_randomsampler_py_cc_0_0, 0))
        self.connect((self.beamforming_randomsampler_py_cc_0_0, 0), (self.beamforming_doaesprit_py_cf_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.beamforming_phasedarray_py_cc_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.qtgui_number_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "bercurve_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

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


def main(top_block_cls=bercurve_test, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(fc=options.fc, mx=options.mx, my=options.my, n=options.n)
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
