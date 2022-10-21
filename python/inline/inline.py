class Here:
    def __init__(
        self,
        test_name: str = None,
        parameterized: bool = False,
        repeated: int = 1,
        tag=[],
        disabled = False
    ):
        """
        Initialize Inline object with test name / parameetrized flag

        :param test_name: test
        :param parameterized: whether the test is parameterized
        :param repeated: number of times to repeat the tests
        :param tag: tags to group tests
        :param disabled: whether the test is disabled
        """

    def given(self, variable, value):
        """
        Set value to a variable.

        :param variable: a variable name
        :param value: a value that will be assigned to the variable
        :returns: Inline object
        """
        return self

    def check_eq(self, actual_value, expected_value):
        """
        Assert whether two values equal

        :param actual_value: the value to check against expected
        :param expected_value: expected value
        :returns: Inline object
        :raises: AssertionError
        """
        return self

    def check_true(self, expr):
        """
        Assert whether a boolean expression is true

        :param expr: a boolean expression
        :returns: Inline object
        :raises: AssertionError
        """
        return self

    def check_false(self, expr):
        """
        Assert whether a boolean expression is false

        :param expr: a boolean expression
        :returns: Inline object
        :raises: AssertionError
        """
        return self


class Group:
    def __init__(self, *arg):
        """
        Initialize Group object with index
        """
