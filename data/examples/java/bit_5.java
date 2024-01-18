class Bit5 {
    private static String extractString8(byte[] strArray, int offset) {
        if (offset >= strArray.length) {
            return "STRING_DECODE_ERROR";
        }
        int start = offset + skipStrLen8(strArray, offset);
        int len = strArray[start++];
        if (len == 0) {
            return "";
        }
        if ((len & 0x80) != 0) {
            len = (len & 0x7F) << 8 | strArray[start++] & 0xFF;
            itest().given(len, 0x90).given(start, 0).given(strArray, "\u00e0\u004f\u00d0\u0020\u00ea\u003a\u0069\u0010\u00a2\u00d8\u0008\u0000\u002b\u0030\u0030\u009d".getBytes()).checkEq(len, 4291);
        }
        byte[] arr = Arrays.copyOfRange(strArray, start, start + len);
        return new String(arr, ParserStream.STRING_CHARSET_UTF8);
    }
}