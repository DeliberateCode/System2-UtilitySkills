#!/usr/bin/env python3
"""Validate an ATFD-style JudgeOutput JSON file.

Usage: judge-lint.py <judge_output.json>
Exits 0 when clean, 1 with errors listed otherwise.
"""
import json
import sys

VALID_CATEGORIES = {
    "action.wrong_tool", "action.wrong_args", "action.missing_action",
    "state.wrong_state", "state.partial_state",
    "communication.wrong_response", "communication.missing_info",
    "communication.hallucination",
    "quality.shallow_output", "quality.suboptimal_approach", "quality.poor_tone",
    "quality.incomplete_analysis", "quality.low_confidence_output",
    "process.tool_loop", "process.infinite_delegation", "process.context_overflow",
    "process.planning_failure",
    "safety.permission_escalation", "safety.data_leakage", "safety.policy_violation",
    "infrastructure.timeout", "infrastructure.error", "infrastructure.max_steps",
    "infrastructure.prompt_injection",
}
VALID_SEVERITIES = {"error", "warning", "info"}
VALID_OUTCOMES = {"pass", "degraded", "fail"}


def err(errors, msg):
    errors.append(msg)


def check(data):
    errors = []
    if not isinstance(data, dict):
        return ["top level must be a JSON object"]

    for field in ("trajectory_id", "has_failure", "findings", "cost"):
        if field not in data:
            err(errors, f"missing required field: {field}")

    if "trajectory_id" in data and not isinstance(data["trajectory_id"], str):
        err(errors, "trajectory_id must be a string")
    if "has_failure" in data and not isinstance(data["has_failure"], bool):
        err(errors, "has_failure must be a boolean")
    if "outcome" in data and data["outcome"] not in VALID_OUTCOMES:
        err(errors, f"outcome must be one of {sorted(VALID_OUTCOMES)}")

    findings = data.get("findings")
    if findings is not None:
        if not isinstance(findings, list):
            err(errors, "findings must be a list")
        else:
            for i, f in enumerate(findings):
                tag = f"findings[{i}]"
                if not isinstance(f, dict):
                    err(errors, f"{tag} must be an object")
                    continue
                if f.get("severity") not in VALID_SEVERITIES:
                    err(errors, f"{tag}.severity must be one of {sorted(VALID_SEVERITIES)}")
                if f.get("category") not in VALID_CATEGORIES:
                    err(errors, f"{tag}.category '{f.get('category')}' not in the 24-subcategory taxonomy")
                if not isinstance(f.get("description"), str) or not f["description"].strip():
                    err(errors, f"{tag}.description must be a non-empty string")
                if "attribution" in f:
                    a = f["attribution"]
                    if not isinstance(a, list) or not all(isinstance(x, int) for x in a):
                        err(errors, f"{tag}.attribution must be a list of event indices (ints)")

    cost = data.get("cost")
    if cost is not None:
        if not isinstance(cost, dict):
            err(errors, "cost must be an object")
        else:
            for field, kind in (("dollar_cost", float), ("latency_seconds", float),
                                ("total_tokens", int), ("api_calls", int)):
                v = cost.get(field)
                if v is None:
                    err(errors, f"cost.{field} is required")
                elif not isinstance(v, kind) or isinstance(v, bool) or v < 0:
                    err(errors, f"cost.{field} must be a non-negative {kind.__name__}")

    return errors


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <judge_output.json>", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1]) as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not read JSON: {exc}", file=sys.stderr)
        return 2
    errors = check(data)
    if errors:
        print(f"{len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("clean: JudgeOutput valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
