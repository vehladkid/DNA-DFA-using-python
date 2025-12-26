🧬 DNA Pattern Matching using DFA & Aho-Corasick Algorithm
Theory Of Computation
Slot: C1+TC1
Faculty: Dr Amutha S

Group Members:
24BAI1040 Tejvir Singh
24BAI1049 Mouli Gupta
24BAI1629 Chitwan Singh
24BAI1631 Sreeansh Dash

📋 Project Overview
This project implements efficient DNA pattern matching algorithms using formal language theory and automata concepts. We develop a web-based bioinformatics tool that finds specific DNA patterns (motifs) in genomic sequences using two advanced algorithms: Deterministic Finite Automaton (DFA) and Aho-Corasick Algorithm.

The application demonstrates real-world applications of Theory of Computation, including state machines, failure functions, trie data structures, and complexity analysis.

🎯 What We're Building
A complete bioinformatics platform that:

✅ Finds DNA patterns in sequences using DFA (single pattern, O(n) time)
✅ Searches multiple patterns simultaneously using Aho-Corasick
✅ Analyzes known motifs (TATA box, restriction sites, CpG islands)
✅ Benchmarks performance and proves O(n) linear time complexity
✅ Provides web interface using Streamlit for easy visualization

Real-World Applications
Gene discovery: Find promoter regions (TATA box, PRIBNOW box)
Restriction mapping: Locate enzyme cut sites (EcoRI, BamHI, etc.)
Disease detection: Identify genetic markers and mutations
Sequence analysis: Process large genomic databases efficiently

🏗️ Architecture & Components
System Architecture
text
┌─────────────────────────────────────────────────┐
│        Streamlit Web Interface (app.py)         │
│  (Home | Pattern Search | Motif | Bench | Info)│
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
   ┌─────────┬──────────┬──────────────┐
   │   DFA   │Aho-Corasick│SequenceMgr │
   │ Engine  │ Algorithm  │   Utilities │
   └─────────┴──────────┴──────────────┘
        │          │          │
        │          └──────┬───┘
        │                 │
        ▼                 ▼
   ┌─────────────────────────────┐
   │  Motif Database (6 motifs)  │
   │  Benchmarking Framework     │
   │  Performance Analyzer       │
   └─────────────────────────────┘

Core Modules
Module	Purpose	Key Algorithm
dfa_engine.py	Single-pattern matching	KMP Failure Function
aho_corasick.py	Multi-pattern matching	Trie + Failure Links
sequence_handler.py	DNA validation & processing	String manipulation
motif_database.py	Biological motif storage	Database lookup
benchmark.py	Performance testing	Time measurement
performance_analyzer.py	Complexity verification	Statistical analysis

🧪 Technology Stack
Backend & Core Algorithms
Python 3.9+ - Main programming language
BioPython 1.81 - DNA sequence handling
Custom implementations - DFA and Aho-Corasick from scratch

Frontend & Visualization
Streamlit 1.28.1 - Interactive web interface
Plotly 5.18.0 - Performance graphs
Matplotlib 3.8.2 - Data visualization
Pandas 2.0.3 - Data manipulation

Testing & Quality
Pytest 7.4.3 - Unit testing (76+ tests)
Pytest-cov 4.1.0 - Code coverage analysis

Development
Git/GitHub - Version control
VSCode - Code editor

🧠 Theory of Computation Concepts
1. Deterministic Finite Automaton (DFA)
Definition: A DFA is a 5-tuple (Q, Σ, δ, q₀, F) where:

Q = Set of states
Σ = Alphabet {A, T, G, C, N}
δ = Transition function
s = Initial state
F = Final states (accepting states)

How it works in our project:

text
Pattern: "ACG"
States: 0 → 1 → 2 → 3 (final)
        ↑ A   ↑ C   ↑ G

When we read "AACGTACG":
Position 0: A → state 1
Position 1: A → state 1 (mismatch, use failure function)
Position 2: C → state 2
Position 3: G → state 3 (MATCH! at position 1)
Position 4: T → state 0
Position 5: A → state 1
Position 6: C → state 2
Position 7: G → state 3 (MATCH! at position 5)
Complexity: O(n) time, O(m) space

n = text length
m = pattern length

2. Aho-Corasick Algorithm
Definition: Multi-pattern matcher using a trie with failure links.

Components:
Trie Construction: Build trie from all patterns
Failure Function: Like KMP, but for trie nodes
Output Function: Track which patterns match at each position
State Diagram Example:
text
Patterns: ["AT", "TA", "TAT"]

        root
        /  \
       A    T
      /      \
     T        A
    / \        \
   ø  [AT]     [TA]
        |        |
        A        T
        |        |
      [TAT]      ø
Complexity: O(n + m + z) time

n = text length
m = total pattern length
z = number of matches

3. KMP Failure Function
Concept: When a mismatch occurs, avoid re-scanning already-matched characters.

Algorithm:

python
For pattern "ABAB":
Position: 0 1 2 3
Pattern:  A B A B
Failure:  0 0 1 2

If we're at position 3 and get a mismatch,
we don't start from 0, we jump to position 2
(failure = 2), potentially saving comparisons.
📊 Algorithm Performance
DFA vs Naive vs Aho-Corasick
Metric	Naive	DFA	Aho-Corasick
Single Pattern	O(n×m)	O(n)	O(n)
Multiple Patterns	O(n×k×m)	O(n×k)	O(n+z)
Space	O(1)	O(m)	O(m)
Backtracking	Yes	No	No
Best for	Small texts	Single search	Multiple patterns

Our Benchmark Results
Expected O(n) behavior:

text
Text Size    Time (ms)
1 KB         0.5
10 KB        5.0         (10x larger → 10x slower ✓)
100 KB       50.0        (100x larger → 100x slower ✓)
1 MB         500.0       (1000x larger → 1000x slower ✓)

🚀 How It Works
Step 1: User Input
text
User enters DNA sequence: "ATGCATGCATGC"
User enters pattern: "ATG"
Step 2: Validation
text
SequenceHandler.validate_sequence("ATGCATGCATGC")
✓ Valid (only A, T, G, C allowed)
Step 3: DFA Initialization
text
DFAStateMachine("ATG")
├─ Build KMP failure function: [0, 0, 0]
├─ Build transition table
└─ Print: "✓ DFA initialized for pattern: ATG"
Step 4: Pattern Matching
text
dfa.match("ATGCATGCATGC")
→ Scan each character once (O(n))
→ Update state using transition table
→ Record matches when state == pattern length
Step 5: Results
text
Found 2 matches:
Position 0: "ATG" (score: 1.0)
Position 5: "ATG" (score: 1.0)
Step 6: Visualization
text
Streamlit displays:
✓ Results table
✓ Highlighted DNA sequence
✓ Performance metrics
📁 Project Structure
text
dna-dfa-matcher/
├── src/
│   ├── __init__.py                 # Package exports
│   ├── dfa_engine.py              # DFA implementation (KMP-based)
│   ├── aho_corasick.py            # Aho-Corasick multi-pattern matching
│   ├── sequence_handler.py        # DNA validation & processing
│   ├── motif_database.py          # 9 biological motifs database
│   ├── benchmark.py               # Performance testing framework
│   └── performance_analyzer.py    # Complexity analysis & reporting
│
├── app/
│   ├── app.py                     # Streamlit web interface (5 pages)
│   └── config.py                  # UI configuration
│
├── tests/
│   ├── test_dfa_engine.py        # 17 DFA tests
│   ├── test_sequence_handler.py  # 21 validation tests
│   ├── test_motif_database.py    # 13 motif tests
│   └── test_benchmark.py          # 25 performance tests
│
├── data/
│   ├── sample_sequences/          # FASTA files for testing
│   └── motifs/                    # Motif reference files
│
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
└── README.md
💡 Key Features
1. DFA Engine ⚙️
✅ Single-pattern matching with O(n) time complexity
✅ KMP failure function for optimal matching
✅ Supports overlapping pattern matches
✅ Handles wildcards (N for any nucleotide)

2. Aho-Corasick 🔍
✅ Multi-pattern simultaneous matching
✅ Efficient trie with failure links
✅ O(n + m + z) complexity
✅ Perfect for motif scanning

3. Sequence Tools 🧪
✅ DNA validation (A, T, G, C, N only)
✅ GC content calculation
✅ Reverse complement generation
✅ FASTA file loading (BioPython)

4. Motif Database 📚
✅ 6 promoter motifs (TATA box, PRIBNOW box, etc.)
✅ 5 restriction enzyme sites (EcoRI, BamHI, etc.)
✅ 1 CpG island site
✅ Complete biological annotations

5. Benchmarking 📊
✅ Scalability testing (1KB → 1MB)
✅ O(n) behavior verification
✅ Algorithm comparison (DFA vs Aho-Corasick)
✅ Performance reports with analysis

6. Web Interface 🌐
✅ Home: Project introduction
✅ Pattern Search: Find custom patterns
✅ Motif Analysis: Search known motifs
✅ Benchmarks: Performance visualization
✅ About: Team & algorithm info

🏃 Getting Started

Prerequisites
Python 3.9+
pip (Python package manager)
Git

Installation
Clone the repository
bash
git clone https://github.com/yourusername/dna-dfa-matcher.git
cd dna-dfa-matcher
Create virtual environment (recommended)

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Run tests (verify everything works)

bash
pytest tests/ -v
Launch web app

bash
cd app
streamlit run app.py
Open browser

text
http://localhost:8501
📈 Usage Examples
Example 1: Find Promoter Motif
python
from src import DFAStateMachine, MotifDatabase

# Get TATA box motif
motif = MotifDatabase.get_motif('TATA_BOX')  # 'TATAAA'

# Search in DNA sequence
dfa = DFAStateMachine(motif)
results = dfa.match("ATGCTATAAACGATGC")

# Output: Found 1 match at position 5
Example 2: Multiple Pattern Search
python
from src import AhoCorasick, MotifDatabase

# Get multiple restriction sites
patterns = [
    MotifDatabase.get_motif('EcoRI'),    # GAATTC
    MotifDatabase.get_motif('BamHI'),    # GGATCC
]

# Search all at once
ac = AhoCorasick(patterns)
results = ac.match("GAATTCGGATCCTAGAATTC")

# Output: Found 3 matches (EcoRI at 0, BamHI at 6, EcoRI at 14)
Example 3: Performance Benchmark
python
from src import BenchmarkRunner, PerformanceAnalyzer

# Benchmark DFA on different text sizes
results = BenchmarkRunner.benchmark_scalability("ATGC")

# Verify O(n) behavior
analysis = PerformanceAnalyzer.check_linear_time(results)
print(analysis['explanation'])  # "✓ DFA exhibits O(n) behavior"

# Generate report
report = PerformanceAnalyzer.generate_report(results)
print(report)

🧪 Testing
Run All Tests
bash
pytest tests/ -v
Run Specific Test File
bash
pytest tests/test_dfa_engine.py -v
Run with Coverage Report
bash
pytest tests/ --cov=src --cov-report=html
Expected Results
text
========================= 76 passed in 2.34s =========================

Test Coverage:
  dfa_engine.py .......... 17/17 tests ✓
  sequence_handler.py ... 21/21 tests ✓
  motif_database.py ..... 13/13 tests ✓
  benchmark.py ......... 15/15 tests ✓
  performance_analyzer.py 10/10 tests ✓
📊 Complexity Analysis
DFA Time Complexity: O(n)
Proof:

Build failure function: O(m) where m = pattern length
Scan text: O(n) where n = text length
Each character processed exactly once (no backtracking)
Total: O(m + n) = O(n) since m << n for genomic data

Aho-Corasick Time Complexity: O(n + m + z)
Breakdown:
Trie construction: O(m)
Text scanning: O(n)
Output matches: O(z)
Total: O(n + m + z)

Space Complexity
Algorithm	Space
DFA	O(m) - transition table
Aho-Corasick	O(m×
Naive	O(1) - constant

🎓 Learning Outcomes
After this project, you'll understand:

✅ Automata Theory: DFA construction and execution
✅ String Algorithms: KMP and Aho-Corasick algorithms
✅ Data Structures: Trie implementation with failure links
✅ Complexity Analysis: O(n) vs O(n²) behavior
✅ Applications: Real-world bioinformatics problems
✅ Software Engineering: Testing, benchmarking, documentation

📝 References
Textbooks
"Introduction to Algorithms" - Cormen, Leiserson, Rivest, Stein
"Pattern Matching Algorithms" - Crochemore, Hancart, Lecroq
"Biological Sequence Analysis" - Durbin, Eddy, Krogh, Mitchison

Algorithms
KMP Algorithm: https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
Aho-Corasick: https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
DFA: https://en.wikipedia.org/wiki/Deterministic_finite_automaton

Tools & Libraries
BioPython: https://biopython.org/
Streamlit: https://streamlit.io/
Pytest: https://pytest.org/

