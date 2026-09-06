"""
MCP Server for Agent Runtime Invariant Assertion Synthesizer Skill.
"""

import json
import sys
from client import InvariantSynthesizer

SYNTHESIZER = InvariantSynthesizer()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "infer_invariants",
                    "description": "Infer active invariants across state snapshots",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "variable_traces": {"type": "array", "items": {"type": "object"}}
                        },
                        "required": ["variable_traces"]
                    }
                },
                {
                    "name": "synthesize_assertion_code",
                    "description": "Generate executable assertion code contract from invariants",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "invariants": {"type": "array", "items": {"type": "object"}}
                        },
                        "required": ["invariants"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "infer_invariants":
            invs = SYNTHESIZER.infer_invariants(args["variable_traces"])
            return {"content": [{"type": "text", "text": json.dumps(invs)}]}

        elif tool_name == "synthesize_assertion_code":
            code = SYNTHESIZER.synthesize_assertion_code(args["invariants"])
            return {"content": [{"type": "text", "text": json.dumps({"assertions": code})}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
