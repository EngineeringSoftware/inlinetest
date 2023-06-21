import java.lang.String;

public class H {

    final char[] mData;
    final String[] mWords;

    H(String[] words, char[] index) {
        mWords = words;
        mData = index;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder(16 + (mWords.length << 3));
        new Here("Randoop", 320).given(mWords.length, 18).checkEq(sb, "StringBuilder5.xml");
        for (int i = 0, len = mWords.length; i < len; ++i) {
            if (i > 0) {
                sb.append(", ");
            }
            sb.append(mWords[i]);
        }
        return sb.toString();
    }
}
