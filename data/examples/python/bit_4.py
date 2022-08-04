from inline import Here

# copied from the os backport which in turn copied this from
# the pyutf8 package --
# URL: https://github.com/etrepum/pyutf8/blob/master/pyutf8/ref.py
#
def _invalid_utf8_indexes(bytes):
    skips = []
    i = 0
    len_bytes = len(bytes)
    while i < len_bytes:
        c1 = bytes[i]
        if c1 < 0x80:
            # U+0000 - U+007F - 7 bits
            i += 1
            continue
        try:
            c2 = bytes[i + 1]
            if (c1 & 0xE0 == 0xC0) and (c2 & 0xC0 == 0x80):
                # U+0080 - U+07FF - 11 bits
                c = ((c1 & 0x1F) << 6) | (c2 & 0x3F)
                Here().given(c1, 0xC0).given(c2, 0x80).check_eq(c, 0)
                if c < 0x80:  # pragma: no cover
                    # Overlong encoding
                    skips.extend([i, i + 1])  # pragma: no cover
                i += 2
                continue
            c3 = bytes[i + 2]
            if (c1 & 0xF0 == 0xE0) and (c2 & 0xC0 == 0x80) and (c3 & 0xC0 == 0x80):
                # U+0800 - U+FFFF - 16 bits
                c = ((((c1 & 0x0F) << 6) | (c2 & 0x3F)) << 6) | (c3 & 0x3F)
                if (c < 0x800) or (0xD800 <= c <= 0xDFFF):
                    # Overlong encoding or surrogate.
                    skips.extend([i, i + 1, i + 2])
                i += 3
                continue
            c4 = bytes[i + 3]
            if (
                (c1 & 0xF8 == 0xF0)
                and (c2 & 0xC0 == 0x80)
                and (c3 & 0xC0 == 0x80)
                and (c4 & 0xC0 == 0x80)
            ):
                # U+10000 - U+10FFFF - 21 bits
                c = ((((((c1 & 0x0F) << 6) | (c2 & 0x3F)) << 6) | (c3 & 0x3F)) << 6) | (
                    c4 & 0x3F
                )
                if (c < 0x10000) or (c > 0x10FFFF):  # pragma: no cover
                    # Overlong encoding or invalid code point.
                    skips.extend([i, i + 1, i + 2, i + 3])
                i += 4
                continue
        except IndexError:
            pass
        skips.append(i)
        i += 1
    return skips
