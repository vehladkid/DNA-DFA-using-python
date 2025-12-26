# src/sequence_handler.py
"""
DNA sequence validation, loading, and processing utilities
"""

from Bio import SeqIO


class SequenceHandler:
    """Load, validate, and process DNA sequences"""
    
    VALID_CHARS = {'A', 'T', 'G', 'C', 'N'}
    
    @staticmethod
    def validate_sequence(sequence):
        """
        Check if sequence contains only ATCG + N (wildcard)
        
        Args:
            sequence: string
        
        Returns:
            bool: True if valid, False otherwise
        
        Example:
            SequenceHandler.validate_sequence("ATGC")  # True
            SequenceHandler.validate_sequence("ATGCX")  # False
        """
        if not sequence:
            return False
        
        seq_upper = sequence.upper()
        return all(c in SequenceHandler.VALID_CHARS for c in seq_upper)
    
    @staticmethod
    def load_fasta(file_path):
        """
        Load DNA sequence from FASTA file
        
        Format:
            >sequence_name
            ATGCATGC
            ATGCATGC
        
        Args:
            file_path: path to .fasta file
        
        Returns:
            List of dicts: [{'id': str, 'sequence': str, 'length': int}, ...]
        
        Example:
            seqs = SequenceHandler.load_fasta("genes.fasta")
            print(seqs[0]['sequence'])
        """
        sequences = []
        
        try:
            for record in SeqIO.parse(file_path, "fasta"):
                seq_str = str(record.seq).upper()
                
                if SequenceHandler.validate_sequence(seq_str):
                    sequences.append({
                        'id': record.id,
                        'description': record.description,
                        'sequence': seq_str,
                        'length': len(seq_str)
                    })
                else:
                    print(f"⚠️  Skipping {record.id}: contains invalid characters")
        
        except Exception as e:
            print(f"❌ Error loading FASTA: {str(e)}")
            return []
        
        print(f"✓ Loaded {len(sequences)} sequences from {file_path}")
        return sequences
    
    @staticmethod
    def calculate_gc_content(sequence):
        """
        Calculate GC content (percentage of G and C)
        
        Formula: (count_G + count_C) / total_length * 100
        
        Args:
            sequence: DNA string
        
        Returns:
            float: percentage (0-100)
        
        Example:
            calculate_gc_content("ATGC")  # 50.0
            calculate_gc_content("AAAA")  # 0.0
        """
        if not sequence:
            return 0.0
        
        seq_upper = sequence.upper()
        gc_count = seq_upper.count('G') + seq_upper.count('C')
        return (gc_count / len(seq_upper)) * 100
    
    @staticmethod
    def get_reverse_complement(sequence):
        """
        Get reverse complement of DNA sequence
        
        Process:
        1. Complement: A↔T, G↔C
        2. Reverse: flip the string
        
        Args:
            sequence: DNA string
        
        Returns:
            str: reverse complement
        
        Example:
            get_reverse_complement("ATGC")
            Step 1: ATGC → complement → TACG
            Step 2: TACG → reverse → GCAT
            Result: "GCAT"
        """
        complement_map = {
            'A': 'T', 'T': 'A',
            'G': 'C', 'C': 'G',
            'N': 'N'
        }
        
        seq_upper = sequence.upper()
        
        # Complement
        complement = ''.join(complement_map.get(c, c) for c in seq_upper)
        
        # Reverse
        return complement[::-1]
    
    @staticmethod
    def clean_sequence(sequence):
        """
        Remove non-DNA characters from sequence
        
        Args:
            sequence: dirty DNA string
        
        Returns:
            str: cleaned sequence (uppercase)
        """
        seq_upper = sequence.upper()
        cleaned = ''.join(c for c in seq_upper if c in SequenceHandler.VALID_CHARS)
        return cleaned
    
    @staticmethod
    def split_sequence(sequence, chunk_size):
        """
        Split sequence into chunks
        
        Args:
            sequence: DNA string
            chunk_size: size of each chunk
        
        Returns:
            list: list of sequence chunks
        """
        return [sequence[i:i+chunk_size] for i in range(0, len(sequence), chunk_size)]
