#!/usr/bin/env python
# coding: utf-8

from nose import main
from nose.tools import *

from msgpack import Packer, Unpacker, packs, unpacks

class ComplexUnpacker(Unpacker):
	def map_cb(self, obj):
		if b'__complex__' in obj:
			return complex(obj['real'], obj['imag'])
		return None

class ComplexPacker(Packer):
	def default(self, obj):
		if isinstance(obj, complex):
			return {b'__complex__': True, b'real': 1, b'imag': 2}
		return Packer.default(self, obj)

def test_encode_hook():
	cp = ComplexPacker()
	packed = cp.pack([3, 1+2j])
	unpacked = unpacks(packed)
	eq_(unpacked[1], {b'__complex__': True, b'real': 1, b'imag': 2})

def test_decode_hook():
	cup = ComplexUnpacker()
	packed = packs([3, {b'__complex__': True, b'real': 1, b'imag': 2}])
	cup.feed(packed)
	unpacked = cup.unpack()
	eq_(unpacked[1], 1+2j)

@raises(TypeError)
def test_bad_hook():
	cp = Packer()
	packed = cp.pack([3, 1+2j])
	unpacked = unpacks(packed)

def _arr_to_str(arr):
	return ''.join(str(c) for c in arr)

class ArrayStrUnpacker(Unpacker):
	def array_cb(self, obj):
		return ''.join(str(c) for c in obj)

def test_array_hook():
	packed = packs([1,2,3])
	cup = ArrayStrUnpacker()
	cup.feed(packed)
	unpacked = cup.unpack()
	eq_(unpacked, b'123')

if __name__ == '__main__':
    test_decode_hook()
    test_encode_hook()
    test_bad_hook()
    test_array_hook()

