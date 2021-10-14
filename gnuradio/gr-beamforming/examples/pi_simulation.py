#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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
import sip
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
from gnuradio.qtgui import Range, RangeWidget
import analog
import beamforming
from gnuradio import qtgui

class pi_simulation(gr.top_block, Qt.QWidget):

    def __init__(self, fc=436e6, mx=4, my=4, n=2, phi_1=70, phi_2=41, theta_1=45, theta_2=75):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "pi_simulation")

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
        self.phi_1 = phi_1
        self.phi_2 = phi_2
        self.theta_1 = theta_1
        self.theta_2 = theta_2

        ##################################################
        # Variables
        ##################################################
        self.const_2 = const_2 = digital.constellation_16qam().base()
        self.const_1 = const_1 = digital.constellation_qpsk().base()
        self.theta = theta = 0
        self.samp_rate = samp_rate = 32000
        self.phi = phi = 0
        self.noise_voltage_1 = noise_voltage_1 = 2
        self.element_separation = element_separation = 10
        self.bps_2 = bps_2 = const_2.bits_per_symbol()
        self.bps_1 = bps_1 = const_1.bits_per_symbol()

        ##################################################
        # Blocks
        ##################################################
        self._theta_range = Range(0, 90, 0.1, 0, 200)
        self._theta_win = RangeWidget(self._theta_range, self.set_theta, 'Elevation', "counter_slider", float)
        self.top_grid_layout.addWidget(self._theta_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._phi_range = Range(-180, 180, 0.1, 0, 200)
        self._phi_win = RangeWidget(self._phi_range, self.set_phi, 'Azimut', "counter_slider", float)
        self.top_grid_layout.addWidget(self._phi_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_voltage_1_range = Range(0, 10, 0.001, 2, 200)
        self._noise_voltage_1_win = RangeWidget(self._noise_voltage_1_range, self.set_noise_voltage_1, 'Noise Voltage 1', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_voltage_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._element_separation_range = Range(0, 100, 0.1, 10, 200)
        self._element_separation_win = RangeWidget(self._element_separation_range, self.set_element_separation, 'Element separation distance [%', "counter_slider", float)
        self.top_grid_layout.addWidget(self._element_separation_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(const_1.points(), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bps_1, gr.GR_MSB_FIRST)
        self.blocks_add_xx_0 = blocks.add_vcc(mx*my)
        self.beamforming_randomsampler_0 = beamforming.randomsampler(mx*my, 8)
        self.beamforming_phasedarray_0 = beamforming.phasedarray(mx, my, theta, phi, 436e6, (299792458/(2*fc)), element_separation)
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(mx, my, fc, (299792458/(2*fc)), n, 128)
        self.beamforming_beamformer_0 = beamforming.beamformer(mx, my, 0)
        self.analog_vectornoise_source_0 = analog.vectornoise_source(noise_voltage_1, mx*my)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.beamforming_doaesprit_py_cf_0, 'doa_port'), (self.beamforming_beamformer_0, 'doa_port'))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_vectornoise_source_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.beamforming_beamformer_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.beamforming_phasedarray_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.beamforming_randomsampler_0, 0), (self.beamforming_doaesprit_py_cf_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.beamforming_beamformer_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.beamforming_randomsampler_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.beamforming_phasedarray_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pi_simulation")
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

    def get_phi_1(self):
        return self.phi_1

    def set_phi_1(self, phi_1):
        self.phi_1 = phi_1

    def get_phi_2(self):
        return self.phi_2

    def set_phi_2(self, phi_2):
        self.phi_2 = phi_2

    def get_theta_1(self):
        return self.theta_1

    def set_theta_1(self, theta_1):
        self.theta_1 = theta_1

    def get_theta_2(self):
        return self.theta_2

    def set_theta_2(self, theta_2):
        self.theta_2 = theta_2

    def get_const_2(self):
        return self.const_2

    def set_const_2(self, const_2):
        self.const_2 = const_2

    def get_const_1(self):
        return self.const_1

    def set_const_1(self, const_1):
        self.const_1 = const_1

    def get_theta(self):
        return self.theta

    def set_theta(self, theta):
        self.theta = theta
        self.beamforming_phasedarray_0.set_elevation(self.theta)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_phi(self):
        return self.phi

    def set_phi(self, phi):
        self.phi = phi
        self.beamforming_phasedarray_0.set_azimuth(self.phi)

    def get_noise_voltage_1(self):
        return self.noise_voltage_1

    def set_noise_voltage_1(self, noise_voltage_1):
        self.noise_voltage_1 = noise_voltage_1
        self.analog_vectornoise_source_0.set_ampl(self.noise_voltage_1)

    def get_element_separation(self):
        return self.element_separation

    def set_element_separation(self, element_separation):
        self.element_separation = element_separation
        self.beamforming_phasedarray_0.set_element_error(self.element_separation)

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
        "--fc", dest="fc", type=eng_float, default="436.0M",
        help="Set Carrier frequency [default=%(default)r]")
    parser.add_argument(
        "--mx", dest="mx", type=intx, default=4,
        help="Set # elements in x [default=%(default)r]")
    parser.add_argument(
        "--my", dest="my", type=intx, default=4,
        help="Set # elements in y [default=%(default)r]")
    parser.add_argument(
        "--n", dest="n", type=intx, default=2,
        help="Set # impinging signals [default=%(default)r]")
    parser.add_argument(
        "--phi-1", dest="phi_1", type=eng_float, default="70.0",
        help="Set Azimut Angle 1 [default=%(default)r]")
    parser.add_argument(
        "--phi-2", dest="phi_2", type=eng_float, default="41.0",
        help="Set Azimut Angle 2 [default=%(default)r]")
    parser.add_argument(
        "--theta-1", dest="theta_1", type=eng_float, default="45.0",
        help="Set Elevation Angle 1 [default=%(default)r]")
    parser.add_argument(
        "--theta-2", dest="theta_2", type=eng_float, default="75.0",
        help="Set Elevation Angle 1 [default=%(default)r]")
    return parser


def main(top_block_cls=pi_simulation, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(fc=options.fc, mx=options.mx, my=options.my, n=options.n, phi_1=options.phi_1, phi_2=options.phi_2, theta_1=options.theta_1, theta_2=options.theta_2)
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
