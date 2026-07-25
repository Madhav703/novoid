import ast
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class DeadCodeItem:
    kind: str
    name: str
    line: int




@dataclass
class AnalysisResult:
    filepath: str
    issues: List[DeadCodeItem] = field(default_factory=list)

    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0


def _collect_definitions(tree: ast.AST) -> Dict[str, int]:
    definitions: Dict[str, int] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            definitions[node.name] = node.lineno

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id not in definitions:
                        definitions[target.id] = node.lineno

        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                name = node.target.id
                if name not in definitions:
                    definitions[name] = node.lineno

    return definitions


def _collect_usages(tree: ast.AST) -> set:
    usages: set = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            usages.add(node.id)

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                usages.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                usages.add(node.func.attr)

    return usages


def _get_definition_kind(tree: ast.AST, name: str) -> str:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == name:
                return "FUNCTION"
    return "VARIABLE"


def analyze_source(source: str, filepath: str = "<string>") -> AnalysisResult:
    result = AnalysisResult(filepath=filepath)

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return result

    definitions = _collect_definitions(tree)
    usages = _collect_usages(tree)

    unused_names = set(definitions.keys()) - usages

    builtin_names = set(dir(__builtins__)) if isinstance(__builtins__, dict) else set(dir(__builtins__))
    unused_names -= builtin_names
    unused_names.discard("__all__")
    unused_names.discard("__version__")
    unused_names.discard("__name__")
    unused_names.discard("__file__")
    unused_names.discard("__doc__")

    for name in sorted(unused_names, key=lambda n: definitions[n]):
        kind = _get_definition_kind(tree, name)
        line = definitions[name]
        result.issues.append(DeadCodeItem(kind=kind, name=name, line=line))

    result.issues.sort(key=lambda i: i.line)

    return result


def analyze_file(filepath: str) -> AnalysisResult:
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            source = fh.read()
    except (OSError, IOError):
        return AnalysisResult(filepath=filepath)

    return analyze_source(source, filepath=filepath)
