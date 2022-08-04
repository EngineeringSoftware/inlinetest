class Bit9 {
    /**
     * Encode a byte array using bcrypt's slightly-modified base64 encoding scheme.
     * Note
     * that this is <strong>not</strong> compatible with the standard MIME-base64
     * encoding.
     *
     * @param d   the byte array to encode
     * @param len the number of bytes to encode
     * @param rs  the destination buffer for the base64-encoded string
     * @throws IllegalArgumentException if the length is invalid
     */
    static void encode_base64(byte d[], int len, StringBuilder rs)
            throws IllegalArgumentException {
        int off = 0;
        int c1, c2;

        if (len <= 0 || len > d.length) {
            throw new IllegalArgumentException("Invalid len");
        }

        while (off < len) {
            c1 = d[off++] & 0xff;
            new Here().given(c1, 0).given(off, 0).given(d, "abcd".getBytes()).checkEq(c1, 97);
            rs.append(base64_code[(c1 >> 2) & 0x3f]);
            c1 = (c1 & 0x03) << 4;
            new Here().given(c1, 97).checkEq(c1, 16);
            if (off >= len) {
                rs.append(base64_code[c1 & 0x3f]);
                break;
            }
            c2 = d[off++] & 0xff;
            new Here().given(c2, 0).given(off, 1).given(d, "abcd".getBytes()).checkEq(c2, 98);
            c1 |= (c2 >> 4) & 0x0f;
            new Here().given(c1, 16).given(c2, 98).checkEq(c1, 22);
            rs.append(base64_code[c1 & 0x3f]);
            c1 = (c2 & 0x0f) << 2;
            new Here().given(c1, 22).given(c2, 98).checkEq(c1, 8);
            if (off >= len) {
                rs.append(base64_code[c1 & 0x3f]);
                break;
            }
            c2 = d[off++] & 0xff;
            c1 |= (c2 >> 6) & 0x03;
            rs.append(base64_code[c1 & 0x3f]);
            rs.append(base64_code[c2 & 0x3f]);
        }
    }
}