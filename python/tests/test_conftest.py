from inline.conftest import InlinetestItem, MalformedException
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
    """)
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
    """)
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
    """)
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
    """)
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
    """)
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
    """)
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
    """)
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
    """)
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
    """)
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 0

    def test_check_true_parameterized_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
    """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(parameterized=True).given(a, [2, 3]).check_true([a == 3, a == 4])
    """)
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
    """)
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
    """)
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
    """)
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
    """)
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
    """)
        for x in (pytester.path, checkfile): 
            reprec = pytester.inline_run("--inlinetest-group=add")
            items = [x.item for x in reprec.getcalls("pytest_itemcollected")]
            assert len(items) == 1

    def test_check_disabled_tests(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
    """ 
        from inline import Here
        def m(a):
            a = a + 1
            Here(disabled=True).given(a, 1).check_eq(a, 2)
            a = a - 1
            Here().given(a, 1).check_eq(a, 0)
    """)
        for x in (pytester.path, checkfile): 
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1
    
    def test_multiple_given(self, pytester: Pytester):
        checkfile = pytester.makepyfile(
    """ 
        from inline import Here
        def m(a, c):
            b = a + c
            Here().given(a, 2).given(c, a + 1).check_true(b == 5)
    """)
        for x in (pytester.path, checkfile):
            items, reprec = pytester.inline_genitems(x)
            assert len(items) == 1 
            res = pytester.runpytest()
            assert res.ret == 0