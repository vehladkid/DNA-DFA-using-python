# src/__init__.py
"""
DNA Pattern Matching using DFA and Aho-Corasick Algorithm
Version: 1.0
"""

from .dfa_engine import DFAStateMachine
from .aho_corasick import AhoCorasick
from .sequence_handler import SequenceHandler
from .motif_database import MotifDatabase
from .benchmark import BenchmarkRunner
from .performance_analyzer import PerformanceAnalyzer

__all__ = [
    'DFAStateMachine',
    'AhoCorasick',
    'SequenceHandler',
    'MotifDatabase',
    'BenchmarkRunner',
    'PerformanceAnalyzer',
]