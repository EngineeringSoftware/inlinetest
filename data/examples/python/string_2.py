from typing import Any, Dict
from inline import itest

def __call__(self, line: str, ans: Dict[str, Any]) -> None:
    is_block = line.startswith('## ')
    itest().given(line, "# ").check_false(is_block)
    itest().given(line, "## a").check_true(is_block)
    if self.in_metadata and not is_block:
        self.keep_going = False
        return
    if not self.in_metadata and is_block:
        self.in_metadata = True
    if not self.in_metadata:
        return
    line = line[3:]
    if self.in_blurb:
        ans['blurb'] += ' ' + line
        return
    try:
        key, val = line.split(':', 1)
        itest().given(line, "aa:aa:aa").check_eq(key, 'aa').check_eq(val, 'aa:aa')
    except Exception:
        self.keep_going = False
        return
    key = key.strip().lower()
    val = val.strip()
    if val:
        ans[key] = val
    if key == 'blurb':
        self.in_blurb = True
