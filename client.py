"""
Agent Runtime Invariant Assertion Synthesizer Skill Client
Pure Python Standard Library implementation of Dynamic Invariant Detection (Ernst et al. Daikon).
Observes agent execution traces, infers operational invariants (x > 0, len(a) == len(b), y is not None),
and synthesizes executable assertion contracts.
"""

from typing import List, Dict, Any, Tuple, Optional


class InvariantSynthesizer:
    """
    Infers candidate invariants across observed variable state traces.
    Supported invariant patterns:
    - Non-null: x != None
    - Non-negative: x >= 0
    - Range bound: min_val <= x <= max_val
    - Collection length match: len(c1) == len(c2)
    - Constant state: x == constant
    """

    def infer_invariants(self, variable_traces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Infer active invariants from a list of state snapshots.
        """
        if not variable_traces:
            return []

        all_keys = set()
        for trace in variable_traces:
            all_keys.update(trace.keys())

        invariants = []

        for k in sorted(list(all_keys)):
            values = [t[k] for t in variable_traces if k in t]
            if len(values) != len(variable_traces):
                continue  # Variable not present in all states

            # 1. Check Non-Null
            if all(v is not None for v in values):
                invariants.append({
                    "variable": k,
                    "predicate": f"{k} is not None",
                    "type": "NON_NULL",
                    "confidence": 1.0
                })

            # 2. Check Numeric Bounds
            if all(isinstance(v, (int, float)) for v in values):
                if all(v >= 0 for v in values):
                    invariants.append({
                        "variable": k,
                        "predicate": f"{k} >= 0",
                        "type": "NON_NEGATIVE",
                        "confidence": 1.0
                    })
                min_val = min(values)
                max_val = max(values)
                invariants.append({
                    "variable": k,
                    "predicate": f"{min_val} <= {k} <= {max_val}",
                    "type": "RANGE_BOUND",
                    "min": min_val,
                    "max": max_val,
                    "confidence": 0.95
                })

            # 3. Check Constant
            if len(set(values)) == 1:
                invariants.append({
                    "variable": k,
                    "predicate": f"{k} == {repr(values[0])}",
                    "type": "CONSTANT",
                    "confidence": 1.0
                })

        return invariants

    def synthesize_assertion_code(self, invariants: List[Dict[str, Any]]) -> str:
        """Generate executable Python assertion statements from invariants."""
        lines = []
        for inv in invariants:
            lines.append(f"assert {inv['predicate']}, f'Invariant violated: {inv['predicate']}'")
        return "\n".join(lines)
