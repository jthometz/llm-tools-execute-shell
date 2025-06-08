# llm-tools-execute-shell

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-datasette/blob/main/LICENSE)

A tool plugin for [LLM](https://llm.datasette.io/en/stable/) that allows you to execute arbitrary shell commands suggested by the LLM.

This tool can be dangerous, and for this reason, this tool prompts for confirmation before running each command. Review all commands carefully before authorizing.



## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

First, clone the repository:
```bash
git clone https://github.com/jthometz/llm-tools-execute-shell.git
```
Then, install the local plugin using `llm install -e`:
```bash
llm install -e path/to/llm-tools-execute-shell
```

## Usage

To run a single prompt:
```bash
▶ llm -T execute_shell "What's the current date and time?" --td

**************************************************************************
* WARNING: The LLM is requesting to execute the following shell command. *
* REVIEW IT CAREFULLY. Executing unintended commands can be dangerous    *
* and may end in disaster, like wiping your entire disk. Do not run any  *
* command if you do not know exactly what it does.                       *
**************************************************************************

'date'

Are you sure you want to run the above command? (y/n): y

Tool call: execute_shell({'command': 'date'})
  Mon Jun  9 07:23:59 AM JST 2025

The current date and time is Mon Jun 9 07:23:59 AM JST 2025.
```

To run in chat mode:
```bash
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
