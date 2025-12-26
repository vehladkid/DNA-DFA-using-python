# src/aho_corasick.py
"""
Aho-Corasick Algorithm for multi-pattern DNA matching
Time: O(n + m + z) where n=text, m=patterns, z=matches
"""

class TrieNode:
    """Node in Aho-Corasick trie"""
    
    def __init__(self):
        self.children = {}
        self.fail = None
        self.patterns = []  # List of pattern indices that end here


class AhoCorasick:
    """Multi-pattern matcher for DNA sequences"""
    
    def __init__(self, patterns):
        """
        Initialize Aho-Corasick automaton with multiple patterns
        
        Args:
            patterns: list of pattern strings
        
        Example:
            ac = AhoCorasick(['ACG', 'TGC', 'GCC'])
            matches = ac.match('ATGCCGTGC')
        """
        self.patterns = [p.upper() for p in patterns]
        self.alphabet = {'A', 'T', 'C', 'G', 'N'}
        self.root = TrieNode()
        self._build_trie()
        self._build_failure_function()
        print(f"✓ Aho-Corasick initialized with {len(patterns)} patterns")
    
    def _build_trie(self):
        """Build trie with all patterns"""
        for i, pattern in enumerate(self.patterns):
            node = self.root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.patterns.append(i)
    
    def _build_failure_function(self):
        """
        Build failure links (like KMP failure function for trie)
        
        For each node, failure link points to longest proper suffix
        that is also a prefix in the trie
        """
        from collections import deque
        
        queue = deque()
        
        # Root's failure link points to itself
        self.root.fail = self.root
        
        # Level 1 nodes fail to root
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)
        
        # Level 2+ nodes
        while queue:
            node = queue.popleft()
            
            for char, child in node.children.items():
                # Find failure link for child
                fail = node.fail
                
                while fail != self.root and char not in fail.children:
                    fail = fail.fail
                
                if char in fail.children:
                    child.fail = fail.children[char]
                else:
                    child.fail = self.root
                
                # Inherit patterns from failure link
                child.patterns.extend(child.fail.patterns)
                queue.append(child)
    
    def match(self, text):
        """
        Find all occurrences of all patterns in text
        
        Args:
            text: DNA sequence string
        
        Returns:
            List of dicts:
            [{
                'position': int,
                'pattern': str,
                'length': int,
                'pattern_id': int
            }, ...]
        
        Time: O(n + z) where n=len(text), z=matches
        """
        matches = []
        text_upper = text.upper()
        node = self.root
        
        for i, char in enumerate(text_upper):
            # Follow failure links until we find a match or reach root
            while node != self.root and char not in node.children:
                node = node.fail
            
            # Transition
            if char in node.children:
                node = node.children[char]
            else:
                node = self.root
            
            # Check for pattern matches at this position
            for pattern_id in node.patterns:
                pattern = self.patterns[pattern_id]
                matches.append({
                    'position': i - len(pattern) + 1,
                    'pattern': pattern,
                    'length': len(pattern),
                    'pattern_id': pattern_id,
                    'score': 1.0
                })
        
        return matches
