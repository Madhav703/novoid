import os
import sys
import click
from novoid.core import analyze_file, AnalysisResult


SEPARATOR = "─" * 50


def _format_kind(kind: str) -> str:
    return kind.ljust(10)


def _print_result(result: AnalysisResult) -> None:
    if not result.has_issues:
        click.echo(click.style("✔  ", fg="green") + f"{result.filepath} - no dead code detected.")
        return

    click.echo(f"\nnovoid report for: {click.style(result.filepath, fg='cyan', bold=True)}")
    click.echo(SEPARATOR)

    for issue in result.issues:
        line_col = click.style(f"[LINE {issue.line:>3}]", fg="yellow")
        kind_col = click.style(_format_kind(issue.kind), fg="magenta")
        name_col = click.style(issue.name, fg="red", bold=True)
        click.echo(f"  {line_col}  {kind_col}  {name_col}")

    click.echo(SEPARATOR)
    count = len(result.issues)
    click.echo(click.style(f"{count} issue(s) found.\n", fg="red"))


def _collect_python_files(path: str):
    files = []
    if os.path.isfile(path):
        if path.endswith(".py"):
            files.append(path)
    elif os.path.isdir(path):
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(os.path.join(dirpath, filename))
    return files


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.version_option(version="0.1.0", prog_name="novoid")
def main(path: str) -> None:
    python_files = _collect_python_files(path)

    if not python_files:
        click.echo(click.style("No Python files found at the given path.", fg="yellow"))
        sys.exit(0)

    total_issues = 0

    for filepath in python_files:
        result = analyze_file(filepath)
        _print_result(result)
        total_issues += len(result.issues)

    if len(python_files) > 1:
        click.echo(SEPARATOR)
        if total_issues == 0:
            click.echo(click.style("✔  All files are clean.", fg="green", bold=True))
        else:
            click.echo(
                click.style(f"Total: {total_issues} issue(s) across {len(python_files)} file(s).", fg="red", bold=True)
            )

    sys.exit(1 if total_issues > 0 else 0)
