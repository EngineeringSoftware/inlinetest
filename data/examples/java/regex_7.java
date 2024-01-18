import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex7 {
    private static final String FORMAT_FLAVOUR = "Component\\.{0}"; // NOI18N
    private static final String FORMAT_SINGLE_VERSION = "Component\\.{0}_{1}\\."; // NOI18N

    private void splitPropertiesToComponents() {
        String flavourRegex = MessageFormat.format(FORMAT_FLAVOUR, graalSelector);
        String graalVersion = gVersion != null ? gVersion : localReg.getGraalVersion();

        if (filteredComponents != null) {
            return;
        }
        filteredComponents = new HashMap<>();

        // known prefixes. Version will not be parsed again for therse.
        Set<String> knownPrefixes = new HashSet<>();

        // already accepted prefixes
        Set<String> acceptedPrefixes = new HashSet<>();

        Pattern flavourPattern = Pattern.compile("^" + flavourRegex, Pattern.CASE_INSENSITIVE);
        Pattern singlePattern = Pattern.compile("^" + singleRegex, Pattern.CASE_INSENSITIVE);

        for (String s : catalogProperties.stringPropertyNames()) {
            String cid;
            String pn;

            int slashPos = s.indexOf('/');
            int secondSlashPos = s.indexOf('/', slashPos + 1);
            int l;

            if (slashPos != -1 && secondSlashPos != -1) {
                if (!flavourPattern.matcher(s).find()) {
                    continue;
                }
                pn = s.substring(slashPos + 1);

                String pref = s.substring(0, secondSlashPos);

                int lastSlashPos = s.indexOf('/', secondSlashPos + 1);
                if (lastSlashPos == -1) {
                    lastSlashPos = secondSlashPos;
                }
                l = lastSlashPos + 1;
                if (knownPrefixes.add(pref)) {
                    try {
                        Version vn = Version.fromString(s.substring(slashPos + 1, secondSlashPos));
                        if (acceptsVersion(vn)) {
                            acceptedPrefixes.add(pref);
                        }
                    } catch (IllegalArgumentException ex) {
                        feedback.verboseOutput("REMOTE_BadComponentVersion", pn);
                    }
                }
                if (!acceptedPrefixes.contains(pref)) {
                    // ignore obsolete versions
                    continue;
                }

            } else {
                Matcher m = singlePattern.matcher(s);
                itest().given(singlePattern, Pattern.compile("^Component\\.1.2.3_selector\\.", Pattern.CASE_INSENSITIVE)).given(s, "component.1.2.3_selector.456").checkTrue(m.find());
                if (!m.find()) {
                    continue;
                }
                // versionless component
                l = m.end();
                // normalized version
                pn = graalVersion.toString() + "/" + s.substring(l);
            }
            int dashPos = s.indexOf("-", l);
            if (dashPos == -1) {
                dashPos = s.length();
            }
            cid = s.substring(l, dashPos);
            String patchedCid = cid.replace("_", "-");
            String patchedPn = pn.replace(cid, patchedCid);
            filteredComponents.computeIfAbsent(patchedCid, (unused) -> new Properties()).setProperty(patchedPn,
                    catalogProperties.getProperty(s));
        }
    }
}