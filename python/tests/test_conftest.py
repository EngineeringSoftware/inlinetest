from inline.conftest import InlinetestItem, MalformedException, TimeoutException
from _pytest.pytester import Pytester
import pytest

# pytest -p pytester
class TestInlinetests:
    def test_inline_parser(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here().given(a, 1).check_eq(a, 2)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            assert isinstance(items[0], InlinetestItem)

    def test_inline_missing_import(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        def m(a):
            a = a + 1
            Here().given(a, 1).check_eq(a, 2)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0

    def test_inline_malformed_given(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here().given(a).check_eq(a, 2)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_inline_malformed_value(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here().given(a).check_eq(2)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_inline_malformed_check_eq(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here().given(a, 1).check_eq(a)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_inline_malformed_check_eq_more_argument(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here().given(a, 1).check_eq(a, 2, 3)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_inline_malformed_check_true(self, pytester: Pytester):
        # [Name(id='a', ctx=Load()), Constant(value=1)]
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here().given(a, 1).check_true(a = 2)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_if(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            if a > 1:
                Here().given(a, 2).check_true(Group(0))
                a = a + 1
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_check_eq_parameterized_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(parameterized=True).given(a, [2, 3]).check_eq(a, [3, 4])
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 2
            res = pytester.runpytest()
            assert res.ret == 0

    def test_malformed_check_eq_parameterized_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(parameterized=True).given(a, [2, 3]).check_eq(a, 3)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_malformed_given_parameterized_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(parameterized=True).given(a, [2]).check_eq(a, [3, 4])
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_check_true_parameterized_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(parameterized=True).given(a, [2, 3]).check_true([a == 3, a == 4])
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 2
            res = pytester.runpytest()
            assert res.ret == 0

    def test_check_false_parameterized_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(parameterized=True).given(a, [2, 3]).check_false([a == 1, a == 2])
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 2
            res = pytester.runpytest()
            assert res.ret == 0

    def test_check_non_positive_repeated_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(repeated = -1).given(a, 1).check_eq(a, 2)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            pytest.raises(MalformedException)

    def test_check_float_repeated_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(parameterized=True).given(a, [2, 3]).check_false([a == 1, a == 2])
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            pytest.raises(MalformedException)

    def test_check_repeated_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(repeated = 2).given(a, 1).check_eq(a, 2)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1

    def test_check_group_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(tag = ["add"]).given(a, 1).check_eq(a, 2)
            a = a - 1
            Here(tag = ["minus"]).given(a, 1).check_eq(a, 0)
    """
        )
        for x in (pytester.path, checkfile):
            reprec = pytester.inline_run("--inlinetest-group=add")
            items = [x.item for x in reprec.getcalls("pytest_itemcollected")]
            assert len(items) == 1

    def test_check_incorrect_group_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(tag = ["add"]).given(a, 1).check_eq(a, 3)
            a = a - 1
            Here(tag = ["minus"]).given(a, 1).check_eq(a, 0)
    """
        )
        for x in (pytester.path, checkfile):
            reprec = pytester.inline_run("--inlinetest-group=add")
            items = [x.item for x in reprec.getcalls("pytest_itemcollected")]
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret != 0

    def test_check_disabled_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(disabled=True).given(a, 1).check_eq(a, 2)
            a = a - 1
            Here().given(a, 1).check_eq(a, 0)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1

    def test_check_disabled_value_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(disabled=True).given(a, 1).check_eq(a, 3)
            a = a - 1
            Here().given(a, 1).check_eq(a, 0)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_multiple_given(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a, c):
            b = a + c
            Here().given(a, 2).given(c, a + 1).check_true(b == 5)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_multiple_malformed_given(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a, c):
            b = a + c
            Here().given(a, 2).given(c).check_true(b == 5)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            pytest.raises(MalformedException)

    def test_if_elif_else_logic(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """
        from inline import Here
        def m(a):
            if a < 21:
                b = "Not yet human"
                Here().given(a, 0).check_true(b == "Not yet human")
            elif a > 22:
                b = 42
                Here().given(a, 25).check_true(b == 42)
            else:
                b = False
                Here().given(a, 21).check_true(b == False)

    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 3
            res = pytester.runpytest()
            assert res.ret == 0

    def test_list_append(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """
        from inline import Here
        def m(i):
            j = h + i
            Here().given(i, ["pineapple", "pear"]).given(h, ["apple", "banana", "orange"]).check_eq(j, ["apple", "banana", "orange", "pineapple", "pear"])
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_list_addition(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """
        from inline import Here
        def m(a):
            a = []
            b = [x + 2 for x in a]
            Here().given(a, [1,2,3,2,1]).check_true(b == [3,4,5,4,3])
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_regex(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """
        import re
        from inline import Here
        def m(x):
            match = re.search("[0123]", x)
            Here().given(x, "hel1o").check_eq(match.start(), 3)
            
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_multivariate(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """
        from inline import Here
        def m(a, b, c, d):
            e = a + b * c - d
            Here().given(a, 3).given(b, 4).given(c,5).given(d,6).check_true(e == 17)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_time(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """
        from inline import Here
        import time
        def m(a):
            a = a + 1
            Here(timeout=10.75).given(a, loop(3)).check_eq(a,4.0)

        def loop(b):
            while True:
                b = b + 1
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            res = pytester.runpytest()
            res.ret == 0
            pytest.raises(TimeoutException)


    def test_assert_neq(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = a - 1
            Here().given(a, 1).check_neq(a, 1)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_assert_none(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = None
            Here().given(a, 1).check_none(a)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_assert_not_none(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            a = 3
            Here().given(a, 1).check_not_none(a)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_assert_same(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            b = a
            Here().given(a, "Hi").check_same(a,b)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_assert_not_same(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            b = a + "a"
            Here().given(a, "Hi").check_not_same(a,b)
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
            res = pytester.runpytest()
            assert res.ret == 0

    def test_fail_statement(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
            """ 
        from inline import Here
        def m(a):
            b = a + "a"
            Here().given(a, "Hi").fail()
    """
        )
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0
            res = pytester.runpytest()