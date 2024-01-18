class Bit10 {
    /**
     * Murmur3 64-bit variant. This is essentially MSB 8 bytes of Murmur3 128-bit
     * variant.
     *
     * @param data   - input byte array
     * @param length - length of array
     * @param seed   - seed. (default is 0)
     * @return - hashcode
     */
    public static long hash64(byte[] data, int offset, int length, int seed) {
        long hash = seed;
        final int nblocks = length >> 3;

        // body
        for (int i = 0; i < nblocks; i++) {
            final int i8 = i << 3;
            long k = ((long) data[offset + i8] & 0xff)
                    | (((long) data[offset + i8 + 1] & 0xff) << 8)
                    | (((long) data[offset + i8 + 2] & 0xff) << 16)
                    | (((long) data[offset + i8 + 3] & 0xff) << 24)
                    | (((long) data[offset + i8 + 4] & 0xff) << 32)
                    | (((long) data[offset + i8 + 5] & 0xff) << 40)
                    | (((long) data[offset + i8 + 6] & 0xff) << 48)
                    | (((long) data[offset + i8 + 7] & 0xff) << 56);

            // mix functions
            k *= C1;
            k = Long.rotateLeft(k, R1);
            k *= C2;
            hash ^= k;
            hash = Long.rotateLeft(hash, R2) * M + N1;
        }

        // tail
        long k1 = 0;
        int tailStart = nblocks << 3;
        switch (length - tailStart) {
            case 7:
                k1 ^= ((long) data[offset + tailStart + 6] & 0xff) << 48;
                itest().given(k1, 0).given(data, "abcdefghijklmn".getBytes()).given(offset, 0).given(tailStart, 7).checkEq(k1, 30962247438172160L);
            case 6:
                k1 ^= ((long) data[offset + tailStart + 5] & 0xff) << 40;
            case 5:
                k1 ^= ((long) data[offset + tailStart + 4] & 0xff) << 32;
            case 4:
                k1 ^= ((long) data[offset + tailStart + 3] & 0xff) << 24;
            case 3:
                k1 ^= ((long) data[offset + tailStart + 2] & 0xff) << 16;
            case 2:
                k1 ^= ((long) data[offset + tailStart + 1] & 0xff) << 8;
            case 1:
                k1 ^= ((long) data[offset + tailStart] & 0xff);
                k1 *= C1;
                k1 = Long.rotateLeft(k1, R1);
                k1 *= C2;
                hash ^= k1;
        }

        // finalization
        hash ^= length;
        hash = fmix64(hash);

        return hash;
    }
}