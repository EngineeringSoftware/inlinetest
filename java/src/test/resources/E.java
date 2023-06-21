public class E {
    public void process(int a, int b) {
        a = a + b;
        new Here(3).given(a, 2).given(b, 1).checkEq(a, 3);
        new Here(3).given(a, -2).given(b, -1).checkEq(a, -3);
        a = a - b;
        new Here(6).given(a, 2).given(b, 1).checkEq(a, 1);
    } 
}
