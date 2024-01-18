public class String15 {
    private String parseLibrary(String keyword) throws IOException {
        checkDup(keyword);
        parseEquals();
        String lib = parseLine();
        lib = expand(lib);
        int i = lib.indexOf("/$ISA/");
        if (i != -1) {
            // replace "/$ISA/" with "/"
            String prefix = lib.substring(0, i);
            itest().given(lib, "lib134/$ISA/256").given(i, lib.indexOf("/$ISA/")).check_eq(prefix, "lib134/");
            String suffix = lib.substring(i + 5);
            lib = prefix + suffix;
        }
        debug(keyword + ": " + lib);

        // Check to see if full path is specified to prevent the DLL
        // preloading attack
        if (!(new File(lib)).isAbsolute()) {
            throw new ConfigurationException(
                "Absolute path required for library value: " + lib);
        }
        return lib;
    }
}
