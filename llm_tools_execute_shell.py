import llm
import subprocess


def execute_shell(command: str) -> str:
    """
    Executes a shell command on the user's system.
    Captures and returns the standard output and standard err, interleaved as a signel string.
    """
    confirmation = None
    while confirmation != "y" and confirmation != "n":
        print("""
**************************************************************************
* WARNING: The LLM is requesting to execute the following shell command. *
* REVIEW IT CAREFULLY. Executing unintended commands can be dangerous    *
* and may end in disaster, like wiping your entire disk. Do not run any  *
* command if you do not know exactly what it does.                       *
**************************************************************************
""")
        print(f"{repr(command)}\n")
        confirmation = input("Are you sure you want to run the above command? (y/n): ").strip().lower()
    if confirmation == 'n':
        return "The shell command was cancelled by the user."
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return str(result.stdout).strip()
    except Exception as e:
        return f"Error: {str(e)}"

@llm.hookimpl
def register_tools(register):
    register(execute_shell)

