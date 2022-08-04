package org.inlinetest;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.github.javaparser.JavaParser;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.ImportDeclaration;
import com.github.javaparser.ast.Modifier.Keyword;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.Name;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.ObjectCreationExpr;
import com.github.javaparser.ast.expr.StringLiteralExpr;
import com.github.javaparser.ast.expr.UnaryExpr;
import com.github.javaparser.ast.expr.VariableDeclarationExpr;
import com.github.javaparser.ast.stmt.AssertStmt;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.ExpressionStmt;
import com.github.javaparser.ast.stmt.ForEachStmt;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.stmt.SwitchEntry;
import com.github.javaparser.ast.type.Type;
import com.github.javaparser.ast.type.VoidType;
import com.github.javaparser.ast.visitor.ModifierVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

public class InlineTestRunnerSourceCode {
    static final String ClassNameStr = "Here";
    static final String CheckEqStr = "checkEq";
    static final String CheckTrueStr = "checkTrue";
    static final String CheckFalseStr = "checkFalse";
    static final String GivenStr = "given";

    /**
     * mvn package
     * mvn exec:java -Dexec.mainClass="org.inlinetest.InlineTestRunnerSourceCode"
     * -Dexec.args="--input_file=/home/liuyu/projects/inlinetest-research/misc/demo/StringManipulation.java
     * --assertion_style=assert"
     * 
     * @param args input file path
     */
    public static void main(String[] args) {
        HashMap<String, String> params = convertToKeyValuePair(args);
        String inputFile = params.get("input_file");
        Path inputFilePath = Paths.get(inputFile).toAbsolutePath();
        if (!Files.exists(inputFilePath)) {
            new RuntimeException("input file does not exist");
            return;
        }
        String modifiedMode = params.get("modified_mode");
        String assertionStyle = params.get("assertion_style");

        String publicClassName = inputFilePath.getFileName().toString().split(".java")[0];
        String inputFolder = inputFilePath.getParent().toFile().toString();

        if (modifiedMode == null || modifiedMode.equals("default")) {
            // do not change source file
        } else if (modifiedMode.equals("guard")) {
            // add inline test into a if statement guard
            // e.g. if(enableInlineTest){inlineTest1()}
            guardTest(inputFilePath.toAbsolutePath().toString());
        } else {
            new RuntimeException("modified_mode: " + modifiedMode + " is not supported");
        }

        if (assertionStyle == null){
            assertionStyle = "assert";
        } else if (!assertionStyle.equals("junit") && !assertionStyle.equals("assert")){
            new RuntimeException("assertion_style: " + assertionStyle + " is not supported");
        }

        String testClassName = publicClassName + "Test";
        String testOutputFile = inputFolder + "/" + testClassName + ".java";
        extractTest(inputFilePath.toAbsolutePath().toString(), testOutputFile, publicClassName, testClassName,
                assertionStyle);
    }

    private static HashMap<String, String> convertToKeyValuePair(String[] args) {
        HashMap<String, String> params = new HashMap<>();

        for (String arg : args) {
            String[] splitFromEqual = arg.split("=");
            String key = splitFromEqual[0].substring(2);
            String value = splitFromEqual[1];
            params.put(key, value);
        }

        return params;
    }

    /***
     * wrap inline test statement with if statement to control inline tests
     * 
     * @param inputFileSource
     * @param outputFile
     */
    private static void guardTest(String inputFileSource) {
        JavaParser javaParser = new JavaParser();

        FileInputStream in = null;
        try {
            in = new FileInputStream(inputFileSource);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return;
        }
        CompilationUnit cu = javaParser.parse(in).getResult().get();
        new WrapConditionMethodVisitor().visit(cu, null);
        try {
            Files.write(Paths.get(inputFileSource), cu.toString().getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static class WrapConditionMethodVisitor extends ModifierVisitor {
        @Override
        public Node visit(MethodCallExpr methodCall, Object arg) {
            boolean isInlineClass = isInlineClass(methodCall);
            if (isInlineClass) {
                Node currentNode = methodCall;
                while (currentNode.getParentNode().isPresent() && !(currentNode instanceof Statement)) {
                    currentNode = methodCall.getParentNode().get();
                }
                if (currentNode.getParentNode().isPresent()) {
                    IfStmt branchStatement = (IfStmt) StaticJavaParser.parseStatement("if(enableInlineTest){"
                        + currentNode.toString() + "}");
                    currentNode.getParentNode().get().replace(currentNode, branchStatement);
                }
                return null;
            } else {
                return methodCall;
            }

        }
    }

    private static boolean isInlineClass(Node node) {
        if (node instanceof ExpressionStmt) {
            return isInlineClass(((ExpressionStmt) node).getExpression());
        } else if (node instanceof MethodCallExpr) {
            if (((MethodCallExpr) node).getScope().isPresent()) {
                return isInlineClass(((MethodCallExpr) node).getScope().get());
            } else {
                return false;
            }
        } else if (node instanceof ObjectCreationExpr) {
            if (((ObjectCreationExpr) node).getTypeAsString().equals(ClassNameStr)) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    /***
     * extract inline tests from input file
     * 
     * @param inputFileSource
     * @param outputFile
     */
    static void extractTest(String inputFileSource, String testOutputFile,
            String publicClassName, String testClassName, String assertionStyle) {
        JavaParser javaParser = new JavaParser();

        FileInputStream in = null;
        try {
            in = new FileInputStream(inputFileSource);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return;
        }

        List<InlineTest> inlineTests = new ArrayList<>();
        CompilationUnit cu = javaParser.parse(in).getResult().get();
        new MethodVisitor(inlineTests).visit(cu, new MethodVisitor.Context());
        String packageName = null;
        if (cu.getPackageDeclaration().isPresent()) {
            packageName = cu.getPackageDeclaration().get().getNameAsString();
        }
        NodeList<ImportDeclaration> imports = cu.getImports();

        CompilationUnit testCU;
        if (assertionStyle.equals("junit")) {
            testCU = buildJunitClass(testClassName, packageName, inlineTests, imports);
        } else if (assertionStyle.equals("assert")) {
            testCU = buildAssertClass(testClassName, packageName, inlineTests, imports);
        } else {
            return;
        }
        try {
            Files.write(Paths.get(testOutputFile), testCU.toString().getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static class MethodVisitor extends VoidVisitorAdapter<MethodVisitor.Context> {
        List<InlineTest> inlineTests;

        public static class Context implements Cloneable {
            HashMap<String, Type> symbolTable = new HashMap<>();

            @Override
            public Context clone() {
                try {
                    Context cloned = (Context) super.clone();
                    cloned.symbolTable = new HashMap<>(symbolTable);
                    return cloned;
                } catch (CloneNotSupportedException e) {
                    throw new RuntimeException(e);
                }
            }
        }

        public MethodVisitor(List<InlineTest> inlineTests) {
            this.inlineTests = inlineTests;
        }

        @Override
        public void visit(ExpressionStmt expressionStmt, Context ctx) {
            super.visit(expressionStmt, ctx);
            if (isInlineClass(expressionStmt)) {
                // Create a new inlineTest
                InlineTest inlineTest = new InlineTest();
                // parse Here()/givens/assertions
                parseInlineTest(expressionStmt, inlineTest, ctx.symbolTable);
                // parse previous statement with the same level
                if (expressionStmt.getParentNode().isPresent()) {
                    Node parentNode = expressionStmt.getParentNode().get();
                    while (!(parentNode instanceof BlockStmt) && !(parentNode instanceof SwitchEntry)) {
                        parentNode = parentNode.getParentNode().get();
                    }
                    if (parentNode instanceof BlockStmt) {
                        BlockStmt blockStmt = (BlockStmt) parentNode;
                        int index = blockStmt.getStatements().indexOf(expressionStmt) - 1;
                        while (index >= 0) {
                            Node prevNode = blockStmt.getStatements().get(index);
                            // previous statement is not expected to be an inline test
                            if (!isInlineClass(prevNode)) {
                                inlineTest.statement.add(prevNode);
                                break;
                            }
                            index -= 1;
                        }
                    } else if (parentNode instanceof SwitchEntry) {
                        SwitchEntry switchEntry = (SwitchEntry) parentNode;
                        int index = switchEntry.getStatements().indexOf(expressionStmt) - 1;
                        while (index >= 0) {
                            Node prevNode = switchEntry.getStatements().get(index);
                            // previous statement is not expected to be an inline test
                            if (!isInlineClass(prevNode)) {
                                inlineTest.statement.add(prevNode);
                                break;
                            }
                            index -= 1;
                        }
                    } else {
                        throw new RuntimeException("to be tested statement should be a statement without control flow");
                    }
                }
                inlineTests.add(inlineTest);
            }
        }

        @Override
        public void visit(BlockStmt blockStmt, Context ctx) {
            Context newCtx = ctx.clone();
            super.visit(blockStmt, newCtx);
        }

        @Override
        public void visit(ForStmt forStmt, Context arg) {
            forStmt.getCompare().ifPresent(l -> l.accept(this, arg));
            forStmt.getInitialization().forEach(p -> p.accept(this, arg));
            forStmt.getUpdate().forEach(p -> p.accept(this, arg));
            forStmt.getComment().ifPresent(l -> l.accept(this, arg));
            forStmt.getBody().accept(this, arg);
        }

        @Override
        public void visit(ForEachStmt forEachStmt, Context ctx) {
            forEachStmt.getIterable().accept(this, ctx);
            forEachStmt.getVariable().accept(this, ctx);
            forEachStmt.getBody().accept(this, ctx);
            forEachStmt.getComment().ifPresent(l -> l.accept(this, ctx));
        }

        @Override
        public void visit(VariableDeclarator VariableDeclarator, Context ctx) {
            super.visit(VariableDeclarator, ctx);
            String varName = VariableDeclarator.getNameAsString();
            Type varType = VariableDeclarator.getType();
            ctx.symbolTable.put(varName, varType);
        }

        @Override
        public void visit(MethodDeclaration methodDeclaration, Context arg) {
            methodDeclaration.getType().accept(this, arg);
            methodDeclaration.getModifiers().forEach(p -> p.accept(this, arg));
            methodDeclaration.getName().accept(this, arg);
            methodDeclaration.getParameters().forEach(p -> p.accept(this, arg));
            methodDeclaration.getReceiverParameter().ifPresent(l -> l.accept(this, arg));
            methodDeclaration.getThrownExceptions().forEach(p -> p.accept(this, arg));
            methodDeclaration.getTypeParameters().forEach(p -> p.accept(this, arg));
            methodDeclaration.getAnnotations().forEach(p -> p.accept(this, arg));
            methodDeclaration.getComment().ifPresent(l -> l.accept(this, arg));
            methodDeclaration.getBody().ifPresent(l -> l.accept(this, arg));
        }

        @Override
        public void visit(Parameter n, Context ctx) {
            ctx.symbolTable.put(n.getNameAsString(), n.getType());
            n.getAnnotations().forEach(p -> p.accept(this, ctx));
            n.getModifiers().forEach(p -> p.accept(this, ctx));
            n.getName().accept(this, ctx);
            n.getType().accept(this, ctx);
            n.getVarArgsAnnotations().forEach(p -> p.accept(this, ctx));
            n.getComment().ifPresent(l -> l.accept(this, ctx));
        }
    }

    private static void parseInlineTest(Node node, InlineTest inlineTest, HashMap<String, Type> symbolTable) {
        if (node instanceof MethodCallExpr) {
            MethodCallExpr methodCall = (MethodCallExpr) node;
            if (methodCall.getName().asString().equals(CheckEqStr)) {
                // checkEq(a, 1);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 2) {
                    throw new RuntimeException("checkEq should have 2 arguments");
                }
                Expression left = args.get(0);
                Expression right = args.get(1);
                // Objects.equals(left, right);

                MethodCallExpr equalsCallExpr = new MethodCallExpr(new NameExpr("Objects"), "equals");
                equalsCallExpr.addArgument(left);
                equalsCallExpr.addArgument(right);

                AssertStmt assertStmt = new AssertStmt(equalsCallExpr);
                inlineTest.assertions.add(assertStmt);

                MethodCallExpr assertEquals = new MethodCallExpr("assertEquals", left, right);
                inlineTest.junitAssertions.add(assertEquals);
            } else if (methodCall.getName().asString().equals(CheckFalseStr)) {
                // checkFalse(a == 2);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 1) {
                    throw new RuntimeException("checkFalse should have 1 arguments");
                }
                Expression left = args.get(0);
                UnaryExpr unaryExpr = new UnaryExpr(left, UnaryExpr.Operator.LOGICAL_COMPLEMENT);
                AssertStmt assertStmt = new AssertStmt(unaryExpr);
                inlineTest.assertions.add(assertStmt);

                MethodCallExpr assertFalse = new MethodCallExpr("assertFalse", left);
                inlineTest.junitAssertions.add(assertFalse);
            } else if (methodCall.getName().asString().equals(CheckTrueStr)) {
                // checkTrue(a == 1);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 1) {
                    throw new RuntimeException("checkTrue should have 1 arguments");
                }
                Expression left = args.get(0);
                AssertStmt assertStmt = new AssertStmt(left);
                inlineTest.assertions.add(assertStmt);

                MethodCallExpr assertTrue = new MethodCallExpr("assertTrue", left);
                inlineTest.junitAssertions.add(assertTrue);
            } else if (methodCall.getName().asString().equals(GivenStr)) {
                // given(a, 1);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 2) {
                    throw new RuntimeException("given should have 2 arguments");
                }
                Expression left = args.get(0);
                // infer the type of the left expression
                Type leftType = symbolTable.getOrDefault(left.toString(), null);
                if (leftType == null) {
                    throw new RuntimeException("left expression in given should be a variable: " + left.toString());
                } else {
                    Expression right = args.get(1);
                    AssignExpr assignExpr = new AssignExpr(new VariableDeclarationExpr(leftType, left.toString()),
                            right,
                            AssignExpr.Operator.ASSIGN);
                    inlineTest.givens.add(assignExpr);
                }
            }
            parseInlineTest(methodCall.getScope().get(), inlineTest, symbolTable);
        } else if (node instanceof ObjectCreationExpr) {
            ObjectCreationExpr objectCreationExpr = (ObjectCreationExpr) node;
            if (objectCreationExpr.getTypeAsString().equals(ClassNameStr)) {
                // new Here()
                if (objectCreationExpr.getArguments().size() > 1) {
                    throw new RuntimeException("new " + ClassNameStr + " should have 0 or 1 arguments");
                } else if (objectCreationExpr.getArguments().size() == 1) {
                    // extract test name
                    Expression arg = objectCreationExpr.getArguments().get(0);
                    if (arg instanceof StringLiteralExpr) {
                        StringLiteralExpr stringLiteralExpr = (StringLiteralExpr) arg;
                        inlineTest.testName = stringLiteralExpr.getValue();
                    }
                }
                // extract line number
                inlineTest.lineNo = objectCreationExpr.getBegin().get().line;
            }
        } else if (node instanceof ExpressionStmt) {
            parseInlineTest(((ExpressionStmt) node).getExpression(), inlineTest, symbolTable);
        }
    }

    private static CompilationUnit buildJunitClass(String className, String packageName, List<InlineTest> inlineTests,
            NodeList<ImportDeclaration> imports) {
        CompilationUnit cu = new CompilationUnit();
        // set the package
        if (packageName != null) {
            cu.setPackageDeclaration(new PackageDeclaration(new Name(packageName)));
        }
        // set the imports
        imports.add(new ImportDeclaration("org.junit.jupiter.api.Test", false, false));
        imports.add(new ImportDeclaration("org.junit.jupiter.api.Assertions", true, true));
        cu.setImports(imports);

        ClassOrInterfaceDeclaration testClass = cu.addClass(className)
                .setPublic(true);
        for (InlineTest inlineTest : inlineTests) {
            testClass.addMember(inlineTest.toJunitMethod());
        }
        return cu;
    }

    private static CompilationUnit buildAssertClass(String className, String packageName,
            List<InlineTest> inlineTests, NodeList<ImportDeclaration> imports) {
        CompilationUnit cu = new CompilationUnit();
        // set the package
        if (packageName != null) {
            cu.setPackageDeclaration(new PackageDeclaration(new Name(packageName)));
        }
        imports.add(new ImportDeclaration("java.util.Objects", false, false));
        cu.setImports(imports);

        ClassOrInterfaceDeclaration testClass = cu.addClass(className)
                .setPublic(true);

        for (InlineTest inlineTest : inlineTests) {
            MethodDeclaration inlineTestMethod = inlineTest.toAssertMethod();
            inlineTestMethod.addModifier(Keyword.STATIC);
            testClass.addMember(inlineTestMethod);
        }

        BlockStmt block = new BlockStmt();
        for (InlineTest inlineTest : inlineTests) {
            block.addStatement(new MethodCallExpr(inlineTest.testName));
        }
        block.addStatement(new MethodCallExpr("System.out.println",
                new StringLiteralExpr("inline tests passed: " + inlineTests.size())));
        MethodDeclaration mainMethod = new MethodDeclaration();
        mainMethod.setName("main").setType(new VoidType()).addModifier(Keyword.PUBLIC).addModifier(Keyword.STATIC)
                .addParameter("String[]", "args")
                .setBody(block);
        testClass.addMember(mainMethod);
        return cu;
    }
}
