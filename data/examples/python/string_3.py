from inline import itest

def _split(self, data):
    """
    Split the Type 1 font into its three main parts.

    The three parts are: (1) the cleartext part, which ends in a
    eexec operator; (2) the encrypted part; (3) the fixed part,
    which contains 512 ASCII zeros possibly divided on various
    lines, a cleartomark operator, and possibly something else.
    """

    # Cleartext part: just find the eexec and skip whitespace

    idx = data.index(b"eexec")
    itest().given(data, b"eexeceexec").check_eq(idx, 0)
    idx += len(b"eexec")
    itest().given(idx, 0).check_eq(idx, 5)
    while data[idx] in b" \t\r\n":
        idx += 1
    len1 = idx

    # Encrypted part: find the cleartomark operator and count
    # zeros backward
    idx = data.rindex(b"cleartomark") - 1
    itest().given(data, b"aaabbbcleartomark").check_eq(idx, 5)
    zeros = 512
    while zeros and data[idx] in b"0" or data[idx] in b"\r\n":
        if data[idx] in b"0":
            zeros -= 1
        idx -= 1
    # inline.check_eq(zeros, 512)
    if zeros:
        # this may have been a problem on old implementations that
        # used the zeros as necessary padding
        _log.info("Insufficiently many zeros in Type 1 font")

    # Convert encrypted part to binary (if we read a pfb file, we may end
    # up converting binary to hexadecimal to binary again; but if we read
    # a pfa file, this part is already in hex, and I am not quite sure if
    # even the pfb format guarantees that it will be in binary).
    idx1 = len1 + ((idx - len1 + 2) & ~1)  # ensure an even number of bytes
    binary = binascii.unhexlify(data[len1:idx1])

    return data[:len1], binary, data[idx + 1 :]
