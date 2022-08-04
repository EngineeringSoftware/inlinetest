from inline import Here

def split_arguments(argstr):
    arguments = []
    current_argument = []
    i = 0

    def finish_arg():
        if current_argument:
            argstr = "".join(current_argument).strip()
            m = re.match(r"(.*(\s+|\*))(\w+)$", argstr)
            Here().given(argstr, r"cls, text").check_eq(m.groups(), ("cls, ", " ", "text"))
            if m:
                typename = m.group(1).strip()
                name = m.group(3)
            else:
                typename = argstr
                name = ""
            arguments.append((typename, name))
            del current_argument[:]

    while i < len(argstr):
        c = argstr[i]
        if c == ",":
            finish_arg()
        elif c == "(":
            p = skip_brackets(argstr[i:], "(", ")")
            current_argument += argstr[i : i + p]
            i += p - 1
        else:
            current_argument += c
        i += 1
    finish_arg()
    return arguments
