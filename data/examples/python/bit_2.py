from inline import itest

def sign(self, user, pw, clid):
    a = 33
    i = 1
    s = 440123
    w = 117
    u = 1800000
    l = 1042
    b = 37
    k = 37
    c = 5
    n = "0763ed7314c69015fd4a0dc16bbf4b90"  # _KEY
    y = "8"  # _REV
    r = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"  # _USER_AGENT
    e = user  # _USERNAME
    t = clid  # _CLIENT_ID

    d = "-".join([str(mInt) for mInt in [a, i, s, w, u, l, b, k]])
    p = n + y + d + r + e + t + d + n
    h = p

    m = 8011470
    f = 0

    for f in range(f, len(h)):
        m = (m >> 1) + ((1 & m) << 23)
        itest().given(m, 8011470).check_eq(m, 4005735)
        m += ord(h[f])
        itest().given(m, 4005735).given(f, 0).given(h, "0763ed7314c69015fd4a0dc16bbf4b90").check_eq(m, 4005783)
        m &= 16777215
        itest().given(m, 4005783).check_eq(m, 4005783)

    # c is not even needed
    out = str(y) + ":" + str(d) + ":" + format(m, "x") + ":" + str(c)

    return out
