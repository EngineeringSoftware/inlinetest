package org.inlinetest;

import java.util.Arrays;
import java.util.stream.Collectors;

import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.type.ArrayType;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.type.IntersectionType;
import com.github.javaparser.ast.type.PrimitiveType;
import com.github.javaparser.ast.type.ReferenceType;
import com.github.javaparser.ast.type.Type;
import com.github.javaparser.ast.type.UnionType;
import com.github.javaparser.ast.type.WildcardType;

public class Util {
    static String depClassPaths;
    static String appSrcPath;
    static boolean loadXml = true;

    static Type getTypeFromStr(String input) {
        input = input.trim();

        // Handle primitive types
        switch (input) {
            case "int":
                return new PrimitiveType(PrimitiveType.Primitive.INT);
            case "boolean":
                return new PrimitiveType(PrimitiveType.Primitive.BOOLEAN);
            case "char":
                return new PrimitiveType(PrimitiveType.Primitive.CHAR);
            case "byte":
                return new PrimitiveType(PrimitiveType.Primitive.BYTE);
            case "short":
                return new PrimitiveType(PrimitiveType.Primitive.SHORT);
            case "long":
                return new PrimitiveType(PrimitiveType.Primitive.LONG);
            case "float":
                return new PrimitiveType(PrimitiveType.Primitive.FLOAT);
            case "double":
                return new PrimitiveType(PrimitiveType.Primitive.DOUBLE);
            // Add cases for other primitives as needed
        }

        // Handle array types
        if (input.endsWith("[]")) {
            return new ArrayType(getTypeFromStr(input.substring(0, input.length() - 2)));
        }

        // Handle wildcard types
        if (input.startsWith("?")) {
            WildcardType wildcardType = new WildcardType();
            if (input.startsWith("? extends ")) {
                wildcardType.setExtendedType(new ClassOrInterfaceType().setName(input.substring(10)));
            } else if (input.startsWith("? super ")) {
                wildcardType.setSuperType(new ClassOrInterfaceType().setName(input.substring(8)));
            }
            return wildcardType;
        }

        // Handle union types (for multi-catch)
        if (input.contains("|")) {
            return new UnionType((NodeList<ReferenceType>) Arrays.stream(input.split("\\|"))
                    .map(String::trim)
                    .map(str -> (new ClassOrInterfaceType().setName(str)).asReferenceType())
                    .collect(Collectors.toList()));
        }

        // Handle intersection types (for generics)
        if (input.contains("&")) {
            return new IntersectionType((NodeList<ReferenceType>) Arrays.stream(input.split("&"))
                    .map(String::trim)
                    .map(str -> (new ClassOrInterfaceType().setName(str)).asReferenceType())
                    .collect(Collectors.toList()));
        }

        // Handle generic types (simplified example)
        if (input.contains("<") && input.contains(">")) {
            String baseType = input.substring(0, input.indexOf('<'));
            String typeParam = input.substring(input.indexOf('<') + 1, input.lastIndexOf('>'));
            return new ClassOrInterfaceType()
                    .setName(baseType)
                    .setTypeArguments(getTypeFromStr(typeParam));
        }

        // Handle simple class or interface types
        return new ClassOrInterfaceType().setName(input);
    }

    public static boolean isConstant(String name) {
        return name.toUpperCase().equals(name);
    }
}
