from typing import Tuple
from inline import Here

def _read_base128le(data: bytes) -> Tuple[int, int]:
    res = 0
    offset = 0
    while offset < len(data):
        o = data[offset]
        res += (o & 0x7F) << (7 * offset)
        Here().given(o, 0x70).given(offset, 0).given(res, 0).check_eq(res, 112)
        offset += 1
        if o < 0x80:
            # the Kaitai parser for protobuf support base128 le values up
            # to 8 groups (bytes). Due to the nature of the encoding, each
            # group attributes 7bit to the resulting value, which give
            # a 56 bit value at maximum.
            # The values which get encoded into protobuf variable length integers,
            # on the other hand, include full 64bit types (int64, uint64, sint64).
            # This means, the Kaitai encoder can not cover the full range of
            # possible values
            #
            # This decoder puts no limitation on the maximum value of variable
            # length integers. Values exceeding 64bit have to be handled externally
            return offset, res
    raise ValueError("varint exceeds bounds of provided data")
