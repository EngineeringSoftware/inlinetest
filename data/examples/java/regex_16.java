import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Regex16 {
    static final Pattern CONTENT_RANGE_HEADER = Pattern.compile("^bytes (\\d+)-(\\d+)/(\\d+)$");

    /**
     * Attempts to extract the length of the content from the response headers of an open connection.
     *
     * @param connection The open connection.
     * @return The extracted length, or {@link C#LENGTH_UNSET}.
     */
    private static long getContentLength(HttpURLConnection connection) {
        long contentLength = C.LENGTH_UNSET;
        String contentLengthHeader = connection.getHeaderField("Content-Length");
        if (!TextUtils.isEmpty(contentLengthHeader)) {
            try {
                contentLength = Long.parseLong(contentLengthHeader);
            } catch (NumberFormatException e) {
                Log.e(TAG, "Unexpected Content-Length [" + contentLengthHeader + "]");
            }
        }
        String contentRangeHeader = connection.getHeaderField("Content-Range");
        if (!TextUtils.isEmpty(contentRangeHeader)) {
            Matcher matcher = CONTENT_RANGE_HEADER.matcher(contentRangeHeader);
            new Here().given(CONTENT_RANGE_HEADER, Pattern.compile("^bytes (\\d+)-(\\d+)/(\\d+)$")).given(contentRangeHeader, "bytes 12-34/56").checkTrue(matcher.find()).checkEq(matcher.group(1), "12").checkEq(matcher.group(2), "34").checkEq(matcher.group(3), "56");
            if (matcher.find()) {
                try {
                    long contentLengthFromRange =
                        Long.parseLong(matcher.group(2)) - Long.parseLong(matcher.group(1)) + 1;
                    if (contentLength < 0) {
                        // Some proxy servers strip the Content-Length header. Fall back to the length
                        // calculated here in this case.
                        contentLength = contentLengthFromRange;
                    } else if (contentLength != contentLengthFromRange) {
                        // If there is a discrepancy between the Content-Length and Content-Range headers,
                        // assume the one with the larger value is correct. We have seen cases where carrier
                        // change one of them to reduce the size of a request, but it is unlikely anybody would
                        // increase it.
                        Log.w(TAG, "Inconsistent headers [" + contentLengthHeader + "] [" + contentRangeHeader
                            + "]");
                        contentLength = max(contentLength, contentLengthFromRange);
                    }
                } catch (NumberFormatException e) {
                    Log.e(TAG, "Unexpected Content-Range [" + contentRangeHeader + "]");
                }
            }
        }
        return contentLength;
    }    
}
