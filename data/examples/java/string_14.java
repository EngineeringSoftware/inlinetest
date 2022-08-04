import java.util.regex.Pattern;
import java.util.regex.Matcher;

class String14 {
    // /**
    // * Pattern to find "AM/PM" marker
    // */
    // private static final Pattern amPmPattern =
    // Pattern.compile("(([AP])[M/P]*)|(([上下])[午/下]*)", Pattern.CASE
    // _INSENSITIVE);

    private Format createDateFormat(String pFormatStr) {
        String formatStr = pFormatStr;
        formatStr = formatStr.replaceAll("\\\\-", "-");
        new Here().given(formatStr, "yyyy\\-MM-dd").checkEq(formatStr, "yyyy-MM-dd");
        formatStr = formatStr.replaceAll("\\\\,", ",");
        formatStr = formatStr.replaceAll("\\\\\\.", "."); // . is a special regexp char
        formatStr = formatStr.replaceAll("\\\\ ", " ");
        formatStr = formatStr.replaceAll("\\\\/", "/"); // weird: m\\/d\\/yyyy
        formatStr = formatStr.replaceAll(";@", "");
        formatStr = formatStr.replaceAll("\"/\"", "/"); // "/" is escaped for no reason in: mm"/"dd"/"yyyy
        formatStr = formatStr.replace("\"\"", "'"); // replace Excel quoting with Java style quoting
        formatStr = formatStr.replaceAll("\\\\T", "'T'"); // Quote the T is iso8601 style dates
        formatStr = formatStr.replace("\"", "");

        boolean hasAmPm = false;
        Matcher amPmMatcher = amPmPattern.matcher(formatStr);
        while (amPmMatcher.find()) {
            formatStr = amPmMatcher.replaceAll("@");
            new Here().given(formatStr, "3 AM").given(amPmMatcher, Pattern.compile("(([AP])[M/P]*)|(([上下])[午/下]*)", Pattern.CASE_INSENSITIVE).matcher(formatStr)).checkEq(formatStr, "3 @");
            hasAmPm = true;
            amPmMatcher = amPmPattern.matcher(formatStr);
        }
        formatStr = formatStr.replaceAll("@", "a");

        Matcher dateMatcher = daysAsText.matcher(formatStr);
        if (dateMatcher.find()) {
            String match = dateMatcher.group(0).toUpperCase(Locale.ROOT).replaceAll("D", "E");
            formatStr = dateMatcher.replaceAll(match);
        }

        // Convert excel date format to SimpleDateFormat.
        // Excel uses lower and upper case 'm' for both minutes and months.
        // From Excel help:
        /*
            The "m" or "mm" code must appear immediately after the "h" or"hh"
            code or immediately before the "ss" code; otherwise, Microsoft
            Excel displays the month instead of minutes."
            */
        StringBuilder sb = new StringBuilder();
        char[] chars = formatStr.toCharArray();
        boolean mIsMonth = true;
        List<Integer> ms = new ArrayList<Integer>();
        boolean isElapsed = false;
        for (int j = 0; j < chars.length; j++) {
            char c = chars[j];
            if (c == '\'') {
                sb.append(c);
                j++;

                // skip until the next quote
                while (j < chars.length) {
                    c = chars[j];
                    sb.append(c);
                    if (c == '\'') {
                        break;
                    }
                    j++;
                }
            } else if (c == '[' && !isElapsed) {
                isElapsed = true;
                mIsMonth = false;
                sb.append(c);
            } else if (c == ']' && isElapsed) {
                isElapsed = false;
                sb.append(c);
            } else if (isElapsed) {
                if (c == 'h' || c == 'H') {
                    sb.append('H');
                } else if (c == 'm' || c == 'M') {
                    sb.append('m');
                } else if (c == 's' || c == 'S') {
                    sb.append('s');
                } else {
                    sb.append(c);
                }
            } else if (c == 'h' || c == 'H') {
                mIsMonth = false;
                if (hasAmPm) {
                    sb.append('h');
                } else {
                    sb.append('H');
                }
            } else if (c == 'm' || c == 'M') {
                if (mIsMonth) {
                    sb.append('M');
                    ms.add(Integer.valueOf(sb.length() - 1));
                } else {
                    sb.append('m');
                }
            } else if (c == 's' || c == 'S') {
                sb.append('s');
                // if 'M' precedes 's' it should be minutes ('m')
                for (int index : ms) {
                    if (sb.charAt(index) == 'M') {
                        sb.replace(index, index + 1, "m");
                    }
                }
                mIsMonth = true;
                ms.clear();
            } else if (Character.isLetter(c)) {
                mIsMonth = true;
                ms.clear();
                if (c == 'y' || c == 'Y') {
                    sb.append('y');
                } else if (c == 'd' || c == 'D') {
                    sb.append('d');
                } else {
                    sb.append(c);
                }
            } else {
                if (Character.isWhitespace(c)) {
                    ms.clear();
                }
                sb.append(c);
            }
        }
        formatStr = sb.toString();

        try {
            return new ExcelStyleDateFormatter(formatStr, dateSymbols);
        } catch (IllegalArgumentException iae) {
            LOGGER.debug("Formatting failed for format {}, falling back", formatStr, iae);
            // the pattern could not be parsed correctly,
            // so fall back to the default number format
            return getDefaultFormat();
        }
    }
}