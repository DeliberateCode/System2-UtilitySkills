# Context: trajectory-metaloop skill

**Status:** draft (Context stage of the Scope → Context → Requirements → Design → Tasks → Implementation → Verification → Ship flow)
**Tracking:** [DeliberateCode/System2-UtilitySkills#6](https://github.com/DeliberateCode/System2-UtilitySkills/issues/6)
**Branch:** `research/trajectory-metaloop` (working files; nothing merged to main, no PR)
**Supersedes:** `research/trajectory-metaloop/concept.md` as the stage artifact (concept approved Oct 10, 2026; retained on the branch as history)
**Repo:** DeliberateCode/System2-UtilitySkills (public)
**Scope:** ship track — Mode A skill first, then Mode B learning system. Research thread: `research-program/`.

## Problem Statement

Agent failures are invisible at scale. A run either "worked" or it didn't —
binary pass/fail misrepresents partial failures, and the taxonomy of *what
went wrong* is ad hoc per team, so failures cannot be measured, compared, or
learned from across runs. Meanwhile, every "self-improving loop" proposal
is overwhelmed by transcript storage: keeping raw trajectories as memory
incurs costs that compound epoch over epoch, which is why most metaloops
become unaffordable on a real workload.

Two gaps, one skill:

1. **Measurable trajectory failure** — detect and classify what went wrong
   against a fixed taxonomy, with step attribution and a cost report.
2. **Memory-efficient metaloop** — distill labeled episodes into a small,
   validated, self-pruning rule store. Never persist raw trajectories.

## Goals

- **G1.** Detect and classify agent-trajectory failures against a fixed
  24-label taxonomy, each finding carrying severity, category, a one-sentence
  description, and step attribution.
- **G2.** Report the judge run's own cost (tokens, API calls, latency,
  dollars) as a mandatory part of every output.
- **G3.** Distill labeled episodes into validated, credit-scored rules —
  extract episodes, cluster them into patterns, aggregate patterns into rule
  candidates, A/B-test candidates on held-out episodes, and update the rule
  store — without persisting raw trajectories.
- **G4.** Reduce failures per 1,000 trajectories epoch over epoch while
  rule-store memory grows sublinearly.
- **G5.** Machine-validate every emitted JudgeOutput before presentation
  (no unvalidated output ever surfaces).

## Non-Goals / Out of Scope

- Real-time monitoring or alerting on live agent fleets.
- Multi-agent Theory-of-Mind attribution beyond step attribution (H-ToM-1..4,
  H-SYN-1 live in the research thread — `research-program/hypotheses.md` —
  not ship deliverables).
- The 36-paper literature corpus (`research-program/papers.md`): grounding
  for the research thread, not a ship deliverable.
- Merging anything into System2-UtilitySkills `main` — this track produces the
  spec chain on the research branch only.

## Users & Use-Cases

- **UC-1 — Judge a run.** Feed a trajectory file; receive categorized findings
  with step attribution plus a cost report. (Mode A)
- **UC-2 — Learn from runs.** Feed labeled episodes; receive validated rules
  with held-out deltas and a ledger of every promotion decision. (Mode B)
- **UC-3 — Verify the loop.** Track (failures/1k, rule-store bytes) per
  epoch against Mode B's acceptance criteria.
- **Intended users:** DeliberateCode contributors who would later adopt the
  skill; agent-reliability researchers needing a cheap failure taxonomy.

## Constraints & Invariants

- **C1.** The 24-subcategory ATFD taxonomy (adapted from galea-foo/atfd,
  CC BY 4.0) is a closed classification vocabulary — dotted
  `category.subcategory`, no invented labels, ever.
- **C2.** Raw trajectories never persist past episode extraction (the memory
  bound that makes the metaloop affordable).
- **C3.** The judge sees only events + task description: no ground-truth
  labels, expected states, or oracle info (judge the trajectory, not the
  agent). *Assumption:* an independent success oracle is still required at the
  select stage to measure task success (rationale: without it, the same system
  that flags failures also measures improvement; resolution: OQ-5).
- **C4.** Cost report is mandatory on every judge run, including the
  researchers' own runs.
- **C5.** Branch-and-PR discipline: issue #6 is the tracking vehicle;
  substantial content lives on `research/trajectory-metaloop` and is
  referenced from the issue; nothing merges from the research branch without
  explicit approval.

## Success Metrics & Acceptance Criteria

- **SM-1.** Failures per 1k trajectories trend down epoch over epoch.
- **SM-2.** Rule-store bytes grow sublinearly over the same epochs.
- **SM-3.** Detection-rate per dollar is the primary optimization target,
  not raw accuracy.
- **AC-1.** Mode A on a sample trajectory emits linter-clean JudgeOutput with
  ≥1 finding categorized per the taxonomy and step-attributed.
- **AC-2.** Mode B over a labeled episode set promotes ≥1 rule with a positive
  held-out delta, ledger-recorded.
- **AC-3.** Rule-store size stays bounded over K epochs while failures/1k
  trends down.
- **AC-4.** Every judge run in the test set includes a complete, non-negative
  cost report.

*Assumption:* SM-1/SM-2 are measurable as stated (rationale: both are
countable per epoch; risk: if the taxonomy cannot be calibrated — see R1 —
SM-1 measures judge noise, not failures).

## Risks & Edge Cases

- **R1 — The instrument may not be valid.** ATFD's category alignment
  collapses 0.545 → 0.093 on real domains (≈ chance). If the judge cannot
  classify reliably, the verdict signal is noise and everything downstream
  (patterns, rules, SM-1) is built on it. *Mitigation:* human calibration
  study (2–3 annotators, 200 trajectories, Cohen's κ) before building the
  loop; kill criterion κ < ~0.4 → fall back to binary + oracles.
- **R2 — Circularity.** Same model family judges and generates; select
  measures judge-flagged failures, not task failures. *Mitigation:*
  independent success oracle required at select (OQ-5); judge/generator
  separation.
- **R3 — Underpowered A/Bs.** Realistic episode counts per pattern may not
  support meaningful held-out deltas. *Mitigation:* power analysis in
  requirements; if n is insufficient, use a cheaper documented proxy rather
  than promoting on noise.
- **R4 — Taxonomy version skew.** Bumping the taxonomy orphans historical
  labels; discarding raw trajectories after episode extraction makes
  re-judging impossible. *Mitigation:* version-stamp every
  finding/episode/rule; retain re-derivable traces (typed event sequences,
  discarding only bulky payloads).
- **R5 — Low-frequency failures never clear the confidence floor** and are
  structurally ignored by design.
- **R6 — ATFD's docs are mid-v2 and internally inconsistent**; no human
  inter-annotator validation exists yet.
- **R7 — Goodhart on the metric.** Detection-rate-per-dollar with no
  precision term rewards flagging everything. *Mitigation:* precision floor
  against the calibration set, with a halt condition.

## Observability / Telemetry expectations

- Per judge run: `dollar_cost`, `latency_seconds`, `total_tokens`,
  `api_calls` — always present, never omitted.
- Per epoch: episodes extracted, patterns formed, rules
  promoted / held / discarded, ledger deltas.
- The ledger is the audit trail: append-only record of every select-stage
  decision. (Adversarial review: as specified it is too thin for forensics —
  it must eventually reference episode ID sets, store content hashes,
  taxonomy versions, exact rule text, and raw A/B counts.)
- Loop verification: (failures/1k, rule-store bytes) per epoch, plotted as a
  time series.

## Rollout & Backward Compatibility

- Research track only: no production rollout, no users to migrate.
- Backward compatibility is about the taxonomy, not a deployment: findings
  are stamped with the taxonomy version; a version bump requires an explicit
  migration map, never silent relabeling (NFR-1 in requirements).

## Open Questions

| # | Question | How to resolve |
|---|---|---|
| OQ-1 | Pattern-formation mechanics: counting-window definition, null-model construction, confidence weighting? | Design stage |
| OQ-2 | Minimum held-out episode count for a meaningful select-stage A/B? | Power analysis in requirements |
| OQ-3 | Credit-score dynamics: start value, clamp bounds, re-validation cadence? | Design stage |
| OQ-4 | Final skill packaging: single `SKILL.md` per repo convention vs multi-file `references/` + `bin/`? | Design stage |
| OQ-5 | What counts as the independent success oracle for select (env state, tests, human spot-checks)? | Requirements/design |
| OQ-6 | Calibration study design: annotators, sample size, κ threshold for "valid instrument"? | Before building the loop (R1 kill criterion) |
| OQ-7 | How much of a trajectory must a re-derivable trace retain? | Design stage |

## Minimal Change Intent

This is a new research track, not a change to existing modules: no
System2-UtilitySkills modules are modified, and all work lives under
`research/trajectory-metaloop/` on the branch. No API surface exists yet, so
none must be preserved. The skill-packaging question (OQ-4) is explicitly
deferred to design — no premature abstraction into `plugin/skills/`.

## Glossary

- **Trajectory:** the ordered, typed event sequence of one agent run
  (`user_message | assistant_message | tool_call | tool_result | system`).
- **Finding:** one classified failure — severity, category, one-sentence
  description, optional step attribution.
- **Degraded:** outcome tier — technically complete but needing human review
  (exact decision rule pending; see requirements).
- **Episode:** extracted tuple `{id, task, action_summary, outcome,
  failure_categories[]}` — the minimal durable unit of the loop.
- **Pattern:** a cluster of episodes clearing the recurrence floor.
- **Rule:** a validated "when <trigger> then <action>" candidate with a credit
  score; the only long-lived memory.
- **Ledger:** the append-only log of select-stage decisions.
- **Death condition:** an eviction trigger for a rule (confidence floor,
  disuse, failed re-validation, reverse ablation).
- **ATFD:** the 7-category / 24-subcategory failure taxonomy adapted from
  galea-foo/atfd (CC BY 4.0).
