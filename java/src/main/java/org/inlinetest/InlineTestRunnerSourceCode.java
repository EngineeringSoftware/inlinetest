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
import java.util.Map;
import java.util.Map.Entry;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.ImportDeclaration;
import com.github.javaparser.ast.Modifier.Keyword;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.ConstructorDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.ArrayCreationExpr;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.BinaryExpr;
import com.github.javaparser.ast.expr.CastExpr;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.IntegerLiteralExpr;
import com.github.javaparser.ast.expr.LambdaExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.Name;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.NullLiteralExpr;
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

        String multipleTestClassesStr;
        if (params.containsKey("multiple_test_classes")) {
            multipleTestClassesStr = params.get("multiple_test_classes");
        } else {
            multipleTestClassesStr = "false";
        }
        boolean multipleTestClasses = Boolean.parseBoolean(multipleTestClassesStr);

        if (params.containsKey("dep_file_path")) {
            String depFilePath = params.get("dep_file_path");
            if (!Files.exists(Paths.get(depFilePath))) {
                new RuntimeException("dep file does not exist: " + depFilePath);
                return;
            }
            try {
                Util.depClassPaths = new String(Files.readAllBytes(Paths.get(depFilePath)));
            } catch (IOException e) {
                throw new RuntimeException();
            }
        }
        if (params.containsKey("app_src_path")) {
            Util.appSrcPath = params.get("app_src_path");
        }

        if (params.containsKey("load_xml")) {
            if (params.get("load_xml").equals("false") || params.get("load_xml").equals("False")) {
                Util.loadXml = false;
            }
        }

        TypeResolver.setup();

        if (modifiedMode == null || modifiedMode.equals("default")) {
            // do not change source file
        } else if (modifiedMode.equals("guard")) {
            // add inline test into a if statement guard
            // e.g. if(enableInlineTest){inlineTest1()}
            guardTest(inputFilePath.toAbsolutePath().toString());
        } else {
            new RuntimeException("modified_mode: " + modifiedMode + " is not supported");
        }

        if (assertionStyle == null) {
            assertionStyle = "assert";
        } else if (!assertionStyle.equals("junit") && !assertionStyle.equals("assert")) {
            new RuntimeException("assertion_style: " + assertionStyle + " is not supported");
        }

        String testClassName = publicClassName + "Test";
        String testOutputFile;
        if (params.containsKey("output_file")) {
            testOutputFile = params.get("output_file");
        } else {
            if (params.containsKey("output_dir")) {
                testOutputFile = params.get("output_dir") + "/" + testClassName + ".java";
            } else {
                testOutputFile = inputFolder + "/" + testClassName + ".java";
            }
        }
        extractTest(inputFilePath.toAbsolutePath().toString(), testOutputFile, publicClassName, testClassName,
                assertionStyle, multipleTestClasses);
    }

    private static HashMap<String, String> convertToKeyValuePair(String[] args) {
        HashMap<String, String> params = new HashMap<>();

        for (String arg : args) {
            String[] splitFromEqual = arg.split("=");
            // key is expected to start with --
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
        FileInputStream in = null;
        try {
            in = new FileInputStream(inputFileSource);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return;
        }
        CompilationUnit cu = StaticJavaParser.parse(in);
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
            boolean isITDeclare = isDeclare(methodCall);
            if (isITDeclare) {
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

    private static boolean isDeclare(Node node) {
        if (node instanceof ExpressionStmt) {
            return isDeclare(((ExpressionStmt) node).getExpression());
        } else if (node instanceof MethodCallExpr) {
            if (((MethodCallExpr) node).getNameAsString().equals(Constant.DECLARE_NAME)) {
                return true;
            }

            if (((MethodCallExpr) node).getScope().isPresent()) {
                return isDeclare(((MethodCallExpr) node).getScope().get());
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
            String publicClassName, String testClassName, String assertionStyle, boolean multipleTestClasses) {
        FileInputStream in = null;
        try {
            in = new FileInputStream(inputFileSource);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return;
        }

        List<InlineTest> inlineTests = new ArrayList<>();
        CompilationUnit cu = StaticJavaParser.parse(in);
        new MethodVisitor(inlineTests).visit(cu, new MethodVisitor.Context());
        String packageName = null;
        if (cu.getPackageDeclaration().isPresent()) {
            packageName = cu.getPackageDeclaration().get().getNameAsString();
        }
        NodeList<ImportDeclaration> imports = cu.getImports();

        if (!multipleTestClasses) {
            // build a test class with inline tests for all target statements
            CompilationUnit testCU;
            if (assertionStyle.equals("junit")) {
                testCU = buildJunitClass(publicClassName, testClassName, packageName, inlineTests, imports);
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
        } else {
            // build test classes with inline tests for each target statement
            Map<Integer, List<InlineTest>> inlineTestsByStatement = new HashMap<>();
            for (InlineTest inlineTest : inlineTests) {
                if (!inlineTestsByStatement.containsKey(inlineTest.targetStmtLineNo)) {
                    inlineTestsByStatement.put(inlineTest.targetStmtLineNo, new ArrayList<>());
                }
                inlineTestsByStatement.get(inlineTest.targetStmtLineNo).add(inlineTest);
            }
            for (Entry<Integer, List<InlineTest>> entry : inlineTestsByStatement.entrySet()) {
                // replace the `last` Test with _<lineNo>Test
                String testClassNameForStatement = publicClassName + "_" + entry.getKey() + "Test";
                String testOutputFileForStatement = testOutputFile.replace("Test.java",
                        "_" + entry.getKey() + "Test.java");
                CompilationUnit testCUForStatement;
                if (assertionStyle.equals("junit")) {
                    testCUForStatement = buildJunitClass(publicClassName, testClassNameForStatement, packageName,
                            entry.getValue(), imports);
                } else if (assertionStyle.equals("assert")) {
                    testCUForStatement = buildAssertClass(testClassNameForStatement, packageName,
                            entry.getValue(), imports);
                } else {
                    return;
                }
                try {
                    Files.write(Paths.get(testOutputFileForStatement), testCUForStatement.toString().getBytes());
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
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
            if (isDeclare(expressionStmt)) {
                // Create a new inlineTest
                InlineTest inlineTest = new InlineTest();
                // parse itest()/givens/assertions
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
                            if (!isDeclare(prevNode)) {
                                // find the target statement
                                if (prevNode instanceof ExpressionStmt) {
                                    Expression expressionInside = ((ExpressionStmt) prevNode).getExpression();
                                    if (expressionInside instanceof AssignExpr) {
                                        Expression target = ((AssignExpr) expressionInside).getTarget();
                                        Type targetType = ctx.symbolTable.getOrDefault(target.toString(), null);
                                        if (targetType == null) {
                                            String targetTypeStr = TypeResolver.sSymbolResolver.calculateType(target)
                                                    .describe();
                                            inlineTest.targetType = Util.getTypeFromStr(targetTypeStr);
                                        } else {
                                            inlineTest.targetType = targetType;
                                        }
                                    }
                                }
                                inlineTest.statement.add(prevNode.removeComment());
                                break;
                            }
                            index -= 1;
                        }
                        if (index == -1 && inlineTest.statement.size() == 0) {
                            if (blockStmt.getParentNode().isPresent()) {
                                Node parent = blockStmt.getParentNode().get();
                                if (parent instanceof IfStmt) {
                                    IfStmt ifStmt = (IfStmt) parent;
                                    if (ifStmt.getThenStmt().equals(blockStmt)) {
                                        inlineTest.statement.add(ifStmt.getCondition());
                                    }
                                }
                            }
                        }
                    } else if (parentNode instanceof SwitchEntry) {
                        SwitchEntry switchEntry = (SwitchEntry) parentNode;
                        int index = switchEntry.getStatements().indexOf(expressionStmt) - 1;
                        while (index >= 0) {
                            Node prevNode = switchEntry.getStatements().get(index);
                            // previous statement is not expected to be an inline test
                            if (!isDeclare(prevNode)) {
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
        public void visit(VariableDeclarator variableDeclarator, Context ctx) {
            super.visit(variableDeclarator, ctx);
            String varName = variableDeclarator.getNameAsString();
            Type varType = variableDeclarator.getType();
            ctx.symbolTable.put(varName, varType);
        }

        @Override
        public void visit(final ConstructorDeclaration n, final Context arg) {
            n.getModifiers().forEach(p -> p.accept(this, arg));
            n.getName().accept(this, arg);
            n.getParameters().forEach(p -> p.accept(this, arg));
            n.getReceiverParameter().ifPresent(l -> l.accept(this, arg));
            n.getThrownExceptions().forEach(p -> p.accept(this, arg));
            n.getTypeParameters().forEach(p -> p.accept(this, arg));
            n.getAnnotations().forEach(p -> p.accept(this, arg));
            n.getComment().ifPresent(l -> l.accept(this, arg));
            n.getBody().accept(this, arg);
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
        public void visit(final LambdaExpr n, final Context arg) {
            n.getParameters().forEach(p -> p.accept(this, arg));
            n.getComment().ifPresent(l -> l.accept(this, arg));
            n.getBody().accept(this, arg);
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

    private static Expression parseNonPrimitiveExpression(Type type, Expression expression) {
        // if the expression is not primitive type, expression represent the path to
        // serialized objects
        // (Route) ITest.xstream.fromXML(Paths.get(System.getProperty("user.dir") +
        // "/.inlinegen/serialized-data/" + "a.xml").toFile())
        return new CastExpr(type, new MethodCallExpr(new NameExpr("ITest.xstream"), "fromXML")
                .addArgument(new MethodCallExpr(new MethodCallExpr(new NameExpr("Paths"), "get")
                        .addArgument(
                                new BinaryExpr().setLeft(
                                        new MethodCallExpr(new NameExpr("System"), "getProperty")
                                                .addArgument(new StringLiteralExpr("user.dir")))
                                        .setOperator(BinaryExpr.Operator.PLUS)
                                        .setRight(
                                                new BinaryExpr()
                                                        .setLeft(new StringLiteralExpr("/.inlinegen/serialized-data/"))
                                                        .setOperator(BinaryExpr.Operator.PLUS)
                                                        .setRight(expression))),
                        "toFile")));

    }

    private static void parseInlineTest(Node node, InlineTest inlineTest, HashMap<String, Type> symbolTable) {
        if (node instanceof MethodCallExpr) {
            MethodCallExpr methodCall = (MethodCallExpr) node;
            if (methodCall.getName().asString().equals(Constant.DECLARE_NAME)) {
                // itest()
                if (methodCall.getArguments().size() >= 3) {
                    throw new RuntimeException(Constant.DECLARE_NAME + " should have arguments less than 3");
                }

                if (methodCall.getArguments().size() == 1) {
                    // extract test name
                    Expression arg = methodCall.getArguments().get(0);
                    if (arg instanceof StringLiteralExpr) {
                        StringLiteralExpr stringLiteralExpr = (StringLiteralExpr) arg;
                        inlineTest.testName = stringLiteralExpr.getValue();
                    } else if (arg instanceof IntegerLiteralExpr) {
                        IntegerLiteralExpr integerLiteralExpr = (IntegerLiteralExpr) arg;
                        inlineTest.targetStmtLineNo = Integer.valueOf(integerLiteralExpr.getValue());
                    } else {
                        throw new RuntimeException(
                                Constant.DECLARE_NAME + " should not have" + arg.getClass().getName() + " as argument");
                    }
                } else if (methodCall.getArguments().size() == 2) {
                    // extract test name and target line number
                    Expression arg1 = methodCall.getArguments().get(0);
                    Expression arg2 = methodCall.getArguments().get(1);
                    if (arg1 instanceof StringLiteralExpr && arg2 instanceof IntegerLiteralExpr) {
                        StringLiteralExpr stringLiteralExpr = (StringLiteralExpr) arg1;
                        IntegerLiteralExpr integerLiteralExpr = (IntegerLiteralExpr) arg2;
                        inlineTest.testName = stringLiteralExpr.getValue();
                        inlineTest.targetStmtLineNo = Integer.valueOf(integerLiteralExpr.getValue());
                    } else {
                        throw new RuntimeException("new " + Constant.DECLARE_NAME + " should not have"
                                + arg1.getClass().getName() + " and " + arg2.getClass().getName() + " as arguments");
                    }
                }
                // extract line number
                inlineTest.lineNo = methodCall.getBegin().get().line;
                // itest().given(...).checkEq(...); is analyzed from the end to the beginning.
                // So when we reach itest(), we finish parsing the inline test.
                return;
            } else if (methodCall.getName().asString().equals(Constant.CHECK_EQ)) {
                // checkEq(a, 1);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 2) {
                    throw new RuntimeException(Constant.CHECK_EQ + " should have 2 arguments");
                }
                // actual value
                Expression left = args.get(0);
                // expected value
                Expression right = args.get(1);
                Expression parsedRight;
                // Objects.equals(left, right);

                MethodCallExpr equalsCallExpr = new MethodCallExpr(new NameExpr("Objects"), "equals");
                equalsCallExpr.addArgument(left);

                Type leftType = symbolTable.getOrDefault(left.toString(), null);
                if (Util.loadXml) {
                    if (leftType == null || Constant.PRIMITIVE_TYPES.contains(leftType.toString())
                            || right instanceof NullLiteralExpr) {
                        parsedRight = right;
                    } else {
                        parsedRight = parseNonPrimitiveExpression(leftType, right);
                    }
                } else {
                    parsedRight = right;
                }
                equalsCallExpr.addArgument(right);
                AssertStmt assertStmt = new AssertStmt(equalsCallExpr);
                inlineTest.assertions.add(assertStmt);

                // assertArrayEquals
                if (left instanceof ArrayCreationExpr || right instanceof ArrayCreationExpr) {
                    MethodCallExpr assertArrayEquals = new MethodCallExpr("assertArrayEquals", parsedRight, left);
                    inlineTest.junitAssertions.add(assertArrayEquals);
                } else {
                    MethodCallExpr assertEquals = new MethodCallExpr("assertEquals", parsedRight, left);
                    inlineTest.junitAssertions.add(assertEquals);
                }
            } else if (methodCall.getName().asString().equals(Constant.CHECK_FALSE)) {
                // checkFalse(a == 2);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 1) {
                    throw new RuntimeException(Constant.CHECK_FALSE + " should have 1 arguments");
                }
                Expression left = args.get(0);
                UnaryExpr unaryExpr = new UnaryExpr(left, UnaryExpr.Operator.LOGICAL_COMPLEMENT);
                AssertStmt assertStmt = new AssertStmt(unaryExpr);
                inlineTest.assertions.add(assertStmt);

                MethodCallExpr assertFalse = new MethodCallExpr("assertFalse", left);
                inlineTest.junitAssertions.add(assertFalse);
            } else if (methodCall.getName().asString().equals(Constant.CHECK_TRUE)) {
                // checkTrue(a == 1);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 1) {
                    throw new RuntimeException(Constant.CHECK_TRUE + " should have 1 arguments");
                }
                Expression left = args.get(0);
                AssertStmt assertStmt = new AssertStmt(left);
                inlineTest.assertions.add(assertStmt);

                MethodCallExpr assertTrue = new MethodCallExpr("assertTrue", left);
                inlineTest.junitAssertions.add(assertTrue);
            } else if (methodCall.getName().asString().equals(Constant.GIVEN)) {
                // given(a, 1);
                List<Expression> args = methodCall.getArguments();
                if (args.size() != 2) {
                    throw new RuntimeException(Constant.GIVEN + " should have 2 arguments");
                }
                Expression left = args.get(0);
                // infer the type of the left expression
                Type leftType = symbolTable.getOrDefault(left.toString(), null);
                if (leftType == null || leftType.isUnknownType()) {
                    try {
                        String leftTypeStr = TypeResolver.sSymbolResolver.calculateType(left).describe();
                        leftType = Util.getTypeFromStr(leftTypeStr);
                    } catch (Exception e) {
                        throw new RuntimeException(
                                "left expression in " + Constant.GIVEN + " should be a variable: " + left.toString()
                                        + " " + e);
                    }
                }
                if (leftType.isWildcardType()) {
                    // change ? super java.lang.String to java.lang.String
                    if (leftType.asWildcardType().getSuperType().isPresent()) {
                        leftType = leftType.asWildcardType().getSuperType().get();
                    } else if (leftType.asWildcardType().getExtendedType().isPresent()) {
                        leftType = leftType.asWildcardType().getExtendedType().get();
                    } else {
                        throw new RuntimeException("left expression in " + Constant.GIVEN
                                + " should be a variable: " + left.toString());
                    }
                }
                Expression right = args.get(1);
                AssignExpr assignExpr;
                // check if the type is primitive or String
                if (Util.loadXml) {
                    if (Constant.PRIMITIVE_TYPES.contains(leftType.toString()) || right instanceof NullLiteralExpr) {
                        assignExpr = new AssignExpr(new VariableDeclarationExpr(leftType, left.toString()),
                                right,
                                AssignExpr.Operator.ASSIGN);
                    } else {
                        // parse the value from xstream to the type
                        // (leftType)ITest.xstream.fromXML(Paths.get(right).toFile())
                        assignExpr = new AssignExpr(new VariableDeclarationExpr(leftType, left.toString()),
                                parseNonPrimitiveExpression(leftType, right),
                                AssignExpr.Operator.ASSIGN);
                    }
                } else {
                    assignExpr = new AssignExpr(new VariableDeclarationExpr(leftType, left.toString()),
                            right,
                            AssignExpr.Operator.ASSIGN);
                }
                inlineTest.givens.add(assignExpr);
            }
            parseInlineTest(methodCall.getScope().get(), inlineTest, symbolTable);
        } else if (node instanceof ExpressionStmt) {
            parseInlineTest(((ExpressionStmt) node).getExpression(), inlineTest, symbolTable);
        }
    }

    private static CompilationUnit buildJunitClass(String testedClass, String className, String packageName,
            List<InlineTest> inlineTests,
            NodeList<ImportDeclaration> imports) {
        CompilationUnit cu = new CompilationUnit();
        // set the package
        if (packageName != null) {
            cu.setPackageDeclaration(new PackageDeclaration(new Name(packageName)));
        }
        // set the imports
        NodeList<ImportDeclaration> testImports = new NodeList<>(imports);
        testImports.add(new ImportDeclaration("org.junit.jupiter.api.Test", false, false));
        testImports.add(new ImportDeclaration("org.junit.jupiter.api.Assertions", true, true));
        testImports.add(new ImportDeclaration("java.nio.file.Paths", false, false));
        testImports.add(new ImportDeclaration("java.util.Objects", false, false));
        testImports.add(new ImportDeclaration("org.inlinetest.ITest", false, false));
        if (packageName != null) {
            testImports.add(new ImportDeclaration(packageName + "." + testedClass, true, true));
        } else {
            testImports.add(new ImportDeclaration(testedClass, true, true));
        }
        cu.setImports(testImports);

        ClassOrInterfaceDeclaration testClass = cu.addClass(className)
                .setPublic(true);

        for (InlineTest inlineTest : inlineTests) {
            try {
                MethodDeclaration testMethod = inlineTest.toJunitMethod();
                if (testMethod != null) {
                    testClass.addMember(inlineTest.toJunitMethod());
                }
            } catch (Exception e) {
                System.err.println("Error when generating test method for " + inlineTest.testName);
                e.printStackTrace();
            }
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
        NodeList<ImportDeclaration> testImports = new NodeList<>(imports);
        testImports.add(new ImportDeclaration("java.util.Objects", false, false));
        testImports.add(new ImportDeclaration("java.nio.file.Paths", false, false));
        testImports.add(new ImportDeclaration("org.inlinetest.ITest", false, false));
        cu.setImports(testImports);

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
