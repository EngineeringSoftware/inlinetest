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
}
