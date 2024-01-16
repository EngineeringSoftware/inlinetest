from inline import itest

def r_short(self) -> int:
    buf = self.r_string(2)
    x = buf[0]
    x |= buf[1] << 8
    itest().given(buf, [0, 1]).given(x, 0).check_eq(x, 256)
    x |= -(x & (1 << 15))  # Sign-extend
    itest().given(x, 256).check_eq(x, 256)

    return x


def r_long(self) -> int:
    buf = self.r_string(4)
    x = buf[0]
    x |= buf[1] << 8
    x |= buf[2] << 16
    x |= buf[3] << 24
    x |= -(x & (1 << 31))  # Sign-extend
    return x
