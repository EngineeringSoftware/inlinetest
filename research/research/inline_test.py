from jsonargparse import CLI
import ast
import seutil as se
import time


class InlineTest:
    # https://docs.python.org/3/tutorial/stdlib.html
    import_libraries = [
        # "import os",
        # "import shutil",
        # "import glob",
        # "import sys",
        # "import argparse",
        "import re",
        # "import math",
        # "import random",
        # "import statistics",
        # "from urllib.request import urlopen",
        # "import smtplib",
        # "from datetime import date",
        # "import zlib",
        # "from timeit import Timer",
        # "import doctest",
        "import unittest",
    ]

    def __init__(self):
        self.check_stmts = []
        self.given_stmts = []
        self.previous_stmts = []
        self.lineno = 0
        self.test_name = ""

    def to_test(self):
        return "\n".join(
            self.import_libraries
            + self.given_stmts[::-1]
            + self.previous_stmts[::-1]
            + self.check_stmts[::-1]
        )

    def __repr__(self):
        if self.test_name:
            return f"Test {self.test_name} at line {self.lineno}\n{self.to_test()}"
        else:
            return f"Test at line {self.lineno}\n{self.to_test()}"

    def execute(self):
        tree = ast.parse(self.to_test())
        codeobj = compile(tree, filename="<ast>", mode="exec")
        start_time = time.time()
        exec(codeobj)
        end_time = time.time()
        print(self.__repr__())
        print(f"Execution time: {round(end_time - start_time, 4)} seconds")


class InlineTestParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self):
        f = open(self.file_path, "r")
        tree = ast.parse(f.read())

        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
                if isinstance(child, ast.stmt):
                    # print("child:", ExtractInlineTest.node_to_source_code(child))
                    # print("parent:", ExtractInlineTest.node_to_source_code(node))
                    # print()
                    node.children = (
                        [child]
                        if not hasattr(node, "children")
                        else [child] + node.children
                    )

        extract_inline_test = ExtractInlineTest()
        extract_inline_test.visit(tree)
        print("finish parsing...")
        return extract_inline_test.inline_test_list


class ExtractInlineTest(ast.NodeTransformer):
    class_name_str = "Here"
    check_eq_str = "check_eq"
    check_true_str = "check_true"
    check_false_str = "check_false"
    given_str = "given"
    cur_inline_test = InlineTest()
    inline_test_list = []

    def __init__(self):
        pass

    @classmethod
    def is_inline_test_class(cls, node):
        if isinstance(node, ast.Call):
            # print("isCall", self.node_to_source_code(node))
            if isinstance(node.func, ast.Name) and node.func.id == cls.class_name_str:
                return True
            elif isinstance(node.func, ast.Attribute):
                # e.g. print(ast.dump(ast.parse('snake.colour', mode='eval'), indent=4))
                # snake is Attribute and colour is Name
                return cls.is_inline_test_class(node.func.value)
            else:
                return False
        else:
            return False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.class_name_str:
            # print("is Here()")
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
            # print("stmt parent", self.node_to_source_code(stmt_node.parent))
            # print("stmt parent child", self.node_to_source_code(stmt_node.parent.children[0]))
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
                        # print("previous_stmt_code:", previous_stmt_code)
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
                    # print(self.check_eq_str)
                    equal_node = ast.Compare(
                        left=node.args[0], ops=[ast.Eq()], comparators=[node.args[1]]
                    )
                    assert_node = ast.Assert(test=equal_node, msg=None)
                    assert_stmt_code = self.node_to_source_code(assert_node)
                    self.cur_inline_test.check_stmts.append(assert_stmt_code)
                else:
                    print("not inline test class")
            elif node.func.attr == self.check_true_str:
                if len(node.args) == 1 and self.is_inline_test_class(node.func.value):
                    # print(self.check_true_str)
                    assert_node = ast.Assert(test=node.args[0], msg=None)
                    assert_stmt_code = self.node_to_source_code(assert_node)
                    self.cur_inline_test.check_stmts.append(assert_stmt_code)
                else:
                    print("not inline test class")
            elif node.func.attr == self.check_false_str:
                # TODO: if the number of arguments is not as expected, it should give a detailed explanation
                if len(node.args) == 1 and self.is_inline_test_class(node.func.value):
                    # print(self.check_false_str)
                    assert_node = ast.Assert(
                        test=ast.UnaryOp(op=ast.Not(), operand=node.args[0]), msg=None
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


# python -m inline.inline_test --file_path inline/examples.py
# python -m inline.inline_test --file_path ../api/python/bit_1.py --task "execute"
def main(file_path: str, task: str = "print", output_file_path: str = None):
    inline_test_parser = InlineTestParser(file_path)
    inline_tests = inline_test_parser.parse()
    if task == "print":
        for inline_test in inline_tests:
            print(inline_test)
            print()
    elif task == "execute":
        failed = False
        for inline_test in inline_tests:
            try:
                inline_test.execute()
            except AssertionError as e:
                print(inline_test, "failed")
                failed = True
        if not failed:
            print("All tests passed")
    elif task == "write":
        se.io.dump(output_file_path, inline_tests, se.io.Fmt.txtList)


if __name__ == "__main__":
    CLI(main, as_positional=False)
