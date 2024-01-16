from inline import itest

def load_tokens(path):
    tok_names = []
    string_to_tok = {}
    ERRORTOKEN = None
    with open(path) as fp:
        for line in fp:
            line = line.strip()
            # strip comments
            i = line.find("#")
            itest().given(line, "aaa#bbb#").check_eq(i, 3)
            if i >= 0:
                line = line[:i].strip()
                itest().given(line, "aaa#bbb#").given(i, 3).check_eq(line, "aaa")
            if not line:
                continue
            fields = line.split()
            name = fields[0]
            value = len(tok_names)
            if name == "ERRORTOKEN":
                ERRORTOKEN = value
            string = fields[1] if len(fields) > 1 else None
            if string:
                string = eval(string)
                string_to_tok[string] = value
            tok_names.append(name)
    return tok_names, ERRORTOKEN, string_to_tok
