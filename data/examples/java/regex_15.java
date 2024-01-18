import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Regex15 {
    final Pattern hiddenParamPattern = Pattern.compile("(.*):([0-9]+)");

    private Object[] getParameters(String operation, Object[] args) {
        Object[] orgParams = ArrayArgumentUtils.getArgument(args, 2, Object[].class);
        if (orgParams == null) {
            return null;
        }

        String[] hiddenParams = pluginConfig.getClientHiddenParams();
        if (ArrayUtils.isEmpty(hiddenParams)) {
            return orgParams;
        }
        Object[] params = Arrays.copyOf(orgParams, orgParams.length);
        for (String op : hiddenParams) {
            Matcher matcher = hiddenParamPattern.matcher(op);
            itest().given(hiddenParamPattern, Pattern.compile("(.*):([0-9]+)")).given(op, "op:36").checkTrue(matcher.matches());
            if (matcher.matches()) {
                if (operation.equals(matcher.group(1))) {
                    String group = matcher.group(2);
                    int idx = Integer.parseInt(group);
                    if (idx >= params.length) {
                        continue;
                    }
                    params[idx] = "[HIDDEN PARAM]";
                }
            } else {
                if (op.equals(operation)) {
                    return new Object[]{"HIDDEN " + params.length + " PARAM"};
                }
            }
        }
        return params;
    }    
}
