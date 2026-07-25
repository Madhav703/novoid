<div align="center">

![Novoid](/novoid_logo.png)


[![PyPI](https://img.shields.io/pypi/v/novoid)](https://pypi.org/project/novoid/)
[![GitHub](https://img.shields.io/badge/github-Madhav703%2Fnovoid-blue?logo=github)](https://github.com/Madhav703/novoid)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Madhav703/novoid/blob/main/LICENSE)

</div>

A minimalist static analysis tool to detect dead code and unused definitions in Python source files.

- GitHub: [https://github.com/Madhav703/novoid](https://github.com/Madhav703/novoid)

## Installation

```bash
pip install novoid
```

## Usage

Analyze a single file:

```bash
novoid main.py
```

Analyze an entire directory:

```bash
novoid ./src
```

## What It Detects

- **Unused functions** - functions that are defined but never called anywhere in the file.
- **Unused variables** - variables that are assigned but never read or referenced.

## Example Output

```
novoid report for: main.py
──────────────────────────────────────
  [LINE  4]  FUNCTION   greet_user
  [LINE  9]  VARIABLE   temp_buffer
──────────────────────────────────────
2 issue(s) found.
```

When no issues are found:

```
✔  main.py - no dead code detected.
```

## Development

```bash
git clone https://github.com/Madhav703/novoid.git
cd novoid
pip install -e "."
pytest tests/
```

## Contributing

Pull requests are welcome at [https://github.com/Madhav703/novoid](https://github.com/Madhav703/novoid).

## License

See [LICENSE](https://github.com/Madhav703/novoid/blob/main/LICENSE)
