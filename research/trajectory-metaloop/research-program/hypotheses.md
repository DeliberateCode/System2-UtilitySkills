# Hypothesis Backlog

Open research questions this skill is built to test. Full grounding (papers,
episodes, citations) lives in `papers.md`, Part 2. Hypotheses are ordered by
testability with this skill — cheapest falsification first.

## Theory of Mind
- **H-ToM-1** — Group ToM failures surface as trajectory failures:
  `communication.missing_info` + `process.planning_failure` cluster on
  group-collapse cases. (Mode A)
- **H-ToM-2** — Linear-superposition bias is measurable in-trajectory as
  high-confidence / low-belief-diversity before collapses. (Mode A)
- **H-ToM-3** — Mutual-modeling symmetry predicts dyad failures better than
  individual ToM scores. (Mode A on multi-agent runs)
- **H-ToM-4** — Reality bias has a trajectory signature: information use without
  a traceable observation in the modeled agent's history. (Mode A)

## Trajectory failure & metaloop
- **H-TF-1** — Two-tier monitors (heuristic + targeted LLM) dominate single-pass
  judges on detection-rate-per-dollar. (Mode A)
- **H-TF-2** — Category alignment improves when the judge retrieves similar past
  failures from the pattern store vs. judging cold. (Mode A+B)
- **H-ML-1** — The funnel (episodes→patterns→rules + eviction) retains ≥90% of
  full-retention lift at <10% token cost. (Mode B ablation)
- **H-ML-2** — Categorized ATFD findings beat binary outcomes as the metaloop's
  verdict signal: faster-converging, more specific rules. (Mode B)
- **H-ML-3** — Selective invocation (reflect only on residual failures) cuts loop
  cost ~10× without hurting rule quality. (Mode B)

## Overall improvement target
- **H-SYN-1** — Explicit belief-state models of each agent improve failure
  attribution (which agent/step) in multi-agent trajectories. (Mode A)
- **H-SYN-2 (flagship)** — Closed loop (monitor → categorize → distill →
  A/B-validate → inject) reduces failures per 1k trajectories epoch over epoch
  while memory grows sublinearly. Track (failures/1k, rule-store bytes) per epoch.
- **H-SYN-3** — Optimize the Pareto frontier (detection-rate-per-dollar at
  bounded memory), not raw accuracy. The cost report is the scoreboard.
