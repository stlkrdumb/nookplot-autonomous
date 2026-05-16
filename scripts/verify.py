#!/usr/bin/env python3
"""
RLM Security Challenge Verifier
Uses RLMSecurityScorer to produce genuine variance verification scores.
Run this before calling nookplot_verify_reasoning_submission.
"""

import json
import sys

def verify(challenge_id: str, trace_content: str, submission_id: str):
    """
    Verify a submission with calibrated score variance.
    Returns dict ready to pass to nookplot_verify_reasoning_submission.
    """
    from scripts.rlm_scorer import score_trace

    result = score_trace(trace_content, "security")
    scores = result["scores"]

    # Build 4D justification with trace-specific references
    justification = (
        f"Correctness: {result['justifications']['correctness']} "
        f"Reasoning: {result['justifications']['reasoning']} "
        f"Efficiency: {result['justifications']['efficiency']} "
        f"Novelty: {result['justifications']['novelty']}"
    )

    # Domain-tagged knowledge insight
    knowledge_insight = (
        f"RLM security traces must go beyond naming the vulnerability — "
        f"include the SWC reference, attack preconditions, economic impact estimate, "
        f"and a concrete fix. Traces missing any of these four elements score below 0.7 "
        f"on reasoning quality regardless of correctness."
    )

    return {
        "submission_id": submission_id,
        "correctness_score": scores["correctness"],
        "reasoning_score": scores["reasoning"],
        "efficiency_score": scores["efficiency"],
        "novelty_score": scores["novelty"],
        "justification": justification,
        "knowledge_insight": knowledge_insight,
        "domain_tags": ["security", "smart-contracts", "solidity", "rlm"],
        "quality_tier": result["quality_tier"],
        "variance_report": result["variance_report"],
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python verify.py <submission_id> <trace_content_file>")
        sys.exit(1)

    submission_id = sys.argv[1]
    trace_file = sys.argv[2]

    with open(trace_file) as f:
        trace_content = f.read()

    result = verify("placeholder", trace_content, submission_id)

    print("=" * 60)
    print("VERIFICATION SCORES (ready to paste into nookplot tool)")
    print("=" * 60)
    print(f"submission_id: {result['submission_id']}")
    print(f"correctness_score: {result['correctness_score']}")
    print(f"reasoning_score: {result['reasoning_score']}")
    print(f"efficiency_score: {result['efficiency_score']}")
    print(f"novelty_score: {result['novelty_score']}")
    print(f"\njustification:\n{result['justification']}")
    print(f"\nknowledge_insight:\n{result['knowledge_insight']}")
    print(f"\ndomain_tags: {result['domain_tags']}")
    print(f"\nquality_tier: {result['quality_tier']}")
    print(f"variance (stddev): {result['variance_report']['std']:.4f}")