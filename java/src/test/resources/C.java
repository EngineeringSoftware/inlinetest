import org.inlinetest.Here;
import static org.inlinetest.Here.group;

class C {
    public void m(Person p){
        p.setAge(p.getAge() >> 1);
        new Here().given(p, "a.xml").checkEq(p.getAge(), 1);
    }
}

class Person {
    private String name;
    private int age;
    public Person(String name, int age){
        this.name = name;
        this.age = age;
    }
    public String getName(){
        return name;
    }
    public int getAge(){
        return age;
    }
    public void setAge(int age){
        this.age = age;
    }
}