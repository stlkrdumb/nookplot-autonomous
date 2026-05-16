#!/usr/bin/env python3
"""
Batch Verification Trace Analyzer
Analyzes multiple verification traces for quality scoring.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple


class BatchTraceAnalyzer:
    """Batch analyzer for verification traces."""
    
    def __init__(self, trace_dir: str):
        self.trace_dir = Path(trace_dir)
        self.results = []
    
    def analyze_directory(self) -> List[Dict]:
        """Analyze all JSON traces in directory."""
        for trace_file in self.trace_dir.glob("*.json"):
            try:
                with open(trace_file) as f:
                    data = json.load(f)
                result = self.analyze_trace(data)
                result['file'] = trace_file.name
                self.results.append(result)
            except Exception as e:
                self.results.append({
                    'file': trace_file.name,
                    'error': str(e)
                })
        return self.results
    
    def analyze_trace(self, trace: Dict) -> Dict:
        """Analyze a single trace."""
        content = trace.get('content', '')
        sections = self._parse_sections(content)
        
        return {
            'correctness': self._score_correctness(sections, content),
            'reasoning': self._score_reasoning(sections),
            'efficiency': self._score_efficiency(sections, content),
            'novelty': self._score_novelty(sections, content),
            'char_count': len(content),
            'section_count': len(sections)
        }
    
    def _parse_sections(self, content: str) -> Dict[str, str]:
        sections = {}
        current = None
        lines = []
        for line in content.split('\n'):
            if line.startswith('## '):
                if current:
                    sections[current] = '\n'.join(lines)
                current = line[3:].strip().lower()
                lines = []
            else:
                lines.append(line)
        if current:
            sections[current] = '\n'.join(lines)
        return sections
    
    def _score_correctness(self, sections, content) -> float:
        score = 0.5
        if any(k in content.lower() for k in ['verify', 'check', 'confirm']):
            score += 0.2
        if any(k in content.lower() for k in ['uncertain', 'might', 'assume']):
            score += 0.1
        if 'approach' in sections:
            score += 0.1
        return min(score, 1.0)
    
    def _score_reasoning(self, sections) -> float:
        score = 0.5
        for section in ['approach', 'steps', 'conclusion', 'uncertainty']:
            if section in sections:
                score += 0.1
        return min(score, 1.0)
    
    def _score_efficiency(self, sections, content) -> float:
        score = 0.5
        if len(content) < 5000:
            score += 0.2
        if 'conclusion' in sections and len(sections['conclusion']) > 50:
            score += 0.15
        return min(score, 1.0)
    
    def _score_novelty(self, sections, content) -> float:
        score = 0.5
        if any(k in content.lower() for k in ['first principles', 'unusual', 'unexpected']):
            score += 0.2
        return min(score, 1.0)
    
    def print_summary(self):
        """Print summary of all analyzed traces."""
        for r in self.results:
            if 'error' in r:
                print(f"{r['file']}: ERROR - {r['error']}")
            else:
                avg = (r['correctness'] + r['reasoning'] + r['efficiency'] + r['novelty']) / 4
                print(f"{r['file']}: avg={avg:.2f} C={r['correctness']:.2f} R={r['reasoning']:.2f} E={r['efficiency']:.2f} N={r['novelty']:.2f} chars={r['char_count']}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        analyzer = BatchTraceAnalyzer(sys.argv[1])
    else:
        analyzer = BatchTraceAnalyzer('traces/')
    
    if os.path.exists(analyzer.trace_dir):
        analyzer.analyze_directory()
        analyzer.print_summary()
    else:
        print(f"Directory {analyzer.trace_dir} not found")
