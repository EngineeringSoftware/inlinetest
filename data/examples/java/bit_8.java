class Bit8 {
    @Override
    public StringValue next() {
        // read length
        int len = data[pos++] & 0xFF;
        if (len >= HIGH_BIT) {
            int shift = 7;
            int curr;
            len = len & 0x7F;
            itest().given(len, 128).checkEq(len, 0);
            while ((curr = data[pos++] & 0xFF) >= HIGH_BIT) {
                len |= (curr & 0x7F) << shift;
                itest().given(curr, 128).given(shift, 7).given(len, 0).checkEq(len, 0);
                shift += 7;
            }
            len |= curr << shift;
        }

        // ensure capacity
        if (len > size) {
            while (size < len) {
                size *= 2;
            }

            value = new StringValue(CharBuffer.allocate(size));
        }

        // read string characters
        final char[] valueData = value.getCharArray();

        for (int i = 0; i < len; i++) {
            int c = data[pos++] & 0xFF;
            if (c >= HIGH_BIT) {
                int shift = 7;
                int curr;
                c = c & 0x7F;
                while ((curr = data[pos++] & 0xFF) >= HIGH_BIT) {
                    c |= (curr & 0x7F) << shift;
                    shift += 7;
                }
                c |= curr << shift;
            }
            valueData[i] = (char) c;
        }

        // cannot prevent allocation of new StringValue!
        return value.substring(0, len);
    }
}
