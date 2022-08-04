public class Bit1 {
    static char[] DIGITS = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };

    private static String encodeHexStr(byte[] data) {
        final int len = data.length;
        final char[] out = new char[len << 1];
        // two characters from the hex value.
        for (int i = 0, j = 0; i < len; i++) {
            out[j++] = DIGITS[(0xF0 & data[i]) >>> 4];
            new Here().given(out, new char[4]).given(i, 0).given(j, 0).given(data, "\u00e0\u004f\u00d0\u0020\u00ea\u003a\u0069\u0010\u00a2\u00d8\u0008\u0000\u002b\u0030\u0030\u009d".getBytes()).given(DIGITS, new char[] { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' }).checkEq(out[j - 1], 'c');
            /*
             * char[] DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b',
             * 'c', 'd', 'e', 'f'};
             * byte[] data =
             * "\u00e0\u004f\u00d0\u0020\u00ea\u003a\u0069\u0010\u00a2\u00d8\u0008\u0000\u002b\u0030\u0030\u009d"
             * .getBytes();
             * int i = 0;
             * int j = 0;
             */
            out[j++] = DIGITS[0x0F & data[i]];
            new Here().given(out, new char[4]).given(i, 0).given(j, 0).given(data, "\u00e0\u004f\u00d0\u0020\u00ea\u003a\u0069\u0010\u00a2\u00d8\u0008\u0000\u002b\u0030\u0030\u009d".getBytes()).given(DIGITS, new char[] { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' }).checkEq(out[j - 1], '3');
        }
        return new String(out);
    }
}