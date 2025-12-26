# src/performance_analyzer.py
"""
Analyze and visualize algorithm performance data
"""


class PerformanceAnalyzer:
    """Analyze benchmark results and verify complexity"""
    
    @staticmethod
    def check_linear_time(results):
        """
        Verify O(n) behavior from benchmark results
        
        Args:
            results: list from benchmark_scalability()
                    [{'text_size': 1000, 'time_ms': 0.1}, ...]
        
        Returns:
            dict: {
                'is_linear': bool,
                'ratios': list of (size_ratio, time_ratio),
                'tolerance': float,
                'explanation': str
            }
        
        Theory:
        If O(n), then:
        - 10x larger text = ~10x longer time
        - 100x larger text = ~100x longer time
        
        Example:
            Text: 1KB → 0.1ms, 10KB → 1ms
            Size ratio: 10KB / 1KB = 10
            Time ratio: 1ms / 0.1ms = 10
            Match: ✓ (within tolerance)
        """
        if len(results) < 2:
            return {
                'is_linear': False,
                'ratios': [],
                'explanation': 'Need at least 2 data points'
            }
        
        tolerance = 0.2  # 20% tolerance
        ratios = []
        all_linear = True
        
        # Compare consecutive results
        for i in range(len(results) - 1):
            curr = results[i]
            next_ = results[i + 1]
            
            size_ratio = next_['text_size'] / curr['text_size']
            time_ratio = next_['time_ms'] / curr['time_ms']
            
            # Check if ratios match
            ratio_diff = abs(size_ratio - time_ratio) / size_ratio
            is_match = ratio_diff <= tolerance
            
            ratios.append({
                'size_ratio': size_ratio,
                'time_ratio': time_ratio,
                'difference': ratio_diff,
                'is_linear': is_match,
            })
            
            if not is_match:
                all_linear = False
        
        # Generate explanation
        if all_linear:
            explanation = "✓ DFA exhibits O(n) behavior: time scales linearly with input size"
        else:
            explanation = "⚠ Deviation from O(n): check for non-linear bottlenecks"
        
        return {
            'is_linear': all_linear,
            'ratios': ratios,
            'tolerance': tolerance,
            'explanation': explanation,
        }
    
    @staticmethod
    def generate_report(benchmark_results):
        """
        Generate formatted text report of benchmarks
        
        Args:
            benchmark_results: list of benchmark data
        
        Returns:
            str: formatted report
        """
        report = []
        report.append("=" * 60)
        report.append("BENCHMARK RESULTS")
        report.append("=" * 60)
        report.append("")
        
        # Table header
        report.append(f"{'Text Size':<15} {'Time (ms)':<15} {'Matches':<15}")
        report.append("-" * 60)
        
        # Table rows
        for result in benchmark_results:
            size = result['text_size']
            time_ms = result['time_ms']
            matches = result['matches']
            
            # Format size nicely
            if size >= 1_000_000:
                size_str = f"{size / 1_000_000:.1f} MB"
            elif size >= 1_000:
                size_str = f"{size / 1_000:.1f} KB"
            else:
                size_str = f"{size} bp"
            
            report.append(f"{size_str:<15} {time_ms:<15.4f} {matches:<15}")
        
        report.append("")
        report.append("=" * 60)
        
        # Analysis section
        analysis = PerformanceAnalyzer.check_linear_time(benchmark_results)
        report.append("ANALYSIS")
        report.append("-" * 60)
        report.append(analysis['explanation'])
        report.append("")
        
        # Ratio analysis
        if analysis['ratios']:
            report.append("Size-Time Ratio Analysis:")
            for i, ratio in enumerate(analysis['ratios']):
                size_ratio = ratio['size_ratio']
                time_ratio = ratio['time_ratio']
                diff = ratio['difference']
                status = "✓" if ratio['is_linear'] else "✗"
                
                report.append(
                    f"  {status} Input {size_ratio:.0f}x larger → "
                    f"Time {time_ratio:.2f}x longer "
                    f"(diff: {diff*100:.1f}%)"
                )
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    @staticmethod
    def calculate_complexity(benchmark_results):
        """
        Estimate time complexity from results
        
        Args:
            benchmark_results: list of benchmark data
        
        Returns:
            dict: {
                'estimated_complexity': 'O(n)', 'O(n log n)', 'O(n²)', etc.
                'confidence': float (0-1),
                'evidence': str
            }
        """
        if len(benchmark_results) < 2:
            return {
                'estimated_complexity': 'Unknown',
                'confidence': 0,
                'evidence': 'Need at least 2 data points'
            }
        
        # Calculate average growth rate
        growth_rates = []
        
        for i in range(len(benchmark_results) - 1):
            curr = benchmark_results[i]
            next_ = benchmark_results[i + 1]
            
            size_ratio = next_['text_size'] / curr['text_size']
            time_ratio = next_['time_ms'] / curr['time_ms']
            
            # Growth rate relative to linear
            growth_rate = time_ratio / size_ratio
            growth_rates.append(growth_rate)
        
        avg_growth = sum(growth_rates) / len(growth_rates)
        
        # Classify complexity
        if avg_growth < 1.1:  # ~1x (linear)
            complexity = 'O(n)'
            confidence = 0.9
        elif avg_growth < 1.2:  # ~1.1x
            complexity = 'O(n log n)'
            confidence = 0.7
        elif avg_growth < 1.5:  # ~1.3-1.4x
            complexity = 'O(n√n)'
            confidence = 0.5
        else:  # >1.5x
            complexity = 'O(n²) or worse'
            confidence = 0.6
        
        evidence = f"Average growth rate: {avg_growth:.2f}x (closer to 1.0 = more linear)"
        
        return {
            'estimated_complexity': complexity,
            'confidence': confidence,
            'growth_rate': avg_growth,
            'evidence': evidence,
        }
    
    @staticmethod
    def summary_stats(benchmark_results):
        """
        Calculate summary statistics
        
        Args:
            benchmark_results: list of benchmark data
        
        Returns:
            dict: summary statistics
        """
        if not benchmark_results:
            return {}
        
        times = [r['time_ms'] for r in benchmark_results]
        sizes = [r['text_size'] for r in benchmark_results]
        
        return {
            'min_time_ms': min(times),
            'max_time_ms': max(times),
            'avg_time_ms': sum(times) / len(times),
            'min_size': min(sizes),
            'max_size': max(sizes),
            'total_matches': sum(r['matches'] for r in benchmark_results),
            'num_tests': len(benchmark_results),
        }
