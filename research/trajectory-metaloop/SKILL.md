---
name: "trajectory_metaloop"
description: "Analyze agent trajectories for measurable failures with the ATFD failure taxonomy, and run a memory-efficient metaloop that distills episodes into validated, credit-scored rules. Use when asked to evaluate agent runs, debug multi-agent failures, or build self-improving agent loops."
---

# Trajectory Metaloop

## Purpose
Measure what goes wrong in agent trajectories and learn from it without drowning in transcripts: detect and classify failures against a fixed taxonomy, then distill labeled episodes into a small, validated, self-pruning rule store.

## Workflow
Two modes. Mode A (`analyze`) runs standalone. Mode B (`learn`) consumes Mode A output — the categorized failure labels are the loop's verdict signal.

### Mode A — analyze a trajectory
1. **Ingest.** Map the agent session/transcript to Trajectory JSON: ordered events typed `user_message | assistant_message | tool_call | tool_result | system`, each with timestamp, content, metadata; plus `task_description`. See `references/trajectory-schema.md`. Never invent events; mark gaps as `system` notes.
2. **Detect (two-tier).** First pass: cheap heuristics for structural failures — same tool ≥5× in a row (`process.tool_loop`), error strings in tool results (`infrastructure.error`), timeouts, step caps. Second pass: targeted LLM review only for what heuristics can't see (communication, quality, safety, state). Record which tier caught each finding.
3. **Classify.** Each finding: `severity` (error|warning|info), a `category` as a dotted `category.subcategory` from `references/atfd-taxonomy.md` (24 valid values — no invented labels), a one-sentence `description`, and optional step `attribution` (event indices). Trajectory outcome: `pass` | `degraded` (complete but needs human review) | `fail`.
4. **Score cost.** Report the judge run's own cost: tokens, API calls, wall latency, estimated dollars. Cost is part of the output, not an afterthought.
5. **Validate.** Run `bin/judge-lint.py` on the emitted JSON before presenting it. Fix and re-validate until clean.

### Mode B — learn (metaloop)
Runs on trajectories already analyzed by Mode A. Needs `has_failure` + categorized findings, never raw transcripts.
1. **Harvest.** Convert each analyzed trajectory to one episode tuple: `{id, task, action_summary, outcome: pass|degraded|fail, failure_categories[]}`. Raw trajectories are ephemeral — harvest, then drop.
2. **Reflect.** Cluster episodes by failure category + task prefix. A cluster becomes a pattern when `confidence = occurrences / total_episodes ≥ 0.3` (tunable); discard below threshold.
3. **Aggregate.** Turn each surviving pattern into a rule candidate: `{id, text: "when <trigger> then <action>", source_pattern, confidence}`. Keep the text terse and actionable.
4. **Select.** A/B each candidate on held-out episodes (not used to form the pattern): run with and without the rule injected. Promote on clear improvement, hold if inconclusive, discard if worse. Record the delta.
5. **Update.** Append promoted rules to `rules.json`; log every decision in `ledger.jsonl` (rule id, verdict, delta, epoch). Revert is single-rule, never whole-store. Evict rules that fail re-validation or sit unused.
6. **Gate.** Skip reflect/select entirely when no new failures arrived since the last epoch. The expensive loop runs on residual failures only.

State files live in a working dir (default `./metaloop-state/`): `episodes.jsonl`, `patterns.json`, `rules.json`, `ledger.jsonl`. See `references/metaloop-method.md` for schemas and a worked example.

## Output Contract
- **Mode A:** one `JudgeOutput` JSON per trajectory — `trajectory_id`, `has_failure`, `findings[{severity, category, description, attribution?}]`, `cost{dollar_cost, latency_seconds, total_tokens, api_calls}` — plus a 3-line human summary: verdict, top finding, cost.
- **Mode B:** updated state files + per-epoch summary: episodes harvested, patterns formed, rules promoted / held / discarded, ledger deltas.
- Never present unvalidated JSON (run the linter). Never claim a rule "works" without a select-stage delta.

## Operating Rules
1. The 24-subcategory taxonomy in `references/atfd-taxonomy.md` is the only classification vocabulary.
2. Judge the trajectory, not the agent: no ground-truth labels, expected states, or oracle info beyond the events + task description.
3. Detection is easy, classification is hard: when torn between subcategories, pick the best fit and note the uncertainty in the description — never invent a label.
4. Cost-report every judge run, including your own.
5. In Mode B the rule store must stay small enough to inject wholesale; every memory needs a death condition (confidence floor, disuse eviction, or failed re-validation).
6. `references/hypotheses.md` lists the open research questions this skill is built to test — consult it when deciding what to measure next.
