package org.inlinetest;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.security.AnyTypePermission;

public class Here {
    public static XStream xstream = new XStream();

    public Here() {
        return;
    }

    public Here(String name) {
        return;
    }

    public Here(int lineNo) {
        return;
    }

    public Here(String name, int lineNo) {
        return;
    }

    public Here checkEq(Object expected, Object actual) {
        return this;
    }

    public Here given(Object variable, Object value) {
        return this;
    }

    public Here checkTrue(Object value) {
        return this;
    }

    public Here checkFalse(Object value) {
        return this;
    }

    public static boolean group() {
        return true;
    }

    static {
        xstream.addPermission(AnyTypePermission.ANY);
    }
}