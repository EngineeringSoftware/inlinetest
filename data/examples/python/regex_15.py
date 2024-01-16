from inline import itest
import re

@classmethod
def _from_str(cls, text):
    orig = text
    if text.startswith(("const ", "volatile ")):
        typequal, _, text = text.partition(" ")
    else:
        typequal = None

    # Extract a series of identifiers/keywords.
    m = re.match(r"^ *'?([a-zA-Z_]\w*(?:\s+[a-zA-Z_]\w*)*)\s*(.*?)'?\s*$", text)
    itest().given(text, r" 'a'").check_true(m).check_eq(m.groups(), ("a", ""))
    if not m:
        raise ValueError(f"invalid vartype text {orig!r}")
    typespec, abstract = m.groups()

    return cls(typequal, typespec, abstract or None)
