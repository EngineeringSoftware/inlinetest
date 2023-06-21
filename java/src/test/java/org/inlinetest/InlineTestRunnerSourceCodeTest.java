package org.inlinetest;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Objects;

import org.junit.jupiter.api.Test;

public class InlineTestRunnerSourceCodeTest {
    @Test
    public void testAssertMode() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("A.java")).getPath();
        String testPath = inputPath.replace("A.java", "ATest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "A", "ATest", "assert", false);
        assertTrue(new File(getClass().getClassLoader().getResource("ATest.java").getPath()).exists());
    }

    @Test
    public void testJunitMode() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("A.java")).getPath();
        String testPath = inputPath.replace("A.java", "ATest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "A", "ATest", "junit", false);
        assertTrue(new File(getClass().getClassLoader().getResource("ATest.java").getPath()).exists());
    }

    @Test
    public void testAssertModeWithIf() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("B.java")).getPath();
        String testPath = inputPath.replace("B.java", "BTest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "B", "BTest", "junit", false);
        assertTrue(new File(getClass().getClassLoader().getResource("BTest.java").getPath()).exists());
    }

    @Test
    public void testXStream() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("C.java")).getPath();
        String testPath = inputPath.replace("C.java", "CTest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "C", "CTest", "junit", false);
        assertTrue(new File(getClass().getClassLoader().getResource("CTest.java").getPath()).exists());
    }

    @Test
    public void testArrayEquals() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("D.java")).getPath();
        String testPath = inputPath.replace("D.java", "DTest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "D", "DTest", "junit", false);
        assertTrue(new File(getClass().getClassLoader().getResource("DTest.java").getPath()).exists());
    }

    @Test
    public void testMultipleTestClasses() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("E.java")).getPath();
        String testPath = inputPath.replace("E.java", "ETest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "E", "ETest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("E_3Test.java").getPath()).exists());
        assertTrue(new File(getClass().getClassLoader().getResource("E_6Test.java").getPath()).exists());
    }

    @Test
    public void testTargetStmtWithType() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("F.java")).getPath();
        String testPath = inputPath.replace("F.java", "FTest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "F", "FTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("F_18Test.java").getPath()).exists());
    }

    @Test
    public void testVariableType() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("G.java")).getPath();
        String testPath = inputPath.replace("G.java", "GTest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "G", "GTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("G_75Test.java").getPath()).exists());
    }

    @Test
    public void testTypeResolve() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("H.java")).getPath();
        String testPath = inputPath.replace("H.java", "HTest.java");
        Util.appSrcPath = inputPath;
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "H", "HTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("H_320Test.java").getPath()).exists());
    }

    @Test
    public void testKeywordThis() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("I.java")).getPath();
        String testPath = inputPath.replace("I.java", "ITest.java");
        Util.appSrcPath = inputPath;
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "I", "ITest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("I_34Test.java").getPath()).exists());
    }

    @Test
    public void testFieldAccessExpr() throws IOException {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("J.java")).getPath();
        String testPath = inputPath.replace("J.java", "JTest.java");
        String home = System.getProperty("user.home");
        Util.appSrcPath = home
                + "/projects/inlinegen-research/_downloads/uwolfer_gerrit-rest-java-client/src/main/java/com/urswolfer/gerrit/client/rest/http/projects/ProjectsRestClient.java";
        String depFilePath = home
                + "/projects/inlinegen-research/log/teco-randoop-test/uwolfer_gerrit-rest-java-client/randoop-tests/randoop-deps.txt";
        Util.depClassPaths = new String(Files.readAllBytes(Paths.get(depFilePath)));
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "J", "JTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("J_116Test.java").getPath()).exists());
    }

    @Test
    public void testConstant() throws IOException {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("K.java")).getPath();
        String testPath = inputPath.replace("K.java", "KTest.java");
        String home = System.getProperty("user.home");
        Util.appSrcPath = home
                + "/projects/inlinegen-research/_downloads/awslabs_amazon-sqs-java-extended-client-lib/src/main/java";
        String depFilePath = home
                + "/projects/inlinegen-research/log/teco-randoop-test/awslabs_amazon-sqs-java-extended-client-lib/randoop-tests/randoop-deps.txt";
        Util.depClassPaths = new String(Files.readAllBytes(Paths.get(depFilePath)));
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "K", "KTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("K_884Test.java").getPath()).exists());
    }

    @Test
    public void testArrayAccessExpr() throws IOException {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("L.java")).getPath();
        String testPath = inputPath.replace("L.java", "LTest.java");
        String home = System.getProperty("user.home");
        Util.appSrcPath = home + "/projects/inlinegen-research/_downloads/FasterXML_woodstox/src/main/java";
        String depFilePath = home
                + "/projects/inlinegen-research/log/teco-randoop-test/FasterXML_woodstox/randoop-tests/randoop-deps.txt";
        Util.depClassPaths = new String(Files.readAllBytes(Paths.get(depFilePath)));
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "L", "LTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("L_512Test.java").getPath()).exists());
        assertTrue(new File(getClass().getClassLoader().getResource("L_516Test.java").getPath()).exists());
        assertTrue(new File(getClass().getClassLoader().getResource("L_522Test.java").getPath()).exists());
    }

    @Test
    public void testConstantInTestedClass() throws IOException {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("M.java")).getPath();
        String testPath = inputPath.replace("M.java", "MTest.java");
        String home = System.getProperty("user.home");
        Util.appSrcPath = home + "/projects/inlinegen-research/_downloads/TNG_property-loader/src/main/java";
        String depFilePath = home
                + "/projects/inlinegen-research/log/teco-randoop-test/TNG_property-loader/randoop-tests/randoop-deps.txt";
        Util.depClassPaths = new String(Files.readAllBytes(Paths.get(depFilePath)));
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "M", "MTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("M_294Test.java").getPath()).exists());
    }

    @Test
    public void testArrayNoRename() throws IOException {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("N.java")).getPath();
        String testPath = inputPath.replace("N.java", "NTest.java");
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "N", "NTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("N_109Test.java").getPath()).exists());
    }

    @Test
    public void testMalformedWrongVariable() throws IOException {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("O.java")).getPath();
        String testPath = inputPath.replace("O.java", "OTest.java");
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "O", "OTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("O_235Test.java").getPath()).exists());
        assertTrue(new File(getClass().getClassLoader().getResource("O_236Test.java").getPath()).exists());
    }

    @Test
    public void testMalformedWrongTargetStmt() throws IOException {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("P.java")).getPath();
        String testPath = inputPath.replace("P.java", "PTest.java");
        TypeResolver.setup();
        // assert RuntimeException is thrown
        assertThrows(RuntimeException.class, () -> {
            InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "P", "PTest", "junit", true);
        });
    }

    @Test
    public void testKeywordThis2() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("Q.java")).getPath();
        String testPath = inputPath.replace("Q.java", "QTest.java");
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "Q", "QTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("Q_28Test.java").getPath()).exists());
    }

    @Test
    public void testIfCondition() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("R.java")).getPath();
        String testPath = inputPath.replace("R.java", "RTest.java");
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "R", "RTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("R_182Test.java").getPath()).exists());
    }

    @Test
    public void testMethodCall() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("RevisionApiResetClient.java")).getPath();
        String testPath = inputPath.replace("RevisionApiResetClient.java", "RevisionApiResetClientTest.java");
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "RevisionApiResetClient", "RevisionApiResetClientTest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("RevisionApiResetClient_9Test.java").getPath()).exists());
        assertTrue(new File(getClass().getClassLoader().getResource("RevisionApiResetClient_11Test.java").getPath()).exists());
    }

    @Test
    public void testEmptyVariableType() throws IOException {
        // TODO: When the variable is com.github.javaparser.ast.type.UnknownType, we cannot get the type name
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("S.java")).getPath();
        String testPath = inputPath.replace("S.java", "STest.java");
        String home = System.getProperty("user.home");
        Util.appSrcPath = home + "/projects/inlinegen-research/_downloads/finos_messageml-utils/src/main/java";
        String depFilePath = home
                + "/projects/inlinegen-research/log/teco-randoop-test/finos_messageml-utils/randoop-tests/randoop-deps.txt";
        Util.depClassPaths = new String(Files.readAllBytes(Paths.get(depFilePath)));
        TypeResolver.setup();
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "S", "STest", "junit", true);
        assertTrue(new File(getClass().getClassLoader().getResource("S_148Test.java").getPath()).exists());
        // laod the test file and check if the variable type is empty
        String testFile = new String(Files.readAllBytes(Paths.get(getClass().getClassLoader().getResource("S_148Test.java").getPath())));
    }
}
