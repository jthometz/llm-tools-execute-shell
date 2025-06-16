# llm-tools-execute-shell

[![PyPI](https://img.shields.io/pypi/v/llm-tools-execute-shell.svg)](https://pypi.org/project/llm-tools-execute-shell/)
[![Changelog](https://img.shields.io/github/v/release/jthometz/llm-tools-execute-shell?include_prereleases&label=changelog)](https://github.com/jthometz/llm-tools-execute-shell/releases)
[![Tests](https://github.com/jthometz/llm-tools-execute-shell/actions/workflows/test.yml/badge.svg)](https://github.com/jthometz/llm-tools-execute-shell/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/jthometz/llm-tools-execute-shell/blob/main/LICENSE)

A tool plugin for [LLM](https://llm.datasette.io/en/stable/) that allows you to execute arbitrary shell commands suggested by the LLM.

This tool can be dangerous, and for this reason, this tool prompts for confirmation before running each command. Review all commands carefully before authorizing.



## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/):
```bash
llm install llm-tools-execute-shell
```

## Usage

To run a single prompt:
```bash
llm --tool execute_shell "What's the current date and time?"
```

To run in chat mode:
```console
$ llm chat --tool execute_shell
...
> My req.py script is broken. Can you run it and fix the error?
...
LLM wants to run command: 'python req.py'

Are you sure you want to run the above command? (y/n): y

Traceback (most recent call last):
  File "/tmp/foo/req.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'

LLM wants to run command: 'pip install requests'

Are you sure you want to run the above command? (y/n): y
...
LLM wants to run command: 'python req.py'

Are you sure you want to run the above command? (y/n): y

{'origin': 'success'}

It looks like the `req.py` script was failing because the `requests` module was not installed. I've installed it for you, and now the script runs successfully.
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-execute-shell
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
