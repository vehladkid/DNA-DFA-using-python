# tests/test_motif_database.py
"""Tests for motif database"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.motif_database import MotifDatabase



class TestMotifRetrieval:
    """Motif lookup tests"""
    
    def test_get_tata_box(self):
        """Retrieve TATA_BOX motif"""
        motif = MotifDatabase.get_motif('TATA_BOX')
        assert motif == 'TATAAA'
    
    def test_get_ecori(self):
        """Retrieve EcoRI motif"""
        motif = MotifDatabase.get_motif('EcoRI')
        assert motif == 'GAATTC'
    
    def test_get_bamhi(self):
        """Retrieve BamHI motif"""
        motif = MotifDatabase.get_motif('BamHI')
        assert motif == 'GGATCC'
    
    def test_get_nonexistent_motif(self):
        """Nonexistent motif returns None"""
        motif = MotifDatabase.get_motif('DOES_NOT_EXIST')
        assert motif is None
    
    def test_get_all_motifs(self):
        """Get all motifs organized by category"""
        all_motifs = MotifDatabase.get_all_motifs()
        assert 'promoters' in all_motifs
        assert 'restrictions' in all_motifs
        assert 'cpg_sites' in all_motifs
    
    def test_list_motif_names(self):
        """List all motif names"""
        names = MotifDatabase.list_motif_names()
        assert 'TATA_BOX' in names
        assert 'EcoRI' in names
        assert len(names) >= 6


class TestMotifInfo:
    """Motif information tests"""
    
    def test_get_motif_info_complete(self):
        """Get complete motif information"""
        info = MotifDatabase.get_motif_info('TATA_BOX')
        assert info is not None
        assert 'sequence' in info
        assert 'organism' in info
        assert 'function' in info
    
    def test_get_motif_info_nonexistent(self):
        """Nonexistent motif info returns None"""
        info = MotifDatabase.get_motif_info('FAKE')
        assert info is None
    
    def test_promoter_motif_has_position(self):
        """Promoter motifs have position info"""
        info = MotifDatabase.get_motif_info('PRIBNOW_BOX')
        assert 'position' in info


class TestMotifCategories:
    """Motif category tests"""
    
    def test_list_promoters(self):
        """List promoter motifs"""
        promoters = MotifDatabase.list_by_category('promoters')
        assert 'TATA_BOX' in promoters
        assert len(promoters) >= 2
    
    def test_list_restrictions(self):
        """List restriction enzyme sites"""
        restrictions = MotifDatabase.list_by_category('restrictions')
        assert 'EcoRI' in restrictions
        assert 'BamHI' in restrictions
        assert len(restrictions) >= 3
    
    def test_list_cpg_sites(self):
        """List CpG sites"""
        cpg = MotifDatabase.list_by_category('cpg_sites')
        assert 'CpG_DINUCLEOTIDE' in cpg
