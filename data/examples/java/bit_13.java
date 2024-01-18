public class Bit13 {
    /**
     * The internal field corresponding to the serialField "bits".
     */
    @CompilationFinal(dimensions = 1) private long[] words;

    public int hashCode() {
        long h = 1234;
        for (int i = words.length; --i >= 0;) {
            h ^= words[i] * (i + 1);
            itest().given(words, new long[]{1L, 2L}).given(h, 1234L).given(i, words.length - 1).checkEq(h, 1238L);
        }
        return (int) ((h >> 32) ^ h);
    }
}
