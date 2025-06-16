import llm
import json
from unittest.mock import patch, call
from llm_tools_execute_shell import execute_shell


def _get_tool_results_for_command(command: str) -> str:
    # Assumes builtins.input is already patched by the caller test function's decorator
    model = llm.get_model("echo")

    tools_list = [execute_shell]

    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {"name": "execute_shell", "arguments": {"command": command}}
                ]
            }
        ),
        tools=tools_list,
    )
    responses = list(chain_response.responses())
    loaded_data = json.loads(responses[-1].text())
    tool_result_dicts = loaded_data["tool_results"]
    return tool_result_dicts[0]["output"]


@patch("builtins.input", return_value="y")
def test_echo_works(_):
    command = "echo 123"
    expected_output = "123"
    actual_output = _get_tool_results_for_command(command)
    assert actual_output == expected_output


@patch("builtins.input", return_value="n")
def test_user_denies_execution(_):
    command = "echo 123"
    expected_output = "The shell command was cancelled by the user."
    actual_output = _get_tool_results_for_command(command)
    assert actual_output == expected_output


@patch("builtins.input", return_value="y")
def test_command_produces_stdout_and_stderr(_):
    command = 'echo "stdout_line" && echo "stderr_line" >&2'
    actual_output = _get_tool_results_for_command(command)
    assert actual_output.strip() == "stdout_line\nstderr_line"


@patch("builtins.input", return_value="y")
def test_command_fails(_):
    command = "ls /this/path/doesnt/exist"
    actual_output = _get_tool_results_for_command(command)
    assert "No such file or directory" in actual_output


@patch("builtins.input", return_value="y")
def test_command_produces_no_output(_):
    command = "true"
    expected_output = ""
    actual_output = _get_tool_results_for_command(command)
    assert actual_output == expected_output


@patch("builtins.input", return_value="y")
def test_command_with_special_characters_in_output(_):
    command = 'printf "line1\\nline2\\ttabbed"'
    expected_output = "line1\nline2\ttabbed"
    actual_output = _get_tool_results_for_command(command)
    assert actual_output == expected_output


@patch("builtins.input", side_effect=["invalid", "y"])
def test_user_provides_invalid_then_valid_confirmation(_):
    command = "echo 123"
    expected_output = "123"
    actual_output = _get_tool_results_for_command(command)
    assert actual_output == expected_output


@patch("subprocess.Popen", side_effect=OSError("Test OSError"))
@patch("builtins.input", return_value="y")
def test_subprocess_run_raises_exception(_, mock_popen):
    command = "echo 123"
    expected_output = "Error: Test OSError"
    actual_output = _get_tool_results_for_command(command)
    assert actual_output == expected_output


@patch("sys.stdout.write")
@patch("builtins.input", return_value="y")
def test_output_is_streamed_to_stdout(mock_input, mock_stdout_write):
    command = 'echo "line1"; sleep 0.01; echo "line2"'
    expected_final_output = "line1\nline2"

    actual_final_output = _get_tool_results_for_command(command)
    assert actual_final_output == expected_final_output

    expected_calls = [call("line1\n"), call("line2\n")]
    mock_stdout_write.assert_has_calls(expected_calls)
