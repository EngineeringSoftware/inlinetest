import org.inlinetest.Here;
import static org.inlinetest.Here.group;

class B {
    public void m(int a, int b){
        if (a >> 1 > 1){
            new Here().given(a, 2).checkFalse(group());
            a = b + 1;
        }
    }
}