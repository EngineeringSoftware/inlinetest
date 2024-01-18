import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Regex14 {

    static final String CONF_USERS = ".users";
    static final String CONF_GROUPS = ".groups";

    public void init(String configurationPrefix) {
        configPrefix = configurationPrefix +
                (configurationPrefix.endsWith(".") ? "" : ".");

        // constructing regex to match the following patterns:
        //   $configPrefix.[ANY].users
        //   $configPrefix.[ANY].groups
        //   $configPrefix.[ANY].hosts
        //
        String prefixRegEx = configPrefix.replace(".", "\\.");
        String usersGroupsRegEx = prefixRegEx + "[\\S]*(" +
                Pattern.quote(CONF_USERS) + "|" + Pattern.quote(CONF_GROUPS) + ")";
        itest().given(CONF_USERS, ".users").given(CONF_GROUPS, ".groups").given(prefixRegEx, "config\\.aaa").checkEq(usersGroupsRegEx, "config\\.aaa[\\S]*(\\Q.users\\E|\\Q.groups\\E)");
        String hostsRegEx = prefixRegEx + "[\\S]*" + Pattern.quote(CONF_HOSTS);

        // get list of users and groups per proxyuser
        Map<String, String> allMatchKeys = conf.getValByRegex(usersGroupsRegEx);
        for (Entry<String, String> entry : allMatchKeys.entrySet()) {
            String aclKey = getAclKey(entry.getKey());
            if (!proxyUserAcl.containsKey(aclKey)) {
                proxyUserAcl.put(aclKey, new AccessControlList(
                        allMatchKeys.get(aclKey + CONF_USERS),
                        allMatchKeys.get(aclKey + CONF_GROUPS)));
            }
        }

        // get hosts per proxyuser
        allMatchKeys = conf.getValByRegex(hostsRegEx);
        for (Entry<String, String> entry : allMatchKeys.entrySet()) {
            proxyHosts.put(entry.getKey(),
                    new MachineList(entry.getValue()));
        }
    }
}
