# trajectory-metaloop — Requirements

**Status:** draft (requirements stage of the concept → reqs → design → tasks flow)
**Tracking:** [DeliberateCode/System2-UtilitySkills#6](https://github.com/DeliberateCode/System2-UtilitySkills/issues/6)
**Branch:** `research/trajectory-metaloop` (working files; nothing merged to main, no PR)
**Extends:** `concept.md` (approved Oct 10, 2026); `spec/context.md` (draft, 12-section conforming conversion)
**Scope:** ship track — Mode A skill first, then Mode B learning system. The research thread (`research-program/`: hypotheses, corpus, evaluations) feeds the ship track through its stage gates; it is not specified here.

## 1. Functional requirements — Mode A (analyze)

- **FR-A1 — Typed ingestion.** Produce a typed trajectory record from an
  agent transcript: ordered events typed `user_message | assistant_message
  | tool_call | tool_result | system`, each with timestamp, content,
  metadata, plus the task description. Never invent events; mark gaps as
  `system` notes.
- **FR-A2 — Two-tier detection with tier-1 thresholds retuned from tier-2 labels.** Tier 1: cheap
  heuristics for structural failures (same tool ≥5× in a row, error strings
  in tool results, timeouts, step caps). Tier 2: targeted LLM review only
  for what heuristics cannot see (communication, quality, safety, state).
  Record the detecting tier per finding. When tier-1 uncertainty is high the
  case escalates to tier-2. A separate retune step adjusts tier-1's
  thresholds from tier-2's verdicts, grouped by batch (batch id defaults
  to run date). Retune state — the threshold table and retune log — is
  local to the skill in standalone use and lives in the loop's state
  directory in the loop case. Track the tier-1 miss rate on tier-2-flagged events — a flat
  gap means the fast tier is frozen and FR-A2 is failing.
- **FR-A3 — Closed-vocabulary classification with per-finding confidence.**
  Each finding carries `severity` (`error | warning | info`), `category`
  (exactly one of the 24 dotted `category.subcategory` labels in
  `references/atfd-taxonomy.md` — no invented labels), `confidence` (0..1,
  required — the judge's self-reported certainty, not free text), a
  one-sentence `description`, and optional step `attribution` (event indices
  grounding the finding).
- **FR-A4 — Outcome tiers decided by an explicit aggregation rule.** Each trajectory resolves to `pass |
  degraded | fail` by an explicit aggregation function, not judge
  impression: `degraded` ⟺ ≥1 error-severity finding AND a task artifact
  exists; `fail` ⟺ ≥1 error-severity finding AND the artifact is missing or
  wrong; `pass` otherwise. Low-confidence findings (below a tunable floor)
  cannot single-handedly flip a tier.
- **FR-A5 — Cost reporting (deferred).** Shelved until the system works end
  to end. When reinstated: every judge run reports monetary cost (from the
  canonical price table), wall latency, total tokens, and API calls; cost
  fields required, never omitted.
- **FR-A6 — Schema validation before presentation.** A validator program must check
  every emitted record against the output schema before presentation; fix
  and re-validate until clean. (Prototype: `bin/judge-lint.py` — the script
  is an example of the capability, not the requirement.)

## 2. Functional requirements — Mode B (learn)

- **FR-B1 — Preserve re-derivable traces; discard only bulky payloads.**
  Convert each Mode-A-analyzed trajectory to one episode record: `{id, task,
  action_summary, outcome, failure_categories[], taxonomy_version,
  trace_ref}`. Retain the typed event sequence — discarding only bulky
  tool-result payloads — so that findings can be re-derived under a future
  taxonomy version. Episode identity is derived from content (trajectory +
  taxonomy version) so reruns are idempotent — never positional. Mode B
  never consumes raw transcripts.
- **FR-B2 — Cluster episodes into patterns by recurrence.** Group episodes by failure
  category and task prefix, regardless of outcome valence, so success modes can
  form patterns as well as failure modes. A group becomes a pattern when its
  recurrence within an explicitly stated counting window exceeds a floor. The floor
  must exceed the recurrence expected under a stated null model (e.g., random
  labeling), with the rationale documented — the requirement is that the floor beats
  chance, not the specific null construction. Whether per-finding confidence weights
  the counts, and how the counting window is defined, are design-time decisions
  (see OQ-1).
- **FR-B3 — Aggregate.** Turn each surviving pattern into a rule candidate:
  `{id, text: "when <trigger> then <action>", source_pattern, confidence}`.
  Rule text is a single when/then conditional.
- **FR-B4 — A/B-test candidates against an independent oracle under pre-registered statistical criteria.**
  Each candidate is A/B-tested on held-out episodes (never the ones that
  formed the pattern): run with and without the rule injected, measured
  against an **independent success oracle** (environment state, task tests,
  or human spot-checks — never the judge's own flags), with the judge and
  generator drawn from separated model families. The A/B runs against the
  store snapshot (store+Δ vs store), not the candidate in isolation; a
  rule-regression suite requires no degradation on episodes existing rules
  handle, and a contradiction check runs at promotion. Statistics: power
  analysis in the test plan; sequential testing with alpha-spending;
  promote on lower confidence bound > 0; Holm–Bonferroni family-wise error
  control across candidates. If the episode budget cannot support the
  required n, FR-B4 is unexecutable as specified — use a cheaper proxy and
  document the substitution explicitly in the ledger. Acceptable proxies
  must remain oracle-verified (for example, a smaller oracle-scored sample
  with wider confidence bounds); judge-flag counts are never an acceptable
  proxy. Record the delta and
  the store content identifier at promotion.
- **FR-B5 — Update with the ledger as source of truth.** The decision ledger
  is the system of record; the rule store is a derived snapshot rebuildable
  by replay from the ledger. Store updates must be atomic and crash-safe.
  Every ledger entry records: rule id, exact rule text, verdict, delta, raw
  A/B counts, held-out episode ID set, store content identifier, taxonomy
  version, epoch. Any historical promotion must be replayable from ledger +
  episodes alone with a reproducing delta.
- **FR-B6 — Evict stale rules; re-validate on a fixed cadence.** Every rule carries a death
  condition: confidence floor, disuse eviction, failed re-validation, or
  reverse ablation (evict when removing the rule helps or is neutral within
  tolerance — a rule survives only if its presence demonstrably reduces
  failures). The
  learning gate (new failures → reflect/select) is split from periodic
  re-validation: re-validate every N epochs regardless of new failures, so
  quiet periods cannot leave stale rules with unchanged credit scores.
  Gate decisions are ledgered as idempotent entries.
- **FR-B7 — Atomic, idempotent epochs.** An epoch commits in idempotent
  stages, each recorded in an epoch progress marker. After a crash, reruns
  resume from the last committed stage instead of restarting the epoch:
  no duplicate appends, no phantom denominators. All stages downstream of
  extraction are deterministic — rerunning them over the same extracted
  episodes reproduces identical counts and confidence values. The judge is
  stochastic; rerunning extraction is not expected to reproduce identical
  episodes.

## 3. Logical data model

The system works with the following logical records. Their attributes and
invariants are requirements; **serialization formats, file names, and
storage layout are design-time decisions** (OQ-9).

- **Trajectory record.** Attributes: id, task description, ordered typed
  events (each: type, timestamp, content, metadata). Invariant: no invented
  events; gaps marked as system notes.
- **Judge-output record.** Attributes: trajectory id, task description,
  taxonomy version, findings[] (each: severity, category, confidence,
  description, optional attribution), outcome tier. Invariant: closed 24-label
  vocabulary.
- **Episode record.** Attributes: content-derived id, task, action summary,
  outcome, failure categories, taxonomy version, trace reference.
  Invariant: the trace suffices to re-derive the finding under a new
  taxonomy version.
- **Pattern record.** Attributes: id, failure category, task prefix, member
  episode ids, confidence, epoch formed.
- **Rule record.** Attributes: id, when/then text, source pattern,
  confidence, credit/strength with update dynamics, status, verdict
  history.
- **Decision-ledger entry.** Attributes: epoch, rule id, exact rule text,
  verdict, delta, raw A/B counts, held-out episode id set, store content
  identifier, taxonomy version. Invariant: append-only; sufficient to
  replay any promotion.
- **Epoch progress record.** Attributes: epoch id, staged commit markers.
  Invariant: reruns are idempotent.

**Mode A→B handoff.** One handoff per judged trajectory: the Judge-output
record plus the retained trace (retention per OQ-7). Mode B consumes this
handoff and never raw transcripts.

## 4. Non-functional requirements

- **NFR-1 — Taxonomy versioning, enforced.** The 24-label vocabulary is
  pinned and versioned; the version is stamped on every finding, episode,
  pattern, and rule. Mixed-version clustering is refused with an explicit
  error, never silently; version bumps require an explicit migration map.
  Bumps are authorized by the human skill operator, never by the loop
  itself. A migration map must cover every label of the old version —
  checked mechanically for complete coverage and valid mapping kinds —
  and pass human review before commit.
- **NFR-2 — Bounded memory.** The rule store must remain small enough to
  inject wholesale. Growth is sublinear by construction (confidence floor +
  eviction); if the store cannot be injected whole, the bounded-memory
  requirement is violated.
- **NFR-3 — Epoch scoreboard with precision floor and halt condition.** The
  scoreboard is **oracle-verified failures prevented per epoch**, with a
  precision floor and a halt condition. (Cost accounting deferred with
  FR-A5.) The precision floor measures finding-level category precision —
  the fraction of judge findings whose category matches adjudicator
  consensus. The threshold is calibrated from the AC-5 gate: precision may
  not fall more than 0.10 below the gate-measured baseline (margin subject
  to recalibration). Each epoch adjudicates a fresh sample via an
  independent decision model (separated model family) or human spot-checks;
  re-scoring the fixed calibration set serves only as a drift warning. Two
  consecutive breaches fire the halt condition.
- **NFR-4 — Deterministic validation gate.** A validator program checks
  every emitted record against the schema; no unvalidated output is ever
  presented.
- **NFR-5 — Rule strength as a function of recency, prediction error, and retrieval outcomes.**
  Rule confidence/credit incorporates recency decay and prediction-error
  weighting; retrieval outcomes update the rule. Exact dynamics are a
  design-stage decision; the requirement is that strength values must
  change with observed outcomes — a fixed constant is not acceptable.

## 5. Acceptance criteria

- **AC-1.** Mode A on a sample trajectory emits validator-clean output with
  ≥1 finding categorized per the taxonomy, confidence-scored, and
  step-attributed.
- **AC-2.** Mode B over a labeled episode set promotes ≥1 rule with a
  positive held-out delta measured against the independent oracle,
  ledger-recorded with full provenance.
- **AC-3.** Rule-store size stays bounded over 5 epochs while oracle-verified
  failures/1k trends down **and task-completion rate does not regress**
  (the completion-rate clause blocks degenerate strategies that cut
  failures by attempting fewer tasks).
- **AC-4 (deferred with FR-A5).** Every judge run in the test set includes a complete,
  non-negative cost report; every epoch includes itemized loop cost.
- **AC-5 — Calibration gate (kill criterion KC-1).** Before building the
  loop: 2–3 annotators, 200 trajectories, Cohen's κ on the 24-label
  taxonomy. κ < ~0.4 → the taxonomy is not a measurement instrument: fall
  back to binary outcomes + oracles, do not build the categorized loop.

## 6. Kill criteria

- **KC-1.** Calibration study fails (κ < ~0.4) → taxonomy is not a valid
  instrument; ship Mode A as measurement-only on binary outcomes, kill the
  categorized closed loop.
- **KC-2.** No independent success oracle is available for the target domain
  → ship Mode A as measurement-only; kill the closed loop (without an
  independent oracle the loop optimizes the judge's flags, not task
  success).

## 7. Out of scope

- Real-time monitoring or alerting on live agent fleets.
- Multi-agent ToM attribution beyond step attribution (H-ToM-1..4, H-SYN-1
  live in the research thread — `research-program/hypotheses.md` — not in
  ship requirements).
- The 36-paper literature corpus (`research-program/papers.md`): grounding
  for the research thread, not a ship deliverable.
- Skill packaging for System2-UtilitySkills (`plugin/skills/` single-file
  layout) — a design-stage decision (OQ-4).

## 8. Open questions for design

- **OQ-1.** Pattern-formation mechanics: counting-window definition, null-model
  construction, and whether per-finding confidence weights the counts.
- **OQ-2.** Power analysis for the select stage: minimum held-out n per
  pattern; if the budget cannot support it, the cheaper documented proxy.
- **OQ-3.** Credit dynamics: prediction-error weighting, recency decay
  constants, re-validation cadence N (NFR-5, FR-B6).
- **OQ-4.** Final skill packaging: single `SKILL.md` per repo convention vs.
  multi-file layout with `references/` + `bin/`.
- **OQ-5.** What counts as the independent success oracle per domain (env
  state, task tests, human spot-checks) — required to have one, open which
  one.
- **OQ-6.** Calibration study protocol: annotator pool, sample, κ threshold
  (AC-5 / KC-1).
- **OQ-7.** Trace retention for re-derivation: exactly which attributes survive
  harvest (typed events yes; bulky payloads no — where is the line?).
- **OQ-8.** Is a periodic offline consolidation pass needed in addition to
  event-driven gating, or does the fixed-cadence re-validation (FR-B6) suffice?
- **OQ-9.** Serialization and storage: JSON vs Parquet vs embedded DB vs …
  — plus file layout and store topology.

## 9. Traceability

| Requirement | Source |
|---|---|
| FR-A1–A6 | concept.md § Approach (Mode A) |
| FR-A2 tier-1 thresholds retuned from tier-2 labels | Adversarial review (neuroscience §5) |
| FR-A3 confidence field | Adversarial review (ai-sci §1) |
| FR-A4 mechanical tiers | Adversarial review (ai-sci §6) |
| FR-B1 re-derivable traces, content-derived IDs | Adversarial review (neuro §1; distsys §1, §4) |
| FR-B2 recurrence clustering, chance-beating floor, valence | Adversarial review (ai-sci §1, §5; neuro §3); simplified — weighting, window, and null mechanics moved to design (OQ-1) |
| FR-B3 | v1 FR-B3 (unchanged) |
| FR-B4 oracle, separation, stats, snapshot A/B, regression suite | Adversarial review (ai-sci §2, §3; distsys §3) |
| FR-B5 ledger-as-truth, provenance | Adversarial review (distsys §2, §6) |
| FR-B6 fixed-cadence re-validation | Adversarial review (distsys §5) |
| FR-B7 epoch transactions | Adversarial review (distsys §1) |
| NFR-1 versioning enforced | Adversarial review (distsys §4; neuro §1) |
| NFR-3 epoch scoreboard | Adversarial review (ai-sci §4) |
| NFR-5 memory dynamics | Adversarial review (neuro §4) |
| AC-3 completion-rate clause | Adversarial review (neuro §3) |
| AC-5, KC-1, KC-2 | Adversarial review (ai-sci kill criteria) |
