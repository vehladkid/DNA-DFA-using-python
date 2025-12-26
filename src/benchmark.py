# src/benchmark.py
"""
Benchmarking framework for DFA and Aho-Corasick algorithms
"""

import time
import random
from .dfa_engine import DFAStateMachine
from .aho_corasick import AhoCorasick


class BenchmarkRunner:
    """Benchmark DNA pattern matching algorithms"""
    
    @staticmethod
    def generate_random_dna(length, gc_percentage=50):
        """
        Generate random DNA sequence
        
        Args:
            length: how many bp (base pairs)
            gc_percentage: % of G+C (rest is A+T)
        
        Returns:
            str: random DNA sequence
        
        Example:
            seq = generate_random_dna(1000, gc_percentage=50)
            # Returns 1000 random A/T/G/C with 50% G+C
        """
        num_gc = int(length * gc_percentage / 100)
        num_at = length - num_gc
        
        chars = (
            ['G', 'C'] * (num_gc // 2) +
            ['A', 'T'] * (num_at // 2)
        )
        random.shuffle(chars)
        return ''.join(chars[:length])
    
    @staticmethod
    def benchmark_dfa(pattern, text, iterations=3):
        """
        Benchmark DFA performance
        
        Args:
            pattern: pattern string
            text: sequence to search
            iterations: how many times to run
        
        Returns:
            dict: {
                'min_ms': float,
                'max_ms': float,
                'avg_ms': float,
                'total_ms': float,
                'matches': int
            }
        """
        dfa = DFAStateMachine(pattern)
        times = []
        matches = 0
        
        for _ in range(iterations):
            start = time.perf_counter()
            result = dfa.match(text)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # ms
            matches = len(result)
        
        return {
            'algorithm': 'DFA',
            'min_ms': min(times),
            'max_ms': max(times),
            'avg_ms': sum(times) / len(times),
            'total_ms': sum(times),
            'matches': matches,
            'text_size': len(text),
            'pattern': pattern,
        }
    
    @staticmethod
    def benchmark_aho_corasick(patterns, text, iterations=3):
        """
        Benchmark Aho-Corasick performance
        
        Args:
            patterns: list of pattern strings
            text: sequence to search
            iterations: how many times to run
        
        Returns:
            dict: benchmark results
        """
        ac = AhoCorasick(patterns)
        times = []
        matches = 0
        
        for _ in range(iterations):
            start = time.perf_counter()
            result = ac.match(text)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # ms
            matches = len(result)
        
        return {
            'algorithm': 'Aho-Corasick',
            'min_ms': min(times),
            'max_ms': max(times),
            'avg_ms': sum(times) / len(times),
            'total_ms': sum(times),
            'matches': matches,
            'text_size': len(text),
            'num_patterns': len(patterns),
        }
    
    @staticmethod
    def benchmark_scalability(pattern, gc_percentage=50):
        """
        Test DFA on different text sizes
        
        Args:
            pattern: pattern string
            gc_percentage: GC% for generated sequences
        
        Returns:
            list: [
                {'text_size': 1000, 'time_ms': 0.1, 'matches': 5},
                ...
            ]
        """
        text_sizes = [1_000, 10_000, 100_000, 1_000_000]
        results = []
        
        for size in text_sizes:
            text = BenchmarkRunner.generate_random_dna(size, gc_percentage)
            bench = BenchmarkRunner.benchmark_dfa(pattern, text, iterations=2)
            
            results.append({
                'text_size': size,
                'time_ms': bench['avg_ms'],
                'matches': bench['matches'],
            })
            
            print(f"Size: {size:>8} bp → Time: {bench['avg_ms']:.4f} ms | Matches: {bench['matches']}")
        
        return results
    
    @staticmethod
    def compare_algorithms(pattern, patterns_list, text):
        """
        Compare DFA vs Aho-Corasick on same text
        
        Args:
            pattern: single pattern (for DFA)
            patterns_list: list of patterns (for Aho-Corasick)
            text: DNA sequence
        
        Returns:
            dict: comparison results
        """
        dfa_result = BenchmarkRunner.benchmark_dfa(pattern, text, iterations=3)
        ac_result = BenchmarkRunner.benchmark_aho_corasick(patterns_list, text, iterations=3)
        
        speedup = ac_result['avg_ms'] / dfa_result['avg_ms']
        
        return {
            'dfa': dfa_result,
            'aho_corasick': ac_result,
            'speedup': speedup,
            'faster': 'DFA' if speedup > 1 else 'Aho-Corasick',
        }
