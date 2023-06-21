package com.tngtech.propertyloader;

import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.List;
import java.util.Properties;
import java.util.Stack;
import com.tngtech.propertyloader.exception.PropertyLoaderException;
import com.tngtech.propertyloader.impl.DefaultPropertyFilterContainer;
import com.tngtech.propertyloader.impl.DefaultPropertyLocationContainer;
import com.tngtech.propertyloader.impl.DefaultPropertySuffixContainer;
import com.tngtech.propertyloader.impl.PropertyFileReader;
import com.tngtech.propertyloader.impl.PropertyLoaderFactory;
import com.tngtech.propertyloader.impl.helpers.HostsHelper;
import com.tngtech.propertyloader.impl.helpers.PropertyFileNameHelper;
import com.tngtech.propertyloader.impl.interfaces.PropertyFilterContainer;
import com.tngtech.propertyloader.impl.interfaces.PropertyLoaderFilter;
import com.tngtech.propertyloader.impl.interfaces.PropertyLoaderOpener;
import com.tngtech.propertyloader.impl.interfaces.PropertyLocationsContainer;
import com.tngtech.propertyloader.impl.interfaces.PropertySuffixContainer;
import org.inlinetest.Here;
import static org.inlinetest.Here.group;

public class M {
    private static final String INCLUDE_KEY = "$include";

    private String[] collectIncludesAndRemoveKey(Properties properties) {
        String[] includes = new String[] {};
        if (properties.containsKey(INCLUDE_KEY)) {
            includes = properties.getProperty(INCLUDE_KEY).split(",");
            new Here("Unit", 294).given(properties, "Properties2.xml").checkEq(includes, new String[] { "testForRecursiveIncludes2", "toBeIncluded" });
            properties.remove(INCLUDE_KEY);
        }
        return includes;
    }
}