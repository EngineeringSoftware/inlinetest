from inline import itest
import re

def remove_markup(text, promote_remaining=True, simplify_links=True):
    """Filter out wiki markup from `text`, leaving only text.

    Parameters
    ----------
    text : str
        String containing markup.
    promote_remaining : bool
        Whether uncaught markup should be promoted to plain text.
    simplify_links : bool
        Whether links should be simplified keeping only their description text.

    Returns
    -------
    str
        `text` without markup.

    """
    text = re.sub(RE_P2, '', text)  # remove the last list (=languages)
    itest().given(RE_P2, re.compile(r'(\n\[\[[a-z][a-z][\w-]*:[^:\]]+\]\])+$', re.UNICODE)).given(text, 'aa\n[[aa:bb]]').check_eq(text, 'aa')
    # the wiki markup is recursive (markup inside markup etc)
    # instead of writing a recursive grammar, here we deal with that by removing
    # markup in a loop, starting with inner-most expressions and working outwards,
    # for as long as something changes.
    text = remove_template(text)
    text = remove_file(text)
    iters = 0
    while True:
        old, iters = text, iters + 1
        text = re.sub(RE_P0, '', text)  # remove comments
        itest().given(RE_P0, re.compile(r'<!--.*?-->', re.DOTALL | re.UNICODE)).given(text, r'<!--aaa-->').check_eq(text, '')
        text = re.sub(RE_P1, '', text)  # remove footnotes
        text = re.sub(RE_P9, '', text)  # remove outside links
        text = re.sub(RE_P10, '', text)  # remove math content
        text = re.sub(RE_P11, '', text)  # remove all remaining tags
        text = re.sub(RE_P14, '', text)  # remove categories
        text = re.sub(RE_P5, '\\3', text)  # remove urls, keep description

        if simplify_links:
            text = re.sub(RE_P6, '\\2', text)  # simplify links, keep description only
        # remove table markup
        text = text.replace("!!", "\n|")  # each table head cell on a separate line
        text = text.replace("|-||", "\n|")  # for cases where a cell is filled with '-'
        text = re.sub(RE_P12, '\n', text)  # remove formatting lines
        text = text.replace('|||', '|\n|')  # each table cell on a separate line(where |{{a|b}}||cell-content)
        text = text.replace('||', '\n|')  # each table cell on a separate line
        text = re.sub(RE_P13, '\n', text)  # leave only cell content
        text = re.sub(RE_P17, '\n', text)  # remove formatting lines

        # remove empty mark-up
        text = text.replace('[]', '')
        # stop if nothing changed between two iterations or after a fixed number of iterations
        if old == text or iters > 2:
            break

    if promote_remaining:
        text = text.replace('[', '').replace(']', '')  # promote all remaining markup to plain text

    return text