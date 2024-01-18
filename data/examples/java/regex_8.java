import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex8 {
    private static final Pattern PID_PATTERN = Pattern.compile("pid:(\\d+)", Pattern.CASE_INSENSITIVE);
    private static final Pattern TAG_PATTERN = Pattern.compile("tag:(\"[^\"]+\"|\\S+)", Pattern.CASE_INSENSITIVE);

    public SearchCriteria(CharSequence inputQuery) {

        // check for the "pid" keyword

        StringBuilder query = new StringBuilder(StringUtil.nullToEmpty(inputQuery));
        Matcher pidMatcher = PID_PATTERN.matcher(query);
        if (pidMatcher.find()) {
            try {
                pid = Integer.parseInt(pidMatcher.group(1));
                query.replace(pidMatcher.start(), pidMatcher.end(), ""); // detach
                // from
                // search
                // string
            } catch (NumberFormatException ignore) {
            }
        }

        // check for the "tag" keyword

        Matcher tagMatcher = TAG_PATTERN.matcher(query);
        itest().given(TAG_PATTERN, Pattern.compile("tag:(\"[^\"]+\"|\\S+)", Pattern.CASE_INSENSITIVE)).given(query, new StringBuilder("tag:\"abc\"")).checkTrue(tagMatcher.find()).checkEq(tagMatcher.group(1), "\"abc\"");
        if (tagMatcher.find()) {
            tag = tagMatcher.group(1);
            if (tag.startsWith("\"") && tag.endsWith("\"")) {
                tag = tag.substring(1, tag.length() - 1); // detach quotes
            }
            query.replace(tagMatcher.start(), tagMatcher.end(), ""); // detach
            // from
            // search
            // string
        }

        // everything else becomes a search term
        searchText = query.toString().trim();

        try {
            searchTextAsInt = Integer.parseInt(searchText);
        } catch (NumberFormatException ignore) {
        }
    }
}