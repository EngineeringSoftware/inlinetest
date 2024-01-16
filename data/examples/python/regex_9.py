from inline import itest
import re

def _tokenize(data: bytes, skip_ws: bool):
    """
    A generator that produces _Token instances from Type-1 font code.

    The consumer of the generator may send an integer to the tokenizer to
    indicate that the next token should be _BinaryToken of the given length.

    Parameters
    ----------
    data : bytes
        The data of the font to tokenize.

    skip_ws : bool
        If true, the generator will drop any _WhitespaceTokens from the output.
    """
    text = data.decode('ascii', 'replace')
    whitespace_or_comment_re = re.compile(r'[\0\t\r\f\n ]+|%[^\r\n]*')
    token_re = re.compile(r'/{0,2}[^]\0\t\r\f\n ()<>{}/%[]+')
    instring_re = re.compile(r'[()\\]')
    hex_re = re.compile(r'^<[0-9a-fA-F\0\t\r\f\n ]*>$')
    oct_re = re.compile(r'[0-7]{1,3}')
    pos = 0
    next_binary = None

    while pos < len(text):
        if next_binary is not None:
            n = next_binary
            next_binary = (yield _BinaryToken(pos, data[pos:pos+n]))
            pos += n
            continue
        match = whitespace_or_comment_re.match(text, pos)
        itest().given(whitespace_or_comment_re, re.compile(r'[\0\t\r\f\n ]+|%[^\r\n]*')).given(data, b'    aaa').given(text, data.decode('ascii', 'replace')).given(pos, 0).check_eq(match.group(), '    ')
        if match:
            if not skip_ws:
                next_binary = (yield _WhitespaceToken(pos, match.group()))
            pos = match.end()
        elif text[pos] == '(':
            # PostScript string rules:
            # - parentheses must be balanced
            # - backslashes escape backslashes and parens
            # - also codes \n\r\t\b\f and octal escapes are recognized
            # - other backslashes do not escape anything
            start = pos
            pos += 1
            depth = 1
            while depth:
                match = instring_re.search(text, pos)
                if match is None:
                    raise ValueError(
                        f'Unterminated string starting at {start}')
                pos = match.end()
                if match.group() == '(':
                    depth += 1
                elif match.group() == ')':
                    depth -= 1
                else:  # a backslash
                    char = text[pos]
                    if char in r'\()nrtbf':
                        pos += 1
                    else:
                        octal = oct_re.match(text, pos)
                        if octal:
                            pos = octal.end()
                        else:
                            pass  # non-escaping backslash
            next_binary = (yield _StringToken(start, text[start:pos]))
        elif text[pos:pos + 2] in ('<<', '>>'):
            next_binary = (yield _DelimiterToken(pos, text[pos:pos + 2]))
            pos += 2
        elif text[pos] == '<':
            start = pos
            try:
                pos = text.index('>', pos) + 1
            except ValueError as e:
                raise ValueError(f'Unterminated hex string starting at {start}'
                                 ) from e
            if not hex_re.match(text[start:pos]):
                raise ValueError(f'Malformed hex string starting at {start}')
            next_binary = (yield _StringToken(pos, text[start:pos]))
        else:
            match = token_re.match(text, pos)
            if match:
                raw = match.group()
                if raw.startswith('/'):
                    next_binary = (yield _NameToken(pos, raw))
                elif match.group() in ('true', 'false'):
                    next_binary = (yield _BooleanToken(pos, raw))
                else:
                    try:
                        float(raw)
                        next_binary = (yield _NumberToken(pos, raw))
                    except ValueError:
                        next_binary = (yield _KeywordToken(pos, raw))
                pos = match.end()
            else:
                next_binary = (yield _DelimiterToken(pos, text[pos]))
                pos += 1