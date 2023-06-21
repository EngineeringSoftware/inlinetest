package com.onelogin.sdk.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.joda.time.DateTime;
import org.json.JSONArray;
import org.json.JSONObject;
import org.inlinetest.Here;
import static org.inlinetest.Here.group;

public class R {

    public long id;

    public long externalId;

    public String email;

    public String username;

    public String firstname;

    public String lastname;

    public String distinguishedName;

    public String phone;

    public String company;

    public String department;

    public String title;

    public int status;

    public int state;

    public String memberOf;

    public String samaccountname;

    public String userprincipalname;

    public long groupId;

    public List<Long> roleIds;

    public Map<String, String> customAttributes = new HashMap<String, String>();

    public String openidName;

    public String localeCode;

    public String comment;

    public long directoryId;

    public long managerAdId;

    public long trustedIdPId;

    public long managerUserId;

    public DateTime activatedAt;

    public DateTime createdAt;

    public DateTime updatedAt;

    public DateTime passwordChangedAt;

    public int invalidLoginAttempts;

    public DateTime invitationSentAt;

    public DateTime lastLogin;

    public DateTime lockedUntil;

    public User(JSONObject data) {
        id = data.optLong("id");
        externalId = data.optLong("external_id");
        email = data.optString("email", null);
        username = data.optString("username", null);
        firstname = data.optString("firstname", null);
        lastname = data.optString("lastname", null);
        distinguishedName = data.optString("distinguished_name", null);
        phone = data.optString("phone", null);
        company = data.optString("company", null);
        department = data.optString("department", null);
        title = data.optString("title", null);
        status = data.optInt("status");
        state = data.optInt("state");
        memberOf = data.optString("member_of", null);
        samaccountname = data.optString("samaccountname", null);
        userprincipalname = data.optString("userprincipalname", null);
        groupId = data.optLong("group_id");
        if (!data.isNull("role_id")) {
            roleIds = new ArrayList<Long>();
            JSONArray roleData = data.getJSONArray("role_id");
            for (int i = 0; i < roleData.length(); i++) {
                roleIds.add(roleData.getLong(i));
            }
        }
        customAttributes = readCustomAttributes(data);
        openidName = data.optString("openid_name", null);
        localeCode = data.optString("locale_code", null);
        comment = data.optString("comment", null);
        directoryId = data.optLong("directory_id");
        managerAdId = data.optLong("manager_ad_id");
        trustedIdPId = data.optLong("trusted_idp_id");
        managerUserId = data.optLong("manager_user_id");
        activatedAt = (data.optString("activated_at", null) == null) ? null : DateTime.parse(data.getString("activated_at"));
        createdAt = (data.optString("created_at", null) == null) ? null : DateTime.parse(data.getString("created_at"));
        updatedAt = (data.optString("updated_at", null) == null) ? null : DateTime.parse(data.getString("updated_at"));
        passwordChangedAt = (data.optString("password_changed_at", null) == null) ? null : DateTime.parse(data.getString("password_changed_at"));
        invalidLoginAttempts = data.optInt("invalid_login_attempts");
        invitationSentAt = (data.optString("invitation_sent_at", null) == null) ? null : DateTime.parse(data.getString("invitation_sent_at"));
        lastLogin = (data.optString("last_login", null) == null) ? null : DateTime.parse(data.getString("last_login"));
        lockedUntil = (data.optString("locked_until", null) == null) ? null : DateTime.parse(data.getString("locked_until"));
    }

    public List<Long> getRoleIDs() {
        return roleIds;
    }

    public long getGroupID() {
        return groupId;
    }

    public UserData getUserData() {
        UserData userData = new UserData();
        userData.id = id;
        userData.externalId = externalId;
        userData.email = email;
        userData.username = username;
        userData.firstname = firstname;
        userData.lastname = lastname;
        userData.distinguishedName = distinguishedName;
        userData.phone = phone;
        userData.company = company;
        userData.department = department;
        userData.title = title;
        userData.status = status;
        userData.state = state;
        userData.memberOf = memberOf;
        userData.samaccountname = samaccountname;
        userData.userprincipalname = userprincipalname;
        userData.openidName = openidName;
        userData.localeCode = localeCode;
        userData.comment = comment;
        userData.directoryId = directoryId;
        userData.managerAdId = managerAdId;
        userData.trustedIdPId = trustedIdPId;
        userData.managerUserId = managerUserId;
        return userData;
    }

    public UserMetaData getUserMetaData() {
        UserMetaData userMetaData = new UserMetaData();
        userMetaData.activatedAt = activatedAt;
        userMetaData.createdAt = createdAt;
        userMetaData.updatedAt = updatedAt;
        userMetaData.passwordChangedAt = passwordChangedAt;
        userMetaData.invalidLoginAttempts = invalidLoginAttempts;
        userMetaData.invitationSentAt = invitationSentAt;
        userMetaData.lastLogin = lastLogin;
        userMetaData.lockedUntil = lockedUntil;
        return userMetaData;
    }

    public Map<String, String> getUserCustomAttributes() {
        return customAttributes;
    }

    public Map<String, Object> getUserParams() throws NoSuchFieldException {
        Map<String, Object> userParams = new HashMap<String, Object>();
        userParams.put("external_id", (this.getClass().getField("externalId") == null) ? null : Long.toString(externalId));
        userParams.put("email", email);
        userParams.put("username", username);
        userParams.put("firstname", firstname);
        userParams.put("lastname", lastname);
        userParams.put("distinguished_name", distinguishedName);
        userParams.put("phone", phone);
        userParams.put("company", company);
        userParams.put("department", department);
        userParams.put("title", title);
        userParams.put("status", status);
        userParams.put("state", state);
        userParams.put("member_of", memberOf);
        userParams.put("samaccountname", samaccountname);
        userParams.put("invalid_login_attempts", samaccountname);
        userParams.put("userprincipalname", userprincipalname);
        userParams.put("group_id", (this.getClass().getField("groupId") == null) ? null : Long.toString(groupId));
        userParams.put("openid_name", openidName);
        userParams.put("locale_code", localeCode);
        userParams.put("comment", comment);
        userParams.put("openid_name", openidName);
        userParams.put("directory_id", (this.getClass().getField("directoryId") == null) ? null : Long.toString(directoryId));
        userParams.put("manager_ad_id", (this.getClass().getField("managerAdId") == null) ? null : Long.toString(managerAdId));
        userParams.put("trusted_idp_id", (this.getClass().getField("trustedIdPId") == null) ? null : Long.toString(trustedIdPId));
        userParams.put("manager_user_id", (this.getClass().getField("managerUserId") == null) ? null : Long.toString(managerUserId));
        return userParams;
    }

    private Map<String, String> readCustomAttributes(JSONObject data) {
        JSONObject jsonObject = (data.optJSONObject("custom_attributes") == null) ? null : data.getJSONObject("custom_attributes");
        if (jsonObject == null) {
            return null;
        }
        Map<String, String> map = new HashMap<String, String>();
        for (Object key : jsonObject.keySet()) {
            if (!jsonObject.isNull(String.valueOf(key))) {
                new Here("Unit", 182).given(jsonObject, "0.xml").given(key, "custAttribute1").checkTrue(group());
                map.put((String) key, (String) jsonObject.get(String.valueOf(key)));
            } else {
                map.put((String) key, null);
            }
        }
        return map;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + (int) (groupId ^ (groupId >>> 32));
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        User other = (User) obj;
        if (id != other.id) {
            return false;
        }
        return true;
    }
}
