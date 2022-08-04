package org.inlinetest;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;
import java.util.Objects;

import org.junit.jupiter.api.Test;

public class InlineTestRunnerSourceCodeTest {
    @Test
    public void testAssertMode() {
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("A.java")).getPath();
        String testPath = inputPath.replace("A.java", "ATest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "A", "ATest", "assert"); 
        assertTrue(new File(getClass().getClassLoader().getResource("ATest.java").getPath()).exists()); 
    }

    @Test
    public void testJunitMode(){
        String inputPath = Objects.requireNonNull(getClass().getClassLoader().getResource("A.java")).getPath();
        String testPath = inputPath.replace("A.java", "ATest.java");
        InlineTestRunnerSourceCode.extractTest(inputPath, testPath, "A", "ATest", "junit"); 
        assertTrue(new File(getClass().getClassLoader().getResource("ATest.java").getPath()).exists());  
    }
}
