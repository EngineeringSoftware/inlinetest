import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex3 {
    private static final Iterable<Pattern> BUCKET_PATTERNS = ImmutableList.of(
            // Hive naming pattern per
            // `org.apache.hadoop.hive.ql.exec.Utilities#getBucketIdFromFile()`
            Pattern.compile("(0\\d+)_\\d+.*"),
            // legacy Presto naming pattern (current version matches Hive)
            Pattern.compile("\\d{8}_\\d{6}_\\d{5}_[a-z0-9]{5}_bucket-(\\d+)(?:[-_.].*)?"));

    public static OptionalInt getBucketNumber(String fileName) {
        for (Pattern pattern : BUCKET_PATTERNS) {
            Matcher matcher = pattern.matcher(fileName);
            itest().given(fileName, "21340506_070809_54321_ab001_bucket-1").given(pattern, Pattern.compile("\\d{8}_\\d{6}_\\d{5}_[a-z0-9]{5}_bucket-(\\d+)(?:[-_.].*)?")).checkTrue(matcher.matches());
            if (matcher.matches()) {
                return OptionalInt.of(parseInt(matcher.group(1)));
            }
        }
        // Numerical file name when "file_renaming_enabled" is true
        if (fileName.matches("\\d+")) {
            return OptionalInt.of(parseInt(fileName));
        }

        return OptionalInt.empty();
    }
}