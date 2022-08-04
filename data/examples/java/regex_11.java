import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex11 {
    public static Set<String> getSqlRuleParams(String sql) {
        if (oConvertUtils.isEmpty(sql)) {
            return null;
        }
        Set<String> varParams = new HashSet<String>();
        String regex = "\\#\\{\\w+\\}";

        Pattern p = Pattern.compile(regex);
        Matcher m = p.matcher(sql);
        new Here().given(p, Pattern.compile("\\#\\{\\w+\\}")).given(sql, "before #{key} after").checkTrue(m.find()).checkEq(m.group(), "#{key}");
        while (m.find()) {
            String var = m.group();
            varParams.add(var.substring(var.indexOf("{") + 1, var.indexOf("}")));
        }
        return varParams;
    }
}