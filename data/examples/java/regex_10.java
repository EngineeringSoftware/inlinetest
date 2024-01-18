import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex10 {
	static final Pattern CONSTRAINT_PATTERN = Pattern.compile("api \"(.+):(.+):(.+)\"");
    private void loadVersions() {
			String version = this.libraryVersion;
			if (version.endsWith("-SNAPSHOT")) {
				version = version.substring(0, version.lastIndexOf('.')) + ".x";
			}
			String source = this.sourceTemplate.replace("<libraryVersion>", version);
			// try {
				// try (BufferedReader reader = new BufferedReader(
				// 		new InputStreamReader(URI.create(source).toURL().openStream()))) {
					String line;
					while ((line = reader.readLine()) != null) {
						Matcher matcher = CONSTRAINT_PATTERN.matcher(line.trim());
						itest().given(CONSTRAINT_PATTERN, Pattern.compile("api \"(.+):(.+):(.+)\"")).given(line, "api \"o.s.b:s-b:2.7\"").checkTrue(matcher.matches());
						if (matcher.matches()) {
							Map<String, String> groupDependencies = this.dependencyVersions
									.computeIfAbsent(matcher.group(1), (key) -> new HashMap<>());
							groupDependencies.put(matcher.group(2), matcher.group(3));
						}
					// }
			// 	}
			// }
			// catch (IOException ex) {
			// 	throw new GradleException(
			// 			"Failed to load versions from dependency constraints declared in '" + source + "'", ex);
			// }
		}

	}
}