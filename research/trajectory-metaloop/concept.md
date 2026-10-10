# trajectory-metaloop — Concept

**Status:** draft (concept stage of the concept → reqs → design → tasks flow)
**Tracking:** [DeliberateCode/System2-UtilitySkills#6](https://github.com/DeliberateCode/System2-UtilitySkills/issues/6)
**Branch:** `research/trajectory-metaloop` (working files; nothing merged)

## Problem

Agent failures are invisible at scale. A run either "worked" or it didn't —
binary pass/fail misrepresents partial failures, and the taxonomy of *what went
wrong* is ad hoc per team. Meanwhile, every "self-improving loop" proposal
drowns in transcripts: keeping raw trajectories as memory is a cost blowup that
compounds epoch over epoch.

Two gaps, one skill:

1. **Measurable trajectory failure** — detect and classify what went wrong
   against a fixed taxonomy, with step attribution and a cost report.
2. **Memory-efficient metaloop** — distill labeled episodes into a small,
   validated, self-pruning rule store. Never persist raw trajectories.

## Approach

**Mode A — analyze.** Map a transcript to typed trajectory JSON
(`user_message | assistant_message | tool_call | tool_result | system`), then
run a two-tier judge: cheap heuristics first (tool loops ≥5×, error strings,
timeouts, step caps), targeted LLM review only for what heuristics can't see
(communication, quality, safety, state). Each finding is classified against the
ATFD 7-category / 24-subcategory taxonomy (dotted `category.subcategory`, no
invented labels), given a severity and step attribution, and rolled up to an
outcome tier: `pass` | `degraded` (complete but needs human review) | `fail`.
Every judge run reports its own cost — tokens, calls, latency, dollars. The
cost report is part of the output, not an afterthought. Emitted JSON is
machine-validated (`bin/judge-lint.py`) before it's presented.

**Mode B — learn.** Runs only on Mode-A output — categorized findings, never
raw transcripts. Harvest each analyzed trajectory to one episode tuple, cluster
episodes by failure category + task prefix into patterns (confidence floor
0.3), turn surviving patterns into terse rule candidates, then A/B each
candidate on held-out episodes: run with and without the rule injected. Promote
on clear improvement, hold if inconclusive, discard if worse; log every
decision in an append-only ledger. The expensive loop runs only when new
failures arrived — residual failures, not routine passes, earn the budget.

## Design principles

- **Detection is easy, classification is hard.** ATFD's category alignment
  collapses from 0.545 (synthetic) to 0.093 (real domains). When torn between
  subcategories, pick the best fit and note the uncertainty — never invent a
  label.
- **Judge the trajectory, not the agent.** No ground-truth labels, expected
  states, or oracle info beyond events + task description.
- **Every memory needs a death condition.** Rules carry credit (5.0 start,
  clamped [0,10]); 3 inconclusive re-validations → archive; reverse check
  (does removing the rule hurt?) → revert; N epochs unused → evict. Revert is
  single-rule, never whole-store. If the store can't be injected wholesale,
  the funnel failed.
- **Optimize detection-rate-per-dollar at bounded memory, not raw accuracy.**
  The cost report is the scoreboard.

## Known caveats

- ATFD's docs are mid-v2 and inconsistent in places; there is no human
  inter-annotator validation yet.
- Real-domain failure categorization is substantially harder than binary
  detection — expect the taxonomy to strain on production traces.
- The metaloop's A/B select stage assumes enough held-out episodes per pattern;
  low-frequency failure modes may never clear the confidence floor.

## Research program

13 hypotheses ordered by testability, cheapest falsification first
(`references/hypotheses.md`). Flagship: **H-SYN-2** — the closed loop
(monitor → categorize → distill → A/B-validate → inject) reduces failures per
1k trajectories epoch over epoch while rule-store memory grows sublinearly.
Track `(failures/1k, rule-store bytes)` per epoch.

## What exists now (prototype)

- `SKILL.md` — the skill contract (Mode A + Mode B, output contracts,
  operating rules)
- `references/atfd-taxonomy.md` — the 24-subcategory classification vocabulary
- `references/trajectory-schema.md` — the typed trajectory input schema
- `references/metaloop-method.md` — funnel schemas, lifecycle/eviction, worked
  example
- `references/hypotheses.md` — the 13-hypothesis backlog
- `bin/judge-lint.py` — machine validator for judge output
- 36-paper literature corpus grounding the hypotheses (ToM, trajectory
  failure, metaloop)

## Next steps

1. Concept → **reqs**: pin the judge's input/output contracts, taxonomy
   versioning, and the minimum viable rule-store semantics.
2. Reqs → **design**: two-tier judge architecture, funnel state layout, ledger
   and eviction mechanics.
3. Design → **tasks**: build plan against the System2-UtilitySkills layout.
