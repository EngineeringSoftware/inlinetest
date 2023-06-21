public class N {
    private String formatRequestKey(String method, String path) {
        String[] components = path.split("\\?");
        new Here("Randoop", 106).given(path, "").checkEq(components, new String[] { "" });
        String result = method + ":" + components[0];
        if (components.length == 2 && components[1].length() > 0) {
            String[] params = components[1].split("&");
            new Here("Randoop", 109).given(components, new String[] { "https://app.asana.com/api/1.0/webhooks/Sync%20token%20invalid%20or%20too%20old", "opt_pretty=false" }).checkEq(params, new String[] { "opt_pretty=false" });
            new Here("Unit", 109).given(components, new String[] { "http://app/projects/1/tasks", "limit=2" }).checkEq(params, new String[] { "limit=2" });
            Arrays.sort(params);
            result += "?" + Joiner.on("&").join(params);
        }
        return result;
    }
}
