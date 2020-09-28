#%%
import pmt
from pmt.pmt_swig import serialize
import zmq
import numpy as np

# %%
_PROTOCOL = "tcp://"
_SERVER = "127.0.0.1"
_PORT = ":5558"
_ADDR = _PROTOCOL + _SERVER + _PORT
# %%
context = zmq.Context()
sock = context.socket(zmq.REP)
rc = sock.bind(_ADDR)
#%%
flanks = pmt.make_f32vector(2, 0.0)
pmt.f32vector_set(flanks, 0, np.radians(15))
pmt.f32vector_set(flanks, 1, np.radians(70))
c = pmt.cons(pmt.to_pmt("doa"), flanks)
#%%
sock.recv()
#%%
sock.send(pmt.serialize_str(c))
# %% De acá para arriba anda
key0 = pmt.intern("doa")
val0 = pmt.from_long(123)
val1 = pmt.from_long(234)
val_list = pmt.list2(val0, val1)
pmt.length(val_list)
# %%
a = pmt.make_dict()
# %%
a = pmt.dict_add(a, key0, val_list)
print(pmt.cdr(a))
# %%
pmt.set_car(a, key0)
pmt.set_cdr(a, val_list)
# %%
print(pmt.cons(pmt.to_pmt("doa"), val_list))
# %%
print(pmt.cons(pmt.to_pmt("doa"), pmt.list2(pmt.from_long(123), pmt.from_long(234))))
# %%
b = pmt.cons(pmt.to_pmt("doa"), pmt.list2(pmt.from_float(123), pmt.from_float(234)))
# %%
pmt.is_float(pmt.cdr(b))
# %%
valb = pmt.cdr(b)
# %%
pmt.make_f32vector(0, 100)
# %%}
flanks = pmt.make_f32vector(2, 0.0)
pmt.f32vector_set(flanks, 0, 12500)
pmt.f32vector_set(flanks, 1, 20)
c = pmt.cons(pmt.to_pmt("doa"), flanks)
# %%
pmt.cdr(c)
# %%
sock.send(pmt.serialize_str(c))
# %%
