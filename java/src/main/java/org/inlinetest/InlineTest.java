package org.inlinetest;

import java.util.ArrayList;
import java.util.List;

import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.type.VoidType;

public class InlineTest {
    public String testName;
    public int lineNo;
    public List<Node> givens;
    public List<Node> statement;
    public List<Node> assertions;
    public List<Node> junitAssertions;

    public InlineTest() {
        this.givens = new ArrayList<Node>();
        this.statement = new ArrayList<Node>();
        this.assertions = new ArrayList<Node>();
        this.junitAssertions = new ArrayList<Node>();
    }

    public String toAssert() {
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
        // create a method
        if (testName == null) {
            testName = "testLine" + String.valueOf(lineNo);
        }

        // add improts
        BlockStmt block = new BlockStmt();

        for (int i = givens.size() - 1; i >= 0; i--) {
            block.addStatement((Expression) givens.get(i));
        }
        for (Node n : statement) {
            block.addStatement((Statement) n);
        }
        for (int i = assertions.size() - 1; i >= 0; i--) {
            block.addStatement((Statement) assertions.get(i));
        }
        MethodDeclaration method = new MethodDeclaration();
        method.setName(testName).setType(new VoidType()).setBody(block).addMarkerAnnotation("Test");
        return method;
    }

    public MethodDeclaration toAssertMethod() {
        // create a method
        if (testName == null) {
            testName = "testLine" + String.valueOf(lineNo);
        }

        // TODO: add imports
        BlockStmt block = new BlockStmt();
        for (int i = givens.size() - 1; i >= 0; i--) {
            block.addStatement((Expression) givens.get(i));
        }
        for (Node n : statement) {
            block.addStatement((Statement) n);
        }
        for (int i = assertions.size() - 1; i >= 0; i--) {
            block.addStatement((Statement) assertions.get(i));
        }
        MethodDeclaration method = new MethodDeclaration();
        method.setName(testName).setType(new VoidType()).setBody(block);
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
