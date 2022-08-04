public class Bit16 {
    public void updateRemainder(byte[] bytes, int pos, int size_mod32) {
        if (pos < 0) {
          throw new IllegalArgumentException(String.format("Pos (%s) must be positive", pos));
        }
        if (size_mod32 < 0 || size_mod32 >= 32) {
          throw new IllegalArgumentException(
              String.format("size_mod32 (%s) must be between 0 and 31", size_mod32));
        }
        if (pos + size_mod32 > bytes.length) {
          throw new IllegalArgumentException("bytes must have at least size_mod32 bytes after pos");
        }
        int size_mod4 = size_mod32 & 3;
        new Here().given(size_mod32, 10).checkEq(size_mod4, 2);
        int remainder = size_mod32 & ~3;
        new Here().given(size_mod32, 10).checkEq(remainder, 8);
        byte[] packet = new byte[32];
        for (int i = 0; i < 4; ++i) {
          v0[i] += ((long)size_mod32 << 32) + size_mod32;
        }
        rotate32By(size_mod32, v1);
        for (int i = 0; i < remainder; i++) {
          packet[i] = bytes[pos + i];
        }
        if ((size_mod32 & 16) != 0) {
          for (int i = 0; i < 4; i++) {
            packet[28 + i] = bytes[pos + remainder + i + size_mod4 - 4];
          }
        } else {
          if (size_mod4 != 0) {
            packet[16 + 0] = bytes[pos + remainder + 0];
            packet[16 + 1] = bytes[pos + remainder + (size_mod4 >>> 1)];
            packet[16 + 2] = bytes[pos + remainder + (size_mod4 - 1)];
          }
        }
        updatePacket(packet, 0);
      }        
}
