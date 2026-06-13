---
name: gemini
description: Run a prompt through Google's Gemini CLI non-interactively via `gemini -p`. Use for getting a second opinion, code review, or any task where you want Gemini's perspective on the current project.
argument-hint: "<prompt> [gemini flags...]"
---

# /sys2:gemini -- Gemini CLI Runner

You are executing the /sys2:gemini skill. Follow these steps exactly.

## Arguments

The user provides:
- **prompt** (required): the instruction to send to Gemini. May be bare text or quoted.
- **additional flags** (optional): any flags supported by `gemini` (e.g. `--model <model>`, `--sandbox`, `--yolo`). These are passed through verbatim.

## Execution

### Argument parsing

1. Split the user's input into the **prompt** portion and any **flags** (tokens starting with `-` or `--`, plus their values).
2. Known Gemini flags that take a value: `--model`/`-m`, `--output-format`/`-o`, `--extensions`/`-e`, `--policy`, `--allowed-mcp-server-names`, `--allowed-tools`, `--include-directories`, `--resume`/`-r`, `--delete-session`. When encountered, consume the next token as the flag's value.
3. Known Gemini boolean flags: `--debug`/`-d`, `--sandbox`/`-s`, `--yolo`/`-y`, `--raw-output`, `--accept-raw-output-risk`, `--screen-reader`, `--list-extensions`/`-l`, `--list-sessions`. These stand alone.
4. Everything that is not a recognized flag or a flag's value is the **prompt**.

### Running Gemini

Run a **single Bash call** with timeout 600000 (10 minutes):

```
gemini -p '<prompt>' [flags...]
```

Shell-quoting rules for the prompt:
- If the prompt contains no single quotes, wrap it in single quotes.
- If it contains single quotes, wrap it in `$'...'` syntax with internal single quotes escaped as `\'`.
- Never pass the prompt unquoted.

### Error handling

If `gemini` exits non-zero, report the exit code and any stderr output to the user.

## Output

Present Gemini's output directly to the user. After completion, report success or failure status.
