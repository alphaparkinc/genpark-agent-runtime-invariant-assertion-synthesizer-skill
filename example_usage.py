"""
Example usage of Agent Runtime Invariant Assertion Synthesizer Skill.
"""

from client import InvariantSynthesizer


def main():
    print("=== Agent Runtime Invariant Assertion Synthesizer Demonstration ===")
    synthesizer = InvariantSynthesizer()

    # Observed agent execution states across 5 iterations
    traces = [
        {"token_budget": 1000, "active_workers": 4, "error_code": 0, "session_id": "sess_88"},
        {"token_budget": 850,  "active_workers": 4, "error_code": 0, "session_id": "sess_88"},
        {"token_budget": 620,  "active_workers": 2, "error_code": 0, "session_id": "sess_88"},
        {"token_budget": 410,  "active_workers": 1, "error_code": 0, "session_id": "sess_88"},
        {"token_budget": 150,  "active_workers": 1, "error_code": 0, "session_id": "sess_88"}
    ]

    print("Observing 5 Execution State Snapshots...")
    invariants = synthesizer.infer_invariants(traces)

    print(f"\nInferred {len(invariants)} Invariants:")
    for inv in invariants:
        print(f"  [{inv['type']:<12}]: {inv['predicate']}")

    print("\nSynthesized Assertion Guard Contract:")
    assertions = synthesizer.synthesize_assertion_code(invariants)
    print(assertions)


if __name__ == "__main__":
    main()
