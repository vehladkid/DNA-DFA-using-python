# src/dfa_engine.py
"""
DFA (Deterministic Finite Automaton) for DNA pattern matching
Uses KMP-like failure function for O(n) time complexity
"""

class DFAStateMachine:
    """Single-pattern DFA matching for DNA sequences"""
    
    def __init__(self, pattern):
        """
        Initialize DFA with pattern
        
        Args:
            pattern: DNA pattern string (ATCG + N for wildcard)
        
        Example:
            dfa = DFAStateMachine("ACG")
            matches = dfa.match("AACGTACG")
        """
        self.pattern = pattern.upper()
        self.alphabet = {'A', 'T', 'C', 'G', 'N'}
        self.states = len(pattern) + 1
        self.transitions = {}
        self.failure_func = [0] * len(pattern)
        self._build_failure_function()
        self._build_transitions()
        print(f"✓ DFA initialized for pattern: {self.pattern} ({len(pattern)} bp)")
    
    def _build_failure_function(self):
        """
        Build KMP failure function (failure_func)
        
        For each position, stores how many characters of pattern to overlap
        when a mismatch occurs
        
        Example: pattern = "ABAB"
        failure_func = [0, 0, 1, 2]
        """
        pattern = self.pattern
        j = 0
        
        for i in range(1, len(pattern)):
            while j > 0 and pattern[i] != pattern[j]:
                j = self.failure_func[j - 1]
            
            if pattern[i] == pattern[j]:
                j += 1
            
            self.failure_func[i] = j
    
    def _build_transitions(self):
        """
        Build state transition table for DFA
        
        For each state and character, compute next state
        Uses failure function to handle mismatches
        """
        pattern = self.pattern
        
        # Initialize transitions
        for state in range(self.states):
            self.transitions[state] = {}
            for char in self.alphabet:
                self.transitions[state][char] = None
        
        # Build explicit transitions
        for state in range(len(pattern)):
            for char in self.alphabet:
                if char == 'N' or char == pattern[state]:
                    # Match: move to next state
                    self.transitions[state][char] = state + 1
                else:
                    # Mismatch: use failure function to find next state
                    self.transitions[state][char] = self._get_failure_state(state, char)
        
        # Final state (match found)
        for char in self.alphabet:
            if char == 'N' or char == pattern[-1]:
                self.transitions[len(pattern)][char] = len(pattern)
            else:
                self.transitions[len(pattern)][char] = self._get_failure_state(
                    len(pattern) - 1, char
                )
    
    def _get_failure_state(self, state, char):
        """
        Find next state on mismatch using failure function
        
        When pattern[state] != char, use failure function to "slide"
        the pattern and try again
        
        Args:
            state: current state (0 to len(pattern)-1)
            char: input character
        
        Returns:
            int: next state
        """
        j = self.failure_func[state - 1] if state > 0 else 0
        
        while j > 0 and self.pattern[j] != char:
            j = self.failure_func[j - 1]
        
        if self.pattern[j] == char or char == 'N':
            return j + 1
        else:
            return 0
    
    def match(self, text):
        """
        Find all occurrences of pattern in text
        
        Args:
            text: DNA sequence string
        
        Returns:
            List of dicts: 
            [{
                'position': int,
                'sequence': str,
                'length': int,
                'score': float (1.0 for exact match)
            }, ...]
        
        Time: O(n) where n = len(text)
        Space: O(k) where k = number of matches
        """
        matches = []
        text_upper = text.upper()
        state = 0
        
        for i, char in enumerate(text_upper):
            # Get next state based on current state and character
            if char not in self.alphabet:
                # Invalid character: reset
                state = 0
                continue
            
            # Transition to next state
            state = self.transitions[state].get(char, 0)
            
            # If we reached final state, record match
            if state == len(self.pattern):
                matches.append({
                    'position': i - len(self.pattern) + 1,
                    'sequence': text_upper[i - len(self.pattern) + 1:i + 1],
                    'length': len(self.pattern),
                    'score': 1.0
                })
                
                # Continue searching for overlapping matches
                state = self.failure_func[state - 1]
        
        return matches
