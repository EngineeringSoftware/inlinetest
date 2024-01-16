from inline import itest
import re

def _merge_string_group(self, line, string_idx: int):
    """
    Merges string group (i.e. set of adjacent strings) where the first
    string in the group is `line.leaves[string_idx]`.

    Returns:
        Ok(new_line), if ALL of the validation checks found in
        __validate_msg(...) pass.
            OR
        Err(CannotTransform), otherwise.
    """
    LL = line.leaves

    is_valid_index = is_valid_index_factory(LL)

    vresult = self._validate_msg(line, string_idx)
    if isinstance(vresult, Err):
        return vresult

    # If the string group is wrapped inside an Atom node, we must make sure
    # to later replace that Atom with our new (merged) string leaf.
    atom_node = LL[string_idx].parent

    # We will place BREAK_MARK in between every two substrings that we
    # merge. We will then later go through our final result and use the
    # various instances of BREAK_MARK we find to add the right values to
    # the custom split map.
    BREAK_MARK = "@@@@@ BLACK BREAKPOINT MARKER @@@@@"

    QUOTE = LL[string_idx].value[-1]

    def make_naked(string: str, string_prefix: str) -> str:
        """Strip @string (i.e. make it a "naked" string)

        Pre-conditions:
            * assert_is_leaf_string(@string)

        Returns:
            A string that is identical to @string except that
            @string_prefix has been stripped, the surrounding QUOTE
            characters have been removed, and any remaining QUOTE
            characters have been escaped.
        """
        assert_is_leaf_string(string)

        RE_EVEN_BACKSLASHES = r"(?:(?<!\\)(?:\\\\)*)"
        naked_string = string[len(string_prefix) + 1 : -1]
        naked_string = re.sub(
            "(" + RE_EVEN_BACKSLASHES + ")" + QUOTE, r"\1\\" + QUOTE, naked_string
        )
        itest().given(RE_EVEN_BACKSLASHES, r"(?:(?<!\\)(?:\\\\)*)").given(QUOTE, "'").given(naked_string, r"'aaabbb'").check_eq(naked_string, r"\'aaabbb\'")
        return naked_string

    # Holds the CustomSplit objects that will later be added to the custom
    # split map.
    custom_splits = []

    # Temporary storage for the 'has_prefix' part of the CustomSplit objects.
    prefix_tracker = []

    # Sets the 'prefix' variable. This is the prefix that the final merged
    # string will have.
    next_str_idx = string_idx
    prefix = ""
    while (
        not prefix
        and is_valid_index(next_str_idx)
        and LL[next_str_idx].type == token.STRING
    ):
        prefix = get_string_prefix(LL[next_str_idx].value).lower()
        next_str_idx += 1

    # The next loop merges the string group. The final string will be
    # contained in 'S'.
    #
    # The following convenience variables are used:
    #
    #   S: string
    #   NS: naked string
    #   SS: next string
    #   NSS: naked next string
    S = ""
    NS = ""
    num_of_strings = 0
    next_str_idx = string_idx
    while is_valid_index(next_str_idx) and LL[next_str_idx].type == token.STRING:
        num_of_strings += 1

        SS = LL[next_str_idx].value
        next_prefix = get_string_prefix(SS).lower()

        # If this is an f-string group but this substring is not prefixed
        # with 'f'...
        if "f" in prefix and "f" not in next_prefix:
            # Then we must escape any braces contained in this substring.
            SS = re.sub(r"(\{|\})", r"\1\1", SS)

        NSS = make_naked(SS, next_prefix)

        has_prefix = bool(next_prefix)
        prefix_tracker.append(has_prefix)

        S = prefix + QUOTE + NS + NSS + BREAK_MARK + QUOTE
        NS = make_naked(S, prefix)

        next_str_idx += 1

    S_leaf = Leaf(token.STRING, S)
    if self.normalize_strings:
        S_leaf.value = normalize_string_quotes(S_leaf.value)

    # Fill the 'custom_splits' list with the appropriate CustomSplit objects.
    temp_string = S_leaf.value[len(prefix) + 1 : -1]
    for has_prefix in prefix_tracker:
        mark_idx = temp_string.find(BREAK_MARK)
        assert (
            mark_idx >= 0
        ), "Logic error while filling the custom string breakpoint cache."

        temp_string = temp_string[mark_idx + len(BREAK_MARK) :]
        breakpoint_idx = mark_idx + (len(prefix) if has_prefix else 0) + 1
        custom_splits.append(CustomSplit(has_prefix, breakpoint_idx))

    string_leaf = Leaf(token.STRING, S_leaf.value.replace(BREAK_MARK, ""))

    if atom_node is not None:
        replace_child(atom_node, string_leaf)

    # Build the final line ('new_line') that this method will later return.
    new_line = line.clone()
    for (i, leaf) in enumerate(LL):
        if i == string_idx:
            new_line.append(string_leaf)

        if string_idx <= i < string_idx + num_of_strings:
            for comment_leaf in line.comments_after(LL[i]):
                new_line.append(comment_leaf, preformatted=True)
            continue

        append_leaves(new_line, line, [leaf])

    self.add_custom_splits(string_leaf.value, custom_splits)
    return Ok(new_line)
