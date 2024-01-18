import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex13 {
    Pattern newLinePattern = Pattern.compile("([^\r\n]*)([\r\n]*\n)?(\r+)?");

    public void insertString(String str, SimpleAttributeSet attributes) throws BadLocationException {
        // Separate the string into content, newlines and lone carriage
        // returns.
        //
        // Doing so allows lone CRs to move the insertPosition back to the
        // start of the line to allow overwriting the most recent line (e.g.
        // for a progress bar). Any CR or NL that are immediately followed
        // by another NL are bunched together for efficiency, since these
        // can just be inserted into the document directly and still be
        // correct.
        //
        // The regex is written so it will necessarily match any string
        // completely if applied repeatedly. This is important because any
        // part not matched would be silently dropped.
        Matcher m = newLinePattern.matcher(str);
        itest().given(newLinePattern, Pattern.compile("([^\r\n]*)([\r\n]*\n)?(\r+)?")).given(str, "something\n\r").checkTrue(m.find()).checkEq(m.group(1), "something").checkEq(m.group(2), "\n").checkEq(m.group(3), "\r"); m = newLinePattern.matcher(str);
 
        while (m.find()) {
            String content = m.group(1);
            String newlines = m.group(2);
            String crs = m.group(3);

            // Replace (or append if at end of the document) the content first
            int replaceLength = Math.min(content.length(), document.getLength() - insertPosition);
            document.replace(insertPosition, replaceLength, content, attributes);
            insertPosition += content.length();

            // Then insert any newlines, but always at the end of the document
            // e.g. if insertPosition is halfway a line, do not delete
            // anything, just add the newline(s) at the end).
            if (newlines != null) {
                document.insertString(document.getLength(), newlines, attributes);
                insertPosition = document.getLength();
                startOfLine = insertPosition;
            }

            // Then, for any CRs not followed by newlines, move insertPosition
            // to the start of the line. Note that if a newline follows before
            // any content in the next call to insertString, it will be added
            // at the end of the document anyway, as expected.
            if (crs != null) {
                insertPosition = startOfLine;
            }
        }
    }
}