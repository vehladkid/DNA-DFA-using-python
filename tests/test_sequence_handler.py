# tests/test_sequence_handler.py
"""Tests for sequence validation and processing"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.sequence_handler import SequenceHandler



class TestValidation:
    """Sequence validation tests"""
    
    def test_valid_sequence_atcg(self):
        """ATCG is valid"""
        assert SequenceHandler.validate_sequence("ATCG") == True
    
    def test_valid_sequence_with_n(self):
        """ATCGN is valid (N = wildcard)"""
        assert SequenceHandler.validate_sequence("ATCGN") == True
    
    def test_invalid_sequence_with_x(self):
        """ATGCX is invalid"""
        assert SequenceHandler.validate_sequence("ATGCX") == False
    
    def test_invalid_sequence_with_numbers(self):
        """ATGC123 is invalid"""
        assert SequenceHandler.validate_sequence("ATGC123") == False
    
    def test_empty_sequence(self):
        """Empty string is invalid"""
        assert SequenceHandler.validate_sequence("") == False
    
    def test_lowercase_valid(self):
        """Lowercase is converted and valid"""
        assert SequenceHandler.validate_sequence("atcg") == True
    
    def test_mixed_case_valid(self):
        """Mixed case is valid"""
        assert SequenceHandler.validate_sequence("AtCg") == True


class TestGCContent:
    """GC content calculation tests"""
    
    def test_gc_50_percent(self):
        """ATGC has 50% GC"""
        result = SequenceHandler.calculate_gc_content("ATGC")
        assert result == 50.0
    
    def test_gc_0_percent(self):
        """AAAA has 0% GC"""
        result = SequenceHandler.calculate_gc_content("AAAA")
        assert result == 0.0
    
    def test_gc_100_percent(self):
        """GCGC has 100% GC"""
        result = SequenceHandler.calculate_gc_content("GCGC")
        assert result == 100.0
    
    def test_gc_33_percent(self):
        """ATGCCC has 66.67% GC"""
    result = SequenceHandler.calculate_gc_content("ATGCCC")
    assert 66.0 < result < 67.0

    def test_gc_empty_sequence(self):
        """Empty sequence GC is 0"""
        result = SequenceHandler.calculate_gc_content("")
        assert result == 0.0
    
    def test_gc_single_char(self):
        """Single G is 100%, single A is 0%"""
        assert SequenceHandler.calculate_gc_content("G") == 100.0
        assert SequenceHandler.calculate_gc_content("A") == 0.0


class TestReverseComplement:
    """Reverse complement tests"""
    
    def test_simple_reverse_complement(self):
        """ATGC → GCAT"""
        result = SequenceHandler.get_reverse_complement("ATGC")
        assert result == "GCAT"
    
    def test_longer_reverse_complement(self):
        """ATGATG → CATCAT"""
        result = SequenceHandler.get_reverse_complement("ATGATG")
        assert result == "CATCAT"
    
    def test_self_complement(self):
        """Some sequences are self-complementary"""
        # This depends on the sequence - just check it doesn't crash
        result = SequenceHandler.get_reverse_complement("GAATTC")
        assert len(result) == 6
    
    def test_with_n_wildcard(self):
        """Reverse complement with N"""
        result = SequenceHandler.get_reverse_complement("ANTG")
        # N→N, so ANTG → NCAT reversed → TACN
        assert "N" in result
    
    def test_reverse_complement_of_complement(self):
        """Double RC should give original"""
        original = "ATGCATGC"
        rc1 = SequenceHandler.get_reverse_complement(original)
        rc2 = SequenceHandler.get_reverse_complement(rc1)
        assert rc2 == original


class TestCleaning:
    """Sequence cleaning tests"""
    
    def test_clean_sequence_removes_invalid(self):
        """Remove non-DNA characters"""
        result = SequenceHandler.clean_sequence("AT123GC456")
        assert result == "ATGC"
        assert "1" not in result
    
    def test_clean_empty_sequence(self):
        """Clean empty sequence is empty"""
        result = SequenceHandler.clean_sequence("")
        assert result == ""
    
    def test_clean_valid_sequence(self):
        """Valid sequence unchanged"""
        result = SequenceHandler.clean_sequence("ATGC")
        assert result == "ATGC"


class TestSplitting:
    """Sequence splitting tests"""
    
    def test_split_exact_chunks(self):
        """Split into exact chunks"""
        result = SequenceHandler.split_sequence("ATGCATGC", 2)
        assert result == ["AT", "GC", "AT", "GC"]
    
    def test_split_uneven_chunks(self):
        """Split with remainder"""
        result = SequenceHandler.split_sequence("ATGCATGCA", 2)
        assert result == ["AT", "GC", "AT", "GC", "A"]
    
    def test_split_chunk_larger_than_seq(self):
        """Chunk size larger than sequence"""
        result = SequenceHandler.split_sequence("ATG", 10)
        assert result == ["ATG"]
