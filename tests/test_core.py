import pytest
from novoid.core import analyze_source, DeadCodeItem


UNUSED_VARIABLE_SOURCE = """
x = 10
y = 20
print(x)
"""

UNUSED_FUNCTION_SOURCE = """
def used_func():
    return 42

def unused_func():
    return 99

result = used_func()
"""

MIXED_SOURCE = """
dead_var = "never used"

def live_func():
    return 1

def dead_func():
    return 2

output = live_func()
"""

ALL_USED_SOURCE = """
def greet(name):
    return "Hello " + name

message = greet("world")
print(message)
"""

EMPTY_SOURCE = ""


def test_unused_variable_detected():
    result = analyze_source(UNUSED_VARIABLE_SOURCE, filepath="test.py")
    names = [issue.name for issue in result.issues]
    assert "y" in names


def test_used_variable_not_flagged():
    result = analyze_source(UNUSED_VARIABLE_SOURCE, filepath="test.py")
    names = [issue.name for issue in result.issues]
    assert "x" not in names


def test_unused_function_detected():
    result = analyze_source(UNUSED_FUNCTION_SOURCE, filepath="test.py")
    names = [issue.name for issue in result.issues]
    assert "unused_func" in names


def test_used_function_not_flagged():
    result = analyze_source(UNUSED_FUNCTION_SOURCE, filepath="test.py")
    names = [issue.name for issue in result.issues]
    assert "used_func" not in names


def test_mixed_dead_code_detected():
    result = analyze_source(MIXED_SOURCE, filepath="test.py")
    names = [issue.name for issue in result.issues]
    assert "dead_var" in names
    assert "dead_func" in names


def test_mixed_live_code_not_flagged():
    result = analyze_source(MIXED_SOURCE, filepath="test.py")
    names = [issue.name for issue in result.issues]
    assert "live_func" not in names


def test_all_used_returns_no_issues():
    result = analyze_source(ALL_USED_SOURCE, filepath="test.py")
    assert not result.has_issues


def test_empty_source_returns_no_issues():
    result = analyze_source(EMPTY_SOURCE, filepath="test.py")
    assert not result.has_issues


def test_issue_kinds_are_correct():
    result = analyze_source(MIXED_SOURCE, filepath="test.py")
    kind_map = {issue.name: issue.kind for issue in result.issues}
    assert kind_map.get("dead_func") == "FUNCTION"
    assert kind_map.get("dead_var") == "VARIABLE"


def test_issue_line_numbers_are_positive():
    result = analyze_source(MIXED_SOURCE, filepath="test.py")
    for issue in result.issues:
        assert issue.line > 0


def test_result_filepath_is_preserved():
    result = analyze_source(UNUSED_VARIABLE_SOURCE, filepath="mymodule.py")
    assert result.filepath == "mymodule.py"


def test_syntax_error_returns_empty_result():
    broken_source = "def broken(:\n    pass"
    result = analyze_source(broken_source, filepath="broken.py")
    assert not result.has_issues
