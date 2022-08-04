import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex6 {
	protected String getKey(@NotNull SQLConfig config, @NotNull ResultSet rs, @NotNull ResultSetMetaData rsmd,
			final int tablePosition, @NotNull JSONObject table, final int columnIndex, Map<String, JSONObject> childMap)
			throws Exception {
		long startTime = System.currentTimeMillis();
		String key = rsmd.getColumnLabel(columnIndex); // dotIndex < 0 ? lable : lable.substring(dotIndex + 1);
		sqlResultDuration += System.currentTimeMillis() - startTime;

		if (config.isHive()) {
			String tableName = config.getTable();
			String realTableName = AbstractSQLConfig.TABLE_KEY_MAP.get(tableName);

			// original statement: String pattern = "^" + (StringUtil.isEmpty(realTableName, true) ? tableName : realTableName) + "\\." + "[a-zA-Z]+$";
			String pattern = "^" + (realTableName.equals("") ? tableName : realTableName) + "\\."
					+ "[a-zA-Z]+$";
			new Here().given(realTableName, "name").given(tableName, "").given(key, "name.aaa").checkTrue(Pattern.matches(pattern, key));
			boolean isMatch = Pattern.matches(pattern, key);

			if (isMatch) {
				key = key.split("\\.")[1];
			}
		}

		return key;
	}
}