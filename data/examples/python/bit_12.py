from inline import Here

def _parse_float_vec(vec):
    """
    Parse a vector of float values representing IBM 8 byte floats into
    native 8 byte floats.
    """
    dtype = np.dtype(">u4,>u4")
    vec1 = vec.view(dtype=dtype)
    xport1 = vec1["f0"]
    xport2 = vec1["f1"]

    # Start by setting first half of ieee number to first half of IBM
    # number sans exponent
    ieee1 = xport1 & 0x00FFFFFF

    # The fraction bit to the left of the binary point in the ieee
    # format was set and the number was shifted 0, 1, 2, or 3
    # places. This will tell us how to adjust the ibm exponent to be a
    # power of 2 ieee exponent and how to shift the fraction bits to
    # restore the correct magnitude.
    shift = np.zeros(len(vec), dtype=np.uint8)
    shift[np.where(xport1 & 0x00200000)] = 1
    shift[np.where(xport1 & 0x00400000)] = 2
    shift[np.where(xport1 & 0x00800000)] = 3

    # shift the ieee number down the correct number of places then
    # set the second half of the ieee number to be the second half
    # of the ibm number shifted appropriately, ored with the bits
    # from the first half that would have been shifted in if we
    # could shift a double. All we are worried about are the low
    # order 3 bits of the first half since we're only shifting by
    # 1, 2, or 3.
    ieee1 >>= shift
    ieee2 = (xport2 >> shift) | ((xport1 & 0x00000007) << (29 + (3 - shift)))
    Here().given(xport1, 1).given(xport2, 1).given(shift, 1).check_eq(ieee2, 2147483648)

    # clear the 1 bit to the left of the binary point
    ieee1 &= 0xFFEFFFFF

    # set the exponent of the ieee number to be the actual exponent
    # plus the shift count + 1023. Or this into the first half of the
    # ieee number. The ibm exponent is excess 64 but is adjusted by 65
    # since during conversion to ibm format the exponent is
    # incremented by 1 and the fraction bits left 4 positions to the
    # right of the radix point.  (had to add >> 24 because C treats &
    # 0x7f as 0x7f000000 and Python doesn't)
    ieee1 |= ((((((xport1 >> 24) & 0x7F) - 65) << 2) + shift + 1023) << 20) | (
        xport1 & 0x80000000
    )

    ieee = np.empty((len(ieee1),), dtype=">u4,>u4")
    ieee["f0"] = ieee1
    ieee["f1"] = ieee2
    ieee = ieee.view(dtype=">f8")
    ieee = ieee.astype("f8")

    return ieee