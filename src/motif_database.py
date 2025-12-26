# src/motif_database.py
"""
Database of known DNA motifs (promoters, restriction sites, etc.)
"""


class MotifDatabase:
    """Store and retrieve DNA motifs"""
    
    PROMOTER_MOTIFS = {
        'TATA_BOX': {
            'sequence': 'TATAAA',
            'organism': 'Eukaryotes',
            'function': 'Transcription initiation',
            'position': 'Gene promoter (-25 to -30)',
            'gc_content': 33.33,
            'description': 'Core promoter element found ~25-30 bp upstream of transcription start'
        },
        'PRIBNOW_BOX': {
            'sequence': 'TATAAT',
            'organism': 'Prokaryotes (E. coli)',
            'function': 'Transcription initiation',
            'position': 'Gene promoter (-10)',
            'gc_content': 33.33,
            'description': '-10 box in bacterial promoter, recognized by sigma factor'
        },
        'KOZAK_SEQUENCE': {
            'sequence': 'GCCRCCATGG',
            'organism': 'Eukaryotes',
            'function': 'Translation initiation',
            'position': 'Start codon region',
            'gc_content': 60.00,
            'description': 'Consensus sequence around AUG start codon for translation initiation'
        },
    }
    
    RESTRICTION_SITES = {
        'EcoRI': {
            'sequence': 'GAATTC',
            'organism': 'E. coli',
            'function': 'Restriction enzyme recognition site',
            'cut_position': 1,
            'overhang': 'sticky',
            'description': 'Cuts DNA leaving 5\' overhang (AATT)'
        },
        'BamHI': {
            'sequence': 'GGATCC',
            'organism': 'Bacillus amyloliquefaciens',
            'function': 'Restriction enzyme recognition site',
            'cut_position': 1,
            'overhang': 'sticky',
            'description': 'Cuts DNA leaving 5\' overhang (GATC)'
        },
        'PstI': {
            'sequence': 'CTGCAG',
            'organism': 'Providencia stuartii',
            'function': 'Restriction enzyme recognition site',
            'cut_position': 3,
            'overhang': 'sticky',
            'description': 'Cuts DNA leaving 3\' overhang (TG)'
        },
        'HindIII': {
            'sequence': 'AAGCTT',
            'organism': 'Haemophilus influenzae',
            'function': 'Restriction enzyme recognition site',
            'cut_position': 3,
            'overhang': 'sticky',
            'description': 'Cuts DNA leaving 5\' overhang (AGCT)'
        },
        'EcoRV': {
            'sequence': 'GATATC',
            'organism': 'E. coli',
            'function': 'Restriction enzyme recognition site',
            'cut_position': 3,
            'overhang': 'blunt',
            'description': 'Produces blunt-ended cuts'
        },
    }
    
    CpG_SITES = {
        'CpG_DINUCLEOTIDE': {
            'sequence': 'CG',
            'organism': 'Mammals',
            'function': 'DNA methylation site',
            'position': 'Gene promoters',
            'description': 'Often methylated, important for gene regulation'
        }
    }
    
    @staticmethod
    def get_motif(name):
        """
        Get motif by name
        
        Args:
            name: motif name (e.g., 'TATA_BOX')
        
        Returns:
            str: pattern sequence
            None: if not found
        
        Example:
            MotifDatabase.get_motif('TATA_BOX')  # 'TATAAA'
        """
        # Check all categories
        for category in [MotifDatabase.PROMOTER_MOTIFS, 
                        MotifDatabase.RESTRICTION_SITES,
                        MotifDatabase.CpG_SITES]:
            if name in category:
                return category[name]['sequence']
        
        return None
    
    @staticmethod
    def get_motif_info(name):
        """
        Get complete motif information
        
        Args:
            name: motif name
        
        Returns:
            dict: complete motif details
            None: if not found
        """
        for category in [MotifDatabase.PROMOTER_MOTIFS,
                        MotifDatabase.RESTRICTION_SITES,
                        MotifDatabase.CpG_SITES]:
            if name in category:
                return category[name]
        
        return None
    
    @staticmethod
    def get_all_motifs():
        """
        Get all available motifs
        
        Returns:
            dict: all motifs organized by category
        """
        return {
            'promoters': MotifDatabase.PROMOTER_MOTIFS,
            'restrictions': MotifDatabase.RESTRICTION_SITES,
            'cpg_sites': MotifDatabase.CpG_SITES,
        }
    
    @staticmethod
    def list_motif_names():
        """
        List all motif names
        
        Returns:
            list: all names
        """
        return (
            list(MotifDatabase.PROMOTER_MOTIFS.keys()) +
            list(MotifDatabase.RESTRICTION_SITES.keys()) +
            list(MotifDatabase.CpG_SITES.keys())
        )
    
    @staticmethod
    def list_by_category(category):
        """
        List motifs by category
        
        Args:
            category: 'promoters', 'restrictions', or 'cpg_sites'
        
        Returns:
            dict: motifs in that category
        """
        categories = {
            'promoters': MotifDatabase.PROMOTER_MOTIFS,
            'restrictions': MotifDatabase.RESTRICTION_SITES,
            'cpg_sites': MotifDatabase.CpG_SITES,
        }
        return categories.get(category, {})
