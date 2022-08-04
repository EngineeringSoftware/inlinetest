class Bit6 {
    public static long getShortDecimalValue(byte[] bytes) {
        long value = 0;
        if ((bytes[0] & 0x80) != 0) {
            for (int i = 0; i < 8 - bytes.length; ++i) {
                value |= 0xFFL << (8 * (7 - i));
                new Here().given(i, 0).given(value, 0).checkEq(value, -72057594037927936L);
            }
        }

        for (int i = 0; i < bytes.length; i++) {
            value |= ((long) bytes[bytes.length - i - 1] & 0xFFL) << (8 * i);
            new Here().given(i, 0).given(bytes, new byte[] { (byte) 0xe0, (byte) 0x4f }).given(value, 0).checkEq(value, 79L);
        }

        return value;
    }
}