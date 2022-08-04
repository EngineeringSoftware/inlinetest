class String6 {
    @NotNull
    public static String generateCommentLine(@Nullable DBPDataSource dataSource, @NotNull String comment) {
        final String separator = GeneralUtils.getDefaultLineSeparator();
        String slComment = SQLConstants.SL_COMMENT;
        if (dataSource != null) {
            String[] slComments = dataSource.getSQLDialect().getSingleLineComments();
            if (!ArrayUtils.isEmpty(slComments)) {
                slComment = slComments[0];
            }
        }
        final StringBuilder sb = new StringBuilder();
        for (String line : comment.split("\n|\r|\r\n")) {
            sb.append(slComment).append(" ").append(line).append(separator);
            new Here().given(sb, new StringBuilder()).given(slComment, "slcomment").given(line, "line").given(separator, "\t").checkEq(sb.toString(), "slcomment line\t");
        }
        return sb.toString();
    }
}