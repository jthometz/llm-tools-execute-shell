# llm-tools-execute-shell

[![PyPI](https://img.shields.io/pypi/v/llm-tools-execute-shell.svg)](https://pypi.org/project/llm-tools-execute-shell/)
[![Changelog](https://img.shields.io/github/v/release/jthometz/llm-tools-execute-shell?include_prereleases&label=changelog)](https://github.com/jthometz/llm-tools-execute-shell/releases)
[![Tests](https://github.com/jthometz/llm-tools-execute-shell/actions/workflows/test.yml/badge.svg)](https://github.com/jthometz/llm-tools-execute-shell/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-datasette/blob/main/LICENSE)

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
llm -T execute_shell "What's the current date and time?" --td
```

To run in chat mode:
```console
$ llm chat -T execute_shell --td
...
> How many words are in foo.txt?
...
'cat foo.txt | wc -w'
Are you sure you want to run the above command? (y/n): y
Tool call: execute_shell({'command': 'cat foo.txt | wc -w'})
  35

There are 35 words in `foo.txt`.

> How many lines?
...
'cat foo.txt | wc -l'
Are you sure you want to run the above command? (y/n): y
Tool call: execute_shell({'command': 'cat foo.txt | wc -l'})
  6

There are 6 lines in `foo.txt`.
>
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
