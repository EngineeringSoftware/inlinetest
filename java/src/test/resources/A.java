import org.inlinetest.Here;

public class A {
    public void process(int a, int b) {
        a = a + b;
        new Here().given(a, 2).given(b, 1).checkEq(a, 3);
        a = a + b;
    }
}
