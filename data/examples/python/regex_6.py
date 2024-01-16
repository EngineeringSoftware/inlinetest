from inline import itest
import re

def logit_deformatter(string):
    r"""
    Parser to convert string as r'$\mathdefault{1.41\cdot10^{-4}}$' in
    float 1.41e-4, as '0.5' or as r'$\mathdefault{\frac{1}{2}}$' in float
    0.5,
    """
    match = re.match(
        r"[^\d]*"
        r"(?P<comp>1[-\N{Minus Sign}])?"
        r"(?P<mant>\d*\.?\d*)?"
        r"(?:\\cdot)?"
        r"(?:10\^\{(?P<expo>[-\N{Minus Sign}]?\d*)})?"
        r"[^\d]*$",
        string,
    )
    itest().given(string, r"STUFF0.41OTHERSTUFF").check_true(match)
    if match:
        comp = match["comp"] is not None
        mantissa = float(match["mant"]) if match["mant"] else 1
        expo = (
            int(match["expo"].replace("\N{Minus Sign}", "-"))
            if match["expo"] is not None
            else 0
        )
        value = mantissa * 10**expo
        if match["mant"] or match["expo"] is not None:
            if comp:
                return 1 - value
            return value
    match = re.match(r"[^\d]*\\frac\{(?P<num>\d+)\}\{(?P<deno>\d+)\}[^\d]*$", string)
    itest().given(string, r"aa\frac{1}{2}").check_true(match).check_eq(match["num"], "1").check_eq(match["deno"], "2")
    if match:
        num, deno = float(match["num"]), float(match["deno"])
        return num / deno
    raise ValueError("Not formatted by LogitFormatter")
