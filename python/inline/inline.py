class Here:
    def __init__(
        self,
        test_name: str = None,
        parameterized: bool = False,
        repeated: int = 1,
        tag=[],
        disabled = False,
        timeout: float = -1.0
    ):
        """
        Initialize Inline object with test name / parametrized flag

        :param test_name: test
        :param parameterized: whether the test is parameterized
        :param repeated: number of times to repeat the tests
        :param tag: tags to group tests
        :param disabled: whether the test is disabled
        :param timeout: seconds to timeout the test, must be an integer
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

#######################################################################
    #TODO Zach - Add More API for Asserts as Development Continues
    def check_null(self, value):
        """
        Assert whether an object is null

        :param object: a value to check against
        :returns: Inline object
        :raises: AssertionError
        """
        return self

    def check_not_null(self, value):
        """
        Assert whether a value is not null

        :param value: a value to check against
        :returns: Inline object
        :raises: AssertionError
        """
        return self

    def check_not_equals(self, actual_value, expected_value):
        """
        Assert whether two values are not equal

        :param actual_value: an value to check against expected
        :param expected_value: expected value
        :returns: Inline object
        :raises: AssertionError
        """
        return self
    
    def check_instance_of(self, actual_type, expected_type):
        """
        Assert whether an object is an instance of a given type

        :param actual_type: the value to check against expected
        :param expected_type: expected type
        :returns: Inline object
        :raises: AssertionError
        """
        return self

    def check_throw(self, executable, expected_type_exception):
        """
        Assert whether an object is an instance of a given type

        :param executable: an executable to run
        :param expected_type_exception: expected type of exception executable should raise
        :returns: Exception
        :raises: AssertionError
        """
        return self

#######################################################################

class Group:
    def __init__(self, *arg):
        """
        Initialize Group object with index
        """
