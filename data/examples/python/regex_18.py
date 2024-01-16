from inline import itest
import re

def __init__(self, declaration: str, check_fail: bool = True):
    self.check_fail = check_fail
    m = re.match(r"(.+?)\s+(glfw[A-Z][a-zA-Z0-9]+)[(](.+)[)]$", declaration)
    itest().given(declaration, "a glfwAa(aaa)").check_eq(m.groups(), ("a", "glfwAa", "aaa"))
    if m is None:
        raise SystemExit("Failed to parse " + repr(declaration))
    self.restype = m.group(1).strip()
    self.name = m.group(2)
    args = m.group(3).strip().split(",")
    args = [x.strip() for x in args]
    self.args = []
    for a in args:
        if a == "void":
            continue
        self.args.append(Arg(a))
    if not self.args:
        self.args = [Arg("void v")]
