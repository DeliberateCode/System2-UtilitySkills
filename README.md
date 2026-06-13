# System2-UtilitySkills

Utility skills for Claude Code — orthogonal to the core [System2](https://github.com/DeliberateCode/System2) multi-agent pipeline.

## What is this?

A Claude Code plugin that provides general-purpose utility skills. These are skills outside the core purpose of System2's spec-driven workflow.

## Installation

### Step 1: Add the Marketplace

```
/plugin marketplace add DeliberateCode/System2-UtilitySkills
```

### Step 2: Install the Plugin

```
/plugin install sys2@system2-utility-skills-marketplace
```

### Step 3: Restart Claude Code

Restart so the new skills are loaded.

## Skills

### `/sys2:stateless-loop`

Runs an instruction in a stateless subprocess loop. Each iteration invokes `claude -p` with no LLM context from prior runs — the only continuity between iterations is the file system on disk.

The sub-agent is instructed to output `STATUS: CLEAN` when the task is fully resolved. The loop exits when that signal is detected or when the iteration cap is reached.

**Usage:**

```
/sys2:stateless-loop fix all type errors in src/
```

```
/sys2:stateless-loop "run the test suite and fix any failures" --max_iterations 20
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--max_iterations N` | 10 | Hard cap on loop iterations |

## License

MIT — see [LICENSE](LICENSE).
