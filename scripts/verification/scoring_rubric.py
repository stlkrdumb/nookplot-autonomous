#!/usr/bin/env python3
"""
Verification Scoring Rubric Generator
Generates scoring rubrics for verification submissions.
"""

import json
import sys


RUBRIC_TEMPLATE = {
    "correctness": {
        "description": "Was the final answer correct?",
        "max_score": 1.0,
        "criteria": [
            {
                "range": [0.9, 1.0],
                "label": "Fully correct",
                "description": "Answer is correct with complete reasoning"
            },
            {
                "range": [0.7, 0.9],
                "label": "Mostly correct",
                "description": "Answer is correct with minor reasoning gaps"
            },
            {
                "range": [0.5, 0.7],
                "label": "Partially correct",
                "description": "Answer is partially correct or has significant gaps"
            },
            {
                "range": [0.0, 0.5],
                "label": "Incorrect",
                "description": "Answer is wrong or reasoning is fundamentally flawed"
            }
        ]
    },
    "reasoning": {
        "description": "Quality of structured reasoning process",
        "max_score": 1.0,
        "criteria": [
            {
                "range": [0.9, 1.0],
                "label": "Excellent",
                "description": "Clear structured sections, step-by-step logic, uncertainty acknowledged"
            },
            {
                "range": [0.7, 0.9],
                "label": "Good",
                "description": "Well-organized reasoning with clear progression"
            },
            {
                "range": [0.5, 0.7],
                "label": "Fair",
                "description": "Reasoning present but lacks clear structure"
            },
            {
                "range": [0.0, 0.5],
                "label": "Poor",
                "description": "No clear reasoning or logical progression"
            }
        ]
    },
    "efficiency": {
        "description": "Reached conclusion without unnecessary steps",
        "max_score": 1.0,
        "criteria": [
            {
                "range": [0.9, 1.0],
                "label": "Excellent",
                "description": "Direct path, identifies dead ends, avoids unnecessary steps"
            },
            {
                "range": [0.7, 0.9],
                "label": "Good",
                "description": "Efficient reasoning with minor unnecessary steps"
            },
            {
                "range": [0.5, 0.7],
                "label": "Fair",
                "description": "Some redundant steps but reaches conclusion"
            },
            {
                "range": [0.0, 0.5],
                "label": "Poor",
                "description": "Excessive unnecessary steps or failure to conclude"
            }
        ]
    },
    "novelty": {
        "description": "Originality and insight in approach",
        "max_score": 1.0,
        "criteria": [
            {
                "range": [0.9, 1.0],
                "label": "Excellent",
                "description": "Original insights, cross-domain connections, novel approaches"
            },
            {
                "range": [0.7, 0.9],
                "label": "Good",
                "description": "Some original elements, good insight application"
            },
            {
                "range": [0.5, 0.7],
                "label": "Fair",
                "description": "Standard approach applied correctly"
            },
            {
                "range": [0.0, 0.5],
                "label": "Poor",
                "description": "No original insight, purely templated response"
            }
        ]
    }
}


def generate_rubric(domain: str = "security") -> json:
    """Generate a domain-specific scoring rubric."""
    rubric = RUBRIC_TEMPLATE.copy()
    rubric['domain'] = domain
    rubric['version'] = '1.0'
    return rubric


def print_rubric_as_markdown(rubric: dict):
    """Print rubric as formatted markdown."""
    print(f"# Verification Scoring Rubric ({rubric['domain']})")
    print(f"Version: {rubric['version']}\n")
    
    for dimension, data in rubric.items():
        if dimension in ['domain', 'version']:
            continue
        print(f"## {dimension.upper()}")
        print(f"**Description:** {data['description']}\n")
        print("| Score Range | Label | Description |")
        print("|-------------|-------|-------------|")
        for criterion in data['criteria']:
            print(f"| {criterion['range'][0]}-{criterion['range'][1]} | {criterion['label']} | {criterion['description']} |")
        print()


if __name__ == '__main__':
    domain = sys.argv[1] if len(sys.argv) > 1 else 'security'
    rubric = generate_rubric(domain)
    print_rubric_as_markdown(rubric)
