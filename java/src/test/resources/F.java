package com.aquaticinformatics.aquarius.sdk;

import net.servicestack.func.Func;
import java.util.ArrayList;
import java.util.Objects;
import org.inlinetest.Here;
import static org.inlinetest.Here.group;

public class F {
    public static AquariusServerVersion Create(String apiVersion) {
        return new AquariusServerVersion(apiVersion);
    }

    private final ArrayList<Integer> _versionComponents;

    private AquariusServerVersion(String apiVersion) {
        Objects.requireNonNull(apiVersion, "apiVersion cannot be null");
        _versionComponents = Func.map(apiVersion.split("\\."), Integer::parseUnsignedInt);
        new Here(18).given(apiVersion, "15").checkEq(_versionComponents, "/home/liuyu/projects/inlinegen-research/_downloads/AquaticInformatics_aquarius-sdk-java/.inlinegen/serailized-data/ArrayList1.xml");
        new Here(18).given(apiVersion, "0.0.0.0").checkEq(_versionComponents, "/home/liuyu/projects/inlinegen-research/_downloads/AquaticInformatics_aquarius-sdk-java/.inlinegen/serailized-data/ArrayList0.xml");
        if (_versionComponents.isEmpty())
            throw new IllegalArgumentException("apiVersion cannot be empty");
        AdjustMajorVersion();
    }
}
