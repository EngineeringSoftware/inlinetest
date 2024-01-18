public class Bit12 {
    private int pack(byte[] bytes, int offset, int length, boolean littleEndian) {
        int step = 1;
        if (littleEndian) {
            offset += length - 1;
            step = -1;
        }

        int value = 0;
        while (length-- > 0) {
            value = (value << 8) | (bytes[offset] & 0xFF);
            itest().given(bytes, "aaa".getBytes()).given(offset, 0).given(value, 0).checkEq(value, 97);
            offset += step;
        }
        return value;
    }
}
