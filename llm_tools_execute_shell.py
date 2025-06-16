import llm
import click
import subprocess
import sys

_warning_shown = False


def execute_shell(command: str) -> str:
    """
    Executes a shell command on the user's system.
    Captures and returns the standard output and standard err, interleaved as a signel string.
    """
    global _warning_shown
    confirmation = None
    while confirmation != "y" and confirmation != "n":
        printed_warning_this_iteration = False
        if not _warning_shown:
            warning_message = """
**************************************************************************
* WARNING: The LLM is requesting to execute a shell command.             *
*                                                                        *
* REVIEW THE COMMAND VERY CAREFULLY BEFORE PROCEEDING.                   *
*                                                                        *
* Executing unknown or malicious commands can be extremely dangerous.    *
* It could lead to irreversible data loss (e.g., wiping your disk) or    *
* compromise your system's security. ONLY PROCEED if you fully           *
* understand the command and its consequences.                           *
*                                                                        *
* This warning will only be displayed once.                              *
**************************************************************************
"""
            click.echo(
                click.style(warning_message, fg="yellow", bold=True),
                err=True,
            )
            _warning_shown = True
        else:
            # Empty newline.
            click.echo(err=True)

        click.echo(
            click.style(
                f"\nLLM wants to run command: {repr(command)}\n", fg="yellow", bold=True
            ),
            err=True,
        )
        confirmation = (
            input("Are you sure you want to run the above command? (y/n): ")
            .strip()
            .lower()
        )
    if confirmation == "n":
        return "The shell command was cancelled by the user."
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        output_lines = []
        if process.stdout:
            sys.stdout.write("\n")
            sys.stdout.flush()
            for line in iter(process.stdout.readline, ""):
                sys.stdout.write(line)
                sys.stdout.flush()
                output_lines.append(line)
            process.stdout.close()
            sys.stdout.write("\n")
            sys.stdout.flush()

        process.wait()

        return "".join(output_lines).strip()
    except Exception as e:
        return f"Error: {str(e)}"


@llm.hookimpl
def register_tools(register):
    register(execute_shell)
