# Research program charter

The research thread for trajectory-metaloop. It runs on its own cadence and
feeds validated findings into the ship track (Mode A skill, then Mode B
learning system) as feature proposals. The ship track never waits on the
research thread.

## Contents

- `hypotheses.md` — the 13-hypothesis backlog, ordered by testability with
  cheapest falsification first.
- `papers.md` — the 36-paper literature corpus grounding the hypotheses.
- `evaluations/` — one note per evaluated hypothesis.
- `charter.md` — this file.

## Cadence

At least one hypothesis evaluated per day, in backlog order. Each evaluation
produces exactly one concrete output: either a test that would validate or
falsify the hypothesis, or a precise statement of the data required to run
such a test. The evaluation note records the design, the findings, and the
disposition (confirmed, refuted, or needs-data).

## Feed-in

A validated finding becomes a feature proposal for the ship track when it
identifies a concrete change to Mode A or Mode B: a new detection, a new
rule type, a calibration improvement, or a cost reduction. The proposal is
recorded in the evaluation note; the ship track adopts it through its own
stage gates. Refuted hypotheses are recorded as refuted — a closed question
is also a result.
