from pathlib import Path
from typing import Optional
from typing import Iterable
from typing import Union
from typing import List
from typing import Tuple
from typing import Any
from typing import Dict
from types import ModuleType
import pytest
from pytest import Collector
from pytest import Config
from pytest import Parser
from pytest import FixtureRequest
from _pytest.pathlib import fnmatch_ex
from _pytest.pathlib import import_path
from _pytest._code.code import TerminalRepr
import ast
import time
import inspect
import copy

# Alternatively, invoke pytest with -p inline)
# pytest_plugins = ["inline"]

# register argparse-style options and ini-file values, called once at the beginning of a test run
def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("collect")
    group.addoption(
        "--inlinetest-modules",
        action="store_true",
        default=False,
        help="run inlinetests in all .py modules",
        dest="inlinetestmodules",
    )
    group.addoption(
        "--inlinetest-glob",
        action="append",
        default=[],
        metavar="pat",
        help="inlinetests file matching pattern, default: *.py",
        dest="inlinetestglob",
    )
    group.addoption(
        "--inlinetest-continue-on-failure",
        action="store_true",
        default=False,
        help="for a given inlinetest, continue to run after the first failure",
        dest="inlinetest_continue_on_failure",
    )
    group.addoption(
        "--inlinetest-ignore-import-errors",
        action="store_true",
        default=False,
        help="ignore inlinetest ImportErrors",
        dest="inlinetest_ignore_import_errors",
    )


def pytest_collect_file(
    file_path: Path,
    parent: Collector,
) -> Optional["InlinetestModule"]:
    config = parent.config
    if _is_inlinetest(config, file_path):
        mod: InlinetestModule = InlinetestModule.from_parent(parent, path=file_path)
        return mod
    return None


def _is_inlinetest(config: Config, file_path: Path) -> bool:
    globs = config.getoption("inlinetestglob") or ["*.py"]
    return any(fnmatch_ex(glob, file_path) for glob in globs)


@pytest.fixture(scope="session")
def inlinetest_namespace() -> Dict[str, Any]:
    """Fixture that returns a :py:class:`dict` that will be injected into the
    namespace of inlinetests."""
    return dict()


######################################################################
## InlineTest
######################################################################
class InlineTest:
    # https://docs.python.org/3/tutorial/stdlib.html
    import_libraries = [
        "import re",
        "import unittest",
        "from unittest.mock import patch",
    ]

    def __init__(self):
        self.check_stmts = []
        self.given_stmts = []
        self.previous_stmts = []
        self.lineno = 0
        self.test_name = ""
        self.globs = {}

    def to_test(self):
        return "\n".join(
            self.import_libraries
            + self.given_stmts[::-1]
            + self.previous_stmts[::-1]
            + self.check_stmts[::-1]
        )

    def __repr__(self):
        if self.test_name:
            return f"inline test {self.test_name}, starting at line {self.lineno}"
        else:
            return f"inline test, starting at line {self.lineno}"

    def is_empty(self) -> bool:
        return not self.check_stmts

    def __eq__(self, other):
        return (
            self.import_libraries == other.import_libraries
            and self.given_stmts == other.given_stmts
            and self.previous_stmts == other.previous_stmts
            and self.check_stmts == other.check_stmts
        )


######################################################################
## InlineTest Parser
######################################################################
class InlineTestParser:
    def parse(self, obj, globs: None):
        # obj = open(self.file_path, "r").read():
        if isinstance(obj, ModuleType):
            tree = ast.parse(open(obj.__file__, "r").read())
        else:
            return []

        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
                if isinstance(child, ast.stmt):
                    node.children = (
                        [child]
                        if not hasattr(node, "children")
                        else [child] + node.children
                    )

        extract_inline_test = ExtractInlineTest()
        extract_inline_test.visit(tree)
        print("finish parsing...")
        if globs:
            for inline_test in extract_inline_test.inline_test_list:
                inline_test.globs = copy.copy(globs)
        return extract_inline_test.inline_test_list


class ExtractInlineTest(ast.NodeTransformer):
    class_name_str = "Here"
    check_eq_str = "check_eq"
    check_true_str = "check_true"
    check_false_str = "check_false"
    given_str = "given"

    def __init__(self):
        self.cur_inline_test = InlineTest()
        self.inline_test_list = []

    def is_inline_test_class(self, node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == self.class_name_str:
                return True
            elif isinstance(node.func, ast.Attribute):
                # e.g. print(ast.dump(ast.parse('snake.colour', mode='eval'), indent=4))
                # snake is Attribute and colour is Name
                return self.is_inline_test_class(node.func.value)
            else:
                return False
        else:
            return False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.class_name_str:
            # get the test name if exists
            if len(node.args) > 0:
                self.cur_inline_test.test_name = self.node_to_source_code(node.args[0])
            # set the line number
            self.cur_inline_test.lineno = node.lineno
            # get the previous stmt that is not Here() by finding the previous sibling
            stmt_node = node.parent
            while not isinstance(stmt_node, ast.Expr):
                stmt_node = stmt_node.parent
            index_stmt_node = stmt_node.parent.children.index(stmt_node)
            if index_stmt_node >= len(stmt_node.parent.children) - 1:
                print("No previous sibling")
            else:
                for i in range(1, len(stmt_node.parent.children) - index_stmt_node):
                    prev_stmt_node = stmt_node.parent.children[index_stmt_node + i]
                    if isinstance(
                        prev_stmt_node.value, ast.Call
                    ) and self.is_inline_test_class(prev_stmt_node.value):
                        continue
                    else:
                        previous_stmt_code = self.node_to_source_code(prev_stmt_node)
                        self.cur_inline_test.previous_stmts.append(previous_stmt_code)
                        break
            # add current inline test to the list
            self.inline_test_list.append(self.cur_inline_test)
            # init a new inline test object
            self.cur_inline_test = InlineTest()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == self.given_str:
                if len(node.args) == 2 and self.is_inline_test_class(node.func.value):
                    assign_node = ast.Assign(targets=[node.args[0]], value=node.args[1])
                    assign_stmt_code = self.node_to_source_code(assign_node)
                    self.cur_inline_test.given_stmts.append(assign_stmt_code)
                else:
                    print("not inline test class")
            elif node.func.attr == self.check_eq_str:
                # check if the function being called is an inline test function
                if len(node.args) == 2 and self.is_inline_test_class(node.func.value):
                    equal_node = ast.Compare(
                        left=node.args[0], ops=[ast.Eq()], comparators=[node.args[1]]
                    )
                    assert_node = ast.Assert(
                        test=equal_node,
                        msg=ast.Call(
                            func=ast.Attribute(
                                ast.Constant(
                                    "{0} == {1}\nActual: {2}\nExpected: {3}\n"
                                ),
                                "format",
                                ast.Load(),
                            ),
                            args=[
                                ast.Constant(self.node_to_source_code(node.args[0])),
                                ast.Constant(self.node_to_source_code(node.args[1])),
                                node.args[0],
                                node.args[1],
                            ],
                            keywords=[],
                        ),
                    )
                    assert_stmt_code = self.node_to_source_code(assert_node)
                    self.cur_inline_test.check_stmts.append(assert_stmt_code)
                else:
                    print("not inline test class")
            elif node.func.attr == self.check_true_str:
                if len(node.args) == 1 and self.is_inline_test_class(node.func.value):
                    assert_node = ast.Assert(
                        test=node.args[0],
                        msg=ast.Call(
                            func=ast.Attribute(
                                ast.Constant(
                                    "bool({0}) is True\nActual: bool({1}) is False\nExpected: bool({1}) is True\n"
                                ),
                                "format",
                                ast.Load(),
                            ),
                            args=[
                                ast.Constant(self.node_to_source_code(node.args[0])),
                                node.args[0],
                            ],
                            keywords=[],
                        ),
                    )
                    assert_stmt_code = self.node_to_source_code(assert_node)
                    self.cur_inline_test.check_stmts.append(assert_stmt_code)
                else:
                    print("not inline test class")
            elif node.func.attr == self.check_false_str:
                if len(node.args) == 1 and self.is_inline_test_class(node.func.value):
                    assert_node = ast.Assert(
                        test=ast.UnaryOp(op=ast.Not(), operand=node.args[0]),
                        msg=ast.Call(
                            func=ast.Attribute(
                                ast.Constant(
                                    "bool({0}) is False\nActual: bool({1}) is True\nExpected: bool({1}) is False\n"
                                ),
                                "format",
                                ast.Load(),
                            ),
                            args=[
                                ast.Constant(self.node_to_source_code(node.args[0])),
                                node.args[0],
                            ],
                            keywords=[],
                        ),
                    )
                    assert_stmt_code = self.node_to_source_code(assert_node)
                    self.cur_inline_test.check_stmts.append(assert_stmt_code)
                else:
                    print("is inline test class")
        return self.generic_visit(node)

    @staticmethod
    def node_to_source_code(node):
        ast.fix_missing_locations(node)
        return ast.unparse(node)


######################################################################
## InlineTest Finder
######################################################################
class InlineTestFinder:
    def __init__(self, parser=InlineTestParser(), recurse=True, exclude_empty=True):
        self._parser = parser
        self._recurse = recurse
        self._exclude_empty = exclude_empty

    def _from_module(self, module, object):
        """
        Return true if the given object is defined in the given
        module.
        """
        if module is None:
            return True
        elif inspect.getmodule(object) is not None:
            return module is inspect.getmodule(object)
        elif inspect.isfunction(object):
            return module.__dict__ is object.__globals__
        elif inspect.ismethoddescriptor(object):
            if hasattr(object, "__objclass__"):
                obj_mod = object.__objclass__.__module__
            elif hasattr(object, "__module__"):
                obj_mod = object.__module__
            else:
                return True  # [XX] no easy way to tell otherwise
            return module.__name__ == obj_mod
        elif inspect.isclass(object):
            return module.__name__ == object.__module__
        elif hasattr(object, "__module__"):
            return module.__name__ == object.__module__
        elif isinstance(object, property):
            return True  # [XX] no way not be sure.
        else:
            raise ValueError("object must be a class or function")

    def _is_routine(self, obj):
        """
        Safely unwrap objects and determine if they are functions.
        """
        maybe_routine = obj
        try:
            maybe_routine = inspect.unwrap(maybe_routine)
        except ValueError:
            pass
        return inspect.isroutine(maybe_routine)

    def find(self, obj, module=None, globs=None, extraglobs=None):
        # Find the module that contains the given object (if obj is
        # a module, then module=obj.).
        if module is False:
            module = None
        elif module is None:
            module = inspect.getmodule(obj)

        # Initialize globals, and merge in extraglobs.
        if globs is None:
            if module is None:
                globs = {}
            else:
                globs = module.__dict__.copy()
        else:
            globs = globs.copy()
        if extraglobs is not None:
            globs.update(extraglobs)
        if "__name__" not in globs:
            globs["__name__"] = "__main__"  # provide a default module name

        # Recursively explore `obj`, extracting InlineTests.
        tests = []
        self._find(tests, obj, module, globs, {})
        return tests

    def _find(self, tests, obj, module, globs, seen):
        if id(obj) in seen:
            return
        seen[id(obj)] = 1
        # Find a test for this object, and add it to the list of tests.
        test = self._parser.parse(obj, globs)
        if test is not None:
            tests.append(test)

        if inspect.ismodule(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                valname = "%s" % (valname)

                # Recurse to functions & classes.
                if (
                    self._is_routine(val) or inspect.isclass(val)
                ) and self._from_module(module, val):
                    self._find(tests, val, valname, module, globs)

        # Look for tests in a class's contained objects.
        if inspect.isclass(obj) and self._recurse:
            for valname, val in obj.__dict__.items():
                # Special handling for staticmethod/classmethod.
                if isinstance(val, (staticmethod, classmethod)):
                    val = val.__func__

                # Recurse to methods, properties, and nested classes.
                if (
                    inspect.isroutine(val)
                    or inspect.isclass(val)
                    or isinstance(val, property)
                ) and self._from_module(module, val):
                    valname = "%s" % (valname)
                    self._find(tests, val, valname, module, globs)


######################################################################
## InlineTest Runner
######################################################################
class InlineTestRunner:
    def run(self, test: InlineTest, out) -> None:
        tree = ast.parse(test.to_test())
        codeobj = compile(tree, filename="<ast>", mode="exec")
        start_time = time.time()
        exec(codeobj, test.globs)
        end_time = time.time()
        out.append(f"Test Execution time: {round(end_time - start_time, 4)} seconds")
        if test.globs:
            test.globs.clear()


class InlinetestItem(pytest.Item):
    def __init__(
        self,
        name: str,
        parent: "InlinetestModule",
        runner: Optional["InlineTestRunner"] = None,
        dtest: Optional["InlineTest"] = None,
    ) -> None:
        super().__init__(name, parent)
        self.runner = runner
        self.dtest = dtest
        self.obj = None
        self.fixture_request: Optional[FixtureRequest] = None

    @classmethod
    def from_parent(
        cls,
        parent: "InlinetestModule",
        *,
        name: str,
        runner: "InlineTestRunner",
        dtest: "InlineTest",
    ):
        # incompatible signature due to imposed limits on subclass
        """The public named constructor."""
        return super().from_parent(name=name, parent=parent, runner=runner, dtest=dtest)

    def setup(self) -> None:
        if self.dtest is not None:
            self.fixture_request = _setup_fixtures(self)
            globs = dict(getfixture=self.fixture_request.getfixturevalue)
            for name, value in self.fixture_request.getfixturevalue(
                "inlinetest_namespace"
            ).items():
                globs[name] = value
            self.dtest.globs.update(globs)

    def runtest(self) -> None:
        assert self.dtest is not None
        assert self.runner is not None
        failures: List[str] = []
        print(f"Running {self.dtest}")
        self.runner.run(self.dtest, out=failures)  # type: ignore[arg-type]
        if failures:
            print(failures)

    def reportinfo(self) -> Tuple[Union["os.PathLike[str]", str], Optional[int], str]:
        assert self.dtest is not None
        return self.path, self.dtest.lineno, "[inlinetest] %s" % self.name


class InlinetestModule(pytest.Module):
    def collect(self) -> Iterable[InlinetestItem]:
        if self.path.name == "conftest.py":
            module = self.config.pluginmanager._importconftest(
                self.path,
                self.config.getoption("importmode"),
                rootpath=self.config.rootpath,
            )
        else:
            try:
                module = import_path(self.path, root=self.config.rootpath)
            except ImportError:
                if self.config.getvalue("inlinetest_ignore_import_errors"):
                    pytest.skip("unable to import module %r" % self.path)
                else:
                    raise ImportError("unable to import module %r" % self.path)
        finder = InlineTestFinder()
        runner = InlineTestRunner()

        for test_list in finder.find(module):
            for test in test_list:
                if not test.is_empty():  # skip empty inline tests
                    yield InlinetestItem.from_parent(
                        # TODO: our current inline test does not have name
                        self,
                        name="",
                        runner=runner,
                        dtest=test,
                    )


def _setup_fixtures(inlinetest_item: InlinetestItem) -> FixtureRequest:
    """Used by InlinetestItem to setup fixture information."""

    def func() -> None:
        pass

    inlinetest_item.funcargs = {}  # type: ignore[attr-defined]
    fm = inlinetest_item.session._fixturemanager
    inlinetest_item._fixtureinfo = fm.getfixtureinfo(  # type: ignore[attr-defined]
        node=inlinetest_item, func=func, cls=None, funcargs=False
    )
    fixture_request = FixtureRequest(inlinetest_item, _ispytest=True)
    fixture_request._fillfixtures()
    return fixture_request
