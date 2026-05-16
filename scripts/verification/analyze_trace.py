#!/usr/bin/env python3
"""
Verification Trace Analyzer
Analyzes Solidity smart contract reasoning traces for quality and completeness.
"""

import json
import sys
from typing import List, Dict, Tuple


class TraceAnalyzer:
    """Analyzes verification traces for scoring dimensions."""
    
    def __init__(self, trace_content: str):
        self.trace = trace_content
        self.sections = self._parse_sections()
    
    def _parse_sections(self) -> Dict[str, str]:
        """Parse structured markdown trace into sections."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in self.trace.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip().lower()
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        return sections
    
    def score_correctness(self) -> float:
        """Score correctness dimension (0-1)."""
        score = 0.5
        
        # Check for claim substantiation
        if 'citation' in self.trace.lower() or 'source' in self.trace.lower():
            score += 0.15
        
        # Check for verification step
        if 'verify' in self.trace.lower() or 'check' in self.trace.lower():
            score += 0.15
        
        # Check for uncertainty acknowledgment
        if 'uncertain' in self.trace.lower() or 'might' in self.trace.lower():
            score += 0.1
        
        # Check for dead-end documentation
        if 'rejected' in self.trace.lower() or 'discarded' in self.trace.lower():
            score += 0.1
        
        return min(score, 1.0)
    
    def score_reasoning(self) -> float:
        """Score reasoning quality dimension (0-1)."""
        score = 0.5
        
        # Structured sections
        if 'approach' in self.sections:
            score += 0.1
        if 'steps' in self.sections:
            score += 0.1
        if 'conclusion' in self.sections:
            score += 0.1
        if 'uncertainty' in self.sections:
            score += 0.1
        
        # Step count (more steps = more thorough)
        steps = self.sections.get('steps', '')
        if steps:
            step_count = steps.lower().count('step ')
            if step_count >= 3:
                score += 0.1
        
        return min(score, 1.0)
    
    def score_efficiency(self) -> float:
        """Score efficiency dimension (0-1)."""
        score = 0.5
        
        # Avoids unnecessary steps
        if len(self.trace) < 5000:
            score += 0.2
        elif len(self.trace) < 10000:
            score += 0.1
        
        # Direct path to conclusion
        if 'conclusion' in self.sections:
            conclusion = self.sections['conclusion']
            if len(conclusion) > 50:
                score += 0.15
        
        # Identifies dead ends quickly
        if 'rejected' in self.trace.lower() or 'abandoned' in self.trace.lower():
            score += 0.15
        
        return min(score, 1.0)
    
    def score_novelty(self) -> float:
        """Score novelty/originality dimension (0-1)."""
        score = 0.5
        
        # Original insights
        if 'first principles' in self.trace.lower():
            score += 0.2
        if 'unusual' in self.trace.lower() or 'unexpected' in self.trace.lower():
            score += 0.2
        
        # Cross-domain connections
        if any(domain in self.trace.lower() for domain in ['security', 'economics', 'game theory']):
            score += 0.1
        
        return min(score, 1.0)
    
    def get_scores(self) -> Dict[str, float]:
        """Return all four dimension scores."""
        return {
            'correctness': self.score_correctness(),
            'reasoning': self.score_reasoning(),
            'efficiency': self.score_efficiency(),
            'novelty': self.score_novelty()
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_trace.py <trace_file.json>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        trace = json.load(f)
    
    analyzer = TraceAnalyzer(trace['content'])
    scores = analyzer.get_scores()
    
    print(json.dumps(scores, indent=2))
    
    composite = sum(scores.values()) / len(scores)
    print(f"\nComposite score: {composite:.2f}")


if __name__ == '__main__':
    main()
