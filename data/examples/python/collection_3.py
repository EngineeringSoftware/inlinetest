from inline import itest

def alphanumeric_encoding(str):
    code_list = [alphanum_list.index(i) for i in str]
    code = ""
    for i in range(1, len(code_list), 2):
        c = bin(code_list[i - 1] * 45 + code_list[i])[2:]
        itest().given(code_list, [1, 2]).given(i, 1).check_eq(c, "101111")
        c = "0" * (11 - len(c)) + c
        itest().given(c, "101111").check_eq(c, "00000101111")
        code += c
    if i != len(code_list) - 1:
        c = bin(code_list[-1])[2:]
        c = "0" * (6 - len(c)) + c
        code += c

    return code
