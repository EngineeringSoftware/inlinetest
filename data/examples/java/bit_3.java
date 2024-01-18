public class Bit3 {
    private static final int MASK_INT_LOWEST_BYTE = 0x000000FF;

    @Nullable
    private int[] readColorTable(int nColors) {
        int nBytes = 3 * nColors;
        int[] tab = null;
        byte[] c = new byte[nBytes];

        try {
            rawData.get(c);

            // TODO: what bounds checks are we avoiding if we know the number of colors?
            // Max size to avoid bounds checks.
            tab = new int[MAX_BLOCK_SIZE];
            int i = 0;
            int j = 0;
            while (i < nColors) {
                int r = ((int) c[j++]) & MASK_INT_LOWEST_BYTE;
                // .given(c[j++], 1).
                itest().given(j, 0).given(c, new byte[512]).given(MASK_INT_LOWEST_BYTE, 0x000000FF).checkEq(r, 0);
                int g = ((int) c[j++]) & MASK_INT_LOWEST_BYTE;
                int b = ((int) c[j++]) & MASK_INT_LOWEST_BYTE;
                tab[i++] = 0xFF000000 | (r << 16) | (g << 8) | b;
                itest().given(r, 1).given(g, 1).given(b, 1).given(i, 0).given(tab, new int[512]).checkEq(tab[i - 1], -16711423);
            }
        } catch (BufferUnderflowException e) {
            if (Log.isLoggable(TAG, Log.DEBUG)) {
                Log.d(TAG, "Format Error Reading Color Table", e);
            }
            header.status = STATUS_FORMAT_ERROR;
        }

        return tab;
    }
}