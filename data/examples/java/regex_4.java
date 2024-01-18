import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex4 {
    Pattern patternKeepIncludes = Pattern.compile(".*^\\s*?//\\s*?KEEP INCLUDES.*?\n(.*?)^\\s*// KEEP INCLUDES END.*?\n", Pattern.DOTALL | Pattern.MULTILINE);

    private void checkKeepSections(File file, Map<String, Object> root) {
        if (file.exists()) {
            try {
                String contents = new String(DaoUtil.readAllBytes(file));

                Matcher matcher;

                matcher = patternKeepIncludes.matcher(contents);
                // itest().given(contents, "FieldsK").checkTrue(matcher.matches());
                itest().given(patternKeepIncludes, Pattern.compile(".*^\\s*?//\\s*?KEEP INCLUDES.*?\n(.*?)^\\s*// KEEP INCLUDES END.*?\n", Pattern.DOTALL | Pattern.MULTILINE)).given(contents, "// KEEP INCLUDES\nabc\n// KEEP INCLUDES END\n").given(matcher, null).checkTrue(matcher.matches());
                if (matcher.matches()) {
                    root.put("keepIncludes", matcher.group(1));
                }

                matcher = patternKeepFields.matcher(contents);
                if (matcher.matches()) {
                    root.put("keepFields", matcher.group(1));
                }

                matcher = patternKeepMethods.matcher(contents);
                if (matcher.matches()) {
                    root.put("keepMethods", matcher.group(1));
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}