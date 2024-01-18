package org.inlinetest;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.security.AnyTypePermission;

public class ITest {
    public static XStream xstream = new XStream();
    public static ITest itest = new ITest();

    private ITest() {
        return;
    }

    public static ITest itest() {
        return itest;
    }

    public static ITest itest(String name, int lineNo) {
        return itest;
    }

    public ITest checkEq(Object expected, Object actual) {
        return itest;
    }

    public ITest given(Object variable, Object value) {
        return itest;
    }

    public ITest checkTrue(Object value) {
        return itest;
    }

    public ITest checkFalse(Object value) {
        return itest;
    }

    public static boolean group() {
        return true;
    }

    static {
        xstream.addPermission(AnyTypePermission.ANY);
    }
}