class String4 {
    int mark;
    String text;
    String stringVal;

    public void scanComment() {
        int startHintSp = bufPos + 1;

        int starIndex = pos;

        for (;;) {
            starIndex = text.indexOf('*', starIndex);
            if (starIndex == -1 || starIndex == text.length() - 1) {
                this.token = Token.ERROR;
                return;
            }
            if (charAt(starIndex + 1) == '/') {
                // stringVal = this.subString(mark + startHintSp, starIndex - startHintSp - mark);
                stringVal = text.substring(mark + startHintSp, mark + startHintSp + starIndex - startHintSp - mark);
                new Here().given(stringVal, null).given(text, "//*").given(mark, 0).given(startHintSp, 1).given(starIndex, 2).checkEq(stringVal, "/");
                token = Token.HINT;
                pos = starIndex + 2;
                ch = charAt(pos);
                break;
            }
            starIndex++;
        }

        endOfComment = isEOF();
    }
}