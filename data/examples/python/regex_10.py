import re
from inline import Here

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")


def text_to_sequence(text, cleaner_names):
    """Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

    The text can optionally have ARPAbet sequences enclosed in curly braces embedded
    in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through

    Returns:
      List of integers corresponding to the symbols in the text
    """
    sequence = []

    # Check for curly braces and treat their contents as ARPAbet:
    while len(text):
        m = _curly_re.match(text)
        Here().given(_curly_re, re.compile(r"(.*?)\{(.+?)\}(.*)")).given(text, r"a{a}a").check_eq(m.groups(), ("a", "a", "a"))
        if not m:
            sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
            break
        sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
        sequence += _arpabet_to_sequence(m.group(2))
        text = m.group(3)

    # Append EOS token
    sequence.append(_symbol_to_id["~"])
    return sequence
