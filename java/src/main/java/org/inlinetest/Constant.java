package org.inlinetest;

import java.util.Arrays;
import java.util.List;

import com.github.javaparser.ast.expr.AssignExpr;

public class Constant {
    final static List<AssignExpr.Operator> COMPOUND_ASSIGN_OPERATORS = Arrays.asList(AssignExpr.Operator.PLUS,
            AssignExpr.Operator.MINUS,
            AssignExpr.Operator.MULTIPLY, AssignExpr.Operator.DIVIDE, AssignExpr.Operator.BINARY_AND,
            AssignExpr.Operator.BINARY_OR, AssignExpr.Operator.XOR, AssignExpr.Operator.REMAINDER,
            AssignExpr.Operator.LEFT_SHIFT, AssignExpr.Operator.SIGNED_RIGHT_SHIFT,
            AssignExpr.Operator.UNSIGNED_RIGHT_SHIFT);

    // enum type of statement: given statement, target statement, assertion statement
    public enum StatementType {
        GIVEN, TARGET, ASSERTION
    }

    final static String DECLARE_NAME = "itest";
    final static String CHECK_EQ = "checkEq";
    final static String CHECK_TRUE = "checkTrue";
    final static String CHECK_FALSE = "checkFalse";
    final static String GIVEN = "given";
    final static String GROUP = "group";
    final static String ASSERT_TRUE = "assertTrue";
    final static String ASSERT_FALSE = "assertFalse";
    final static List<String> PRIMITIVE_TYPES = Arrays.asList("int", "long", "double", "float", "boolean", "char",
            "byte", "short",
            "String", "java.lang.String", "int[]", "long[]", "double[]", "float[]", "boolean[]", "char[]", "byte[]",
            "short[]",
            "String[]", "java.lang.String[]");
}
