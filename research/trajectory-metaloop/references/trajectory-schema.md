# Trajectory & JudgeOutput Schemas

Adapted from galea-foo/atfd `src/atfd/schema.py` (CC BY 4.0). JSON field names are kept identical so output can feed ATFD tooling.

## Trajectory (input to Mode A)

```json
{
  "trajectory_id": "run_2026_10_10_001",
  "task_description": "Book a flight and hotel for two under $1500",
  "domain": "travel",
  "events": [
    {"type": "user_message", "timestamp": "2026-10-10T10:00:00Z",
     "content": "Book me...", "metadata": {}},
    {"type": "assistant_message", "timestamp": "2026-10-10T10:00:12Z",
     "content": "I'll search flights...", "metadata": {"model": "muse-spark"}},
    {"type": "tool_call", "timestamp": "2026-10-10T10:00:13Z",
     "content": "{\"tool\": \"flight_search\", \"args\": {...}}", "metadata": {}},
    {"type": "tool_result", "timestamp": "2026-10-10T10:00:15Z",
     "content": "{...}", "metadata": {"latency_ms": 2100}},
    {"type": "system", "timestamp": "2026-10-10T10:00:00Z",
     "content": "transcript starts mid-run; 3 prior turns unavailable", "metadata": {}}
  ]
}
```

Event `type` enum: `user_message | assistant_message | tool_call | tool_result | system`. Use `system` events to mark gaps, redactions, or harness notes — never silently invent missing turns.

## JudgeOutput (output of Mode A)

```json
{
  "trajectory_id": "run_2026_10_10_001",
  "has_failure": true,
  "outcome": "fail",
  "findings": [
    {"severity": "error",
     "category": "action.wrong_args",
     "description": "Booked SFO→JFK instead of the requested SFO→BOS",
     "attribution": [7, 9]},
    {"severity": "warning",
     "category": "communication.missing_info",
     "description": "Never told the user the total exceeded the $1500 budget",
     "attribution": [12]}
  ],
  "cost": {"dollar_cost": 0.023, "latency_seconds": 8.4,
           "total_tokens": 11200, "api_calls": 2}
}
```

- `severity` enum: `error | warning | info`.
- `category`: one of the 24 dotted strings in `atfd-taxonomy.md`.
- `attribution`: optional list of event indices grounding the finding.
- `outcome` enum: `pass | degraded | fail`.
- `cost` reports *the judge run itself* — always filled, never omitted.

## Mapping agent transcripts

| Source concept | Trajectory field |
|---|---|
| Session / run id | `trajectory_id` |
| User's original request | `task_description` |
| Each model turn | `assistant_message` |
| Each tool invocation (name + args) | `tool_call` |
| Each tool response | `tool_result` |
| Missing/redacted context | `system` note |
