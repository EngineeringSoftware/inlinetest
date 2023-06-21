package org.inlinetest;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.inlinetest.Constant.StatementType;

import com.github.javaparser.JavaParser;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.UnaryExpr;
import com.github.javaparser.ast.expr.VariableDeclarationExpr;
import com.github.javaparser.ast.stmt.AssertStmt;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.ExpressionStmt;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.type.Type;
import com.github.javaparser.ast.type.VoidType;

public class InlineTest {
    public String testName;
    public int lineNo;
    public int targetStmtLineNo;
    public List<Node> givens;
    public List<Node> statement;
    public Type targetType; // when target statement is assignment stmt, record the type of target in
                            // assignment stmt
    public List<Node> assertions;
    public List<Node> junitAssertions;

    public InlineTest() {
        this.givens = new ArrayList<Node>();
        this.statement = new ArrayList<Node>();
        this.assertions = new ArrayList<Node>();
        this.junitAssertions = new ArrayList<Node>();
    }

    public String toAssert() {
        if (this.statement.size() == 0) {
            return "";
        }

        StringBuilder sb = new StringBuilder();
        // sb.append("@Test\n");
        if (this.testName == null) {
            sb.append("public void testLine" + String.valueOf(lineNo) + "() {\n");
        } else {
            sb.append("public void " + testName + "(){\n");
        }

        for (int i = givens.size() - 1; i >= 0; i--) {
            sb.append(givens.get(i).toString() + "\n");
        }
        for (Node n : statement) {
            sb.append(n.toString() + "\n");
        }
        for (Node n : assertions) {
            sb.append(n.toString() + "\n");
        }
        sb.append("}\n");
        return sb.toString();
    }

    public MethodDeclaration toJunitMethod() {
        if (this.statement.size() == 0) {
            return null;
        }

        // create a method
        if (testName == null) {
            testName = "testLine" + String.valueOf(lineNo);
        }

        String testCaseName = "testLine" + String.valueOf(lineNo);

        // add improts
        BlockStmt block = new BlockStmt();

        // visitor to rename variables
        VariableRenameVisitor.Context context = new VariableRenameVisitor.Context();
        VariableRenameVisitor vrVisitor = new VariableRenameVisitor();

        // add givens
        context.statementType = StatementType.GIVEN;

        // sanity check if variable is initialized
        Set<String> initializedVariables = new HashSet<String>();

        for (int i = givens.size() - 1; i >= 0; i--) {
            Expression expression = (Expression) givens.get(i).clone();
            expression.accept(vrVisitor, context);
            block.addStatement(expression);

            if (givens.get(i) instanceof AssignExpr) {
                Expression target = ((AssignExpr) givens.get(i)).getTarget();
                if (target instanceof VariableDeclarationExpr) {
                    for (VariableDeclarator vd : ((VariableDeclarationExpr) target).getVariables()) {
                        String name = vd.getNameAsString();
                        if (initializedVariables.contains(name)) {
                            throw new RuntimeException("Variable " + name + " is initialized twice");
                        }
                        initializedVariables.add(vd.getNameAsString());
                    }
                }
            }
        }

        // rename variables in target statement if they are renamed in givens
        if (statement.get(0) instanceof Statement) {
            // target statement
            context.statementType = StatementType.TARGET;
            Statement targetStatement = (Statement) statement.get(0).clone();
            // check assignment statement
            if (targetStatement instanceof ExpressionStmt) {
                Expression expressionInside = ((ExpressionStmt) targetStatement).getExpression();
                if (expressionInside instanceof AssignExpr) {
                    Expression target = ((AssignExpr) expressionInside).getTarget();
                    Type targetType = this.targetType;

                    boolean variableInitialized = false;
                    for (Node given : givens) {
                        if (given instanceof AssignExpr) {
                            Expression givenTarget = ((AssignExpr) given).getTarget();
                            if (givenTarget instanceof VariableDeclarationExpr) {
                                for (VariableDeclarator vd : ((VariableDeclarationExpr) givenTarget).getVariables()) {
                                    if (vd.getNameAsString().equals(target.toString())) {
                                        variableInitialized = true;
                                    }
                                }
                            }
                        }
                    }

                    if (!variableInitialized) {
                        if (targetType == null) {
                            throw new RuntimeException("Cannot resolve type of " + target.toString());
                        }
                        targetStatement.accept(vrVisitor, context);
                        if (!Constant.COMPOUND_ASSIGN_OPERATORS
                                .contains(((AssignExpr) expressionInside).getOperator())) {
                            targetStatement = StaticJavaParser
                                    .parseStatement(targetType.toString() + " " + targetStatement.toString());
                        }
                    }
                }
            }
            targetStatement.accept(vrVisitor, context);
            block.addStatement(targetStatement);

            // add assertions
            context.statementType = StatementType.ASSERTION;

            // sanity check if variable is asserted
            Set<String> assertedVariables = new HashSet<String>();

            for (int i = junitAssertions.size() - 1; i >= 0; i--) {
                ExpressionStmt expressionStmt = new ExpressionStmt((Expression) junitAssertions.get(i)).clone();

                Expression expression = expressionStmt.getExpression();
                if (expression instanceof MethodCallExpr) {
                    MethodCallExpr methodCallExpr = (MethodCallExpr) expression;
                    if (methodCallExpr.getNameAsString().equals("assertEquals")) {
                        Expression firstArgument = methodCallExpr.getArgument(0);
                        if (firstArgument instanceof NameExpr) {
                            String name = ((NameExpr) firstArgument).getNameAsString();
                            if (assertedVariables.contains(name)) {
                                throw new RuntimeException("Variable " + name + " is asserted twice");
                            }
                            assertedVariables.add(name);
                        }
                    }
                }
                
                expressionStmt.accept(vrVisitor, context);
                block.addStatement(expressionStmt);
            }
        } else if (statement.get(0) instanceof Expression) {
            // target statement is if condition
            Expression targetExpression = (Expression) statement.get(0);
            for (int i = assertions.size() - 1; i >= 0; i--) {
                // check if there is group()
                // node is expected to be group() or !group()
                Node node = assertions.get(i);
                if (node instanceof AssertStmt) {
                    AssertStmt assertStmt = (AssertStmt) node;
                    Expression expression = assertStmt.getCheck();
                    if (expression instanceof MethodCallExpr) {
                        if (expression.toString().equals("group()")) {
                            // Statement builtAssertStmt = new AssertStmt(new
                            // EnclosedExpr(targetExpression)).clone();
                            Statement builtAssertStmt = new ExpressionStmt(
                                    new MethodCallExpr().setName("assertTrue").addArgument(targetExpression)).clone();
                            builtAssertStmt.accept(vrVisitor, context);
                            block.addStatement(builtAssertStmt);
                        } else {
                            Statement builtAssertStmt = new ExpressionStmt(
                                new MethodCallExpr().setName("assertTrue").addArgument(expression)).clone();
                            builtAssertStmt.accept(vrVisitor, context);
                            block.addStatement(builtAssertStmt);
                        }
                        // else {
                        //     throw new RuntimeException(
                        //             "The expression is not a group() call: " + expression.toString());
                        // }
                    } else if (expression instanceof UnaryExpr) {
                        if (expression.toString().equals("!group()")) {
                            // assertFalse(targetExpression);
                            Statement builtAssertStmt = new ExpressionStmt(
                                    new MethodCallExpr().setName("assertFalse").addArgument(targetExpression)).clone();
                            // UnaryExpr unaryExpr = (UnaryExpr) expression;
                            // Statement builtAssertStmt = new AssertStmt(
                            // new UnaryExpr(new EnclosedExpr(targetExpression),
                            // unaryExpr.getOperator())).clone();
                            builtAssertStmt.accept(vrVisitor, context);
                            block.addStatement(builtAssertStmt);
                        } else {
                            Statement builtAssertStmt = new ExpressionStmt(
                                new MethodCallExpr().setName("assertFalse").addArgument(((UnaryExpr)expression).getExpression())).clone();
                            builtAssertStmt.accept(vrVisitor, context);
                            block.addStatement(builtAssertStmt);
                        }
                        // else {
                        //     throw new RuntimeException(
                        //             "The expression is not a !group() call: " + expression.toString());
                        // }
                    } else {
                        Statement builtAssertStmt = new ExpressionStmt(
                            new MethodCallExpr().setName("assertTrue").addArgument(expression)).clone();
                        builtAssertStmt.accept(vrVisitor, context);
                        block.addStatement(builtAssertStmt);
                    }
                } else {
                    throw new RuntimeException("The node is not an assert statement" + node.toString());
                }
            }
        }
        MethodDeclaration method = new MethodDeclaration();

        method.setName(testCaseName).setType(new VoidType()).setBody(block).addMarkerAnnotation("Test");
        new JavaParser().parseClassOrInterfaceType("Exception").getResult().ifPresent(method::addThrownException);
        return method;
    }

    public MethodDeclaration toAssertMethod() {
        if (this.statement.size() == 0) {
            return null;
        }

        if (testName == null) {
            testName = "testLine" + String.valueOf(lineNo);
        }

        // create a method
        String testCaseName = "testLine" + String.valueOf(lineNo);

        // TODO: add imports
        BlockStmt block = new BlockStmt();
        for (int i = givens.size() - 1; i >= 0; i--) {
            block.addStatement((Expression) givens.get(i));
        }
        for (Node n : statement) {
            // TODO: consider group()
            block.addStatement((Statement) n);
        }
        for (int i = assertions.size() - 1; i >= 0; i--) {
            block.addStatement((Statement) assertions.get(i));
        }
        MethodDeclaration method = new MethodDeclaration();
        method.setName(testCaseName).setType(new VoidType()).setBody(block);
        return method;
    }

    public String toString() {
        if (this.testName == null) {
            return "Test at line " + this.lineNo;
        } else {
            return "Test" + testName + " at line " + this.lineNo;
        }
    }
}
