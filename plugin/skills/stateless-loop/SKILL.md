---
name: stateless-loop
description: Run an instruction in a stateless subprocess loop using `claude -p` until the task reports STATUS: CLEAN or max iterations are reached. Use for repetitive fix-and-check workflows where each iteration starts with no LLM context from prior runs.
argument-hint: "<instruction> [--max_iterations N]"
---

# /sys2:stateless-loop -- Stateless Subprocess Loop

You are executing the /sys2:stateless-loop skill. Follow these steps exactly:

## Arguments

The user provides:
- **instruction** (required): the task to run each iteration. May be bare text or quoted.
- **--max_iterations N** (optional): iteration cap, default 10.

## Execution

Run the loop script via Bash. Pass the instruction as a single shell-quoted argument.

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/stateless-loop/stateless_loop.py" <instruction> [--max_iterations N]
```

Shell-quoting rules:
- If the instruction contains no single quotes, wrap it in single quotes.
- If it contains single quotes, wrap it in double quotes and escape any `"`, `$`, or `` ` `` inside.
- Never pass the instruction unquoted.

## Output

The script streams subprocess output in real time. Present it directly to the user.

If the script exits 0, report the iteration count. If it exits non-zero, report the exit status.
