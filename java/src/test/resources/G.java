public class G {
    /**
     * Raw offset (in <code>mRawAttrs</code>) of the first attribute
     * instance that was created through default value expansion.
     */
    private final int mDefaultOffset;

    public G(String[] rawAttrs, int defOffset) {
        mRawAttrs = rawAttrs;
        mAttrMap = null;
        mAttrHashSize = 0;
        mAttrSpillEnd = 0;
        mDefaultOffset = (defOffset << 2);
        new Here("Randoop", 75).given(defOffset, 524288).checkEq(mDefaultOffset, 2097152);
        new Here("Randoop", 75).given(defOffset, 100000).checkEq(mDefaultOffset, 400000);
        new Here("Randoop", 75).given(defOffset, 1952986079).checkEq(mDefaultOffset, -777990276);
        new Here("Randoop", 75).given(defOffset, 512).checkEq(mDefaultOffset, 2048);
    }
}
