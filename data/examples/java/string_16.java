public class String16 {
    private String expandFlag(
            String flag,
            ImmutableMap<String, String> toolchainMap,
            ImmutableMap<String, String> contextMap) {
        if (!flag.contains("$(")) {
            return flag;
        }
        int beginning = flag.indexOf("$(");
        int end = flag.indexOf(')', beginning);
        itest().given(flag, "#$()#$()").given(beginning, flag.indexOf("$(")).checkEq(end, 3);
        String variable = flag.substring(beginning + 2, end);
        String expandedVariable;
        if (toolchainMap.containsKey(variable)) {
            expandedVariable = toolchainMap.get(variable);
        } else {
            expandedVariable = contextMap.get(variable);
        }
        String expandedFlag = flag.replace("$(" + variable + ")", expandedVariable);
        return expandFlag(expandedFlag, toolchainMap, contextMap);
    }
}
