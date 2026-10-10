# Memory-Efficient Metaloop Method

The capture method behind Mode B. Design sources: metaloop's harvest→reflect→aggregate→select→update pipeline, MENTOR's rule-graph memory, DPPO's diagnose-gated curation, Reflexion's verbal-reflection buffer, and RecMem's recurrence-gated consolidation. The through-line: **never persist raw trajectories; each stage's output is the next stage's input, each step cutting volume by an order of magnitude or more.**

## The funnel

```
trajectories ──harvest──▶ episodes ──reflect──▶ patterns ──aggregate──▶ rules
     (dropped)        (jsonl tuples)      (clusters+confidence)   (validated, scored)
```

## Record schemas

**Episode** (`episodes.jsonl`, one per line) — the minimal durable unit:
```json
{"id": "ep_0042", "task": "book flight+hotel <$1500",
 "action_summary": "booked wrong destination, omitted budget warning",
 "outcome": "fail", "failure_categories": ["action.wrong_args", "communication.missing_info"],
 "epoch": 3}
```

**Pattern** (`patterns.json`) — a cluster that cleared the confidence floor:
```json
{"id": "pat_07", "failure_category": "action.wrong_args",
 "task_prefix": "book flight",
 "episodes": ["ep_0042", "ep_0051", "ep_0063"],
 "confidence": 0.43, "epoch_formed": 3}
```
`confidence = occurrences / total_episodes`. Floor default `0.3` (tunable).

**Rule** (`rules.json`) — the only thing that lives long-term:
```json
{"id": "rule_011", "text": "when booking travel then echo destination + total back to user before confirming",
 "source_pattern": "pat_07", "confidence": 0.43,
 "credit": 5.0, "status": "active",
 "verdict_history": [{"epoch": 4, "verdict": "promote", "delta": 0.18}]}
```

**Ledger** (`ledger.jsonl`) — every select-stage decision, append-only:
```json
{"epoch": 4, "rule": "rule_011", "verdict": "promote|hold|discard|revert|evict",
 "delta": 0.18, "n_heldout": 12}
```

## Lifecycle & eviction (every memory needs a death condition)

- **Credit:** starts 5.0, clamped [0, 10]. Gains on successful re-validation, loses on disuse or failed re-checks. Freeze at ≥8 (`retained`); reforge at ≤2.
- **Eviction triggers:** 3 consecutive inconclusive validations → archive; reverse check (does removing the rule hurt?) → if removal helps or is neutral, revert; N epochs unused → evict.
- **Revert is single-rule**, never whole-store restore.
- **IDs are content hashes**, never positional — positional ids silently drop rules on reorder.

## Selective invocation (the cost control)

- The cheap detector (Mode A tier-1 heuristics) is the gate: no new failures → skip reflect/select this epoch entirely.
- Reflection/validation budget goes to residual failures and low-confidence patterns only — routine passes stay single-pass.
- Reference point: RecMem cut memory-construction tokens 77–87% with the same gating idea (consolidate only on sustained recurrence).

## Worked mini-example

1. Epoch 3 harvests 40 episodes; 6 share `action.wrong_args` on flight-booking tasks → `pat_07` at confidence 0.43 → kept (above the 0.3 floor).
2. Aggregate → `rule_011`: "when booking travel then echo destination + total back to user before confirming".
3. Select: 12 held-out booking episodes, half run with the rule injected. Failure rate 5/6 → 1/6 with the rule: delta +0.67 → promote.
4. Ledger records the promotion; rule_011 ships in the next epoch's prompt.
5. Epoch 9: rule_011 unused for 5 epochs and a re-check shows no delta → evicted. The store stays small enough to inject wholesale.

## What NOT to do

- Don't persist raw trajectories past harvest (the #1 memory blowup).
- Don't promote without a held-out delta — correlation in the harvest set is not evidence.
- Don't let the rule store grow unbounded: if it can't be injected wholesale, the funnel failed — tighten the confidence floor or eviction cadence.
