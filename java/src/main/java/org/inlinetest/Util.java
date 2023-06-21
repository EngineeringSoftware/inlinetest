package org.inlinetest;

import com.github.javaparser.ast.type.ArrayType;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.type.PrimitiveType;
import com.github.javaparser.ast.type.Type;

public class Util {
    static String depClassPaths;
    static String appSrcPath;
    static boolean loadXml = true;

    static Type getTypeFromStr(String input) {
        input = input.trim();

        if (input.equals("int")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.INT);
        } else if (input.equals("boolean")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.BOOLEAN);
        } else if (input.equals("char")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.CHAR);
        } else if (input.equals("byte")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.BYTE);
        } else if (input.equals("short")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.SHORT);
        } else if (input.equals("long")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.LONG);
        } else if (input.equals("float")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.FLOAT);
        } else if (input.equals("double")) {
            return new PrimitiveType().setType(PrimitiveType.Primitive.DOUBLE);
        } else if (input.endsWith("[]")) {
            return new ArrayType(getTypeFromStr(input.substring(0, input.length() - 2)));
        } else {
            return new ClassOrInterfaceType().setName(input);
        }
    }

    public static boolean isConstant(String name) {
        return name.toUpperCase().equals(name);
    }
}
