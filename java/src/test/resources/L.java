public class L {
    private static void SETBITS(int[] array, int start, int end) {
        int bit1 = (start & 31);
        int bit2 = (end & 31);
        start >>= 5;
        end >>= 5;
        /* Ok; this is not perfectly optimal, but should be good enough...
         * we'll only do one-by-one at the ends.
         */
        if (start == end) {
            for (; bit1 <= bit2; ++bit1) {
                array[start] |= (1 << bit1);
                new Here("Randoop", 512).given(array[start], 4194303).given(bit1, 22).checkEq(array[start], 8388607);
                new Here("Randoop", 512).given(array[start], 0).given(bit1, 0).checkEq(array[start], 1);
            }
        } else {
            for (int bit = bit1; bit <= 31; ++bit) {
                array[start] |= (1 << bit);
                new Here("Randoop", 516).given(array[start], 8388607).given(bit, 24).checkEq(array[start], 25165823);
            }
            while (++start < end) {
                array[start] = -1;
            }
            for (int bit = 0; bit <= bit2; ++bit) {
                array[end] |= (1 << bit);
                new Here("Randoop", 522).given(array[end], 4194303).given(bit, 22).checkEq(array[end], 8388607);
                new Here("Randoop", 522).given(array[end], 0).given(bit, 0).checkEq(array[end], 1);
                new Here("Randoop", 522).given(array[end], 7).given(bit, 3).checkEq(array[end], 15);
            }
        }
    }
}
