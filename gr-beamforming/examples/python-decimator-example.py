# https://gnuradio.blogspot.com/2018/03/discuss-gnuradio-working-with-grc.html
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING. If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
import copy
from gnuradio import gr

class vave(gr.decim_block):
"""
Vector Average with Decimation. Only one vector is returned for N input.
This block is intended to reduce the downstream CPU load.
"""
def __init__(self, vlen, vdecimate):
gr.decim_block.__init__(self,
name="vave",
in_sig=[(numpy.float32, int(vlen))],
out_sig=[(numpy.float32, int(vlen))],
decim=int(vdecimate))
self.vlen = int(vlen)
self.vdecimate = int(vdecimate)
self.sum = numpy.zeros(self.vlen)
self.count = 0
self.oneovern = 1./float(self.vdecimate)

def forecast( self, noutput_items, ninput_items):
if noutput_items == None:
return self.vdecimate
# print 'Forecast: ', noutput_items
for i in range(len(nout_items)):
ninput_items[i] = noutput_items[i]*self.vdecimate
# print 'Forecast: ', ninput_items
return ninput_items
# return self.vdecimate

def work(self, input_items, output_items):
"""
Work averages all input vectors and outputs one vector for all inputs
"""
inn = input_items[0]

# get the number of input vectors
n = len( input_items) # number of input PORTS (only 1)
nv = len(inn) # number of vectors in this port

nout = len( output_items) #number of putput ports
ini = inn[0] # first input vector
li = len(ini) # length of first input vector
# print 'Number work vectors: ', nv, ' Length: ',li
ncp = min( li, self.vlen)

noutports = len( output_items)
if noutports != 1:
print '!!!!!!! Unexpected number of output ports: ', noutports
out = output_items[0] # vectors in PORT 0
nout = len(out) # number of output vectors
out0 = out[0] # get the first output vector
lo = len(out0) # length of 1st output vector
# print 'Number work outputs: ', nout,' Length: ',lo

iout = 0 # count the number of output vectors
for i in range(nv):
# get the lenght of one input
ini = inn[i]
ncp = min( li, self.vlen)

# now save this vector until all are received
self.sum[0:ncp] = self.sum[0:ncp] + ini[0:ncp]
self.count = self.count + 1

# indicate consumption of a vector from input

if self.count >= self.vdecimate:
# normalize output average
self.sum = self.oneovern * self.sum
# out0[:] = copy.deepcopy(self.sum)
outi = out[iout]
outi = self.sum
out[iout] = outi
iout = iout+1
# now reset the count and restart the sum
self.count = 0
self.sum = numpy.zeros( self.vlen)
# self.produce(0,len(output_items[0]))
# self.consume_each(nv)
# return no
# end for all input vectors
# if here, then not enough vectors input to produce an output
# self.consume(0,nv)
output_items[0] = out
# print 'N outputs: ', len(output_items[0]), iout
return len(output_items[0])
# end vave()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING. If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from vave import vave

class qa_vave (gr_unittest.TestCase):

def setUp (self):
self.tb = gr.top_block ()

def tearDown (self):
self.tb = None

def test_001_t (self):
vsize = 1024
vdecimate = 4
vin = numpy.zeros(2*vsize*vdecimate)
for i in range(vsize):
vin[i] = float(i)
vin[(vsize*vdecimate)+i] = vin[i]
# create a set of vectors
src = blocks.vector_source_f( vin.tolist())
s2v = blocks.stream_to_vector(gr.sizeof_float, vsize)
# block we're testing
vblock = vave( vsize, vdecimate)

v2s = blocks.vector_to_stream( gr.sizeof_float, vsize)
snk = blocks.vector_sink_f(vsize)

self.tb.connect (src, s2v)
self.tb.connect (s2v, vblock)
self.tb.connect (vblock, snk)
# self.tb.connect (v2s, snk)
expected = vin[0:(2*vsize)]/4.
expected[vsize:] = expected[0:vsize]
print 'Expected: ', expected[0:7]
outdata = None
waittime = 0.01

self.tb.run ()
outdata = snk.data()
print 'Output: ', outdata[0:7]
# check data
self.assertFloatTuplesAlmostEqual (expected, outdata, 6)

if __name__ == '__main__':
gr_unittest.run(qa_vave, "qa_vave.xml")
<?xml version="1.0"?>
<block>
<name>vave</name>
<key>vave_vave</key>
<category>[vave]</category>
<import>import vave</import>
<make>vave.vave($vlen, $vdecimate)</make>
<!-- Make one 'param' node for every Parameter you want settable from the GUI.
Sub-nodes:
* name
* key (makes the value accessible as $keyname, e.g. in the make node)
* type -->
<param>
<name>Vec Decimate</name>
<key>vdecimate</key>
<value>4</value>
<type>int</type>
</param>
<param>
<name>Vec Length</name>
<key>vlen</key>
<value>10</value>
<type>int</type>
</param>

<!-- Make one 'sink' node per input. Sub-nodes:
* name (an identifier for the GUI)
* type
* vlen
* optional (set to 1 for optional inputs) -->
<sink>
<name>in</name>
<type>float</type>
<vlen>$vlen</vlen>
</sink>

<!-- Make one 'source' node per output. Sub-nodes:
* name (an identifier for the GUI)
* type
* vlen
* optional (set to 1 for optional inputs) -->
<source>
<name>out</name>
<type>float</type>
<vlen>$vlen</vlen>
</source>
</block>
Hi