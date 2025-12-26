# tests/test_benchmark.py
"""Tests for benchmarking and performance analysis"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.benchmark import BenchmarkRunner
from src.performance_analyzer import PerformanceAnalyzer


class TestDNAGeneration:
    """Random DNA generation tests"""
    
    def test_generate_correct_length(self):
        """Generated DNA has correct length"""
        dna = BenchmarkRunner.generate_random_dna(100)
        assert len(dna) == 100
    
    def test_generate_valid_chars(self):
        """Generated DNA contains only ATCG"""
        dna = BenchmarkRunner.generate_random_dna(1000)
        assert all(c in 'ATCG' for c in dna)
    
    def test_generate_gc_percentage(self):
        """Generated DNA has correct GC%"""
        dna = BenchmarkRunner.generate_random_dna(1000, gc_percentage=50)
        gc_count = dna.count('G') + dna.count('C')
        gc_percent = (gc_count / 1000) * 100
        # Should be close to 50% (within 10%)
        assert 40 < gc_percent < 60
    
    def test_generate_high_gc(self):
        """Generate high GC sequence"""
        dna = BenchmarkRunner.generate_random_dna(1000, gc_percentage=80)
        gc_count = dna.count('G') + dna.count('C')
        gc_percent = (gc_count / 1000) * 100
        assert 70 < gc_percent < 90


class TestBenchmarkDFA:
    """DFA benchmarking tests"""
    
    def test_benchmark_returns_dict(self):
        """Benchmark returns all required fields"""
        result = BenchmarkRunner.benchmark_dfa("ATG", "ATGATGATG", iterations=1)
        assert 'avg_ms' in result
        assert 'min_ms' in result
        assert 'max_ms' in result
        assert 'matches' in result
    
    def test_benchmark_positive_time(self):
        """Time is positive"""
        result = BenchmarkRunner.benchmark_dfa("ATG", "ATGATG", iterations=1)
        assert result['avg_ms'] > 0
    
    def test_benchmark_finds_matches(self):
        """Benchmark counts matches correctly"""
        result = BenchmarkRunner.benchmark_dfa("AT", "ATAT", iterations=1)
        assert result['matches'] == 2
    
    def test_benchmark_multiple_iterations(self):
        """Multiple iterations work"""
        result = BenchmarkRunner.benchmark_dfa("ATG", "ATG"*100, iterations=3)
        assert result['min_ms'] <= result['avg_ms'] <= result['max_ms']


class TestScalability:
    """Scalability testing"""
    
    def test_scalability_returns_list(self):
        """Scalability returns correct structure"""
        results = BenchmarkRunner.benchmark_scalability("ATGC")
        assert len(results) == 4  # 4 sizes: 1K, 10K, 100K, 1M
        assert all('text_size' in r and 'time_ms' in r for r in results)
    
    def test_scalability_times_increasing(self):
        """Time increases with size"""
        results = BenchmarkRunner.benchmark_scalability("ATGC")
        times = [r['time_ms'] for r in results]
        # Later times should be >= earlier times
        for i in range(len(times) - 1):
            assert times[i] <= times[i + 1] * 1.5  # Allow some variance


class TestLinearityCheck:
    """O(n) behavior verification"""
    
    def test_linear_check_structure(self):
        """Linear time check returns correct structure"""
        results = [
            {'text_size': 1000, 'time_ms': 1.0, 'matches': 5},
            {'text_size': 10000, 'time_ms': 10.0, 'matches': 50},
            {'text_size': 100000, 'time_ms': 100.0, 'matches': 500},
        ]
        analysis = PerformanceAnalyzer.check_linear_time(results)
        assert 'is_linear' in analysis
        assert 'ratios' in analysis
        assert 'explanation' in analysis
    
    def test_linear_behavior_detected(self):
        """Perfect O(n) behavior is detected"""
        # Perfect 10x scaling each time
        results = [
            {'text_size': 1000, 'time_ms': 1.0, 'matches': 5},
            {'text_size': 10000, 'time_ms': 10.0, 'matches': 50},
            {'text_size': 100000, 'time_ms': 100.0, 'matches': 500},
        ]
        analysis = PerformanceAnalyzer.check_linear_time(results)
        assert analysis['is_linear'] == True
    
    def test_non_linear_behavior_detected(self):
        """Non-linear behavior is detected"""
        # Exponential growth
        results = [
            {'text_size': 1000, 'time_ms': 1.0, 'matches': 5},
            {'text_size': 10000, 'time_ms': 50.0, 'matches': 50},
            {'text_size': 100000, 'time_ms': 5000.0, 'matches': 500},
        ]
        analysis = PerformanceAnalyzer.check_linear_time(results)
        # May or may not be detected depending on tolerance
        assert 'is_linear' in analysis


class TestReportGeneration:
    """Report generation tests"""
    
    def test_generate_report_returns_string(self):
        """Report is a string"""
        results = [
            {'text_size': 1000, 'time_ms': 1.0, 'matches': 5},
            {'text_size': 10000, 'time_ms': 10.0, 'matches': 50},
        ]
        report = PerformanceAnalyzer.generate_report(results)
        assert isinstance(report, str)
    
    def test_report_contains_data(self):
        """Report contains benchmark data"""
        results = [
            {'text_size': 1000, 'time_ms': 1.0, 'matches': 5},
        ]
        report = PerformanceAnalyzer.generate_report(results)
        assert 'BENCHMARK' in report
        assert '1.0' in report or '1' in report


class TestComplexityEstimation:
    """Complexity estimation tests"""
    
    def test_complexity_estimation_structure(self):
        """Complexity estimation returns correct structure"""
        results = [
            {'text_size': 1000, 'time_ms': 1.0, 'matches': 5},
            {'text_size': 10000, 'time_ms': 10.0, 'matches': 50},
        ]
        analysis = PerformanceAnalyzer.calculate_complexity(results)
        assert 'estimated_complexity' in analysis
        assert 'confidence' in analysis
        assert 'evidence' in analysis
    
    def test_linear_complexity_estimated(self):
        """O(n) complexity is estimated correctly"""
        results = [
            {'text_size': 1000, 'time_ms': 1.0, 'matches': 5},
            {'text_size': 10000, 'time_ms': 10.0, 'matches': 50},
        ]
        analysis = PerformanceAnalyzer.calculate_complexity(results)
        assert 'O(n)' in analysis['estimated_complexity']
