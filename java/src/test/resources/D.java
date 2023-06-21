public class D {
    private String formatRequestKey(String method, String path) {
        String[] components = path.split("\\?");
        new Here().given(path, "").checkEq(components, new String[] { "" });
        String result = method + ":" + components[0];
        if (components.length == 2 && components[1].length() > 0) {
            String[] params = components[1].split("&");
            new Here().given(components, new String[] { "https://app.asana.com/api/1.0/webhooks/Sync%20token%20invalid%20or%20too%20old", "opt_pretty=false" }).checkEq(params, new String[] { "opt_pretty=false" });
            Arrays.sort(params);
            result += "?" + Joiner.on("&").join(params);
        }
        return result;
    }
}
