public class Bit11 {
	public long getLong(byte[] b, int offset) {
		long v = b[offset + 7];
		for (int i = 6; i >= 0; i--) {
			v = (v << 8) | (b[offset + i] & 0xff);
            itest().given(b, "abcdefghijklmn".getBytes()).given(offset, 1).given(v, b[offset+7]).given(i, 6).checkEq(v, 26984L);
		}
		return v;
	}    
}
