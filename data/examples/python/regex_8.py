from inline import itest
import re

def _analyze_einsum_string(equation, bias_axes, input_shape, output_shape):
    """Analyzes an einsum string to determine the required weight shape."""

    dot_replaced_string = re.sub(r"\.\.\.", "0", equation)

    # This is the case where no ellipses are present in the string.
    split_string = re.match("([a-zA-Z]+),([a-zA-Z]+)->([a-zA-Z]+)", dot_replaced_string)
    itest().given(dot_replaced_string, "a,b->c").check_eq(split_string.group(1), "a").check_eq(split_string.group(2), "b").check_eq(split_string.group(3), "c")
    if split_string:
        return _analyze_split_string(split_string, bias_axes, input_shape, output_shape)

    # This is the case where ellipses are present on the left.
    split_string = re.match(
        "0([a-zA-Z]+),([a-zA-Z]+)->0([a-zA-Z]+)", dot_replaced_string
    )
    if split_string:
        return _analyze_split_string(
            split_string, bias_axes, input_shape, output_shape, left_elided=True
        )

    # This is the case where ellipses are present on the right.
    split_string = re.match(
        "([a-zA-Z]{2,})0,([a-zA-Z]+)->([a-zA-Z]+)0", dot_replaced_string
    )
    if split_string:
        return _analyze_split_string(split_string, bias_axes, input_shape, output_shape)

    raise ValueError(
        f"Invalid einsum equation '{equation}'. Equations must be in the form "
        "[X],[Y]->[Z], ...[X],[Y]->...[Z], or [X]...,[Y]->[Z]...."
    )
