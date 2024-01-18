import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Regex18 {
    // %[argument_index$][flags][width][.precision][t]conversion
    private static final String formatSpecifier = "%(\\d+\\$)?([-#+ 0,(\\<]*)?(\\d+)?(\\.\\d+)?([tT])?([a-zA-Z%])";

    private static Pattern fsPattern = Pattern.compile(formatSpecifier);

    // Look for format specifiers in the format string.
    private static List<FormatSpecifier> parse(String s)
            throws FormatFlagsConversionMismatchException,
            FormatterNumberFormatException {
        ArrayList<FormatSpecifier> al = new ArrayList<FormatSpecifier>();
        Matcher m = fsPattern.matcher(s);
        itest().given(fsPattern, Pattern.compile("%(\\d+\\$)?([-#+ 0,(\\<]*)?(\\d+)?(\\.\\d+)?([tT])?([a-zA-Z%])")).given(s, "%33$#8.2tf").checkTrue(m.find()).checkEq(m.group(1), "33$").checkEq(m.group(2), "#").checkEq(m.group(3), "8").checkEq(m.group(4), ".2").checkEq(m.group(5), "t").checkEq(m.group(6), "f");
        int i = 0;
        while (i < s.length()) {
            if (m.find(i)) {
                // Anything between the start of the string and the beginning
                // of the format specifier is either fixed text or contains
                // an invalid format string.
                if (m.start() != i) {
                    // Make sure we didn't miss any invalid format specifiers
                    checkText(s.substring(i, m.start()));
                }

                // Expect 6 groups in regular expression
                String[] sa = new String[6];
                for (int j = 0; j < m.groupCount(); j++) {
                    sa[j] = m.group(j + 1);
                }
                al.add(new FormatSpecifier(m.group(0), sa));
                i = m.end();
            } else {
                // No more valid format specifiers. Check for possible invalid
                // format specifiers.
                checkText(s.substring(i));
                // The rest of the string is fixed text
                break;

            }
        }

        return al;
    }
}
